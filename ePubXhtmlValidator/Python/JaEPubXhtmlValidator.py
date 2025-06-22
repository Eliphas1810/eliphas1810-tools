from lxml import etree
import tkinter
from tkinter import filedialog
from tkinter import messagebox
import os
import re
import zipfile


root = tkinter.Tk()
root.geometry("800x300")
root.title("電子書籍(ePub)内XHTMLチェッカー")

epub_string_var = tkinter.StringVar()
epub_string_var.set("")

epub_label = tkinter.Label(root, textvariable=epub_string_var)
epub_label.place(x=10, y=40)

# 電子書籍(ePub)ファイル選択ボタンが押された時の処理
def select_epub():
    try:
        epub_string_var.set(filedialog.askopenfilename(title="電子書籍(ePub)ファイル選択", multiple=False, filetypes=[("ePub", ".epub")], initialdir=os.path.expanduser("~")))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

epub_select_button = tkinter.Button(root, text="電子書籍(ePub)ファイル選択", command=select_epub)
epub_select_button.place(x=10, y=10)

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=120)

# 電子書籍(ePub)内XHTMLチェックボタンが押された時の処理
def validate_epub_xhtml():
    xhtml_file_name = ""
    try:
        epub = epub_string_var.get()

        if epub == "":
            message_string_var.set("電子書籍(ePub)ファイルを選択してください。")
            return
        if os.path.exists(epub) == False:
            message_string_var.set("電子書籍(ePub)ファイルを選択し直してください。")
            return

        xsd = ""
        with open(os.path.join(os.getcwd(), "modified-xhtml1-strict.xsd"), "r", encoding="utf-8") as file:
            xsd = file.read().encode("utf-8")

        parser = etree.XMLParser(schema = etree.XMLSchema(etree.XML(xsd)))

        # .epubファイルを展開
        # zip展開
        with zipfile.ZipFile(epub) as zip_file:
            for file_name in zip_file.namelist():
                if re.match("^.+\\.[xX][hH][tT][mM][lL]$", file_name):
                    xhtml_file_name = file_name
                    with zip_file.open(file_name) as file:
                        xhtml_bytes = file.read()
                        xhtml = xhtml_bytes.decode("utf-8")

                        # lxmlにおける名前空間付きの属性への対応方法が分からなかったので、
                        # 名前空間付きの属性を削除
                        xhtml_bytes = re.sub(' +[a-zA-Z]+:[a-zA-Z]+="[^"]+"', "", xhtml).encode("utf-8")

                        root = etree.fromstring(xhtml_bytes, parser)

                        # text = "".join(root.itertext()) # HTMLアンエスケープした文字が返されてしまいます。

                        text = xhtml

                        # XML宣言文を削除
                        text = re.sub("<\\?xml[^>]*>", "", text)
                        #
                        # タグを削除
                        #
                        # 開始タグを削除
                        text = re.sub("<[a-zA-Z][^>]*>", "", text)
                        # 終了タグを削除
                        text = re.sub("</[a-zA-Z][^>]*>", "", text)

                        # print(text)

                        if re.search("'", text):
                            message_string_var.set(xhtml_file_name + ": HTMLエスケープされていません。: '")
                            print(text)
                            return
                        elif re.search('"', text):
                            message_string_var.set(xhtml_file_name + ': HTMLエスケープされていません。: "')
                            print(text)
                            return
                        elif re.search("<", text):
                            message_string_var.set(xhtml_file_name + ": HTMLエスケープされていません。: <")
                            print(text)
                            return
                        elif re.search(">", text):
                            message_string_var.set(xhtml_file_name + ": HTMLエスケープされていません。: >")
                            print(text)
                            return
                        elif re.search("&[^#aqgl]", text):
                            message_string_var.set(xhtml_file_name + ": HTMLエスケープされていません。: &")
                            print(text)
                            return

        message_string_var.set(epub + "内のXHTMLにエラーは無いようです。")

    except Exception as exception:
        message_string_var.set(xhtml_file_name + ": " + str(exception))

validate_epub_xhtml_button = tkinter.Button(root, text="電子書籍(ePub)内XHTMLチェック", command=validate_epub_xhtml)
validate_epub_xhtml_button.place(x=10, y=80)

root.mainloop()
