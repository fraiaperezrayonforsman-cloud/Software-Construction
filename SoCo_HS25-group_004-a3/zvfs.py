import struct
import time
import os

from struct import pack, unpack

#Constant variables
HEADER_SIZE = 64
FILE_ENTRY = 64
FILE_CAPACITY = 32
MAGIC = b"ZVFSDSK1"
ALIGNMENT = 64
VERSION = 1
FILE_TABLE_OFFSET = 64
DATA_START_OFFSET = 64*(1+32)

FORMAT_STRING_HEADER = '<8s B B 2s H H H 2s I I I I H 26s'
FORMAT_STRING_FILE_ENTRY = '<32s I I B B 2s Q 12s'

def mkfs(zvfs_name):
    try:
        with open(zvfs_name, "wb") as filesys:
            header = pack(
                MAGIC,
                VERSION,
                0,
                b'\x00\x00',
                0,
                FILE_CAPACITY,
                FILE_ENTRY,
                b'\x00\x00',
                FILE_TABLE_OFFSET,
                DATA_START_OFFSET,
                DATA_START_OFFSET,
                0,
                0,
                b'\x00' * 26,
                FORMAT_STRING_HEADER,
                FORMAT_STRING_FILE_ENTRY
            )
            filesys.write(header)
        
        zero_entry = b'\x00' * FILE_ENTRY
        filesys.write(zero_entry * FILE_CAPACITY)
    except:
        IOError("could not create Virtual Filesystem correclty")

def padding_estimation(data_size):
    dif = data_size % FILE_ENTRY
    if dif == 0:
        return 0
    else:
        return ALIGNMENT - dif
    
def field_update():
    try:
        