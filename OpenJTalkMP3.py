import tkinter
from tkinter import filedialog
import tempfile
import re
import subprocess
import os
import threading
from pydub import AudioSegment
import datetime

root = tkinter.Tk()
root.geometry("700x700")
root.title("テキストエリアの文字をOpenJTalkで読み上げます。")

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=550)

file_string_var = tkinter.StringVar()
file_string_var.set("")

file_label = tkinter.Label(root, textvariable=file_string_var)
file_label.place(x=10, y=40)

# .htsvoiceファイル選択ボタンが押された時の処理
def select_file():

    message_string_var.set("")

    voice_file_path = filedialog.askopenfilename(title=".htsvoiceファイル選択", multiple=False, filetypes=[(".htsvoiceファイル", ".htsvoice")])

    if "'" in voice_file_path:
        message_string_var.set("'が含まれない.htsvoiceファイルを選択してください。")
        return

    file_string_var.set(voice_file_path)

file_select_button = tkinter.Button(root, text=".htsvoiceファイル選択", command=select_file)
file_select_button.place(x=10, y=10)

textarea = tkinter.Text(width=80, height=30)
textarea.place(x=10, y=70)

vertical_scrollbar = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)

vertical_scrollbar.place(x=580, y=70, height=430)

vertical_scrollbar.config(command=textarea.yview)

textarea.config(yscrollcommand=vertical_scrollbar.set)

cancel_flag = False

# 読み上げ処理
def read():

    global cancel_flag
    cancel_flag = False

    message_string_var.set("")

    voice_file_path = file_string_var.get()
    if voice_file_path == "":
        message_string_var.set(".htsvoiceファイルを選択してください。")
        return

    # if "'" in voice_file_path:
        # message_string_var.set("'が含まれない.htsvoiceファイルを選択してください。")
        # return

    # 一時ディレクトリを作成
    temp_dir = tempfile.TemporaryDirectory()

    text = textarea.get("1.0", "end -1c")
    line_list = text.splitlines()
    for line in line_list:

        if cancel_flag:
            message_string_var.set("中止しました。")
            break

        # 全角等号を「は」に置換
        line = re.sub("＝", "は", line)

        # 漢字、ひらがな、カタカナ、数字、アルファベット、一部の全角記号以外を全角空白に置換
        line = re.sub("[^一-鿋々ぁ-ゖァ-ヺｦ-ﾟー0-9０-９a-zA-Zａ-ｚＡ-Ｚ＋×÷]", "　", line)

        # 先頭の半角空白と全角空白の連続を除去
        line = re.sub("^[ 　]+", "", line)

        # 末尾の半角空白と全角空白の連続を除去
        line = re.sub("[ 　]+$", "", line)

        # 半角空白と全角空白の連続を全角空白に置換
        line = re.sub("[ 　]{2,}", "　", line)

        if line == "":
            continue

        # 全角空白の連続の場合
        if re.match("^　+$", line):
            continue

        subprocess.call("echo '" + line + "' | open_jtalk -x /var/lib/mecab/dic/open-jtalk/naist-jdic -m '" + voice_file_path + "' -ow '" + os.path.join(temp_dir.name, "temp.wav") + "' -r 0.8", shell=True)
        subprocess.call("aplay -q '" + os.path.join(temp_dir.name, "temp.wav") + "'", shell=True)

    temp_dir.cleanup()

    message_string_var.set("読み上げが終わりました。")


# 読み上げボタンが押された時の処理
def run_read():
    thread = threading.Thread(target=read)
    thread.start()

read_button = tkinter.Button(root, text="読み上げ", command=run_read)
read_button.place(x=10, y=510)

# キャンセルボタンが押された時の処理
def cancel():
    global cancel_flag
    cancel_flag = True

cancel_button = tkinter.Button(root, text="中止", command=cancel)
cancel_button.place(x=100, y=510)

save_dir_string_var = tkinter.StringVar()
save_dir_string_var.set("")

save_dir_label = tkinter.Label(root, textvariable=save_dir_string_var)
save_dir_label.place(x=10, y=610)

# 保存ディレクトリ選択ボタンが押された時の処理
def select_save_dir():
    save_dir = filedialog.askdirectory(initialdir=os.path.expanduser("~"))
    save_dir_string_var.set(save_dir)

save_dir_select_button = tkinter.Button(root, text="保存ディレクトリ選択", command=select_save_dir)
save_dir_select_button.place(x=10, y=580)

# 保存ボタンが押された時の処理
def save():
    message_string_var.set("")

    save_dir = save_dir_string_var.get()
    if save_dir == "":
        message_string_var.set("保存ディレクトリを選択してください。")
        return

    voice_file_path = file_string_var.get()
    if voice_file_path == "":
        message_string_var.set(".htsvoiceファイルを選択してください。")
        return

    # if "'" in voice_file_path:
        # message_string_var.set("'が含まれない.htsvoiceファイルを選択してください。")
        # return

    # 一時ディレクトリを作成
    temp_dir = tempfile.TemporaryDirectory()

    text = textarea.get("1.0", "end -1c")
    line_list = text.splitlines()
    wav_count = 0
    for line in line_list:

        # 全角等号を「は」に置換
        line = re.sub("＝", "は", line)

        # 漢字、ひらがな、カタカナ、数字、アルファベット、一部の全角記号以外を全角空白に置換
        line = re.sub("[^一-鿋々ぁ-ゖァ-ヺｦ-ﾟー0-9０-９a-zA-Zａ-ｚＡ-Ｚ＋×÷]", "　", line)

        # 先頭の半角空白と全角空白の連続を除去
        line = re.sub("^[ 　]+", "", line)

        # 末尾の半角空白と全角空白の連続を除去
        line = re.sub("[ 　]+$", "", line)

        # 半角空白と全角空白の連続を全角空白に置換
        line = re.sub("[ 　]{2,}", "　", line)

        if line == "":
            continue

        # 全角空白の連続の場合
        if re.match("^　+$", line):
            continue

        subprocess.call("echo '" + line + "' | open_jtalk -x /var/lib/mecab/dic/open-jtalk/naist-jdic -m '" + voice_file_path + "' -ow '" + os.path.join(temp_dir.name, "temp" + str(wav_count + 1) + ".wav") + "' -r 0.8", shell=True)
        wav_count = wav_count + 1

    if wav_count <= 0:
        temp_dir.cleanup()
        message_string_var.set("読み上げ対象と成る有効な文字が無かったので保存しませんでした。")
        return

    if wav_count == 1:
        audioSegment = AudioSegment.from_file(os.path.join(temp_dir.name, "temp1.wav"), format="wav")
        audioSegment.export(os.path.join(save_dir, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.mp3")), format="mp3")
        temp_dir.cleanup()
        message_string_var.set("保存しました" + os.path.join(save_dir, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.mp3")))
        return

    audioSegment = AudioSegment.from_file(os.path.join(temp_dir.name, "temp1.wav"), format="wav")
    for number in range(2, wav_count + 1):
        audioSegment = audioSegment + AudioSegment.from_file(os.path.join(temp_dir.name, "temp" + str(number) + ".wav"), format="wav")
    audioSegment.export(os.path.join(save_dir, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.mp3")), format="mp3")
    temp_dir.cleanup()
    message_string_var.set("保存しました" + os.path.join(save_dir, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.mp3")))

save_button = tkinter.Button(root, text="保存", command=save)
save_button.place(x=10, y=640)


root.mainloop()
