# ZEST Virtual File System 

**HS25  SoCo-group  004**

## Project Introduction 
The goal of our project was to create a simplified virtual filesystem, stored entirely inside a binary file with .zvfs extension.

# mkfs
1. We create a path to a file system, writing it in binary. 
2. We add define a header with the virtual file system's metadata in byte format. For this we use the pack() function from the struct library. 
3. We write the header to the filesystem. 
4. We create the space where the files will be stored. Our virtual filesystem can store up to 32 files, we initialize our file table with zero entries.
5. If opening or writing the filesystem fails, then we get an IOError.

...\SoCo_HS25-group_004-a3>python zvfs.py mkfs filesystem1.zvfs
Zest Virtual Filesystem filesystem1.zvfs created correctly

# padding_estimation (helper function)
helper function to estimate padding for correct alignment
1. We estimate the remainder between the data size and the alignment
2. If there is no difference we return 0 padding
3. If there is a difference we return the correct amount of padding needed for alignment. 

# field_update (helper function)
helper function to update metadata once a new file is added to the filesystem
1. it first reads the filesystem in binary mode.
2. it looks for the specified offset in the filesystem
3. it updates the value in that offset with the specified format using the pack function.
4. If field could not be updated correctly we catch an IOError

# addfs
1. We make sure that the new file exists
2. We read the new file in binary mode and assign it to file_data.
3. We define file_name containing the final component of the pathname.
4. We assert that the file_name length is no longer than 31 characters.
5. We calculate the padding needed according to the length of the file.
6. We open the filesystem in read binary mode, and set the pointer to the start.
7. Translate the header from binary format into usable information. 
8. We ensure that the number of files in the filesystem is smaller than the file capacity, i.e. 32. Additionally, we check that the filesystem we opened is truly our ZVFS by assessing our magic string.
9. We check whether there is free space for a new file. For each file space we check whether it is empty. If an empty spot is found we set entry_offset to current_offset. 
10. We add file by setting a pointer at the next free offset and writing the file data into it. We add padding if needed (depending on the file name length).
11. We define the new file's metdata and we write into the free space we had found on step 9. 
12. We update the fields next_free_offset and the file count on the system's metadata. 
13. In case of an error in the process we raise IOError.

...SoCo_HS25-group_004-a3>python zvfs.py addfs filesystem1.zvfs test_file1.txt
The test_file1.txt was added correctly to filesystem1.zvfs

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
1. We open the filesystem using "r+b" to activate both reading and writing in binary mode. We need this as rmfs must inspect and modify bytes. 
2. The header is unpacked with unpack() so we can extract file_count, file_capacity and table offsets. 
3. We iterate over all file entries and compute each entry's offset. 
4. Empty entries are skipped by checking whether the first byte is zero.
5. For each entry, we unpack name and deleted flag. 
6. We compare the stored filename to the requested one and mark the match as deleted by changing only the deleted-flag byte.
7. Finally, header counters are updated to reflect that one file became inactive and one slot is considered as deleted.

♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py rmfs filesystem2.zvfs test_file1.txt
File test_file1.txt marked as deleted.

♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs rmfs filesystem1.zvfs test_file2.txt
File test_file2.txt marked as deleted

# gifs 
1. We use os.path.getsize to retrieve the total size of the filesystem
2. We extract only the relevant header fields.
3. The number of free entries is calculated by subtracting active and deleted entries from total capacity.

♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py gifs filesystem1.zvfs
Filesystem file     : filesystem1.zvfs
Files present       : 2
Free entries        : 30
Deleted files       : 0
Total size          : 2240 bytes

♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 javac zvfs.java
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs gifs filesystem1.zvfs
Filesystem file     : filesystem1.zvfs
Files present       : 2
Free entries        : 30
Deleted files       : 0
Total size          : 2240 bytes

# dfrgfs
1. We begin by reading and unpacking the header to obtain offsets. For the defragmentation we must know exactly where the file table starts, where the data region begins and how many entries exist. 
2. We scan all entries and collect only active files. 
3. A new_offset is initialized to the start of the data region. All rewritten files will be placed from this offset onward, eliminating the unused gaps.
4. The data of each active file is rewritten, and only the start field in its entry is updated. 
5. Padding is applied after each file to maintain the alignment.
6. After rewriting files, we rescan the table and physically clear all deleted entries.
7. Finally, we truncate the filesystem to physically free the storage.

♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py dfrgfs filesystem1.zvfs
3 files defragmented
192 bytes freed

♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs dfrgfs filesystem1.zvfs              
1 files defragmented
64 bytes freed

# Showcase whole code in Python
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py mkfs filesystem3.zvfs
Zest Virtual Filesystem filesystem3.zvfs created correctly
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 echo Hello, world! > test_file3.txt
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 echo The weather is nice today > test_file4.txt
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py addfs filesystem3.zvfs test_file3.txt
The test_file3.txt was added correctly to filesystem3.zvfs
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py addfs filesystem3.zvfs test_file4.txt
The test_file4.txt was added correctly to filesystem3.zvfs
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py lsfs filesystem3.zvfs
Name: test_file3.txt
Size: 14 bytes
Created: 2025-12-09 10:56:33
Name: test_file4.txt
Size: 26 bytes
Created: 2025-12-09 10:56:51
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py catfs filesystem3.zvfs test_file3.txt
Hello, world!

♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 rm test_file3.txt
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py getfs filesystem3.zvfs test_file3.txt
File 'test_file3.txt' has been extracted.
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py gifs filesystem3.zvfs
Filesystem file     : filesystem3.zvfs
Files present       : 2
Free entries        : 30
Deleted files       : 0
Total size          : 2240 bytes
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py rmfs filesystem3.zvfs test_file3.txt
File test_file3.txt marked as deleted.
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py gifs filesystem3.zvfs
Filesystem file     : filesystem3.zvfs
Files present       : 1
Free entries        : 30
Deleted files       : 1
Total size          : 2240 bytes
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py lsfs filesystem3.zvfs
Name: test_file4.txt
Size: 26 bytes
Created: 2025-12-09 10:56:51
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py dfrgfs filesystem3.zvfs
1 files defragmented
64 bytes freed
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py gifs filesystem3.zvfs  
Filesystem file     : filesystem3.zvfs
Files present       : 1
Free entries        : 31
Deleted files       : 0
Total size          : 2176 bytes
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 python zvfs.py lsfs filesystem3.zvfs  
Name: test_file4.txt
Size: 26 bytes
Created: 2025-12-09 10:56:51

# Showcase whole code in Java
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs mkfs filesystem4.zvfs
Zest Virtual Filesystem filesystem4.zvfs created correctly.
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 echo Hello, world! > test_file5.txt
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 echo The weather is nice today > test_file6.txt
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs addfs filesystem4.zvfs test_file5.txt
Thetest_file5.txtwas added correctly tofilesystem4.zvfs
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs addfs filesystem4.zvfs test_file6.txt
Thetest_file6.txtwas added correctly tofilesystem4.zvfs
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs lsfs filesystem4.zvfs
Name: test_file5.txt
Size: 234881024 bytes
Created: 4501419-04-07 03:33:48

Name: test_file6.txt
Size: 436207616 bytes
Created: 287769698-10-16 19:20:53
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs catfs filesystem4.zvfs test_file5.txt
Hello, world!

♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 rm test_file5.txt
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs getfs filesystem4.zvfs test_file
5.txt
File has been extracted
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs gifs filesystem4.zvfs
Filesystem file     : filesystem4.zvfs
Files present       : 2
Free entries        : 30
Deleted files       : 0
Total size          : 2240 bytes
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs rmfs filesystem4.zvfs test_file5.txt
File test_file5.txt marked as deleted
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs gifs filesystem4.zvfs          
Filesystem file     : filesystem4.zvfs
Files present       : 1
Free entries        : 31
Deleted files       : 0
Total size          : 2240 bytes
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs lsfs filesystem4.zvfs
Name: test_file6.txt
Size: 26 bytes
Created: 2025-12-09 11:23:53
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs dfrgfs filesystem4.zvfs              
1 files defragmented
64 bytes freed
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs gifs filesystem4.zvfs              
Filesystem file     : filesystem4.zvfs
Files present       : 1
Free entries        : 31
Deleted files       : 0
Total size          : 2176 bytes
♥ ~/Desktop/Uni/2. Jahr/Software Construction/hs25-soco-group-004/SoCo_HS25-group_004-a3 java zvfs lsfs filesystem4.zvfs                
Name: test_file6.txt
Size: 26 bytes
Created: 2025-12-09 15:15:18

# Major Java Challenges
A particularly challenging part was defining the metadata layout and the sizes of header and file-entry fields. Continuously got BufferOverflowException or newPosition > limit. 

# AI Prompts
"I'm struggling with Step 9, guide me step by step to help me solve it"
"My Java Code is not working because of missing syntax, help me complete it"
"In my Java Code catfs throws a null error, why?"
"dfrgfs destroys the second file to 0 bytes and the wrong date, please help me find the issue in the java code"

# Authors
Natalia Piegat (missbo-cyber is my github account which I have linked in my Visual Studio), Julie Truc, Fraia Pérez-Rayón

