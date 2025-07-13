import heapq
import pickle

def create_freq_table(s):

    freq_table = {}

    for c in s:
        if c not in freq_table:
            freq_table[c] = 1
        else:
            freq_table[c] += 1
    return freq_table

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
            char_to_binary[node.char] = binary_string
        dfs(node.left, binary_string + ["0"])
        dfs(node.right, binary_string + ["1"])

    dfs(huffman_tree, [])

    return char_to_binary, binary_to_char

def convert_string_to_binary(s, char_to_binary):
    bsu = []
    for c in s:
        bsu.append(char_to_binary[c])

    bs = []
    for a in bsu:
        s = "".join(a)
        bs.append(s)

    return "".join(bs)

def store_bits(bits, binary_to_char, binary_to_char_filename, binary_filename):
    encoded_bits = bits.encode('utf-8')

    with open(binary_to_char_filename, 'wb') as f:
        pickle.dump(binary_to_char, f)

    with open(binary_filename, "wb") as f:
        f.write(encoded_bits)


def load_bits(binary_to_char_filename, binary_filename):

    with open(binary_to_char_filename, 'rb') as file:
        binary_to_char = pickle.load(file)

    with open(binary_filename, "rb") as f:
        encoded_bits = f.read()
        decoded_bits = encoded_bits.decode('utf-8')
        return decoded_bits, binary_to_char

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
    bits = convert_string_to_binary(s, char_to_binary)
    store_bits(bits, binary_to_char, "table.pkl", "moby_dick.bin")
    decoded_bits, comp_table = load_bits("table.pkl", "moby_dick.bin")
    print_file(decoded_bits, comp_table)

    
main()



