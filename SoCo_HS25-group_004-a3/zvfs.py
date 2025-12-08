import time
import os
import sys

from pathlib import Path
from struct import pack, unpack

#Constant variables
HEADER_SIZE = 64
FILE_ENTRY_SIZE = 64
FILE_CAPACITY = 32
MAGIC = b"ZVFSDSK1"
ALIGNMENT = 64
VERSION = 1
FILE_TABLE_OFFSET = 64
DATA_START_OFFSET = HEADER_SIZE + (FILE_CAPACITY * FILE_ENTRY_SIZE)

FORMAT_STRING_HEADER = '<8s B B 2s H H H 2s I I I I H 26s'
FORMAT_STRING_FILE_ENTRY = '<32s I I B B 2s Q 12s'

def mkfs(zvfs_name):
    try:
        with open(zvfs_name, "wb") as filesys:
            header = pack(
                FORMAT_STRING_HEADER,
                MAGIC,
                VERSION,
                0,
                b'\x00\x00',
                0,
                FILE_CAPACITY,
                FILE_ENTRY_SIZE,
                b'\x00\x00',
                FILE_TABLE_OFFSET,
                DATA_START_OFFSET,
                DATA_START_OFFSET,
                0,
                0,
                b'\x00' * 26
            )
            filesys.write(header)
        
            zero_entry = b'\x00' * FILE_ENTRY_SIZE
            filesys.write(zero_entry * FILE_CAPACITY)
        print(f"Zest Virtual Filesystem {zvfs_name} created correctly")
    except IOError as error:
        print(f"could not create Zest Virtual Filesystem correclty: {error}")

def padding_estimation(data_size):
    dif = data_size % ALIGNMENT
    if dif == 0:
        return 0
    else:
        return ALIGNMENT - dif
    
def field_update(zvfs_file, offset, format, value):
    try:
        with open(zvfs_file, "r+b") as file:
            file.seek(offset)
            file.write(pack(format, value))
    except IOError as error:
        print(f"could not update field: {error}")

def addfs(zvfs_name, new_file):
    new_file = Path(new_file)
    assert new_file.exists(), "filepath does not exist"
    try:
        with open(new_file, "rb") as file:
            file_data = file.read()
        file_len = len(file_data)
        file_name = os.path.basename(new_file)
        assert file_len < 32, f"{file_name} is larger than 32 characters" 
        padding = padding_estimation(file_len)
        
        #look for free space in file system
        with open(zvfs_name, "r+b") as filesys:
            filesys.seek(0)
            header_translated = unpack(FORMAT_STRING_HEADER, filesys.read(HEADER_SIZE))
            (magic, _, _, _, file_count, file_capacity, _, _, _, _, next_free_offset,_, _, _) = header_translated

            assert file_count < file_capacity, "no more space left for new files"
            assert magic == MAGIC, "invalid magic string"

            entry_offset = -1

            for i in range(FILE_CAPACITY):
                current_offset = FILE_TABLE_OFFSET + i * FILE_ENTRY_SIZE
                filesys.seek(current_offset)
                entry = filesys.read(FILE_ENTRY_SIZE)

                if entry[0]==0:
                    entry_offset = current_offset
                    break
                
            assert entry_offset > -1, "no free file entry available"

            #add file
            filesys.seek(next_free_offset)
            filesys.write(file_data)
            if padding > 0:
                filesys.write(b'\x00'*padding)
    
            new_next_free_offset = next_free_offset + file_len + padding

            #write new file entry
            file_name_padding = file_name.encode('utf-8') + b'\x00'

            timestamp = int(time.time())

            file_entry_data = pack(
                FORMAT_STRING_FILE_ENTRY,
                file_name_padding,
                next_free_offset,
                file_len,
                0,
                0,
                b'\x00\x00',
                timestamp,
                b'\x00' * 12)
            filesys.seek(entry_offset)
            filesys.write(file_entry_data)

        #update header fields
        field_update(zvfs_name, 28, 'I', new_next_free_offset)
        field_update(zvfs_name, 12, 'H', file_count + 1)

        print(f"The {new_file} was added correctly to {zvfs_name}")

    except IOError as error:
        print(f"Error while adding new file to filesystem: {error}")
        
        
def lsfs(zvfs_name):
    zvfs_name = Path(zvfs_name)
    assert zvfs_name.exists(), f"Filesystem {zvfs_name} does not exist"
    try:
        with open(zvfs_name, "rb") as filesys:
            for i in range(FILE_CAPACITY):
                entry_offset = FILE_TABLE_OFFSET + i * FILE_ENTRY_SIZE
                filesys.seek(entry_offset)
                file = filesys.read(FILE_ENTRY_SIZE)

                entry = unpack(FORMAT_STRING_FILE_ENTRY, file)

                name = entry[0]
                length = entry[2]
                flag_deleted = entry[4]
                created = entry[6]

                if name[0] == 0 or flag_deleted == 1:
                    continue

                filename = name.split(b'\x00')[0].decode('utf-8')
                creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created))

                print(f"Name: {filename}")
                print(f"Size: {length} bytes")
                print(f"Created: {creation_time}")

    except IOError as error:
        print(f"Error while reading all the files in the filesystem: {error}")

def catfs(zvfs_name, filename):
    zvfs_name = Path(zvfs_name)
    assert zvfs_name.exists(), f"Filesystem {zvfs_name} does not exist"

    filename = Path(filename).name 
    find = False

    try:
        with open(zvfs_name, "rb") as filesys:
            for i in range(FILE_CAPACITY):
                entry_offset = FILE_TABLE_OFFSET + i * FILE_ENTRY_SIZE
                filesys.seek(entry_offset)
                file = filesys.read(FILE_ENTRY_SIZE)

                entry = unpack(FORMAT_STRING_FILE_ENTRY, file)
                name = entry[0]
                start = entry[1]
                length = entry[2]
                flag_deleted = entry[4]

                if name[0] == 0 or flag_deleted == 1:
                    continue

                entry_name = name.split(b'\x00')[0].decode('utf-8')
                if entry_name == filename:  
                    find = True
                    filesys.seek(start)
                    file_data = filesys.read(length)
                    print(file_data.decode('utf-8'))
                    break 
                if find == False:
                    print('This file does not exists in this filesystem')
                        
    except IOError as error:
        print(f"Error while printing out the file content: {error}")

def getfs(zvfs_name, filename):
    zvfs_name = Path(zvfs_name)
    assert zvfs_name.exists(), f"Filesystem {zvfs_name} does not exist"

    filename = Path(filename).name
    find = False

    try:
        with open(zvfs_name, "rb") as filesys:
            for i in range(FILE_CAPACITY):
                entry_offset = FILE_TABLE_OFFSET + i * FILE_ENTRY_SIZE
                filesys.seek(entry_offset)
                file = filesys.read(FILE_ENTRY_SIZE)

                entry = unpack(FORMAT_STRING_FILE_ENTRY, file)
                name = entry[0]
                start = entry[1]
                length = entry[2]
                flag_deleted = entry[4]

                if name[0] == 0 or flag_deleted == 1:
                    continue

                entry_name = name.split(b'\x00')[0].decode('utf-8')
                if entry_name == filename:
                    find = True
                    filesys.seek(start)
                    file_data = filesys.read(length)

                    with open(filename, "wb") as writer:
                        writer.write(file_data)

                    print(f"File '{filename}' has been extracted.")
                    break

            if find == False:
                print(f"File '{filename}' does not exist in the filesystem {zvfs_name}.")

    except IOError as error:
        print(f"Error while extracting a file from the filesystem: {error}")

def gifs(zvfs_name):
    try:
        total_size = os.path.getsize(zvfs_name)
        
        with open(zvfs_name, "rb") as fs:
            fs.seek(0)
            header = fs.read(HEADER_SIZE)
            _, _, _, _, file_count, file_capacity, _, _, _, _, _, _, deleted_files, _ = unpack(FORMAT_STRING_HEADER, header)
            free_entries = file_capacity - file_count - deleted_files
            
            print(f"Filesystem file     : {zvfs_name}")
            print(f"Files present       : {file_count}")
            print(f"Free entries        : {free_entries}")
            print(f"Deleted files       : {deleted_files}")
            print(f"Total size          : {total_size} bytes")
    
    except FileNotFoundError:
        print(f"{zvfs_name} does not exist")
        
    except IOError as error:
        print(f"Error while reading filesystem: {error}")

def rmfs(zvfs_name, filename):
    found = False
    
    try:
        with open(zvfs_name, "r+b") as fs:
            fs.seek(0)
            header = fs.read(HEADER_SIZE)
            (_,
            _,
            _,
            _,
            file_count,
            file_capacity,
            file_entry_size,
            _,
            file_table_offset,
            _,
            _,
            _,
            deleted_files,
            _) = unpack(FORMAT_STRING_HEADER, header)
            
            for i in range(file_capacity):
                entry_offset = file_table_offset + i * file_entry_size
                fs.seek(entry_offset)
                entry = fs.read(file_entry_size)
                
                if entry[0] == 0:
                    continue 
                
                (name, _, _, _, flag, _, _, _) = unpack(FORMAT_STRING_FILE_ENTRY, entry)
                
                entry_name = name.split(b'\x00', 1)[0].decode('utf-8')

                if entry_name != filename:
                    continue
                
                found = True
                
                if flag == 1:
                    print(f"File {filename} is already marked as deleted.")
                    break
                
                flag_offset = entry_offset +  32 + 4 + 4 + 1
                field_update(zvfs_name, flag_offset, 'B', 1)
                
                field_update(zvfs_name, 12, 'H', file_count - 1) 
                field_update(zvfs_name, 36, 'H', deleted_files + 1) 
                
                print(f"File {filename} marked as deleted.")
    
        if found == False:
            print(f"File {filename} not found in filesystem.")
    
    except IOError as error:
        print(f"Error while reading filesystem: {error}")

def dfrgfs(zvfs_name):
    zvfs_name = Path(zvfs_name)
    assert zvfs_name.exists(), f"Filesystem {zvfs_name} doesn't exist"

    deleted_entries = 0
    freed_bytes = 0

    try:
        with open(zvfs_name, "r+b") as fs:
            fs.seek(0)
            header = fs.read(HEADER_SIZE)
            (_,
            _,
            _,
            _,
            _,
            file_capacity,
            file_entry_size,
            _,
            file_table_offset,
            data_start_offset,
            _,
            _,
            _,
            _) = unpack(FORMAT_STRING_HEADER, header)

            files = []

            for i in range(file_capacity):
                entry_offset = file_table_offset + i * file_entry_size
                fs.seek(entry_offset)
                entry = fs.read(file_entry_size)

                if entry[0] == 0:
                    continue

                (name, start, length, _, flag, _, created, _) = unpack(FORMAT_STRING_FILE_ENTRY, entry)

                if flag == 1:
                    deleted_entries += 1
                    freed_bytes += length + padding_estimation(length)
                    continue

                files.append((entry_offset, name, start, length, created))

            new_offset = data_start_offset

            for (entry_off, name, old_start, length, created) in files:
                fs.seek(old_start)
                data = fs.read(length)

                fs.seek(new_offset)
                fs.write(data)

                field_update(zvfs_name, entry_off + 32, 'I', new_offset)

                pad = padding_estimation(length)
                if pad:
                    fs.write(b'\x00' * pad)

                new_offset += length + pad

            for i in range(file_capacity):
                entry_offset = file_table_offset + i * file_entry_size
                fs.seek(entry_offset)
                entry = fs.read(file_entry_size)

                if entry[0] != 0:
                    (_, _, _, _, flag_deleted, _, _, _) = unpack(FORMAT_STRING_FILE_ENTRY, entry)
                    if flag_deleted == 1:
                        fs.seek(entry_offset)
                        fs.write(b"\x00" * file_entry_size)

            fs.truncate(new_offset)

        field_update(zvfs_name, 28, 'I', new_offset)     
        field_update(zvfs_name, 36, 'H', 0)              
        field_update(zvfs_name, 12, 'H', len(files))     

        print(f"{deleted_entries} files defragmented")
        print(f"{freed_bytes} bytes freed")

    except IOError as error:
        print(f"Error while defragmenting filesystem: {error}")

def main(args):
    assert len(args) > 2, "not enough arguments"
    command = args[1]
    if command == "mkfs" and len(args) == 3:
        mkfs(args[2])
    elif command == "addfs" and len(args) == 4:
        addfs(args[2], args[3])
    elif command == "gifs" and len(args) == 3:
        gifs(args[2])
    elif command == 'lsfs' and len(args) == 3:
        lsfs(args[2])
    elif command == "catfs" and len(args) == 4:
        catfs(args[2], args[3])
    elif command == 'getfs' and len(args) == 4:
        getfs(args[2],args[3])
    elif command == "rmfs" and len(args) == 4:
        rmfs(args[2], args[3])
    elif command == "dfrgfs" and len(args) == 3:
        dfrgfs(args[2])
    else:
        print(f"Unknown command {command} or incorrect number of args")

if __name__ == '__main__':
    main(sys.argv)

