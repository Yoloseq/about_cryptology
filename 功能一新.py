import tkinter as tk
from tkinter import filedialog, messagebox
import string
import json
import random

# 替换函数
def encrypt(plain_text, key_map):
    return ''.join([key_map.get(c, c) for c in plain_text.lower()])

def decrypt(cipher_text, key_map):
    reverse_map = {v: k for k, v in key_map.items()}
    return ''.join([reverse_map.get(c, c) for c in cipher_text.lower()])

# 构建映射表
def build_mapping(key_string):
    if len(key_string) != 26 or not all(c in string.ascii_lowercase for c in key_string):
        raise ValueError("密钥必须包含26个不同的英文字母")
    if len(set(key_string)) != 26:
        raise ValueError("密钥中不能有重复字母")
    return dict(zip(string.ascii_lowercase, key_string))

# 随机生成密钥
def generate_random_key():
    letters = list(string.ascii_lowercase)
    random.shuffle(letters)
    return ''.join(letters)

# 显示并复制密钥
def show_generated_key():
    generated_key = generate_random_key()
    messagebox.showinfo("生成的密钥", f"随机生成的密钥是：\n{generated_key}")
    
    # 复制密钥按钮
    def copy_key():
        root.clipboard_clear()
        root.clipboard_append(generated_key)
        messagebox.showinfo("复制成功", "密钥已复制到剪贴板")
    
    copy_button = tk.Button(root, text="复制密钥", command=copy_key)
    copy_button.pack(pady=5)

# 加密操作
def do_encrypt():
    try:
        key = key_entry.get().lower()
        key_map = build_mapping(key)
        plain = input_text.get("1.0", tk.END)
        encrypted = encrypt(plain, key_map)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, encrypted)
    except ValueError as e:
        messagebox.showerror("密钥错误", str(e))

# 解密操作
def do_decrypt():
    try:
        key = key_entry.get().lower()
        key_map = build_mapping(key)
        cipher = input_text.get("1.0", tk.END)
        decrypted = decrypt(cipher, key_map)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted)
    except ValueError as e:
        messagebox.showerror("密钥错误", str(e))

# 保存密钥
def save_key():
    key = key_entry.get().lower()
    try:
        key_map = build_mapping(key)
        file_path = filedialog.asksaveasfilename(defaultextension=".json", title="保存密钥")
        if file_path:
            with open(file_path, "w") as f:
                json.dump(key_map, f)
            messagebox.showinfo("保存成功", "密钥已保存")
    except ValueError as e:
        messagebox.showerror("密钥错误", str(e))

# 导入密钥
def load_key():
    file_path = filedialog.askopenfilename(title="导入密钥文件", filetypes=[("JSON 文件", "*.json")])
    if file_path:
        with open(file_path, "r") as f:
            key_map = json.load(f)
            # 反向构建 key string（确保顺序）
            key_list = [key_map.get(c, '?') for c in string.ascii_lowercase]
            if '?' in key_list or len(set(key_list)) != 26:
                messagebox.showerror("密钥错误", "导入的密钥无效")
                return
            key_entry.delete(0, tk.END)
            key_entry.insert(0, ''.join(key_list))
            messagebox.showinfo("导入成功", "密钥已加载")

# GUI构建
root = tk.Tk()
root.title("功能1：单表代换加密 / 解密工具")

# 密钥输入
tk.Label(root, text="密钥（26个小写英文字母）:").pack()
key_entry = tk.Entry(root, width=40)
key_entry.pack(pady=5)

# 随机生成密钥按钮
tk.Button(root, text="随机生成密钥", command=show_generated_key).pack(pady=5)

# 文本输入
tk.Label(root, text="输入内容（明文或密文）：").pack()
input_text = tk.Text(root, height=6, width=80)
input_text.pack()

# 按钮区域
button_frame = tk.Frame(root)
button_frame.pack(pady=5)
tk.Button(button_frame, text="加密", command=do_encrypt).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="解密", command=do_decrypt).grid(row=0, column=1, padx=10)
tk.Button(button_frame, text="保存密钥", command=save_key).grid(row=0, column=2, padx=10)
tk.Button(button_frame, text="导入密钥", command=load_key).grid(row=0, column=3, padx=10)

# 输出结果
tk.Label(root, text="输出结果：").pack()
output_text = tk.Text(root, height=6, width=80)
output_text.pack()

root.mainloop()
