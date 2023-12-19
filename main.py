import math

import tkinter as tk
from tkinter import ttk

import huffman
import fano


def visualize_huffman_tree(node, x, y, dx, dy, parent_code="", level=0):
    if node is not None:
        circle_radius = 30
        initial_x_offset = 16 * circle_radius
        x_offset = initial_x_offset / (2 ** level)
        y_offset = 80

        canvas.create_oval(x - circle_radius, y - circle_radius, x + circle_radius, y + circle_radius, fill='white',
                           outline='black')
        canvas.create_text(x, y, text=f"{node.char}\n{node.prob:.3f}", font=("Arial", 10))

        if node.left is not None:
            left_x = x - x_offset
            left_y = y + y_offset
            left_dx = dx / 2
            canvas.create_line(x, y + circle_radius, left_x, left_y - circle_radius, width=2, fill='blue')
            canvas.create_text((x + left_x) / 2, (y + left_y) / 2, text="0", font=("Arial", 10))
            visualize_huffman_tree(node.left, left_x, left_y, left_dx, dy, parent_code + "0", level + 1)

        if node.right is not None:
            right_x = x + x_offset
            right_y = y + y_offset
            right_dx = dx / 2
            canvas.create_line(x, y + circle_radius, right_x, right_y - circle_radius, width=2, fill='red')
            canvas.create_text((x + right_x) / 2, (y + right_y) / 2, text="1", font=("Arial", 10))
            visualize_huffman_tree(node.right, right_x, right_y, right_dx, dy, parent_code + "1", level + 1)


def binary_entropy(p, char_arr):
    n = len(p)
    str_res = 'H = -('
    str_num = ''
    H_X = 0
    for i in range(n):
        str_res += f'p({char_arr[i]}) * log(p({char_arr[i]}))'
        tmp = round(math.log2(p[i]), 4)
        H_X += round(p[i] * tmp, 4)
        str_num += f'{p[i]:.3f} +  * ({tmp:.3f})'
        if i < n - 1:
            str_res += ' + '
            str_num += ' + '
    H_X *= (-1)
    H_X = round(H_X, 4)
    str_res += ') = -(' + str_num + ') = ' + str(H_X) + '\n'
    return str_res, H_X


def code_length(codes):
    str_res = ""
    str_num = ""
    str_res += "L = "
    L = 0
    for i in range(len(codes)):
        str_res += f"{codes[i][1]} * {len(codes[i][0])}"
        tmp = round(codes[i][1] * len(codes[i][0]), 3)
        str_num += f"{tmp}"
        L += tmp
        if i < len(codes) - 1:
            str_res += ' + '
            str_num += ' + '
    str_res += " = " + str_num
    str_res += f" = {L:.3f}"
    L = round(L, 3)
    return str_res, L


def redundancy(H, L):
    r = round(L - H, 3)
    str_res = f"r = L - H = {L} - {H} = " + str(r)
    return str_res

    symbols = [(f"z{i + 1}", p) for i, p in enumerate(probabilities)]
    symbols.sort(key=lambda x: x[1], reverse=True)
    root = build_tree(symbols)
    return root


def calculate_huffman_tree():
    probabilities = [float(entry.get()) for entry in probability_entries]
    root = huffman.build_huffman_tree(probabilities)
    codes = huffman.huffman_codes(root)
    display_result(codes, root, probabilities, canvas)


def calculate_phano_tree():
    probabilities = [float(entry.get()) for entry in probability_entries]
    root = fano.build_shannon_fano_tree(probabilities)
    codes = huffman.huffman_codes(root)
    display_result(codes, root, probabilities, canvas)


def add_input_element():
    label = ttk.Label(input_frame, text=f"P(Z{len(probability_entries) + 1}):")
    label.grid(row=0, column=len(probability_entries), padx=5, pady=5)
    entry = ttk.Entry(input_frame, width=5)
    entry.insert(0, "0")
    entry.grid(row=1, column=len(probability_entries), padx=5, pady=5)
    probability_entries.append(entry)


def remove_input_element():
    if len(probability_entries) > 0:
        last_label = input_frame.grid_slaves(row=0, column=len(probability_entries) - 1)
        last_entry = input_frame.grid_slaves(row=1, column=len(probability_entries) - 1)
        last_label[0].grid_remove()
        last_entry[0].grid_remove()
        probability_entries.pop()


def display_result(codes, root, input_elements, canvas=None):
    result_text = "\n".join([f"{char} = {code[0]}, L = {len(code[0])}" for char, code in codes.items()])
    codesList = list(codes.values())
    L = code_length(codesList)
    input_element_strings = [f"z{i + 1}" for i in range(len(input_elements))]
    H = binary_entropy(input_elements, input_element_strings)
    result_text += "\n" + "\n" + L[0] + "\n" + "\n" + H[0] + "\n" + "\n" + str(redundancy(H[1], L[1]))
    result_label.config(text=result_text)
    canvas.delete("all")
    visualize_huffman_tree(root, 300, 50, 120, 0)


def on_canvas_scroll(event):
    if event.delta:
        if event.delta > 0:
            canvas.scale("all", event.x, event.y, 1.2, 1.2)
        elif event.delta < 0:
            canvas.scale("all", event.x, event.y, 0.8, 0.8)


def on_canvas_drag_start(event):
    canvas.scan_mark(event.x, event.y)


def on_canvas_drag(event):
    canvas.scan_dragto(event.x, event.y, gain=1)


window = tk.Tk()
window.title("Huffman Coding")
window.geometry("1000x800")

input_frame = ttk.Frame(window)
input_frame.pack()

probability_entries = []
for i in range(10):
    label = ttk.Label(input_frame, text=f"P(Z{i + 1}):")
    label.grid(row=0, column=i, padx=5, pady=5)
    entry = ttk.Entry(input_frame, width=5)
    entry.insert(0, "0")
    entry.grid(row=1, column=i, padx=5, pady=5)
    probability_entries.append(entry)

add_button = ttk.Button(input_frame, text="Add Input", command=add_input_element)
add_button.grid(row=1, column=19, padx=5, pady=10)

remove_button = ttk.Button(input_frame, text="Remove Input", command=remove_input_element)
remove_button.grid(row=1, column=20, padx=5, pady=10)

calculate_button = ttk.Button(input_frame, text="Calculate Huffman Codes", command=calculate_huffman_tree)
calculate_button.grid(row=2, column=10, columnspan=10, pady=10)

calculate_button = ttk.Button(input_frame, text="Calculate Phano Codes", command=calculate_phano_tree)
calculate_button.grid(row=2, column=2, columnspan=11, pady=10)

result_frame = ttk.Frame(window)
result_frame.pack()

canvas = tk.Canvas(result_frame, width=800, height=600, bg='white')
canvas.grid(row=0, column=1)

result_label = ttk.Label(result_frame, text="", wraplength=250)
result_label.grid(row=0, column=0)

canvas.bind("<MouseWheel>", on_canvas_scroll)
canvas.bind("<ButtonPress-1>", on_canvas_drag_start)
canvas.bind("<B1-Motion>", on_canvas_drag)

window.mainloop()
