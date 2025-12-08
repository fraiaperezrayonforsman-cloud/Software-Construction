# ZEST Virtual File System 

**HS25  SoCo-group  004**

## Project Introduction 
The goal of our project was to create a simplified virtual filesystem, stored entirely inside a binary file with .zvfs extension. 

# lsfs 
1. First we check if the provided filesystem exists by using .exists() function. 
2. We open zvfs_name in the binary read mode "rb".
3. We extract information which we need: name, length and created which is UNIX timestamp of created time. Moreover we check the deleted flag as we have to make sure we do not print files that were deleted.
4. We convert the filename to string using "UTF-8" decoding.
5. Moreover we convert UNIX timestamp into a readable date. 
6. Finally, we print the file information. 

Output of the function in Python:
python zvfs.py lsfs filesystem1.zvfs
Name: test_file1.txt
Size: 16 bytes
Created: 2025-11-16 19:54:05
Name: test_file1.txt
Size: 16 bytes
Created: 2025-11-16 19:54:52
Name: test_file2.txt
Size: 27 bytes
Created: 2025-12-06 11:49:53

Output of the function in Java:
java zvfs lsfs filesystem1.zvfs
Name: test_file1.txt
Size: 16 bytes
Created: 2025-11-16 19:54:05

Name: test_file1.txt
Size: 16 bytes
Created: 2025-11-16 19:54:52

Name: test_file2.txt
Size: 27 bytes
Created: 2025-12-06 11:49:53

# catfs 
1. First we check if the provided filesystem exists by using .exists() function. 
2. Then we extract a name of the file  with Path().name
3. We use a flag called "find" to indicate whether a requested file exists in the filesystem.
4. Then we unpack a file and we check whether an entry is empty or file is deleted. 
5. We check if the file is the one we want and if yes we change "find" flag to true and we print the file content.

Output of the function in Python:
python zvfs.py catfs filesystem1.zvfs test_file1.txt
Hello, world! 

Output of the function in Java:
java zvfs catfs filesystem1.zvfs test_file1.txt
Hello, world! 

# getfs 
1. First we check if the provided filesystem exists by using .exists() function. 
2. Then we extract a name of the file with Path().name
3. We use a flag called "find" to indicate whether a requested file to extract exists in the filesystem.
4. Then we unpack a file and we check whether an entry is empty or file is deleted. 
5. After we find a file we read it using fields start and length from file entry. 
6. In the new file we write what we just read.
7. Finally we print that a file has been extracted. 

Output of the function in Python:

(base) missbo@Missbos-MacBook-Air SoCo_HS25-group_004-a3 % rm test_file1.txt
(base) missbo@Missbos-MacBook-Air SoCo_HS25-group_004-a3 % python zvfs.py getfs filesystem1.zvfs test_file1.txt
File 'test_file1.txt' has been extracted.

Output of the function in Java: 
(base) missbo@Missbos-MacBook-Air SoCo_HS25-group_004-a3 % javac zvfs.java
(base) missbo@Missbos-MacBook-Air SoCo_HS25-group_004-a3 % rm test_file1.txt
(base) missbo@Missbos-MacBook-Air SoCo_HS25-group_004-a3 % java zvfs getfs fil
esystem1.zvfs test_file1.txt
File has been extracted

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
