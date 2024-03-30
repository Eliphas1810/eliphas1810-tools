import tkinter
from tkinter import messagebox
from tkinter import filedialog
import os
import re

root = tkinter.Tk()
root.geometry("800x300")
root.title("ビット反転")

in_file_string_var = tkinter.StringVar()
in_file_string_var.set("")

in_file_label = tkinter.Label(root, textvariable=in_file_string_var)
in_file_label.place(x=10, y=40)

# 入力ファイル選択ボタンが押された時の処理
def select_in_file():
    try:
        in_file_string_var.set(filedialog.askopenfilename(initialdir=os.path.expanduser("~"), multiple=False, filetypes=[("zipファイル", ".zip"), ("テキスト ファイル", ".txt"), ("ブラウザのブックマーク", ".json"), ("バイナリー ファイル", ".bin"), ("全ての種類のファイル", "*")]))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

in_file_select_button = tkinter.Button(root, text="入力ファイル選択", command=select_in_file)
in_file_select_button.place(x=10, y=10)

out_dir_string_var = tkinter.StringVar()
out_dir_string_var.set("")

out_dir_label = tkinter.Label(root, textvariable=out_dir_string_var)
out_dir_label.place(x=10, y=110)

# 出力ディレクトリ選択ボタンが押された時の処理
def select_out_dir():
    try:
        out_dir_string_var.set(filedialog.askdirectory(initialdir=os.path.expanduser("~")))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

out_dir_select_button = tkinter.Button(root, text="出力ディレクトリ選択", command=select_out_dir)
out_dir_select_button.place(x=10, y=80)

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=180)

# ビット反転ボタンが押された時の処理
def flip_bit():
    try:

        in_file = in_file_string_var.get()
        out_dir = out_dir_string_var.get()

        if in_file == "":
            message_string_var.set("入力ファイルを選択してください。")
            return

        if out_dir == "":
            message_string_var.set("出力ディレクトリを選択してください。")
            return

        message_string_var.set("ビット反転中です……。")

        in_file_name = os.path.basename(in_file)

        out_file_name = ""
        if re.match("^.+\.[bB][iI][nN]$", in_file_name):
            out_file_name = re.sub("\.[bB][iI][nN]$", "", in_file_name)
        else:
            out_file_name = in_file_name + ".bin"

        with open(os.path.join(out_dir, out_file_name), "wb") as file:
            with open(in_file, "rb") as f:

                while True:
                    bytes = f.read(1024)
                    read_byte_size = len(bytes)
                    if read_byte_size == 0:
                        break

                    # ビットを反転
                    integer = ~ int.from_bytes(bytes, byteorder="little", signed=True)

                    file.write(integer.to_bytes(read_byte_size, byteorder="little", signed=True))

        message_string_var.set("ビット反転が完了しました。" + os.path.join(out_dir, out_file_name))

    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

flip_bit_button = tkinter.Button(root, text="ビットを反転", command=flip_bit)
flip_bit_button.place(x=10, y=150)

root.mainloop()
