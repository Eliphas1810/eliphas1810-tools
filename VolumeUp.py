import tkinter
from tkinter import filedialog
import re
from pydub import AudioSegment

root = tkinter.Tk()
root.geometry("700x300")
root.title("MP3音量アップ")

file_string_var = tkinter.StringVar()
file_string_var.set("")

file_label = tkinter.Label(root, textvariable=file_string_var)
file_label.place(x=10, y=40)

# .htsvoiceファイル選択ボタンが押された時の処理
def select_file():
    file_path = filedialog.askopenfilename(title="MP3ファイル選択", multiple=False, filetypes=[("MP3", ".mp3")])
    file_string_var.set(file_path)

file_select_button = tkinter.Button(root, text="MP3ファイル選択", command=select_file)
file_select_button.place(x=10, y=10)

decibel_label = tkinter.Label(text="デシベル")
decibel_label.place(x=10, y=70)

decibel_textbox = tkinter.Entry(width=10)
decibel_textbox.insert(tkinter.END, "10")
decibel_textbox.place(x=90, y=70)

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=150)

# 音量アップボタンが押された時の処理
def up_volume():

    message_string_var.set("")

    file_path = file_string_var.get()
    if file_path == "":
        message_string_var.set("MP3ファイルを選択してください")
        return

    decibel = decibel_textbox.get()
    if decibel == "":
        message_string_var.set("デシベルを入力してください")
        return

    if re.match("^[0-9]+$", decibel) == None:
        message_string_var.set("半角数字でデシベルを入力してください")
        return

    audioSegment = AudioSegment.from_file(file_path, format="mp3")
    audioSegment = audioSegment + int(decibel)
    audioSegment.export(re.sub("\.[mM][pP]3$", "", file_path) + " VolumeUp.mp3", format="mp3")

    message_string_var.set("音量をアップしたMP3を保存しました。" + re.sub("\.[mM][pP]3$", "", file_path) + " VolumeUp.mp3")

volume_up_button = tkinter.Button(root, text="音量アップ", command=up_volume)
volume_up_button.place(x=10, y=110)


root.mainloop()
