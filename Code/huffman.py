import ast


class Node:

    def __init__(self, prob, symbol, left=None, right=None):
        # probability of symbol
        self.prob = prob

        # symbol
        self.symbol = symbol

        # left node
        self.left = left

        # right node
        self.right = right

        # tree direction (0,1)
        self.code = ''


codes = dict()


def calculate_probability(data):
    """
    A helper function to calculate the probability of symbols in given data
    """
    symbols = dict()
    for element in data:
        if symbols.get(element) is None:
            symbols[element] = 1
        else:
            symbols[element] += 1
    return symbols


def calculate_codes(node, val=''):
    """
    A helper function to print the codes of symbols by traveling the huffman tree
    """
    # huffman code for current node
    new_val = val + str(node.code)

    if node.left:
        calculate_codes(node.left, new_val)
    if node.right:
        calculate_codes(node.right, new_val)

    if not node.left and not node.right:
        codes[node.symbol] = new_val

    return codes


def output_encoded(data, coding):
    """
    A helper function to obtain the encoded output
    """
    encoding_output = []
    for c in data:
        encoding_output.append(coding[c])

    string = ''.join([str(item) for item in encoding_output])
    return string


def create_huff_tree(symbols_with_probs):
    symbols = symbols_with_probs.keys()
    nodes = []

    # converting symbols and probabilities into huffman tree nodes
    for symbol in symbols:
        nodes.append(Node(symbols_with_probs.get(symbol), symbol))

    while len(nodes) > 1:
        # sort all the nodes in ascending order based on their probability
        nodes = sorted(nodes, key=lambda x: x.prob)

        # pick two smallest nodes
        right = nodes[0]
        left = nodes[1]

        left.code = 0
        right.code = 1

        # combine the two smallest nodes to create new node
        new_node = Node(left.prob + right.prob, left.symbol + right.symbol, left, right)

        nodes.remove(left)
        nodes.remove(right)
        nodes.append(new_node)

    return nodes[0]


def huffman_encoding(data):
    symbol_with_probs = calculate_probability(data)

    tree = create_huff_tree(symbol_with_probs)

    huff_encoding = calculate_codes(tree)
    encoded_output = output_encoded(data, huff_encoding)
    return encoded_output, symbol_with_probs


def huffman_decoding(encoded_data, freq_dict):
    huffman_tree = create_huff_tree(ast.literal_eval(freq_dict))
    tree_head = huffman_tree
    decoded_output = []

    for x in encoded_data:
        if x == '1':
            huffman_tree = huffman_tree.right
        elif x == '0':
            huffman_tree = huffman_tree.left
        try:
            if huffman_tree.left.symbol is None and huffman_tree.right.symbol is None:
                pass
        except AttributeError:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head

    return decoded_output
