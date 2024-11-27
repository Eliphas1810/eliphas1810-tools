import tkinter
from tkinter import filedialog
from tkinter import messagebox
import os
import re

root = tkinter.Tk()
root.geometry("800x300")
root.title(".ttcファイルを1つ以上の.ttfファイルに変換")

ttc_string_var = tkinter.StringVar()
ttc_string_var.set("")

ttc_label = tkinter.Label(root, textvariable=ttc_string_var)
ttc_label.place(x=10, y=40)

# .ttcファイル選択ボタンが押された時の処理
def select_ttc():
    try:
        ttc_string_var.set(filedialog.askopenfilename(initialdir=os.path.expanduser("~"), multiple=False, filetypes=[(".ttcファイル", ".ttc")]))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

ttc_select_button = tkinter.Button(root, text=".ttcファイル選択", command=select_ttc)
ttc_select_button.place(x=10, y=10)

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

# .ttcファイルから.ttfファイルへ変換ボタンが押された時の処理
def ttc_to_ttf():
    try:

        ttc = ttc_string_var.get()
        out_dir = out_dir_string_var.get()

        if ttc == "":
            message_string_var.set(".ttcファイルを選択してください。")
            return

        if out_dir == "":
            message_string_var.set("出力ディレクトリを選択してください。")
            return

        with open(ttc, "rb") as file:

            # .ttcファイルはビッグ エンディアン(ネス)
            # TTC Headerを読み込んでいく

            # 4バイトのASCII文字列のTTC Tagを読み込みUTF-8へ変換
            # "ttcf"
            ttc_tag = file.read(4).decode()

            # 4バイトのVersionを読み込み16進数表記のUTF-8文字列へ変換
            # "00010000"か"00020000"
            # "00010000"はTTC Header Version 1.0を意味
            # "00020000"はTTC Header Version 2.0を意味
            version = file.read(4).hex()

            # 4バイトのnumFontsを読み込み整数へ変換
            num_fonts = int.from_bytes(file.read(4), byteorder="big", signed=False)

            offset_list = []
            # numFontsの数だけ、くり返し
            for index in range(0, num_fonts):
                # 4バイトの各フォントのデータの開始バイトを読み込みへ整数へ変換
                # 0バイト目から開始バイトまでのバイト数
                offset_list.append(int.from_bytes(file.read(4), byteorder="big", signed=False))

            # TTC Header Version 2.0の場合は、numFontsの後にデジタル署名のTTC Headerが有るが、無視

            max_index = num_fonts - 1
            font_name = re.sub("\\.[tT][tT][cC]$", "", os.path.basename(ttc))
            # numFontsの数だけ、くり返し
            for index in range(0, num_fonts):
                file.seek(offset_list[index], os.SEEK_SET)
                with open(os.path.join(out_dir, font_name + str(index + 1) + ".ttf"), "wb") as f:
                    if index == max_index:
                        f.write(file.read())
                    else:
                        f.write(file.read(offset_list[index + 1] - offset_list[index]))

        message_string_var.set(".ttcファイルから.ttfファイルへの変換が完了しました。")

    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

ttc_to_ttf_button = tkinter.Button(root, text=".ttcファイルから.ttfファイルへ変換", command=ttc_to_ttf)
ttc_to_ttf_button.place(x=10, y=150)

root.mainloop()
