import tkinter as tk
import threading
import time
import os
from datetime import datetime
from tkinter import messagebox

GROW_TIME = 5

class CarrotButton:
    def __init__(self, master, x, y, index, update_counter):
        self.master = master
        self.index = index
        self.state = 0
        self.update_counter = update_counter  

        self.btn = tk.Button(master, text=f"Грядка {index+1}", bg="sienna4", fg="white", command=self.on_click)
        self.btn.place(x=x, y=y, width=160, height=50)

        self.stage_label = tk.Label(master, text="Стадия: пусто", font=("Arial", 12))
        self.stage_label.place(x=x, y=80, width=160, height=25)

        self.label_image = tk.Label(master, text="")
        self.label_image.place(x=x, y=105, width=160, height=400)

    def on_click(self):
        if self.state == 0:
            self.state = 1
            self.btn.config(bg="yellow", fg="black", text="Посажено")
            self.stage_label.config(text="Стадия: посажено")
            threading.Thread(target=self.grow_stage).start()

            self._try_load_image("./carrot/1.png")

        elif self.state == 3:
            self.state = 0
            self.btn.config(bg="sienna4", fg="white", text=f"Грядка {self.index+1}")
            self.stage_label.config(text="Стадия: пусто")
            self.label_image.config(image='', text="")
            self.update_counter()

    def grow_stage(self):
        def mark_grown():
            self.stage_label.config(text="Стадия: созрело")

        def label_btn_growth():
            self.btn.config(bg="lightgreen", text="Растёт")
            self._try_load_image("./carrot/5.png")

        def label_btn_reif():
            self.btn.config(bg="green4", fg="white", text="Созрело")

        time.sleep(GROW_TIME)
        self.btn.after(0, label_btn_growth)
        def set_growing():
            self.stage_label.config(text="Стадия: растёт")
        self.stage_label.after(0, set_growing)
        self.state = 2

        time.sleep(GROW_TIME)
        self.btn.after(0, label_btn_reif)
        self.stage_label.after(0, mark_grown)
        self.state = 3

        self._try_load_image("./carrot/8.png")

    def _try_load_image(self, path):
        if not os.path.exists(path):
            self.label_image.config(image='', text="(Image not found)")
            return
        try:
            img = tk.PhotoImage(file=path)
            self.photo = img
            self.label_image.config(image=self.photo, text="")
        except Exception:
            self.label_image.config(image='', text="(Image error)")

root = tk.Tk()
root.title("Carrot Farm")
root.geometry("600x600")

count = 0

count_label = tk.Label(root, text="Собрано: 0", font=("Arial", 16))
count_label.place(x=250, y=540)

def update_count():
    global count
    count += 1
    count_label.config(text=f"Собрано: {count}")

def save_result():
    global count
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write(f"{timestamp} — Собрано: {count}\n")
        messagebox.showinfo("Сохранено", f"Результат сохранён: {count}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить результат:\n{e}")

save_btn = tk.Button(root, text="Сохранить", bg="steelblue", fg="white", command=save_result)
save_btn.place(x=420, y=540, width=100, height=30)


start_x = 50
gap_x = 170
y_pos = 30
buttons = []
for i in range(3):
    x = start_x + i * gap_x
    cb = CarrotButton(root, x, y_pos, i, update_count)
    buttons.append(cb)

root.mainloop()
