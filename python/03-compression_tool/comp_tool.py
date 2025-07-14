import heapq
import pickle
from bitarray import bitarray

def create_freq_table(s):

    freq_table = {}

    for c in s:
        if c not in freq_table:
            freq_table[c] = 1
        else:
            freq_table[c] += 1
    return freq_table

def encode_text(text, code_map):
    encoded_text = bitarray()
    for char in text:
        encoded_text.extend(code_map[char])
    return encoded_text

def create_huffman_tree(freq_table):

    class Node:
        def __init__(self, freq, char=False):
            self.freq = freq
            self.char = char
            self.right = None
            self.left = None

    heap = []
    tiebreaker = 0

    for k, v in freq_table.items():
        n = Node(v, k)
        heapq.heappush(heap, (n.freq, tiebreaker, n))
        tiebreaker += 1

    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        n = Node(a[0] + b[0])
        n.left = a
        n.right = b
        heapq.heappush(heap, (n.freq, tiebreaker, n))
        tiebreaker += 1
    return heap[0]

def create_char_to_binary_mapping(huffman_tree):

    char_to_binary = {}
    binary_to_char = {}

    def dfs(n, binary_string):
        if not n:
            return
        _ , _ , node = n
        if not node.left and not node.right:
            binary_to_char["".join(binary_string)] = node.char 
            char_to_binary[node.char] = bitarray("".join(binary_string))
        dfs(node.left, binary_string + ["0"])
        dfs(node.right, binary_string + ["1"])

    dfs(huffman_tree, [])

    return char_to_binary, binary_to_char

def store_bits(bits, binary_to_char, filename):
    with open(filename, 'wb') as f:
        pickle.dump((binary_to_char, bits), f)

def load_bits(filename):
    with open(filename, 'rb') as file:
        comp_table, bits = pickle.load(file)
        return bits.to01(), comp_table

def print_file(decoded_bits, comp_table):
    bits = []
    decoded_string = []
    for bit in decoded_bits:
        bits.append(bit) 
        bit_str = "".join(bits)
        if bit_str in comp_table:
            decoded_string.append(comp_table[bit_str])
            bits = []
    print("".join(decoded_string))

def main():
    with open("moby_dick.txt", "r") as file:
        s = file.read()
    freq_table = create_freq_table(s)
    huffman_tree = create_huffman_tree(freq_table)
    char_to_binary, binary_to_char = create_char_to_binary_mapping(huffman_tree)
    bits = encode_text(s, char_to_binary)
    store_bits(bits, binary_to_char, "test_string.pkl")
    decoded_bits, comp_table = load_bits("test_string.pkl")
    print_file(decoded_bits, comp_table)

main()



