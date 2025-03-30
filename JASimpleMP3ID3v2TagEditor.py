import tkinter
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import os
import re

root = tkinter.Tk()
root.geometry("800x650")
root.title("MP3のID3v2タグ編集")


def get_encoding_name(minor_version, encoding_byte):
    if encoding_byte == 0:
        # return "laten_1"
        return "cp932" # 過去の日本語のアプリケーションにはISO-8859-1でShift-JISのテキストを書き込んでいた物が有ったそうです。
    elif encoding_byte == 1:
        return "utf_16"
    elif minor_version == 4 and encoding_byte == 2:
        return "utf_16_be"
    elif minor_version == 4 and encoding_byte == 3:
        return "utf_8"
    else:
        return None


mp3_file_path = ""
image_mimetype = ""
image_bytes = "".encode()
mpeg_frame_bytes = "".encode()


photo_image = None


# MP3ファイル選択ボタンが押された時の処理
def select_mp3_file():
    try:
        global mp3_file_path
        global image_mimetype
        global image_bytes
        global mpeg_frame_bytes

        global photo_image

        mp3_file_path = filedialog.askopenfilename(title="MP3ファイル選択", multiple=False, filetypes=[("MP3", ".mp3")], initialdir=os.path.expanduser("~"))

        if not mp3_file_path:
            return

        bytes = "".encode()
        with open(mp3_file_path, mode="rb") as file:
            bytes = file.read()

        message_string_var.set("")

        new_mp3_file_name_textbox.delete(0, tkinter.END)
        mp3_file_name = os.path.basename(mp3_file_path)
        new_mp3_file_name_textbox.insert(tkinter.END, "新" + mp3_file_name)

        title_textbox.delete(0, tkinter.END)
        artist_textbox.delete(0, tkinter.END)
        album_textbox.delete(0, tkinter.END)
        track_textbox.delete(0, tkinter.END)

        id3 = bytes[0:3].decode()
        if id3 != "ID3":
            # ID3v2タグが無い場合
            mpeg_frame_bytes = bytes
            return

        minor_version = bytes[3]
        if minor_version <= 2 or 5 <= minor_version:
            message_string_var.set("当アプリケーションはID3v2.3とID3v2.4以外には未対応です。他のアプリケーションを利用してください。")
            return

        flag = bytes[5]
        has_ex_header = (flag & 0x02) != 0

        header_size = 0
        header_size += ((bytes[6] & 0xFF) << 21)
        header_size += ((bytes[7] & 0xFF) << 14)
        header_size += ((bytes[8] & 0xFF) << 7)
        header_size += (bytes[9] & 0xFF)

        byte_index = 10

        if has_ex_header:
            ex_header_size = 0
            if minor_version == 3:
                ex_header_size += (bytes[10] << 24)
                ex_header_size += (bytes[11] << 16)
                ex_header_size += (bytes[12] << 8)
                ex_header_size += bytes[13]
            else:
                ex_header_size += (bytes[10] << 21)
                ex_header_size += (bytes[11] << 14)
                ex_header_size += (bytes[12] << 7)
                ex_header_size += bytes[13]
            byte_index += ex_header_size

        while byte_index < header_size:

            frame_id = bytes[byte_index:byte_index + 4].decode("utf_8", "ignore")

            byte_index += 4

            if byte_index == 14 and not re.match("^[A-Z][A-Z][A-Z][A-Z0-9]$", frame_id):
                byte_index -= 4
                ex_header_size = 0
                if minor_version == 3:
                    ex_header_size += (bytes[10] << 24)
                    ex_header_size += (bytes[11] << 16)
                    ex_header_size += (bytes[12] << 8)
                    ex_header_size += bytes[13]
                else:
                    ex_header_size += (bytes[10] << 21)
                    ex_header_size += (bytes[11] << 14)
                    ex_header_size += (bytes[12] << 7)
                    ex_header_size += bytes[13]
                byte_index += ex_header_size
                continue

            frame_size = 0
            if minor_version == 3:
                frame_size += (bytes[byte_index] << 24)
                frame_size += (bytes[byte_index + 1] << 16)
                frame_size += (bytes[byte_index + 2] << 8)
                frame_size += bytes[byte_index + 3]
            else:
                frame_size += (bytes[byte_index] << 21)
                frame_size += (bytes[byte_index + 1] << 14)
                frame_size += (bytes[byte_index + 2] << 7)
                frame_size += bytes[byte_index + 3]
            byte_index += 4

            byte_index += 2 # フレームのフラグは無視して飛ばします。

            if re.match("^TIT2$|^TPE1$|^TALB$|^TRCK$", frame_id):

                encoding_byte = bytes[byte_index]
                encoding_name = get_encoding_name(minor_version, encoding_byte)
                byte_index += 1

                content = bytes[byte_index:byte_index + frame_size - 1].decode(encoding_name, "strict")
                byte_index += (frame_size - 1)

                if frame_id == "TIT2":
                    title_textbox.insert(tkinter.END, content)
                elif frame_id == "TPE1":
                    artist_textbox.insert(tkinter.END, content)
                elif frame_id == "TALB":
                    album_textbox.insert(tkinter.END, content)
                elif frame_id == "TRCK":
                    track_textbox.insert(tkinter.END, content)

            elif frame_id == "APIC":

                encoding_byte = bytes[byte_index]
                encoding_name = get_encoding_name(minor_version, encoding_byte)
                byte_index += 1

                mimetype_byte_array = "".encode()
                for index in range(frame_size - 1):
                    if bytes[byte_index + index] == 0x00: # NULL
                        mimetype_byte_array = bytes[byte_index:byte_index + index]
                        break
                image_mimetype = mimetype_byte_array.decode(encoding_name, "strict")
                byte_index += (len(mimetype_byte_array) + 1)

                byte_index += 1 # Picture Type(画像の種類)を無視して飛ばします。

                description_byte_array = "".encode()
                for index in range(frame_size - 1 - len(mimetype_byte_array) - 1 - 1):
                    if bytes[byte_index + index] == 0x00: # NULL
                        description_byte_array = bytes[byte_index:byte_index + index]
                        break
                byte_index += (len(description_byte_array) + 1)

                image_bytes = bytes[byte_index:byte_index + frame_size - 1 - len(mimetype_byte_array) - 1 - 1 - len(description_byte_array) - 1]
                byte_index += len(image_bytes)

                if 1 <= len(image_bytes):
                    photo_image = ImageTk.PhotoImage(data=image_bytes)
                    image_canvas.create_image(0, 0, anchor="nw", image=photo_image)

            else:
                byte_index += frame_size

        if header_size < byte_index:
            byte_index = header_size

        mpeg_frame_bytes = bytes[byte_index:len(bytes)]

    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise


select_mp3_file_button = tkinter.Button(root, text="MP3ファイル選択", command=select_mp3_file)
select_mp3_file_button.place(x=10, y=10)

new_mp3_file_name_label = tkinter.Label(text="新MP3ファイル名")
new_mp3_file_name_label.place(x=10, y=50)

new_mp3_file_name_textbox = tkinter.Entry(width=80)
new_mp3_file_name_textbox.place(x=120, y=50)

title_label = tkinter.Label(text="曲名")
title_label.place(x=10, y=80)

title_textbox = tkinter.Entry(width=80)
title_textbox.place(x=120, y=80)

artist_label = tkinter.Label(text="アーティスト")
artist_label.place(x=10, y=110)

artist_textbox = tkinter.Entry(width=80)
artist_textbox.place(x=120, y=110)

album_label = tkinter.Label(text="アルバム")
album_label.place(x=10, y=140)

album_textbox = tkinter.Entry(width=80)
album_textbox.place(x=120, y=140)

track_label = tkinter.Label(text="トラック番号")
track_label.place(x=10, y=170)

track_textbox = tkinter.Entry(width=80)
track_textbox.place(x=120, y=170)


image_canvas = tkinter.Canvas(root, width = 780, height = 300)
image_canvas.place(x=10, y=200)

image_canvas.config(scrollregion=(0, 0, 1000, 1000))

horizontal_scrollbar = tkinter.Scrollbar(root, orient=tkinter.HORIZONTAL)
vertical_scrollbar = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)

horizontal_scrollbar.place(x=10, y=500, width=780)
vertical_scrollbar.place(x=780, y=200, height=300)

horizontal_scrollbar.config(command=image_canvas.xview)
vertical_scrollbar.config(command=image_canvas.yview)

image_canvas.config(xscrollcommand=horizontal_scrollbar.set)
image_canvas.config(yscrollcommand=vertical_scrollbar.set)


# ジャケット画像ファイル選択ボタンが押された時の処理
def select_image_file():
    try:
        global image_mimetype
        global image_bytes

        global photo_image

        image_file_path = filedialog.askopenfilename(title="ジャケット画像ファイル選択", multiple=False, filetypes=[("All", "*")], initialdir=os.path.expanduser("~"))

        if not image_file_path:
            return

        if re.match("^.+\\.[jJ][pP][eE]?[gG]$", image_file_path):
            image_mimetype = "image/jpeg"
        elif re.match("^.+\\.[pP][nN][gG]$", image_file_path):
            image_mimetype = "image/png"
        else:
            message_string_var.set("JPEG形式かPNG形式の画像ファイルを選択してください。")
            return

        with open(image_file_path, mode="rb") as file:
            image_bytes = file.read()

        photo_image = ImageTk.PhotoImage(data=image_bytes)
        image_canvas.create_image(0, 0, anchor="nw", image=photo_image)

    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise


select_image_file_button = tkinter.Button(root, text="ジャケット画像ファイル選択", command=select_image_file)
select_image_file_button.place(x=10, y=520)

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=590)

# 新MP3ファイル作成ボタンが押された時の処理
def make_mp3_file():
    try:
        global mp3_file_path
        global image_mimetype
        global image_bytes
        global mpeg_frame_bytes

        if len(mpeg_frame_bytes) <= 0:
            message_string_var.set("MP3ファイルを選択してください。")
            return

        new_mp3_file_name = new_mp3_file_name_textbox.get()
        title = title_textbox.get()
        artist = artist_textbox.get()
        album = album_textbox.get()
        track = track_textbox.get()

        if new_mp3_file_name == "":
            message_string_var.set("新MP3ファイル名を記入してください。")
            return
        if title == "":
            message_string_var.set("曲名を記入してください。")
            return
        if artist == "":
            message_string_var.set("アーティストを記入してください。")
            return
        if track == "":
            message_string_var.set("例えば1などをトラック番号に記入してください。")
            return

        title_bytes = title.encode("utf_16")
        artist_bytes = artist.encode("utf_16")
        track_bytes = track.encode("utf_16")

        album_bytes = "".encode("utf_16")
        if album != "":
            album_bytes = album.encode("utf_16");

        image_mimetype_bytes = image_mimetype.encode("utf_8") #UTF-8はISO-8859-1を包含

        header_size = 0
        header_size += 10
        header_size += (10 + 1 + len(title_bytes))
        header_size += (10 + 1 + len(artist_bytes))
        header_size += (10 + 1 + len(track_bytes))
        if album != "":
            header_size += (10 + 1 + len(album_bytes))
        if 1 <= len(image_bytes):
            header_size += (10 + 1 + len(image_mimetype_bytes) + 1 + 1 + 1 + len(image_bytes))

        mp3_dir = os.path.dirname(mp3_file_path)

        with open(os.path.join(mp3_dir, new_mp3_file_name), "wb") as file:
            file.write(0x49.to_bytes(1, "big")) # I
            file.write(0x44.to_bytes(1, "big")) # D
            file.write(0x33.to_bytes(1, "big")) # 3
            file.write(0x03.to_bytes(1, "big")) # マイナーバージョン3
            file.write(0x00.to_bytes(1, "big")) # バッチバージョン0
            file.write(0x00.to_bytes(1, "big")) # ヘッダーのフラグ
            file.write(((((header_size << 4) & 0xFFFFFFFF) >> 25) & 0xFF).to_bytes(1, "big"))
            file.write(((((header_size << 11) & 0xFFFFFFFF) >> 25) & 0xFF).to_bytes(1, "big"))
            file.write(((((header_size << 18) & 0xFFFFFFFF) >> 25) & 0xFF).to_bytes(1, "big"))
            file.write(((((header_size << 25) & 0xFFFFFFFF) >> 25) & 0xFF).to_bytes(1, "big"))

            file.write(0x54.to_bytes(1, "big")) # T
            file.write(0x49.to_bytes(1, "big")) # I
            file.write(0x54.to_bytes(1, "big")) # T
            file.write(0x32.to_bytes(1, "big")) # 2
            file.write((((1 + len(title_bytes)) >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(title_bytes)) << 8 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(title_bytes)) << 16 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(title_bytes)) << 24 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
            file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
            file.write(0x01.to_bytes(1, "big")) # テキストのフレームの文字コード。BOM付きUTF-16は16進数で01。
            for index in range(len(title_bytes)):
                file.write(title_bytes[index].to_bytes(1, "big"))

            file.write(0x54.to_bytes(1, "big")) # T
            file.write(0x50.to_bytes(1, "big")) # P
            file.write(0x45.to_bytes(1, "big")) # E
            file.write(0x31.to_bytes(1, "big")) # 1
            file.write((((1 + len(artist_bytes)) >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(artist_bytes)) << 8 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(artist_bytes)) << 16 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(artist_bytes)) << 24 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
            file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
            file.write(0x01.to_bytes(1, "big")) # テキストのフレームの文字コード。BOM付きUTF-16は16進数で01。
            for index in range(len(artist_bytes)):
                file.write(artist_bytes[index].to_bytes(1, "big"))

            file.write(0x54.to_bytes(1, "big")) # T
            file.write(0x52.to_bytes(1, "big")) # R
            file.write(0x43.to_bytes(1, "big")) # C
            file.write(0x4B.to_bytes(1, "big")) # K
            file.write((((1 + len(track_bytes)) >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(track_bytes)) << 8 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(track_bytes)) << 16 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write((((1 + len(track_bytes)) << 24 >> 24) & 0xFF).to_bytes(1, "big"))
            file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
            file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
            file.write(0x01.to_bytes(1, "big")) # テキストのフレームの文字コード。BOM付きUTF-16は16進数で01。
            for index in range(len(track_bytes)):
                file.write(track_bytes[index].to_bytes(1, "big"))

            if album != "":
                file.write(0x54.to_bytes(1, "big")) # T
                file.write(0x41.to_bytes(1, "big")) # A
                file.write(0x4C.to_bytes(1, "big")) # L
                file.write(0x42.to_bytes(1, "big")) # B
                file.write((((1 + len(album_bytes)) >> 24) & 0xFF).to_bytes(1, "big"))
                file.write((((1 + len(album_bytes)) << 8 >> 24) & 0xFF).to_bytes(1, "big"))
                file.write((((1 + len(album_bytes)) << 16 >> 24) & 0xFF).to_bytes(1, "big"))
                file.write((((1 + len(album_bytes)) << 24 >> 24) & 0xFF).to_bytes(1, "big"))
                file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
                file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
                file.write(0x01.to_bytes(1, "big")) # テキストのフレームの文字コード。BOM付きUTF-16は16進数で01。
                for index in range(len(album_bytes)):
                    file.write(album_bytes[index].to_bytes(1, "big"))

            if 1 <= len(image_bytes):
                file.write(0x41.to_bytes(1, "big")) # A
                file.write(0x50.to_bytes(1, "big")) # P
                file.write(0x49.to_bytes(1, "big")) # I
                file.write(0x43.to_bytes(1, "big")) # C
                file.write((((1 + len(image_mimetype_bytes) + 1 + 1 + 1 + len(image_bytes)) >> 24) & 0xFF).to_bytes(1, "big"))
                file.write((((1 + len(image_mimetype_bytes) + 1 + 1 + 1 + len(image_bytes)) << 8 >> 24) & 0xFF).to_bytes(1, "big"))
                file.write((((1 + len(image_mimetype_bytes) + 1 + 1 + 1 + len(image_bytes)) << 16 >> 24) & 0xFF).to_bytes(1, "big"))
                file.write((((1 + len(image_mimetype_bytes) + 1 + 1 + 1 + len(image_bytes)) << 24 >> 24) & 0xFF).to_bytes(1, "big"))
                file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
                file.write(0x00.to_bytes(1, "big")) # フレームのフラグ
                file.write(0x00.to_bytes(1, "big")) # フレームの文字コード。ISO-8859-1は16進数で00。
                for index in range(len(image_mimetype_bytes)):
                    file.write(image_mimetype_bytes[index].to_bytes(1, "big"))
                file.write(0x00.to_bytes(1, "big")) # NULL
                file.write(0x03.to_bytes(1, "big")) # Picture Type(画像の種類)。Front Cover(表カバー)は16進数で03。
                file.write(0x00.to_bytes(1, "big")) # Description(説明)の終了を表すNULL
                for index in range(len(image_bytes)):
                    file.write(image_bytes[index].to_bytes(1, "big"))

            for index in range(len(mpeg_frame_bytes)):
                file.write(mpeg_frame_bytes[index].to_bytes(1, "big"))

        message_string_var.set("新MP3ファイル作成が完了しました。" + os.path.join(mp3_dir, new_mp3_file_name))

    except Exception as exception:
        messagebox.showerror(exception.__class__.__name__, str(exception))
        raise


make_mp3_file_button = tkinter.Button(root, text="新MP3ファイル作成", command=make_mp3_file)
make_mp3_file_button.place(x=10, y=560)

root.mainloop()