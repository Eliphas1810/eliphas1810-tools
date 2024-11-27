import tkinter
from tkinter import filedialog
from tkinter import messagebox
import os
import re
import tempfile
import zipfile

root = tkinter.Tk()
root.geometry("800x400")
root.title("1つ以上の.txtファイルを.odtファイルに変換")

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

# .odtファイル書き込みディレクトリ選択ボタンが押された時の処理
def select_out_dir():
    try:
        out_dir_string_var.set(filedialog.askdirectory(initialdir=os.path.expanduser("~")))
    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

out_dir_select_button = tkinter.Button(root, text=".odtファイル書き込みディレクトリ選択", command=select_out_dir)
out_dir_select_button.place(x=10, y=80)

title_label = tkinter.Label(text="文書のタイトル")
title_label.place(x=10, y=150)

title_textbox = tkinter.Entry(width=80)
title_textbox.place(x=100, y=150)

serif_label = tkinter.Label(text="セリフ フォント")
serif_label.place(x=10, y=190)

serif_textbox = tkinter.Entry(width=80)
serif_textbox.place(x=130, y=190)
serif_textbox.insert(0, "Noto Serif CJK JP")

sans_serif_label = tkinter.Label(text="サン セリフ フォント")
sans_serif_label.place(x=10, y=230)

sans_serif_textbox = tkinter.Entry(width=80)
sans_serif_textbox.place(x=130, y=230)
sans_serif_textbox.insert(0, "Noto Sans CJK JP")

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=310)

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
        serif = serif_textbox.get()
        sans_serif = sans_serif_textbox.get()

        if in_dir == "":
            message_string_var.set("読み込みディレクトリを選択してください。")
            return
        if out_dir == "":
            message_string_var.set("書き込みディレクトリを選択してください。")
            return
        if title == "":
            message_string_var.set("文書のタイトルを記入してください。")
            return
        if serif == "":
            message_string_var.set("セリフ フォントを記入してください。")
            return
        if sans_serif == "":
            message_string_var.set("サン セリフ フォントを記入してください。")
            return
        if os.path.exists(in_dir) == False:
            message_string_var.set("読み込みディレクトリを選択し直してください。")
            return
        if os.path.exists(out_dir) == False:
            message_string_var.set("書き込みディレクトリを選択し直してください。")
            return
        if os.path.exists(os.path.join(out_dir, title + ".odt")) == True:
            message_string_var.set(os.path.join(out_dir, title + ".odt") + "ファイルが既に存在します。変換を中止しました。")
            return

        file_name_list = os.listdir(in_dir)
        text_file_name_list = []
        for file_name in file_name_list:
            # ファイルの場合
            if os.path.isfile(os.path.join(in_dir, file_name)):
                # .txtファイルの場合
                if re.match("^.+\\.[tT][xX][tT]$", file_name):
                    text_file_name_list.append(file_name)

        text_file_name_list.sort()

        if len(text_file_name_list) == 0:
            message_string_var.set(".txtファイル読み込みディレクトリに.txtファイルが有りません。")
            return

        # 一時ディレクトリを作成
        temp_dir = tempfile.TemporaryDirectory()

        # mimetypeファイルを新規作成
        with open(os.path.join(temp_dir.name, "mimetype"), "w", encoding="utf-8", newline="\n") as file:
            file.write('application/vnd.oasis.opendocument.text')

        # META-INFディレクトリを新規作成
        meta_inf_dir = os.path.join(temp_dir.name, "META-INF")
        os.mkdir(meta_inf_dir)

        # META-INF/manifest.xmlを新規作成
        with open(os.path.join(meta_inf_dir, "manifest.xml"), "w", encoding="utf-8", newline="\n") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<manifest:manifest\n')
            file.write('    xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0"\n')
            file.write('    manifest:version="1.3"\n')
            file.write('    xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0"\n')
            file.write('>\n')
            file.write('    <manifest:file-entry manifest:full-path="/" manifest:version="1.3" manifest:media-type="application/vnd.oasis.opendocument.text" />\n')
            file.write('    <manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml" />\n')
            file.write('    <manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml" />\n')
            file.write('</manifest:manifest>\n')

        # content.xmlファイルを新規作成
        with open(os.path.join(temp_dir.name, "content.xml"), "w", encoding="utf-8", newline="\n") as file:
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
            file.write('        <style:font-face style:name="' + escape_xml(sans_serif) + '" svg:font-family="&apos;' + escape_xml(sans_serif) + '&apos;" style:font-family-generic="swiss" style:font-pitch="variable" />\n')
            file.write('        <style:font-face style:name="' + escape_xml(serif) + '" svg:font-family="&apos;' + escape_xml(serif) + '&apos;" style:font-family-generic="roman" style:font-pitch="variable"/>\n')
            file.write('        <style:font-face style:name="' + escape_xml(serif) + '" svg:font-family="&apos;' + escape_xml(serif) + '&apos;" style:font-family-generic="system" style:font-pitch="variable"/>\n')
            file.write('    </office:font-face-decls>\n')
            file.write('    <office:automatic-styles>\n')
            file.write('        <style:style style:name="P1" style:family="paragraph" style:parent-style-name="Title">\n')
            file.write('            <loext:graphic-properties draw:fill-gradient-name="gradient" draw:fill-hatch-name="hatch" />\n')
            file.write('            <style:paragraph-properties fo:line-height="1.058cm" />\n')
            file.write('            <style:text-properties style:font-name-asian="' + escape_xml(serif) + '" />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="P2" style:family="paragraph" style:parent-style-name="Heading_20_1">\n')
            file.write('            <loext:graphic-properties draw:fill-gradient-name="gradient" draw:fill-hatch-name="hatch" />\n')
            file.write('            <style:paragraph-properties fo:line-height="1.058cm" fo:text-align="center" style:justify-single-word="false" />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="P3" style:family="paragraph" style:parent-style-name="Standard">\n')
            file.write('            <loext:graphic-properties draw:fill-gradient-name="gradient" draw:fill-hatch-name="hatch" />\n')
            file.write('            <style:paragraph-properties fo:line-height="1.058cm" />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="Ru1" style:family="ruby">\n')
            file.write('            <style:ruby-properties style:ruby-align="distribute-space" style:ruby-position="above" loext:ruby-position="above" />\n')
            file.write('            <!-- style:ruby-alignのdistribute-spaceは端に付かないルビの均等割付「121」。 -->\n')
            file.write('            <!-- style:ruby-alignのdistribute-letterは端に付くルビの均等割付「010」。 -->\n')
            file.write('        </style:style>\n')
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
            file.write('            <text:p text:style-name="P1">' + escape_xml(title) + '</text:p>\n')
            # .txtファイルの数だけ、くり返し
            for text_file_name in text_file_name_list:
                file.write('\n')
                file.write('\n')
                file.write('\n')
                file.write('\n')
                file.write('            <text:p text:style-name="P3" /><!-- 空行 -->\n')
                file.write('            <text:p text:style-name="P3" /><!-- 空行 -->\n')
                file.write('            <text:p text:style-name="P3" /><!-- 空行 -->\n')
                file.write('            <text:p text:style-name="P3" /><!-- 空行 -->\n')
                file.write('\n')
                file.write('            <text:h text:style-name="P2" text:outline-level="1">' + escape_xml(re.sub("^[0-9]*[ 　]*|\\.[tT][xX][tT]$", "", text_file_name)) + '</text:h>\n')
                file.write('\n')
                file.write('            <text:p text:style-name="P3" /><!-- 空行 -->\n')
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
                            file.write('            <text:p text:style-name="P3" /><!-- 空行 -->\n')
                        # 読み込んだ行が普通のテキストの場合
                        else:
                            # XMLエスケープ
                            text = escape_xml(text)
                            # 漢字(ひらがなかカタカナ)をルビに置換
                            text = re.sub("([一-鿋々]+)\\(([ぁ-ゖァ-ヺー]+)\\)", '<text:ruby text:style-name="Ru1"><text:ruby-base>\\1</text:ruby-base><text:ruby-text>\\2</text:ruby-text></text:ruby>', text)
                            # ｜るび対象《ルビ》をルビに置換
                            text = re.sub("｜([^《]+)《([^》]+)》", '<text:ruby text:style-name="Ru1"><text:ruby-base>\\1</text:ruby-base><text:ruby-text>\\2</text:ruby-text></text:ruby>', text)
                            # 漢字《ひらがなかカタカナ》をルビに置換
                            text = re.sub("([一-鿋々]+)《([ぁ-ゖァ-ヺー]+)》", '<text:ruby text:style-name="Ru1"><text:ruby-base>\\1</text:ruby-base><text:ruby-text>\\2</text:ruby-text></text:ruby>', text)
                            file.write('            <text:p text:style-name="P3">' + text + '</text:p>\n')

            file.write('        </office:text>\n')
            file.write('    </office:body>\n')
            file.write('</office:document-content>\n')

        # styles.xmlファイルを新規作成
        with open(os.path.join(temp_dir.name, "styles.xml"), "w", encoding="utf-8", newline="\n") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<office:document-styles\n')
            file.write('    xmlns:officeooo="http://openoffice.org/2009/office"\n')
            file.write('    xmlns:css3t="http://www.w3.org/TR/css3-text/"\n')
            file.write('    xmlns:rpt="http://openoffice.org/2005/report"\n')
            file.write('    xmlns:dc="http://purl.org/dc/elements/1.1/"\n')
            file.write('    xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0"\n')
            file.write('    xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" \n')
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
            file.write('    xmlns:grddl="http://www.w3.org/2003/g/data-view#"\n')
            file.write('    xmlns:loext="urn:org:documentfoundation:names:experimental:office:xmlns:loext:1.0"\n')
            file.write('    xmlns:dom="http://www.w3.org/2001/xml-events"\n')
            file.write('    xmlns:field="urn:openoffice:names:experimental:ooo-ms-interop:xmlns:field:1.0"\n')
            file.write('    xmlns:math="http://www.w3.org/1998/Math/MathML"\n')
            file.write('    xmlns:form="urn:oasis:names:tc:opendocument:xmlns:form:1.0"\n')
            file.write('    xmlns:script="urn:oasis:names:tc:opendocument:xmlns:script:1.0"\n')
            file.write('    xmlns:xhtml="http://www.w3.org/1999/xhtml"\n')
            file.write('    office:version="1.3"\n')
            file.write('>\n')
            file.write('    <office:font-face-decls>\n')
            file.write('        <style:font-face style:name="' + escape_xml(serif) + '" svg:font-family="&apos;' + escape_xml(serif) + '&apos;" style:font-family-generic="roman" style:font-pitch="variable" />\n')
            file.write('        <style:font-face style:name="' + escape_xml(sans_serif) + '" svg:font-family="&apos;' + escape_xml(sans_serif) + '&apos;" style:font-family-generic="swiss" style:font-pitch="variable" />\n')
            file.write('        <style:font-face style:name="' + escape_xml(serif) + '" svg:font-family="&apos;' + escape_xml(serif) + '&apos;" style:font-family-generic="system" style:font-pitch="variable" />\n')
            file.write('    </office:font-face-decls>\n')
            file.write('    <office:styles>\n')
            file.write('        <draw:gradient draw:name="gradient" draw:style="linear" draw:start-color="#000000" draw:end-color="#ffffff" draw:start-intensity="100%" draw:end-intensity="100%" draw:angle="0deg" draw:border="0%" />\n')
            file.write('        <draw:hatch draw:name="hatch" draw:style="single" draw:color="#3465a4" draw:distance="0.02cm" draw:rotation="0" />\n')
            file.write('        <style:default-style style:family="graphic">\n')
            file.write('            <style:graphic-properties\n')
            file.write('                svg:stroke-color="#3465a4"\n')
            file.write('                draw:fill-color="#729fcf"\n')
            file.write('                fo:wrap-option="no-wrap"\n')
            file.write('                draw:shadow-offset-x="0.3cm"\n')
            file.write('                draw:shadow-offset-y="0.3cm"\n')
            file.write('                draw:start-line-spacing-horizontal="0.283cm"\n')
            file.write('                draw:start-line-spacing-vertical="0.283cm"\n')
            file.write('                draw:end-line-spacing-horizontal="0.283cm"\n')
            file.write('                draw:end-line-spacing-vertical="0.283cm"\n')
            file.write('                style:flow-with-text="false"\n')
            file.write('            />\n')
            file.write('            <style:paragraph-properties\n')
            file.write('                style:text-autospace="ideograph-alpha"\n')
            file.write('                style:line-break="strict"\n')
            file.write('                style:writing-mode="lr-tb"\n')
            file.write('                style:font-independent-line-spacing="false"\n')
            file.write('            >\n')
            file.write('                <style:tab-stops />\n')
            file.write('            </style:paragraph-properties>\n')
            file.write('            <style:text-properties\n')
            file.write('                style:use-window-font-color="true"\n')
            file.write('                loext:opacity="0%"\n')
            file.write('                style:font-name="' + escape_xml(serif) + '"\n')
            file.write('                fo:font-size="14pt"\n')
            file.write('                fo:language="en"\n')
            file.write('                fo:country="US"\n')
            file.write('                style:letter-kerning="true"\n')
            file.write('                style:font-name-asian="' + escape_xml(serif) + '"\n')
            file.write('                style:font-size-asian="14pt"\n')
            file.write('                style:language-asian="ja"\n')
            file.write('                style:country-asian="JP"\n')
            file.write('                style:font-name-complex="' + escape_xml(serif) + '"\n')
            file.write('                style:font-size-complex="14pt"\n')
            file.write('                style:language-complex="hi"\n')
            file.write('                style:country-complex="IN"\n')
            file.write('            />\n')
            file.write('        </style:default-style>\n')
            file.write('        <style:default-style style:family="paragraph">\n')
            file.write('            <style:paragraph-properties\n')
            file.write('                fo:orphans="2"\n')
            file.write('                fo:widows="2"\n')
            file.write('                fo:hyphenation-ladder-count="no-limit"\n')
            file.write('                style:text-autospace="ideograph-alpha"\n')
            file.write('                style:punctuation-wrap="hanging"\n')
            file.write('                style:line-break="strict"\n')
            file.write('                style:tab-stop-distance="1.251cm"\n')
            file.write('                style:writing-mode="page"\n')
            file.write('            />\n')
            file.write('            <style:text-properties\n')
            file.write('                style:use-window-font-color="true"\n')
            file.write('                loext:opacity="0%"\n')
            file.write('                style:font-name="' + escape_xml(serif) + '"\n')
            file.write('                fo:font-size="14pt"\n')
            file.write('                fo:language="en"\n')
            file.write('                fo:country="US"\n')
            file.write('                style:letter-kerning="true"\n')
            file.write('                style:font-name-asian="' + escape_xml(serif) + '"\n')
            file.write('                style:font-size-asian="14pt"\n')
            file.write('                style:language-asian="ja"\n')
            file.write('                style:country-asian="JP"\n')
            file.write('                style:font-name-complex="' + escape_xml(serif) + '"\n')
            file.write('                style:font-size-complex="14pt"\n')
            file.write('                style:language-complex="hi"\n')
            file.write('                style:country-complex="IN"\n')
            file.write('            />\n')
            file.write('        </style:default-style>\n')
            file.write('        <style:default-style style:family="table">\n')
            file.write('            <style:table-properties table:border-model="collapsing" />\n')
            file.write('        </style:default-style>\n')
            file.write('        <style:default-style style:family="table-row">\n')
            file.write('            <style:table-row-properties fo:keep-together="auto" />\n')
            file.write('        </style:default-style>\n')
            file.write('        <style:style style:name="Standard" style:family="paragraph" style:class="text" />\n')
            file.write('        <style:style style:name="Heading" style:family="paragraph" style:parent-style-name="Standard" style:next-style-name="Text_20_body" style:class="text">\n')
            file.write('            <style:paragraph-properties fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" style:contextual-spacing="false" fo:keep-with-next="always" />\n')
            file.write('            <style:text-properties\n')
            file.write('                style:font-name="' + escape_xml(sans_serif) + '"\n')
            file.write('                fo:font-family="&apos;' + escape_xml(sans_serif) + '&apos;"\n')
            file.write('                style:font-family-generic="swiss"\n')
            file.write('                style:font-pitch="variable"\n')
            file.write('                fo:font-size="14pt"\n')
            file.write('                style:font-name-asian="' + escape_xml(serif) + '"\n')
            file.write('                style:font-family-asian="&apos;' + escape_xml(serif) + '&apos;"\n')
            file.write('                style:font-family-generic-asian="system"\n')
            file.write('                style:font-pitch-asian="variable"\n')
            file.write('                style:font-size-asian="14pt"\n')
            file.write('            />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style\n')
            file.write('            style:name="Text_20_body"\n')
            file.write('            style:display-name="Text body"\n')
            file.write('            style:family="paragraph"\n')
            file.write('            style:parent-style-name="Standard"\n')
            file.write('            style:class="text"\n')
            file.write('        >\n')
            file.write('            <style:paragraph-properties\n')
            file.write('                fo:margin-top="0cm"\n')
            file.write('                fo:margin-bottom="0.247cm"\n')
            file.write('                style:contextual-spacing="false"\n')
            file.write('                fo:line-height="115%"\n')
            file.write('            />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="List" style:family="paragraph" style:parent-style-name="Text_20_body" style:class="list">\n')
            file.write('            <style:text-properties style:font-size-asian="14pt" style:font-name-complex="' + escape_xml(sans_serif) + '" style:font-family-complex="' + escape_xml(sans_serif) + '" style:font-family-generic-complex="swiss" />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="Caption" style:family="paragraph" style:parent-style-name="Standard" style:class="extra">\n')
            file.write('            <style:paragraph-properties fo:margin-top="0.212cm" fo:margin-bottom="0.212cm" style:contextual-spacing="false" text:number-lines="false" text:line-number="0" />\n')
            file.write('            <style:text-properties fo:font-size="14pt" fo:font-style="italic" style:font-size-asian="14pt" style:font-style-asian="italic" style:font-name-complex="' + escape_xml(sans_serif) + '" style:font-family-complex="' + escape_xml(sans_serif) + '" style:font-family-generic-complex="swiss" style:font-size-complex="14pt" style:font-style-complex="italic" />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="Index" style:family="paragraph" style:parent-style-name="Standard" style:class="index">\n')
            file.write('            <style:paragraph-properties text:number-lines="false" text:line-number="0" />\n')
            file.write('            <style:text-properties style:font-size-asian="14pt" style:font-name-complex="' + escape_xml(sans_serif) + '" style:font-family-complex="' + escape_xml(sans_serif) + '" style:font-family-generic-complex="swiss" />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="Title" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:class="chapter">\n')
            file.write('            <style:paragraph-properties fo:text-align="center" style:justify-single-word="false" />\n')
            file.write('            <style:text-properties fo:font-size="28pt" fo:font-weight="bold" style:font-size-asian="28pt" style:font-weight-asian="bold" style:font-size-complex="28pt" style:font-weight-complex="bold" />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="Heading_20_1" style:display-name="Heading 1" style:family="paragraph" style:parent-style-name="Heading" style:next-style-name="Text_20_body" style:default-outline-level="1" style:class="text">\n')
            file.write('            <style:paragraph-properties fo:margin-top="0.423cm" fo:margin-bottom="0.212cm" style:contextual-spacing="false" />\n')
            file.write('            <style:text-properties fo:font-size="18pt" fo:font-weight="bold" style:font-size-asian="18pt" style:font-weight-asian="bold" style:font-size-complex="18pt" style:font-weight-complex="bold" />\n')
            file.write('        </style:style>\n')
            file.write('        <style:style style:name="Rubies" style:family="text">\n')
            file.write('            <style:text-properties fo:font-size="6pt" style:text-underline-style="none" style:font-size-asian="6pt" style:font-size-complex="6pt" style:text-emphasize="none" />\n')
            file.write('        </style:style>\n')
            file.write('        <text:outline-style style:name="Outline">\n')
            file.write('            <text:outline-level-style text:level="1" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="2" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="3" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="4" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="5" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="6" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="7" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="8" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="9" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('            <text:outline-level-style text:level="10" style:num-format="">\n')
            file.write('                <style:list-level-properties text:list-level-position-and-space-mode="label-alignment">\n')
            file.write('                    <style:list-level-label-alignment text:label-followed-by="listtab" />\n')
            file.write('                </style:list-level-properties>\n')
            file.write('            </text:outline-level-style>\n')
            file.write('        </text:outline-style>\n')
            file.write('        <text:notes-configuration text:note-class="footnote" style:num-format="1" text:start-value="0" text:footnotes-position="page" text:start-numbering-at="document" />\n')
            file.write('        <text:notes-configuration text:note-class="endnote" style:num-format="i" text:start-value="0" />\n')
            file.write('        <text:linenumbering-configuration text:number-lines="false" text:offset="0.499cm" style:num-format="1" text:number-position="left" text:increment="5" />\n')
            file.write('    </office:styles>\n')
            file.write('    <office:automatic-styles>\n')
            file.write('        <style:page-layout style:name="Mpm1">\n')
            file.write('            <style:page-layout-properties fo:page-width="21.001cm" fo:page-height="29.7cm" style:num-format="1" style:print-orientation="portrait" fo:margin-top="2cm" fo:margin-bottom="2cm" fo:margin-left="2cm" fo:margin-right="2cm" style:writing-mode="lr-tb" style:footnote-max-height="0cm" loext:margin-gutter="0cm">\n')
            file.write('                <style:footnote-sep style:width="0.018cm" style:distance-before-sep="0.101cm" style:distance-after-sep="0.101cm" style:line-style="solid" style:adjustment="left" style:rel-width="25%" style:color="#000000" />\n')
            file.write('            </style:page-layout-properties>\n')
            file.write('            <style:header-style />\n')
            file.write('            <style:footer-style />\n')
            file.write('        </style:page-layout>\n')
            file.write('    </office:automatic-styles>\n')
            file.write('    <office:master-styles>\n')
            file.write('        <style:master-page style:name="Standard" style:page-layout-name="Mpm1" />\n')
            file.write('    </office:master-styles>\n')
            file.write('</office:document-styles>\n')

        # .odtファイルを作成
        # zip圧縮
        with zipfile.ZipFile(os.path.join(out_dir, title + ".odt"), 'w', zipfile.ZIP_STORED) as zip_file:
            zip_file.write(os.path.join(temp_dir.name, "mimetype"), "mimetype")
            zip_file.write(os.path.join(meta_inf_dir, "manifest.xml"), "META-INF/manifest.xml")
            zip_file.write(os.path.join(temp_dir.name, "content.xml"), "content.xml")
            zip_file.write(os.path.join(temp_dir.name, "styles.xml"), "styles.xml")

        # 一時ディレクトリを削除
        temp_dir.cleanup()

        message_string_var.set("1つ以上の.txtファイルから.odtファイルへの変換が完了しました。")

    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise

convert_button = tkinter.Button(root, text="変換", command=convert)
convert_button.place(x=10, y=270)

root.mainloop()
