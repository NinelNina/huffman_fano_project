from matplotlib import pyplot as plt


class ShannonFanoNode:
    def __init__(self, char, prob, char_count):
        self.char = char
        self.prob = prob
        self.char_count = char_count
        self.bit = ""
        self.left = None
        self.right = None


def build_shannon_fano_tree(probabilities):
    def split_symbols(symbols):
        total_prob = sum(char[1] for char in symbols)
        left_prob = 0
        split_index = 0

        tmp = []
        for i, symbol in enumerate(symbols):
            left_prob += symbol[1]
            tmp.append(abs(total_prob / 2 - left_prob))
            if i > 0:
                if tmp[i] > tmp[i - 1]:
                    split_index = i - 1
                    left_prob -= symbol[1]
                    break

        return symbols[:split_index + 1], symbols[split_index + 1:]

    def build_tree(symbols):
        if len(symbols) == 1:
            return ShannonFanoNode(symbols[0][0], symbols[0][1], 1)

        left, right = split_symbols(symbols)
        left_symbols = [item[0] for item in left]
        right_symbols = [item[0] for item in right]

        left_probabilities = [item[1] for item in left]
        right_probabilities = [item[1] for item in right]

        total_left_probability = sum(left_probabilities)
        total_right_probability = sum(right_probabilities)

        root_symb = ''.join(left_symbols + right_symbols)
        total_probability = total_left_probability + total_right_probability

        root = ShannonFanoNode(
            root_symb,
            total_probability,
            len(left) + len(right)
        )

        root.left = build_tree(left)
        root.right = build_tree(right)

        return root

    symbols = [(f"z{i + 1}", p) for i, p in enumerate(probabilities)]
    symbols.sort(key=lambda x: x[1], reverse=True)
    root = build_tree(symbols)

    def assign_codes(node, code=""):
        if node:
            if node.char is not None:
                if node.char_count == 1:
                    print(f"{node.char} = {code}, L = {len(code)}")
            assign_codes(node.left, code + "0")
            assign_codes(node.right, code + "1")

    assign_codes(root)
    return root