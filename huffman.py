import heapq


class Node:
    def __init__(self, char, prob, char_count):
        self.char = char
        self.prob = prob
        self.char_count = char_count
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.prob < other.prob


def build_huffman_tree(probabilities):
    list = [Node("z" + str(i + 1), p, 1) for i, p in enumerate(probabilities)]

    list.sort(reverse=True)

    for i in list:
        print(i.char + " = " + str(i.prob))
    print("\n")

    heapq.heapify(list)

    while len(list) > 1:
        left = heapq.heappop(list)
        right = heapq.heappop(list)

        if left.char_count > right.char_count:
            left, right = right, left
        merge_node = Node(left.char + right.char, round(left.prob + right.prob, 4), left.char_count + right.char_count)
        merge_node.left = left
        merge_node.right = right
        heapq.heappush(list, merge_node)

    return list[0]


def huffman_codes(root):
    codes = {}

    def assign_codes(node, code=""):
        if node:
            if node.char_count == 1:
                codes[node.char] = (code, node.prob)
            assign_codes(node.left, code + "0")
            assign_codes(node.right, code + "1")

    assign_codes(root)
    return codes