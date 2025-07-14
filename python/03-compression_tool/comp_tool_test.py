from comp_tool import create_huffman_tree, create_freq_table, create_char_to_binary_mapping, encode_text, print_file
from sys import getsizeof

freq_table = {
        "C":32,
        "D":42,
        "E":120,
        "K":7,
        "L":42,
        "M":24,
        "U":37,
        "Z":2
        }

def test_huffman_tree():
    t = create_huffman_tree(freq_table)
    assert t[2].freq == 306
    assert t[2].left[2].freq == 120
    assert t[2].right[2].freq == 186
    assert t[2].right[2].freq == 186
    assert t[2].right[2].right[2].freq == 107
    assert t[2].right[2].right[2].right[2].freq == 65

def test_valid_conversion():
    s = "aaabbc"
    freq_table = create_freq_table(s)
    huffman_tree = create_huffman_tree(freq_table)
    char_to_binary, binary_to_char = create_char_to_binary_mapping(huffman_tree)
    bits = encode_text(s, char_to_binary)
    converted_back_string = print_file(bits.to01(), binary_to_char)
    assert converted_back_string == s

def test_compression_performance():
    s = "asdfadddddddddddddddddddddddddddddddddddddddddddasdfadasdfadsfasdfaslfasdfkljlaskdjflkjalskdjflkasjdlfjalskdjflaksjflasdfasdfasfllsjdfasdfkjalkadfaf"
    freq_table = create_freq_table(s)
    huffman_tree = create_huffman_tree(freq_table)
    char_to_binary, _ = create_char_to_binary_mapping(huffman_tree)
    bits = encode_text(s, char_to_binary)
    memory_size_of_string = getsizeof(s)
    memory_size_of_bits = getsizeof(bits)
    assert 0.70 * memory_size_of_string > memory_size_of_bits




