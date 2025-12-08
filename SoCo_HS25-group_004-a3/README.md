# ZEST Virtual File System 

**HS25  SoCo-group  004**

## Project Introduction 
The goal of our project was to create a simplified virtual filesystem, stored entirely inside a binary file with .zvfs extension. 

# lsfs 
1. First we check if the provided filesystem exists by using .exists() function. 
2. We open zvfs_name in the binary read mode "rb".
3. We extract information which we need: name, length and created which is UNIX timestamp of created time. Moreover we check the deleted flag as we have to make sure we do not print files that were deleted.
4. We convert the filename to sring using "UTF-8" decoding.
5. Moreover we convert UNIX timestamp into a readable date. 
6. Finally, we print the file information. 

# rmfs
1. We open the filesystem using "r+b+ to activate both reading and writing in binary mode. We need this as rmfs must inspect and modify bytes. 
2. The header is unpacked with unpack() so we can extract file_count, file_capacity and table offsets. 
3. We iterate over all file entries and compute each entry's offset. 
4. Empty entries are skipped by checking whether the first byte is zero.
5. For each entry, we unpack name and deleted flag. 
6. We compare the stored filename to the requested one and mark the match as deleted by changing only the deleted-flag byte.
7. Finally, header counters are updated to reflect that one file became inactive and one slot is considered as deleted.

# gifs 
1. We use os.path.getsize to retrieve the total size of the filesystem
2. We extract only the relevant header fields.
3. The number of free entries is calculated by subtracting active and deleted entries from total capacity.

# dfrgfs
1. We begin by reading and unpacking the header to obtain offsets. For the defragmentation we must know exactly where the file table starts, where the data region begins and how many entries exist. 
2. We scan all entries and collect only active files. 
3. A new_offset is initialized to the start of the data region. All rewritten files will be placed from this offset onward, eliminating the unused gaps.
4. The data of each active file is rewritten, and only the start field in its entry is updated. 
5. Padding is applied after each file to maintain the alignment.
6. After rewriting files, we rescan the table and physically clear all deleted entries.
7. Finally, we truncate the filesystem to physically free the storage.

# Authors 
