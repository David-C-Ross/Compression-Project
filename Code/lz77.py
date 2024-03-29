def compress(input_string, max_offset=2047, max_length=31):
    """Compress the input string into a list of (length, offset, char) values"""

    # Create the input
    input_array = str(input_string[:])

    # Create a string of the characters which have been passed
    window = ""

    # Store output in this list
    output = []

    while input_array != "":
        length, offset = best_length_offset(window, input_array, max_length, max_offset)
        output.append((offset, length, input_array[0]))
        window += input_array[:length]
        input_array = input_array[length:]

    return output


def to_bytes(compressed_representation, offset_bits=11, length_bits=5):
    """Turn the compression representation into a byte array"""
    output = bytearray()

    offset_length_bytes = int((offset_bits + length_bits) / 8)

    for value in compressed_representation:
        offset, length, char = value
        offset_length_value = (offset << length_bits) + length

        for count in range(offset_length_bytes):
            output.append(
                (offset_length_value >> (8 * (offset_length_bytes - count - 1)))
                & 0b11111111
            )

        if char is not None:
            if offset == 0:
                output.append(ord(char))
        else:
            output.append(0)

    return output


def best_length_offset(window, input_string, max_length=31, max_offset=2047):
    """Take the window and an input string and return the offset and length
    with the biggest length of the input string as a substring"""

    if max_offset < len(window):
        cut_window = window[-max_offset:]
    else:
        cut_window = window

    # Return (0, 0) if the string provided is empty
    if input_string is None or input_string == "":
        return 0, 0

    # Initialise result parameters - best case so far
    length, offset = (1, 0)

    # This should also catch the empty window case
    if input_string[0] not in cut_window:
        best_length = repeating_length_from_start(input_string[0], input_string[1:])
        return min((length + best_length), max_length), offset

    # Best length now zero to allow occurrences to take priority
    length = 0

    # Test for every string in the window, in reverse order to keep the offset as low as possible
    # Look for either the whole window or up to max offset away, whichever is smaller
    for index in range(1, (len(cut_window) + 1)):
        # Get the character at this offset
        char = cut_window[-index]
        if char == input_string[0]:
            found_offset = index
            # Collect any further strings which can be found
            found_length = repeating_length_from_start(
                cut_window[-index:], input_string
            )
            if found_length > length:
                length = found_length
                offset = found_offset

    # Only return up to the maximum length
    # This will capture the maximum number of characters allowed
    # although it might not capture the maximum amount of characters *possible*
    return min(length, max_length), offset


def repeating_length_from_start(window, input_string):
    """Get the maximum repeating length of the input from the start of the window"""
    if window == "" or input_string == "":
        return 0

    if window[0] == input_string[0]:
        return 1 + repeating_length_from_start(
            window[1:] + input_string[0], input_string[1:]
        )
    else:
        return 0


def decompress(data):
    """Turn the list of (offset, length, char) into an output string"""

    output = ""

    for value in data:
        offset, length, char = value

        if length == 0:
            if char is not None:
                output += char
        else:
            if offset == 0:
                if char is not None:
                    output += char
                    length -= 1
                    offset = 1
            start_index = len(output) - offset
            for i in range(length):
                output += output[start_index + i]

    return output


def from_bytes(compressed_bytes, offset_bits=11, length_bits=5):
    """Take in the compressed format and return a higher level representation"""

    output = []
    offset_length_bytes = int((offset_bits + length_bits) / 8)

    while len(compressed_bytes) > 0:
        offset_length_value = 0
        for _ in range(offset_length_bytes):
            if compressed_bytes:
                offset_length_value = (offset_length_value * 256) + int(
                    compressed_bytes.pop(0)
                )

        offset = offset_length_value >> length_bits
        length = offset_length_value & ((2 ** length_bits) - 1)

        if offset > 0:
            char_out = None
        else:
            # Get the next character and convert to an ascii character
            char_out = str(chr(compressed_bytes.pop(0)))

        output.append((offset, length, char_out))

    return output
