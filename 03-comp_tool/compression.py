import heapq
import pickle
from collections import defaultdict
from bitarray import bitarray

class Node:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = defaultdict(int)
    for char in text:
        frequency[char] += 1
    
    priority_queue = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)
    
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = Node(None, left.freq + right.freq, left, right)
        heapq.heappush(priority_queue, merged)
    
    return priority_queue[0]

def generate_huffman_codes(node, code='', code_map={}):
    if node is None:
        return

    if node.char is not None:
        code_map[node.char] = bitarray(code)
        return

    generate_huffman_codes(node.left, code + '0', code_map)
    generate_huffman_codes(node.right, code + '1', code_map)
    
    return code_map

def encode_text(text, code_map):
    encoded_text = bitarray()
    for char in text:
        encoded_text.extend(code_map[char])
    return encoded_text

def save_compressed_file(output_filename, encoded_text, huffman_tree):
    with open(output_filename, 'wb') as f:
        pickle.dump((encoded_text, huffman_tree), f)

def compress_file(input_filename, output_filename):
    with open(input_filename, 'r') as f:
        text = f.read()
    
    huffman_tree = build_huffman_tree(text)
    code_map = generate_huffman_codes(huffman_tree)
    encoded_text = encode_text(text, code_map)
    
    save_compressed_file(output_filename, encoded_text, huffman_tree)

def load_compressed_file(input_filename):
    with open(input_filename, 'rb') as f:
        encoded_text, huffman_tree = pickle.load(f)
    return encoded_text, huffman_tree

def decode_text(encoded_text, huffman_tree):
    decoded_text = []
    node = huffman_tree
    for bit in encoded_text:
        if bit == 0:
            node = node.left
        else:
            node = node.right
        
        if node.char is not None:
            decoded_text.append(node.char)
            node = huffman_tree
    
    return ''.join(decoded_text)

def decompress_file(input_filename, output_filename):
    encoded_text, huffman_tree = load_compressed_file(input_filename)
    decoded_text = decode_text(encoded_text, huffman_tree)
    
    with open(output_filename, 'w') as f:
        f.write(decoded_text)

# Example usage
input_filename = '135-0.txt'
output_filename = 'compressed.bin'
compress_file(input_filename, output_filename)
print(f"File '{input_filename}' has been compressed to '{output_filename}'")

compressed_filename = 'compressed.bin'
decompressed_filename = 'decompressed.txt'
decompress_file(compressed_filename, decompressed_filename)
print(f"File '{compressed_filename}' has been decompressed to '{decompressed_filename}'")
