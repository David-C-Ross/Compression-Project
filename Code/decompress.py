import bwt
import lz77
import huffman
from bitarray import bitarray


if __name__ == '__main__':

    print('program usage : <input.txt> <output.txt>')
    input_file, output_file = input().split()

    data = bitarray()

    try:
        with open(input_file, 'rb') as f:
            data.fromfile(f)
        with open('huffman.txt', 'r') as f:
            huff_dict = f.read()
    except IOError:
        print('Could not open input files ...')
        raise

    decoded_huff = huffman.huffman_decoding(data.to01(), huff_dict)
    decoded = lz77.decompress(lz77.from_bytes(bytearray(decoded_huff)))
    # decoded = bwt.ibwt(decoded)

    try:
        with open(output_file, 'w') as f:
            f.write(decoded)
            print('File was decompressed successfully and saved to output path ...')
    except IOError:
        print('Could not write to output file ...')
        raise
