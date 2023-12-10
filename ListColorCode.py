import tkinter
from tkinter import filedialog
from PIL import Image

root = tkinter.Tk()
root.geometry("800x500")
root.title("全カラーコード取得")

file_string_var = tkinter.StringVar()
file_string_var.set("")

file_label = tkinter.Label(root, textvariable=file_string_var)
file_label.place(x=10, y=40)

image_canvas = tkinter.Canvas(root, width = 350, height = 350)
image_canvas.place(x=10, y=70)

image_canvas.config(scrollregion=(0, 0, 1000, 1000))

horizontal_scrollbar = tkinter.Scrollbar(root, orient=tkinter.HORIZONTAL)
vertical_scrollbar = tkinter.Scrollbar(root, orient=tkinter.VERTICAL)

horizontal_scrollbar.place(x=10, y=430, width=350)
vertical_scrollbar.place(x=370, y=70, height=350)

horizontal_scrollbar.config(command=image_canvas.xview)
vertical_scrollbar.config(command=image_canvas.yview)

image_canvas.config(xscrollcommand=horizontal_scrollbar.set)
image_canvas.config(yscrollcommand=vertical_scrollbar.set)

color_code_list_textbox = tkinter.Entry(width=80)
color_code_list_textbox.place(x=10, y=450)

photo_image = None

def select_file():

    global photo_image

    photo_image = None
    color_code_list_textbox.delete(0, tkinter.END)

    # tkinterだけではPNG画像しか扱えない
    file_path = filedialog.askopenfilename(title="PNG画像ファイル選択", multiple=False, filetypes=[("PNG", ".png")])
    file_string_var.set(file_path)
    if file_string_var.get() == "":
        return
    photo_image = tkinter.PhotoImage(file=file_path)
    image_canvas.create_image(0, 0, image=photo_image, anchor="nw")
    image = Image.open(file_path)
    rgba = image.convert("RGBA")
    size = rgba.size
    color_code_list = []
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b, a = rgba.getpixel((x, y))
            color_code_list.append("#" + format(r, "02X") + format(g, "02X") + format(b, "02X"))

    color_code_list_textbox.insert(tkinter.END, ",".join(set(color_code_list)))

file_select_button = tkinter.Button(root, text="PNG画像ファイル選択", command=select_file)
file_select_button.place(x=10, y=10)


root.mainloop()
