import bwt
import lz77
import huffman
from bitarray import bitarray

if __name__ == '__main__':

    print('program usage : <input.txt> <output.txt>')
    input_file, output_file = input().split()

    # read the input file
    try:
        with open(input_file, 'rb') as f:
            data = f.read()
    except IOError:
        print('Could not open input file ...')
        raise

    # data = bwt.bwt(str(data))
    lz77_encoding = lz77.compress(data)
    huff_encoding, huff_tree = huffman.huffman_encoding(lz77.to_bytes(lz77_encoding))

    try:
        with open(output_file, 'wb') as f:
            f.write(bitarray(huff_encoding))
        with open('huffman.txt', 'w') as f:
            f.write(str(huff_tree))
        print('File was compressed successfully and saved to output path ...')
    except IOError:
        print('Could not write to output file ...')
        raise
