import tkinter
from tkinter import filedialog
from PIL import Image
import os
import re
import datetime

root = tkinter.Tk()
root.geometry("800x600")
root.title("色変更")

file_string_var = tkinter.StringVar()
file_string_var.set("")

file_label = tkinter.Label(root, textvariable=file_string_var)
file_label.place(x=10, y=40)

image_canvas = tkinter.Canvas(root, width = 250, height = 250)
image_canvas.place(x=10, y=70)

image_canvas.config(scrollregion=(0, 0, 1000, 1000))

horizontal_scrollbar = tkinter.Scrollbar(root, orient=tkinter.HORIZONTAL)
vertical_scrollbar = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)

horizontal_scrollbar.place(x=10, y=330, width=250)
vertical_scrollbar.place(x=270, y=70, height=250)

horizontal_scrollbar.config(command=image_canvas.xview)
vertical_scrollbar.config(command=image_canvas.yview)

image_canvas.config(xscrollcommand=horizontal_scrollbar.set)
image_canvas.config(yscrollcommand=vertical_scrollbar.set)

color_code_list_label = tkinter.Label(root, text="変更前のカラーコード一覧")
color_code_list_label.place(x=10, y=350)

color_code_list_textbox = tkinter.Entry(width=55)
color_code_list_textbox.place(x=170, y=350)

color_code_list_comment_label = tkinter.Label(root, text="#00FF00等の16進数表記")
color_code_list_comment_label.place(x=620, y=350)

color_code_label = tkinter.Label(root, text="変更後のカラーコード")
color_code_label.place(x=10, y=390)

color_code_textbox = tkinter.Entry(width=10)
color_code_textbox.place(x=150, y=390)
color_code_textbox.insert(tkinter.END, "#FFFFFF")

alpha_label = tkinter.Label(root, text="変更後の透明度")
alpha_label.place(x=270, y=390)

alpha_textbox = tkinter.Entry(width=5)
alpha_textbox.place(x=380, y=390)
alpha_textbox.insert(tkinter.END, "255")

alpha_comment_label = tkinter.Label(root, text="0は透明。255は不透明")
alpha_comment_label.place(x=430, y=390)

photo_image = None

# PNG画像ファイル選択ボタンが押された時の処理
def select_file():

    global photo_image

    photo_image = None

    # tkinterだけではPNG画像しか扱えない
    file_path = filedialog.askopenfilename(title="PNG画像ファイル選択", multiple=False, filetypes=[("PNG", ".png")])
    file_string_var.set(file_path)
    if file_string_var.get() == "":
        return
    photo_image = tkinter.PhotoImage(file=file_path)
    image_canvas.create_image(0, 0, image=photo_image, anchor="nw")

file_select_button = tkinter.Button(root, text="PNG画像ファイル選択", command=select_file)
file_select_button.place(x=10, y=10)

out_dir_string_var = tkinter.StringVar()
out_dir_string_var.set("")

out_dir_label = tkinter.Label(root, textvariable=out_dir_string_var)
out_dir_label.place(x=10, y=470)

# 変更後PNG画像保存ディレクトリ選択ボタンが押された時の処理
def select_out_dir():
    out_dir_string_var.set(filedialog.askdirectory(initialdir=os.path.expanduser("~")))

out_dir_select_button = tkinter.Button(root, text="変更後PNG画像保存ディレクトリ選択", command=select_out_dir)
out_dir_select_button.place(x=10, y=430)

message_string_var = tkinter.StringVar()
message_string_var.set("")

message_label = tkinter.Label(root, textvariable=message_string_var)
message_label.place(x=10, y=550)

# 色変更ボタンが押された時の処理
def change_color():

    message_string_var.set("")

    if file_string_var.get() == "":
        message_string_var.set("PNG画像ファイルを選択してください。")
        return

    before_rgb_list = re.findall("#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", color_code_list_textbox.get())
    if len(before_rgb_list) == 0:
        message_string_var.set("変更前のカラーコードを指定してください。")
        return

    if re.match("^#[0-9a-fA-F]{6}$", color_code_textbox.get()) == None:
        message_string_var.set("変更後のカラーコードを例えば#00FF00のように16進数表記で指定してください。")
        return
    after_rgb_list = re.findall("#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})", color_code_textbox.get())
    after_r = int(after_rgb_list[0][0], 16)
    after_g = int(after_rgb_list[0][1], 16)
    after_b = int(after_rgb_list[0][2], 16)

    if re.match("^[0-9]{1,3}$", alpha_textbox.get()) == None:
        message_string_var.set("変更後の透明度を半角数字による0から255までの整数で指定してください。")
        return
    after_alpha = int(alpha_textbox.get())
    if 256 <= after_alpha:
        message_string_var.set("変更後の透明度を0から255までの整数で指定してください。")
        return

    out_dir = out_dir_string_var.get()
    if out_dir == "":
        message_string_var.set("変更後PNG画像保存ディレクトリを選択してください。")
        return

    before_image = Image.open(file_string_var.get())
    before_rgba = before_image.convert("RGBA")
    size = before_rgba.size
    after_image = Image.new("RGBA", size)
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b, a = before_rgba.getpixel((x, y))
            target_rgb_exist = False
            for before_rgb in before_rgb_list:
                target_r = int(before_rgb[0], 16)
                target_g = int(before_rgb[1], 16)
                target_b = int(before_rgb[2], 16)
                if r == target_r and g == target_g and b == target_b:
                    target_rgb_exist = True
                    break
            if target_rgb_exist:
                after_image.putpixel((x, y), (after_r, after_g, after_b, after_alpha))
            else:
                after_image.putpixel((x, y), (r, g, b, a))
    after_image_file_path = os.path.join(out_dir, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.png"))
    after_image.save(after_image_file_path)
    message_string_var.set("変更後のPNG画像を保存しました。" + after_image_file_path)

color_change_button = tkinter.Button(root, text="色変更", command=change_color)
color_change_button.place(x=10, y=510)

root.mainloop()
