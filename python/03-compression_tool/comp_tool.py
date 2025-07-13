import heapq
import pickle

s = "aaabbc"

freq_table = {}

# freq_table = {
#         "C":32,
#         "D":42,
#         "E":120,
#         "K":7,
#         "L":42,
#         "M":24,
#         "U":37,
#         "Z":2
#         }
for c in s:
    if c not in freq_table:
        freq_table[c] = 1
    else:
        freq_table[c] += 1

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

char_to_binary = {}
binary_to_char = {}

def dfs(n, binary_string):
    if not n:
        return
    _ , _ , node = n
    # if not node:
    #     return
    if not node.left and not node.right:
        binary_to_char["".join(binary_string)] = node.char 
        char_to_binary[node.char] = binary_string
    dfs(node.left, binary_string + ["0"])
    dfs(node.right, binary_string + ["1"])

dfs(heap[0], [])

bsu = []
for c in s:
    bsu.append(char_to_binary[c])

bs = []
for a in bsu:
    s = "".join(a)
    bs.append(s)

bs = "".join(bs)

encoded_bits = bs.encode('utf-8')

with open('test_string.pkl', 'wb') as f:
    pickle.dump((binary_to_char, encoded_bits), f)

with open('test_string.pkl', 'rb') as file:
    loaded_file = pickle.load(file)

comp_table, bits = loaded_file
decoded_bits = bits.decode('utf-8')

bits = []
decoded_string = ""
for bit in decoded_bits:
    bits.append(bit) 
    bit_str = "".join(bits)
    if bit_str in comp_table:
        decoded_string += comp_table[bit_str]
        bits = []
print(decoded_string)
