import tkinter
from tkinter import filedialog
from tkinter import messagebox
import os
import re

root = tkinter.Tk()
root.geometry("800x300")
root.title("1つ以上の.txtファイルを.odtファイル内のcontent.xmlファイルに変換")

in_dir_string_var = tkinter.StringVar()
in_dir_string_var.set("")

in_dir_label = tkinter.Label(root, textvariable=in_dir_string_var)
in_dir_label.place(x=10, y=40)

# .txtファイル読み込みディレクトリ選択ボタンが押された時の処理
def select_in_dir():
    try:
        in_dir_string_var.set(filedialog.askdirectory(initialdir=os.path.expanduser("~")))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

in_dir_select_button = tkinter.Button(root, text=".txtファイル読み込みディレクトリ選択", command=select_in_dir)
in_dir_select_button.place(x=10, y=10)

out_dir_string_var = tkinter.StringVar()
out_dir_string_var.set("")

out_dir_label = tkinter.Label(root, textvariable=out_dir_string_var)
out_dir_label.place(x=10, y=110)

# content.xmlファイル書き込みディレクトリ選択ボタンが押された時の処理
def select_out_dir():
    try:
        out_dir_string_var.set(filedialog.askdirectory(initialdir=os.path.expanduser("~")))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

out_dir_select_button = tkinter.Button(root, text="content.xmlファイル書き込みディレクトリ選択", command=select_out_dir)
out_dir_select_button.place(x=10, y=80)

title_label = tkinter.Label(text="文書のタイトル")
title_label.place(x=10, y=150)

title_textbox = tkinter.Entry(width=80)
title_textbox.place(x=100, y=150)

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=220)

# XMLエスケープ
# XMLエスケープは'を&apos;に置換
def escape_xml(text):
    text = re.sub("&", "&amp;", text)
    text = re.sub('"', "&quot;", text)
    text = re.sub("'", "&apos;", text)
    text = re.sub("<", "&lt;", text)
    text = re.sub(">", "&gt;", text)
    return text

# 変換ボタンが押された時の処理
def convert():
    try:
        in_dir = in_dir_string_var.get()
        out_dir = out_dir_string_var.get()
        title = title_textbox.get()

        if in_dir == "":
            message_string_var.set(".txtファイル読み込みディレクトリを選択してください。")
            return
        if out_dir == "":
            message_string_var.set("content.xmlファイル書き込みディレクトリを選択してください。")
            return
        if title == "":
            message_string_var.set("文書のタイトルを記入してください。")
            return
        if os.path.exists(in_dir) == False:
            message_string_var.set(".txtファイル読み込みディレクトリを選択し直してください。")
            return
        if os.path.exists(out_dir) == False:
            message_string_var.set("content.xmlファイル書き込みディレクトリを選択し直してください。")
            return
        if os.path.exists(os.path.join(out_dir, "content.xml")) == True:
            message_string_var.set(os.path.join(out_dir, "content.xml") + "ファイルが既に存在します。変換を中止しました。")
            return

        file_name_list = os.listdir(in_dir)
        text_file_name_list = []
        for file_name in file_name_list:
            # ファイルの場合
            if os.path.isfile(os.path.join(in_dir, file_name)):
                # .txtファイルの場合
                if re.match("^.+\.[tT][xX][tT]$", file_name):
                    text_file_name_list.append(file_name)

        text_file_name_list.sort()

        if len(text_file_name_list) == 0:
            message_string_var.set(".txtファイル読み込みディレクトリに.txtファイルが有りません。")
            return

        # content.xmlファイルを作成
        with open(os.path.join(out_dir, "content.xml"), "w", encoding="utf-8", newline="\n") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<office:document-content\n')
            file.write('    xmlns:officeooo="http://openoffice.org/2009/office"\n')
            file.write('    xmlns:css3t="http://www.w3.org/TR/css3-text/"\n')
            file.write('    xmlns:grddl="http://www.w3.org/2003/g/data-view#"\n')
            file.write('    xmlns:xhtml="http://www.w3.org/1999/xhtml"\n')
            file.write('    xmlns:formx="urn:openoffice:names:experimental:ooxml-odf-interop:xmlns:form:1.0"\n')
            file.write('    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
            file.write('    xmlns:rpt="http://openoffice.org/2005/report"\n')
            file.write('    xmlns:dc="http://purl.org/dc/elements/1.1/"\n')
            file.write('    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"\n')
            file.write('    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"\n')
            file.write('    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"\n')
            file.write('    xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"\n')
            file.write('    xmlns:oooc="http://openoffice.org/2004/calc"\n')
            file.write('    xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0"\n')
            file.write('    xmlns:ooow="http://openoffice.org/2004/writer"\n')
            file.write('    xmlns:meta="urn:oasis:names:tc:opendocument:xmlns:meta:1.0"\n')
            file.write('    xmlns:xlink="http://www.w3.org/1999/xlink"\n')
            file.write('    xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0"\n')
            file.write('    xmlns:ooo="http://openoffice.org/2004/office"\n')
            file.write('    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"\n')
            file.write('    xmlns:dr3d="urn:oasis:names:tc:opendocument:xmlns:dr3d:1.0"\n')
            file.write('    xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0"\n')
            file.write('    xmlns:number="urn:oasis:names:tc:opendocument:xmlns:datastyle:1.0"\n')
            file.write('    xmlns:of="urn:oasis:names:tc:opendocument:xmlns:of:1.2"\n')
            file.write('    xmlns:calcext="urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0"\n')
            file.write('    xmlns:tableooo="http://openoffice.org/2009/table"\n')
            file.write('    xmlns:drawooo="http://openoffice.org/2010/draw"\n')
            file.write('    xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0"\n')
            file.write('    xmlns:dom="http://www.w3.org/2001/xml-events"\n')
            file.write('    xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0"\n')
            file.write('    xmlns:xsd="http://www.w3.org/2001/XMLSchema"\n')
            file.write('    xmlns:math="http://www.w3.org/1998/Math/MathML"\n')
            file.write('    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"\n')
            file.write('    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"\n')
            file.write('    xmlns:xforms="http://www.w3.org/2002/xforms"\n')
            file.write('    office:version="1.3"\n')
            file.write('>\n')
            file.write('    <office:scripts/>\n')
            file.write('    <office:font-face-decls>\n')
            file.write('        <style:font-face style:name="Noto Sans CJK JP" svg:font-family="&apos;Noto Sans CJK JP&apos;" style:font-family-generic="system" style:font-pitch="variable" />\n')
            file.write('        <style:font-face style:name="Noto Serif CJK JP" svg:font-family="&apos;Noto Serif CJK JP&apos;" style:font-family-generic="roman" style:font-pitch="variable" />\n')
            file.write('        <style:font-face style:name="Noto Serif CJK JP1" svg:font-family="&apos;Noto Serif CJK JP&apos;" style:font-family-generic="system" style:font-pitch="variable" />\n')
            file.write('        <style:font-face style:name="TakaoPGothic" svg:font-family="TakaoPGothic" style:font-family-generic="swiss" />\n')
            file.write('        <style:font-face style:name="TakaoPGothic1" svg:font-family="TakaoPGothic" style:font-family-generic="system" style:font-pitch="variable" />\n')
            file.write('    </office:font-face-decls>\n')
            file.write('    <office:automatic-styles>\n')
            file.write('\n')
            file.write('        <style:style style:name="P3" style:family="paragraph" style:parent-style-name="Title">\n')
            file.write('            <style:text-properties style:font-name="Noto Sans CJK JP Regular" fo:font-size="28pt" style:font-name-asian="Noto Sans CJK JP Regular" style:font-size-asian="28pt" style:font-size-complex="28pt" />\n')
            file.write('        </style:style>\n')
            file.write('\n')
            file.write('        <style:style style:name="P2" style:family="paragraph" style:parent-style-name="Heading_20_1">\n')
            file.write('            <style:paragraph-properties fo:text-align="center" style:justify-single-word="false" />\n')
            file.write('            <style:text-properties style:font-name="Noto Sans CJK JP Regular" fo:font-size="14pt" style:font-name-asian="Noto Sans CJK JP Regular" style:font-size-asian="14pt" style:font-size-complex="14pt" />\n')
            file.write('        </style:style>\n')
            file.write('\n')
            file.write('        <style:style style:name="P1" style:family="paragraph" style:parent-style-name="Standard">\n')
            file.write('            <style:text-properties fo:font-size="14pt" style:font-name-asian="Noto Serif CJK JP" style:font-size-asian="14pt" style:font-size-complex="14pt"/>\n')
            file.write('        </style:style>\n')
            file.write('\n')
            file.write('        <style:style style:name="Ru1" style:family="ruby">\n')
            file.write('            <style:ruby-properties style:ruby-align="distribute-space" style:ruby-position="above" loext:ruby-position="above" />\n')
            file.write('            <!-- style:ruby-alignのdistribute-spaceは端に付かないルビの均等割付「010」。 -->\n')
            file.write('            <!-- style:ruby-alignのdistribute-letterは端に付くルビの均等割付「121」。 -->\n')
            file.write('        </style:style>\n')
            file.write('\n')
            file.write('    </office:automatic-styles>\n')
            file.write('    <office:body>\n')
            file.write('        <office:text>\n')
            file.write('            <text:sequence-decls>\n')
            file.write('                <text:sequence-decl text:display-outline-level="0" text:name="Illustration" />\n')
            file.write('                <text:sequence-decl text:display-outline-level="0" text:name="Table" />\n')
            file.write('                <text:sequence-decl text:display-outline-level="0" text:name="Text" />\n')
            file.write('                <text:sequence-decl text:display-outline-level="0" text:name="Drawing" />\n')
            file.write('                <text:sequence-decl text:display-outline-level="0" text:name="Figure" />\n')
            file.write('            </text:sequence-decls>\n')
            file.write('\n')
            file.write('            <text:p text:style-name="P3">' + escape_xml(title) + '</text:p>\n')
            # .txtファイルの数だけ、くり返し
            for text_file_name in text_file_name_list:
                file.write('\n')
                file.write('\n')
                file.write('\n')
                file.write('\n')
                file.write('            <text:p text:style-name="P1"/><!-- 空行 -->\n')
                file.write('            <text:p text:style-name="P1"/><!-- 空行 -->\n')
                file.write('            <text:p text:style-name="P1"/><!-- 空行 -->\n')
                file.write('            <text:p text:style-name="P1"/><!-- 空行 -->\n')
                file.write('\n')
                file.write('            <text:h text:style-name="P2" text:outline-level="1">' + escape_xml(re.sub("^[0-9]*[ 　]*|\.[tT][xX][tT]$", "", text_file_name)) + '</text:h>\n')
                file.write('\n')
                file.write('            <text:p text:style-name="P1"/><!-- 空行 -->\n')
                file.write('\n')
                with open(os.path.join(in_dir, text_file_name), "r", encoding="utf-8") as f:
                    while True:
                        text = f.readline()
                        if text == '':
                            break
                        # 文末の改行コードを削除
                        text = re.sub("\n$", "", text)
                        # 読み込んだ行が空行の場合
                        if text == "":
                            file.write('            <text:p text:style-name="P1"/><!-- 空行 -->\n')
                        # 読み込んだ行が普通のテキストの場合
                        else:
                            # XMLエスケープ
                            text = escape_xml(text)
                            # 漢字(ひらがなかカタカナ)をルビに置換
                            text = re.sub("([一-鿋々]+)\(([ぁ-ゖァ-ヺー]+)\)", '<text:ruby text:style-name="Ru1"><text:ruby-base>\\1</text:ruby-base><text:ruby-text>\\2</text:ruby-text></text:ruby>', text)
                            # ｜るび対象《ルビ》をルビに置換
                            text = re.sub("｜([^《]+)《([^》]+)》", '<text:ruby text:style-name="Ru1"><text:ruby-base>\\1</text:ruby-base><text:ruby-text>\\2</text:ruby-text></text:ruby>', text)
                            # 漢字《ひらがなかカタカナ》をルビに置換
                            text = re.sub("([一-鿋々]+)《([ぁ-ゖァ-ヺー]+)》", '<text:ruby text:style-name="Ru1"><text:ruby-base>\\1</text:ruby-base><text:ruby-text>\\2</text:ruby-text></text:ruby>', text)
                            file.write('            <text:p text:style-name="P1">' + text + '</text:p>\n')

            file.write('        </office:text>\n')
            file.write('    </office:body>\n')
            file.write('</office:document-content>\n')

        message_string_var.set("content.xmlファイルへの変換が完了しました。")

    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

make_epub_button = tkinter.Button(root, text="変換", command=convert)
make_epub_button.place(x=10, y=190)

root.mainloop()
