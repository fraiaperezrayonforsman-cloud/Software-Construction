import java.io.IOException;
import java.io.RandomAccessFile;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
//import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;


public class zvfs {
    public static final int HEADER_SIZE = 64;
    public static final int FILE_ENTRY_SIZE = 64;
    public static final int FILE_CAPACITY = 32;
    public static final byte[] MAGIC = "ZVFSDSK1".getBytes(StandardCharsets.US_ASCII);
    public static final int ALIGNMENT = 64;
    public static final int VERSION = 1;
    public static final int FILE_TABLE_OFFSET = 64;
    public static final int DATA_START_OFFSET = HEADER_SIZE + (FILE_CAPACITY * FILE_ENTRY_SIZE);

    public static void mkfs(String zvfs_name){
        try (RandomAccessFile file = new RandomAccessFile(zvfs_name,"rw")){
        ByteBuffer header = ByteBuffer.allocate(HEADER_SIZE).order(ByteOrder.LITTLE_ENDIAN);
        header.put(MAGIC);
        header.put((byte) VERSION);
        header.put((byte) 0);
        header.putShort((short) 0);
        header.putShort((short) 0);
        header.putShort((short) FILE_CAPACITY);
        header.putShort((short) FILE_ENTRY_SIZE);
        header.putShort((short) 0);
        header.putInt(FILE_TABLE_OFFSET);
        header.putInt(DATA_START_OFFSET);
        header.putInt(DATA_START_OFFSET);
        header.putShort((short) 0);
        header.put(new byte[26]);

        header.flip();
        file.write(header.array());

        byte[] zeroEntry = new byte[FILE_ENTRY_SIZE];
        for (int i = 0; i < FILE_CAPACITY; i++)
            file.write(zeroEntry);

        System.out.println("Zest Virtual Filesystem " + zvfs_name + " created correctly.");

    } catch (IOException error) {System.out.println("Could not create filesystem: " + error.getMessage());
    } 
}
    public static int paddingEstimation(int data_size) {
        int dif = data_size % ALIGNMENT;
        return dif == 0 ? 0: ALIGNMENT - dif;
    }

    public static void field_update(String zvfs_file, long offset, String format, long value){
        try (RandomAccessFile file = new RandomAccessFile(zvfs_file, "rw")){
            ByteBuffer buf = ByteBuffer.allocate(8).order(ByteOrder.LITTLE_ENDIAN);
            switch (format) {
                case "I":  
                    buf.putInt((int) value);
                    break;
                case "H":  
                    buf.putShort((short) value);
                    break;
                default:
                    throw new IllegalArgumentException("Unsupported format: " + format);
            }
            buf.flip();
            file.seek(offset);
            file.write(buf.array(), 0, buf.remaining());
        } catch (IOException error){
            System.out.println("Could not update field:" + error.getMessage());
        } 
    }
    
    public static void addfs(String zvfs_name, String new_file){
        try {
            Path p = Paths.get(new_file);
            if (!p.toFile().exists()) 
                throw new IOException("filepath does not exist");
            byte[] file_data = java.nio.file.Files.readAllBytes(p);
            int file_len = file_data.length;

            String file_name = p.getFileName().toString();
            if (file_name.length() >= 32) throw new IOException(file_name + "is larger than 32 characters");

            int padding = paddingEstimation(file_len);

            //look for free space in filesystem
            try (RandomAccessFile filesys = new RandomAccessFile(zvfs_name, "rw")){
                filesys.seek(0);
                byte[] header_translated = new byte[HEADER_SIZE];
                filesys.readFully(header_translated);

                ByteBuffer h = ByteBuffer.wrap(header_translated).order(ByteOrder.LITTLE_ENDIAN);
                
                byte[] magic = new byte[8];

                h.get(magic);              
                h.get();                  
                h.get();                  
                h.getShort();             
                short file_count = h.getShort();
                short file_capacity = h.getShort();
                h.getShort();               
                h.getShort();            
                h.getInt();                 
                h.getInt();                
                int next_free_offset = h.getInt();
                h.getShort();
                byte[] reserved = new byte[26]; 
                h.get(reserved);                  

                if (file_count >= file_capacity) throw new IOException("no more space left for new files");
                if (!java.util.Arrays.equals(magic, MAGIC)) throw new IOException("invalid magic string");
                
                int entry_offset = -1;

                for (int i=0; i < FILE_CAPACITY; i++){
                    int current_offset = FILE_TABLE_OFFSET + i * FILE_ENTRY_SIZE;
                    filesys.seek(current_offset);
                    if (filesys.readByte() == 0){
                        entry_offset = current_offset;
                        break;
                    }
                }

                if (entry_offset == -1) throw new IOException("no free file entry available");

                filesys.seek(next_free_offset);
                filesys.write(file_data);

                if (padding > 0) 
                    filesys.write(new byte[padding]);
                
                int new_next_free_offset = next_free_offset + file_len + padding;
                
                // add file
                ByteBuffer entry = ByteBuffer.allocate(FILE_ENTRY_SIZE);
                byte [] file_name_enc = file_name.getBytes(StandardCharsets.UTF_8);
                byte [] name_field = new byte[32];
                int len_file_name = Math.min(file_name_enc.length, 31);
                System.arraycopy(file_name_enc, 0, name_field, 0, len_file_name);
                name_field[len_file_name] = 0;

                int timestamp = (int) (System.currentTimeMillis()/1000);
                
                entry.put(name_field);
                entry.putInt(next_free_offset);
                entry.putInt(file_len);
                entry.put((byte) 0);
                entry.put((byte) 0);
                entry.putShort((short) 0);
                entry.putLong(timestamp);
                entry.put(new byte[12]);

                entry.flip();
                filesys.seek(entry_offset);
                filesys.write(entry.array());

                //update header fields
                field_update(zvfs_name, 28, "I",new_next_free_offset);
                field_update(zvfs_name, 12, "H", file_count + 1);

                System.out.println("The" + new_file + "was added correctly to" + zvfs_name);
                } catch (IOException error) {
                System.out.println("Error while adding new file to filesystem: " + error);
            }
    } catch (IOException error){
        System.out.println("Error while adding new file to filesystem:"+ error);
}
}

public static void lsfs(String zvfsName) {
    try {
        Path p = Paths.get(zvfsName);
        if (!p.toFile().exists()) {
            throw new IOException("Filesystem does not exist");
        }

        try (RandomAccessFile fs = new RandomAccessFile(zvfsName, "r")) {

            for (int i = 0; i < FILE_CAPACITY; i++) {
                int entryOffset = FILE_TABLE_OFFSET + i * FILE_ENTRY_SIZE;
                fs.seek(entryOffset);

                byte[] entryBytes = new byte[FILE_ENTRY_SIZE];
                fs.readFully(entryBytes);

                ByteBuffer b = ByteBuffer.wrap(entryBytes).order(ByteOrder.LITTLE_ENDIAN);

                byte[] nameBytes = new byte[32];
                b.get(nameBytes);

                int start = b.getInt();
                int len = b.getInt();
                byte flags = b.get();
                byte deleted = b.get();
                b.getShort();
                long created = b.getLong();

                if (nameBytes[0] == 0 || deleted == 1)
                    continue;

                String name = new String(nameBytes, StandardCharsets.UTF_8).split("\0")[0];

                String time = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss")
                        .format(new java.util.Date(created * 1000L));

                System.out.println("Name: " + name);
                System.out.println("Size: " + len + " bytes");
                System.out.println("Created: " + time);
                System.out.println();
            }

        }

    } catch (IOException e) {
        System.out.println("Error accessing or reading filesystem: " + e.getMessage());
    }
}

    public static void catfs(String zvfsName, String fileName) {
        try {
            Path p = Paths.get(zvfsName);
            if (!p.toFile().exists()) {
                throw new IOException("Filesystem does not exist");
            }
            Path path = Paths.get(fileName);
            String justName = path.getFileName().toString(); 
            boolean find = false;
            try (RandomAccessFile fs = new RandomAccessFile(zvfsName, "r")) {

                for (int i = 0; i < FILE_CAPACITY; i++) {

                    int entryOffset = FILE_TABLE_OFFSET + i * FILE_ENTRY_SIZE;
                    fs.seek(entryOffset);

                    byte[] entryBytes = new byte[FILE_ENTRY_SIZE];
                    fs.readFully(entryBytes);

                    ByteBuffer b = ByteBuffer.wrap(entryBytes).order(ByteOrder.LITTLE_ENDIAN);

                    byte[] nameBytes = new byte[32];
                    b.get(nameBytes);

                    int start = b.getInt();
                    int len = b.getInt();
                    byte flags = b.get();
                    byte deleted = b.get();
                    b.getShort();
                    long created = b.getLong();

                    if (nameBytes[0] == 0 || deleted == 1)
                        continue;

                    String entryName = new String(nameBytes, StandardCharsets.UTF_8).split("\0")[0];

                    if (entryName.equals(justName)) {
                        find = true;
                        fs.seek(start);
                        byte[] fileData = new byte[len];
                        fs.readFully(fileData);
                        System.out.println(new String(fileData, StandardCharsets.UTF_8));
                        break;
                    }
                }
                if (find == false)
                    System.out.println("This file does not exists in this filesystem");
            }

        } catch (IOException e) {
            System.out.println("Error reading filesystem: " + e.getMessage());
        }
    }

    public static void main(String[] args) {

        if (args.length < 2) {
            System.out.println("not enough arguments");
            return;
        }

        String command = args[0];

        switch (command) {
            case "mkfs":
                mkfs(args[1]);
                break;

            case "addfs":
                if (args.length != 3) {
                    System.out.println("Usage: addfs <filesystem> <file>");
                } else {
                    addfs(args[1], args[2]);
                }
                break;

            case "lsfs":
                if(args.length != 2){
                    System.out.println("Usage: lsfs <filesystem>");
                }
                else{
                    lsfs(args[1]);
                }
                break;
            case "catfs":
                if(args.length != 3){
                    System.out.println("Usage: catfs <filesystem> <file>");
                }
                else{
                    catfs(args[1],args[2]);
                }
                break;
            default:
                System.out.println("Unknown command: " + command);
                break;
        }
    }
}



    


  