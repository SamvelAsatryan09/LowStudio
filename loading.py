from tkinter import *
from PIL import ImageTk, Image
import os

root = Tk()
root.resizable(False, False)
root.overrideredirect(True)

window_width = 1000
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Устанавливаем размер холста равным размеру окна
canvas = Canvas(root, width=window_width, height=window_height)
canvas.pack()

# Убедитесь, что изображение находится в правильной папке и имеет подходящий размер
image_path = "Assets/loading.jpeg"
if os.path.exists(image_path):
    pilImage = Image.open(image_path)
    image = ImageTk.PhotoImage(pilImage)
    imagesprite = canvas.create_image(window_width // 2, window_height // 2, image=image)
else:
    print(f"Image not found at path: {image_path}")

# Закрываем окно через 5 секунд
root.after(5000, root.destroy)

root.mainloop()
