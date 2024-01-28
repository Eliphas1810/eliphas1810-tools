import tkinter
from tkinter import filedialog
from tkinter import messagebox
import os
import glob
import tempfile
import shutil
import zipfile

root = tkinter.Tk()
root.geometry("800x300")
root.title(".odt再圧縮")

in_dir_string_var = tkinter.StringVar()
in_dir_string_var.set("")

in_dir_label = tkinter.Label(root, textvariable=in_dir_string_var)
in_dir_label.place(x=10, y=40)

# .odt再圧縮ディレクトリ選択ボタンが押された時の処理
def select_in_dir():
    try:
        in_dir_string_var.set(filedialog.askdirectory(initialdir=os.path.expanduser("~")))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

in_dir_select_button = tkinter.Button(root, text=".odt再圧縮ディレクトリ選択", command=select_in_dir)
in_dir_select_button.place(x=10, y=10)

out_dir_string_var = tkinter.StringVar()
out_dir_string_var.set("")

out_dir_label = tkinter.Label(root, textvariable=out_dir_string_var)
out_dir_label.place(x=10, y=100)

# .odt保存ディレクトリ選択ボタンが押された時の処理
def select_out_dir():
    try:
        out_dir_string_var.set(filedialog.askdirectory(initialdir=os.path.expanduser("~")))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

out_dir_select_button = tkinter.Button(root, text=".odt保存ディレクトリ選択", command=select_out_dir)
out_dir_select_button.place(x=10, y=70)

title_label = tkinter.Label(text="文書のタイトル")
title_label.place(x=10, y=130)

title_textbox = tkinter.Entry(width=80)
title_textbox.place(x=100, y=130)

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=190)

# .odt再圧縮ボタンが押された時の処理
def recompress_odt():
    try:
        in_dir = in_dir_string_var.get()
        out_dir = out_dir_string_var.get()
        title = title_textbox.get()

        if in_dir == "":
            message_string_var.set(".odt再圧縮ディレクトリを選択してください。")
            return
        if out_dir == "":
            message_string_var.set(".odt保存ディレクトリを選択してください。")
            return
        if title == "":
            message_string_var.set("文書のタイトルを記入してください。")
            return
        if os.path.exists(in_dir) == False:
            message_string_var.set(".odt再圧縮ディレクトリを選択し直してください。")
            return
        if os.path.exists(out_dir) == False:
            message_string_var.set(".odt保存ディレクトリを選択し直してください。")
            return
        if os.path.exists(os.path.join(out_dir, title + ".odt")) == True:
            message_string_var.set(os.path.join(out_dir, title + ".odt") + "ファイルは既に存在します。文書のタイトルを記入し直してください。")
            return
        if os.path.exists(os.path.join(in_dir, "mimetype")) == False:
            message_string_var.set(os.path.join(in_dir, "mimetype") + "ファイルが無いです。")
            return
        if os.path.exists(os.path.join(in_dir, "META-INF/manifest.xml")) == False:
            message_string_var.set(os.path.join(in_dir, "META-INF/manifest.xml") + "ファイルが無いです。")
            return

        # 一時ディレクトリを作成
        temp_dir = tempfile.TemporaryDirectory()

        # .odt再圧縮ディレクトリのディレクトリとファイルを再帰的にサブ ディレクトリのサブ ディレクトリまで全て検索していきます。
        for current_dir_path, sub_dir_name_list, file_name_list in os.walk(in_dir):
            sub_dir_path = current_dir_path[len(in_dir):]
            # .odt再圧縮ディレクトリのディレクトリ構造を全て一時ディレクトリへコピー
            for sub_dir_name in sub_dir_name_list:
                os.mkdir(os.path.join(temp_dir.name + sub_dir_path, sub_dir_name))
            # .odt再圧縮ディレクトリのファイルを全て一時ディレクトリへコピー
            for file_name in file_name_list:
                shutil.copyfile(os.path.join(current_dir_path, file_name), os.path.join(temp_dir.name + sub_dir_path, file_name))

        # .odtファイルを作成
        # zip圧縮
        with zipfile.ZipFile(os.path.join(out_dir, title + ".odt"), 'w', zipfile.ZIP_STORED) as zip_file:
            # mimetypeファイルをzipファイルに最初に追加
            zip_file.write(os.path.join(temp_dir.name, "mimetype"), "mimetype")
            # 一時ディレクトリの(ディレクトリと)ファイルを再帰的にサブ ディレクトリのサブ ディレクトリまで全て検索していきます。
            for current_dir_path, sub_dir_name_list, file_name_list in os.walk(temp_dir.name):
                for file_name in file_name_list:
                    sub_dir_path = current_dir_path[len(temp_dir.name):]
                    # mimetypeファイル以外をzipファイルに追加
                    if file_name != "mimetype" or sub_dir_path != "":
                        zip_file.write(os.path.join(temp_dir.name + sub_dir_path, file_name), os.path.join(sub_dir_path, file_name))

        # 一時ディレクトリを削除
        temp_dir.cleanup()

        message_string_var.set(".odtの再圧縮が完了しました。")

    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

recompress_odt_button = tkinter.Button(root, text=".odt再圧縮", command=recompress_odt)
recompress_odt_button.place(x=10, y=160)

root.mainloop()
