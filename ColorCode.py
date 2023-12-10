import tkinter

root = tkinter.Tk()
root.geometry("800x200")
root.title("色表示")

color_code_label = tkinter.Label(text="カラーコード")
color_code_label.place(x=10, y=10)

color_code_textbox = tkinter.Entry(width=20)
color_code_textbox.insert(tkinter.END, "#00FF00")
color_code_textbox.place(x=90, y=10)

color_code_comment_label = tkinter.Label(text="#000000〜#FFFFFFの16進数のRGB値か、black等の色の名前を入力してください")
color_code_comment_label.place(x=260, y=10)

canvas = tkinter.Canvas(root, width = 50, height = 50)
canvas.place(x=10, y=80)

# ボタンが押された時の処理
def show_color():
    color_code = color_code_textbox.get()
    canvas.create_rectangle(0, 0, 50, 50, fill=color_code)

color_show_button = tkinter.Button(root, text="色表示", command=show_color)
color_show_button.place(x=10, y=40)

root.mainloop()
