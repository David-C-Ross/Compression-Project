# Compression-Project
An implementation of a compression/decompression algorithm using [lz77](https://en.wikipedia.org/wiki/LZ77_and_LZ78) and [huffman coding](https://en.wikipedia.org/wiki/Huffman_coding).  

The default settings for the lz77 compression is using a max offset of 2047 and a max match length of 31. These parameters can be altered manually in the program if wanted.

### How to run:

1. Open the terminal
2. Set the current directory to the one where compress.py/decompress.py are located.
3. To compress a file type:  
   ```bash
   python3 compress.py <InputFileName> <OutputFileName>  
   ```  
   To decompress a file type:
   ```bash
   python3 compress.py <InputFileName> <OutputFileName>
   ```
4. The compressed/ decompressed file will be stored as `OutputFileName` in the same directory.
     
