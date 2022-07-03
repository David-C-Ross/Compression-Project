import lz77
import huffman
from bitarray import bitarray

if __name__ == '__main__':

    print('program usage : <input.txt> <output.txt>')
    input_file, output_file = input().split()

    # read the input file
    try:
        with open(input_file, 'r') as f:
            data = f.read()
    except IOError:
        print('Could not open input file ...')
        raise
    lz77_encoded = lz77.compress(data)
    final_encoding, huff_tree = huffman.huffman_encoding(lz77_encoded)
    try:
        with open(output_file, 'wb') as f:
            f.write(bitarray(final_encoding).tobytes())
            print('File was compressed successfully and saved to output path ...')
        with open('huffman.txt', 'w') as f:
            f.write(str(huff_tree))
    except IOError:
        print('Could not write to output file ...')
        raise
