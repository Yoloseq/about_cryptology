import tkinter as tk
import subprocess
import os
import sys

def run_feature_1():
    path = os.path.join(os.path.dirname(__file__), "功能一新.py")
    subprocess.Popen([sys.executable, path])

def run_feature_2():
    path = os.path.join(os.path.dirname(__file__), "功能二新.py")
    subprocess.Popen([sys.executable, path])

root = tk.Tk()
root.title("单表代换密码工具总控制台")
root.geometry("300x150")

tk.Label(root, text="请选择要运行的功能：", font=("Arial", 14)).pack(pady=15)

tk.Button(root, text="功能1：加密/解密", font=("Arial", 12), width=20, command=run_feature_1).pack(pady=5)
tk.Button(root, text="功能2：辅助破译", font=("Arial", 12), width=20, command=run_feature_2).pack(pady=5)

root.mainloop()
