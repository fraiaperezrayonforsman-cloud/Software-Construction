import time
import os
import sys
from struct import pack, unpack

# --- Constant variables ---
HEADER_SIZE = 64
FILE_ENTRY_SIZE = 64 # Renamed to reflect its meaning
FILE_CAPACITY = 32
MAGIC = b"ZVFSDSK1"
ALIGNMENT = 64
VERSION = 1
FILE_TABLE_OFFSET = 64
DATA_START_OFFSET = HEADER_SIZE + (FILE_CAPACITY * FILE_ENTRY_SIZE) # Correct Calculation: 64 + (32 * 64) = 2112

FORMAT_STRING_HEADER = '<8s B B 2s H H H 2s I I I I H 26s'
FORMAT_STRING_FILE_ENTRY = '<32s I I B B 2s Q 12s'

def mkfs(zvfs_name):
    print(f"Creating new filesystem: {zvfs_name}")
    try:
        with open(zvfs_name, "wb") as filesys:
            # 1. Pack Header (FORMAT_STRING_HEADER must be the first argument!)
            header = pack(
                FORMAT_STRING_HEADER,
                MAGIC,
                VERSION,
                0, # flags
                b'\x00\x00', # reserved0
                0, # file_count
                FILE_CAPACITY,
                FILE_ENTRY_SIZE,
                b'\x00\x00', # reserved1
                FILE_TABLE_OFFSET,
                DATA_START_OFFSET, # data_start_offset
                DATA_START_OFFSET, # next_free_offset (points to the start of data region)
                0, # free_entry_offset
                0, # deleted_files
                b'\x00' * 26 # reserved2
            )
            filesys.write(header)
            
            # 2. Write 32 zeroed File Entries (2048 bytes)
            zero_entry = b'\x00' * FILE_ENTRY_SIZE
            filesys.write(zero_entry * FILE_CAPACITY)
        print(f"Filesystem {zvfs_name} created successfully.")

    except IOError as error:
        print(f"Could not create Virtual Filesystem correctly: {error}")

def padding_estimation(data_size):
    """Calculates the zero-padding needed to align data to the 64-byte block size."""
    # Use ALIGNMENT constant instead of FILE_ENTRY_SIZE for clarity in this function
    if data_size % ALIGNMENT == 0:
        return 0
    else:
        return ALIGNMENT - (data_size % ALIGNMENT)
    
def field_update(zvfs_file, offset, format, value):
    """Utility to update a single field in the header."""
    try:
        # Corrected file mode: 'r+b' with no spaces
        with open(zvfs_file, "r+b") as file: 
            file.seek(offset)
            file.write(pack(format, value))
    except IOError as error:
        print(f"Could not update field: {error}")

def addfs(zvfs_name, new_file):
    if not os.path.exists(new_file):
        print(f"Error: File to add '{new_file}' does not exist.")
        return
        
    try:
        # 1. Read file to add data (Corrected: using .read())
        with open(new_file, "rb") as file:
            file_data = file.read()
        
        file_len = len(file_data)
        file_name = os.path.basename(new_file) # Corrected: using new_file path string
        
        # Corrected: check length of the file name string
        if len(file_name) >= 32:
             print(f"Error: Filename '{file_name}' must be less than 32 characters.")
             return
             
        padding = padding_estimation(file_len)
        
        # 2. Look for free space in file system and read header
        with open(zvfs_name, "r+b") as filesys:
            filesys.seek(0)
            header_translated = unpack(FORMAT_STRING_HEADER, filesys.read(HEADER_SIZE))
            
            # Unpacking header (using '_' for ignored fields)
            (magic, _, _, _, file_count, file_capacity, _, _, _, _, next_free_offset, _, _, _) = header_translated

            if magic != MAGIC: # Corrected: Check for equality
                print("Error: Invalid ZVFS file magic string.")
                return

            if file_count >= file_capacity:
                print("Error: No more space left for new files.")
                return

            entry_offset = -1
            
            # Find first free file entry
            for i in range(FILE_CAPACITY):
                # Corrected offset calculation: i * FILE_ENTRY_SIZE
                current_offset = FILE_TABLE_OFFSET + i * FILE_ENTRY_SIZE 
                filesys.seek(current_offset)
                entry = filesys.read(FILE_ENTRY_SIZE)

                # Check first byte of the name field for null (free spot)
                if entry[0] == 0:
                    entry_offset = current_offset
                    break
                
            if entry_offset == -1: # Corrected: Check for not-found
                print("Error: No free file entry available.")
                return

            # 3. Add file data and padding
            file_start_offset = next_free_offset
            filesys.seek(file_start_offset)
            filesys.write(file_data)
            if padding > 0:
                filesys.write(b'\x00' * padding)
            
            # 4. Updating header fields
            new_next_free_offset = file_start_offset + file_len + padding

            # 5. Write New File Entry
            file_name_padded = file_name.encode('utf-8') + b'\x00' # Null terminated
            timestamp = int(time.time())

            file_entry_data = pack(
                FORMAT_STRING_FILE_ENTRY,
                file_name_padded,
                file_start_offset,
                file_len,
                0, # type: 0
                0, # flag: 0
                b'\x00\x00', # reserved0
                timestamp,
                b'\x00' * 12
            )
            filesys.seek(entry_offset)
            filesys.write(file_entry_data)
        
        # 6. Update header fields (AFTER closing the file in 'r+b' mode)
        field_update(zvfs_name, 28, 'I', new_next_free_offset) # next_free_offset at 28
        field_update(zvfs_name, 12, 'H', file_count + 1) # file_count at 12

        print(f"The {new_file} was added correctly to {zvfs_name}")

    except IOError as error:
        print(f"Error while adding new file to filesystem: {error}")
    
# Main execution logic moved out of addfs
def main(args):
    if len(args) < 2:
        print("Usage: python zvfs.py <command> <arguments...>")
        return
        
    command = args[1]

    if command == "mkfs" and len(args) == 3:
        mkfs(args[2])
    elif command == "addfs" and len(args) == 4:
        addfs(args[2], args[3])
    else:
        print(f"Unknown command {command} or incorrect number of args")

if __name__ == '__main__':
    main(sys.argv)