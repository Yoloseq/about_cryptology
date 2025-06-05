import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import string
import matplotlib.pyplot as plt
from nltk.corpus import words
import re
import random

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 全局变量
current_mapping = {}
locked_mapping = {}  # 锁定的手动映射
english_words = set(words.words())
ENGLISH_FREQ = 'etaoinshrdlcumwfgypbvkjxqz'

def enforce_unique_mapping(mapping):
    used_values = set()
    unique_mapping = {}
    for k, v in mapping.items():
        if v not in used_values:
            unique_mapping[k] = v
            used_values.add(v)
    return unique_mapping

def analyze_frequency(cipher_text):
    letters_only = [c for c in cipher_text.lower() if c in string.ascii_lowercase]
    counter = Counter(letters_only)
    sorted_letters = [item[0] for item in counter.most_common()]
    used_values = set()
    mapping = {}
    for c in sorted_letters:
        for target in ENGLISH_FREQ:
            if target not in used_values:
                mapping[c] = target
                used_values.add(target)
                break
    return mapping

def apply_mapping(text, mapping):
    result = ""
    for ch in text:
        if ch.lower() in mapping:
            mapped_char = mapping[ch.lower()]
            result += mapped_char.lower()
        else:
            result += ch.lower()
    return result

def evaluate_mapping(mapping):
    decrypted = apply_mapping(input_text.get("1.0", tk.END), mapping).lower()
    words_list = re.findall(r'[a-zA-Z]+', decrypted)
    match_count = sum(1 for w in words_list if w.lower() in english_words)
    return match_count / max(1, len(words_list)), decrypted

def optimize_mapping():
    global current_mapping, locked_mapping
    best_mapping = current_mapping.copy()
    best_score, _ = evaluate_mapping(best_mapping)

    for _ in range(500):
        temp_mapping = best_mapping.copy()

        # 找出未锁定的key
        unlocked_keys = [k for k in temp_mapping if k not in locked_mapping]
        if len(unlocked_keys) < 2:
            break

        a, b = random.sample(unlocked_keys, 2)
        temp_mapping[a], temp_mapping[b] = temp_mapping[b], temp_mapping[a]

        # 强制将锁定映射写回
        for lk, lv in locked_mapping.items():
            temp_mapping[lk] = lv

        temp_mapping = enforce_unique_mapping(temp_mapping)
        score, _ = evaluate_mapping(temp_mapping)
        if score > best_score:
            best_score = score
            best_mapping = temp_mapping.copy()

    current_mapping = best_mapping
    result_text = apply_mapping(input_text.get("1.0", tk.END), current_mapping)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result_text)
    update_mapping_table()
    messagebox.showinfo("迭代优化完成", f"最终匹配率为：{best_score:.2%}")

def auto_decrypt():
    global current_mapping, locked_mapping
    cipher_text = input_text.get("1.0", tk.END)
    current_mapping = analyze_frequency(cipher_text)
    current_mapping = enforce_unique_mapping(current_mapping)
    locked_mapping = {}  # 重置锁定映射
    decrypted = apply_mapping(cipher_text, current_mapping)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, decrypted.lower())
    update_mapping_table()

def manual_replace():
    global current_mapping, locked_mapping
    a = from_entry.get().lower()
    b = to_entry.get().lower()
    if a in string.ascii_lowercase and b in string.ascii_lowercase:
        old_b = current_mapping.get(a, None)
        conflict_key = None
        for k, v in current_mapping.items():
            if v == b and k != a:
                conflict_key = k
                break
        if conflict_key:
            current_mapping[conflict_key] = old_b
            if conflict_key in locked_mapping:
                del locked_mapping[conflict_key]
        current_mapping[a] = b
        locked_mapping[a] = b  # 加入锁定映射
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, apply_mapping(input_text.get("1.0", tk.END), current_mapping).lower())
        update_mapping_table()
    else:
        messagebox.showerror("输入错误", "请输入有效的单个英文字母。")

def show_frequency_chart():
    cipher_text = input_text.get("1.0", tk.END)
    letters_only = [c for c in cipher_text.lower() if c in string.ascii_lowercase]
    counter = Counter(letters_only)
    labels, values = zip(*counter.most_common())
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color='skyblue')
    plt.title("密文中字符频率分布")
    plt.xlabel("字符")
    plt.ylabel("频率")
    plt.show()

def check_dictionary():
    decrypted = output_text.get("1.0", tk.END).lower()
    words_list = re.findall(r'[a-zA-Z]+', decrypted)
    match_count = sum(1 for w in words_list if w.lower() in english_words)
    total_words = len(words_list)
    percentage = (match_count / total_words * 100) if total_words > 0 else 0
    messagebox.showinfo("词典匹配建议",
                        f"解密文本中有 {match_count}/{total_words} 个单词匹配英文词典。\n"
                        f"匹配率：{percentage:.1f}%\n"
                        "匹配率越高，解密越可能正确。")

def update_mapping_table():
    table_text.delete("1.0", tk.END)
    lines = ["当前映射规则（密文字母 -> 明文字母）:"]
    for k in sorted(current_mapping.keys()):
        if k in locked_mapping:
            lines.append(f"   {k} → {current_mapping[k]}  (已锁定)")
        else:
            lines.append(f"   {k} → {current_mapping[k]}")
    table_text.insert(tk.END, "\n".join(lines))

def import_file():
    file_path = filedialog.askopenfilename(title="选择密文文件")
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, content)

def export_result():
    result = output_text.get("1.0", tk.END).lower()
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="保存解密结果")
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(result)
        messagebox.showinfo("保存成功", "解密结果已保存（已全部转为小写）。")

# GUI
root = tk.Tk()
root.title("单表代换密文破译工具（支持锁定映射）")

tk.Label(root, text="请输入密文：").pack()
input_text = tk.Text(root, height=8, width=90)
input_text.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=5)
tk.Button(button_frame, text="自动破译", command=auto_decrypt).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="迭代优化", command=optimize_mapping).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="查看频率图", command=show_frequency_chart).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="词典匹配建议", command=check_dictionary).grid(row=0, column=3, padx=5)

manual_frame = tk.Frame(root)
manual_frame.pack(pady=5)
tk.Label(manual_frame, text="手动替换：").grid(row=0, column=0)
from_entry = tk.Entry(manual_frame, width=3)
from_entry.grid(row=0, column=1)
tk.Label(manual_frame, text="→").grid(row=0, column=2)
to_entry = tk.Entry(manual_frame, width=3)
to_entry.grid(row=0, column=3)
tk.Button(manual_frame, text="执行替换", command=manual_replace).grid(row=0, column=4, padx=10)

tk.Label(root, text="解密结果：").pack()
output_text = tk.Text(root, height=8, width=90)
output_text.pack()

tk.Label(root, text="当前映射表：").pack()
table_text = tk.Text(root, height=10, width=40)
table_text.pack()

file_frame = tk.Frame(root)
file_frame.pack(pady=5)
tk.Button(file_frame, text="导入密文文件", command=import_file).grid(row=0, column=0, padx=5)
tk.Button(file_frame, text="导出解密结果", command=export_result).grid(row=0, column=1, padx=5)

root.mainloop()
