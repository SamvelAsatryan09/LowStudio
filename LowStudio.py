from tkinter import *
from tkinter import PhotoImage, Button
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import os
import pathlib
import re
import time
from tkinter import ttk
import sys

os.system('py loading.py')
time.sleep(5)

root = Tk()

suggestion_count = 0
file_path= ''
pathName = ''

if file_path == '':
    root.title('LowStudio')
else:
    root.title(file_path)

root.iconbitmap('LowStudio.ico')
root.geometry('1366x768')
root.configure(bg="#808080")
root.resizable(True,True)
root.state('zoomed')

fontsio = 12
fontsi = 14
font = ('Ubuntu', fontsi)

previousText = ''
suggestion_prefix = ''

def rgb(rgb):
    return "#%02x%02x%02x" % rgb

normal = rgb((173, 140, 62))           # Обычный текст
keywords = rgb((101, 7, 125))          # Ключевые слова
comments = rgb((128, 128, 128))        # Комментарии
string = rgb((25, 120, 6))             # Строки
function = rgb((6, 91, 120))           # Функции и классы
background = rgb((44, 55, 59))         # Фон
values = rgb((250, 61, 47))            # Константы и специальные значения
red = rgb((224, 10, 2))                # Присваивание
operators = rgb((189, 10, 4))          # Логические операторы
arithmetic = rgb((189, 10, 4))         # Арифметические операторы
comparison = rgb((189, 10, 4))         # Операторы сравнения
logical = rgb((189, 10, 4))            # Логические операторы
builtin_functions = rgb((25, 45, 69))  # Встроенные функции
numbers = rgb((250, 189, 47))          # Числа
variables = rgb((248, 248, 242))       # Идентификаторы переменных
decorators = rgb((174, 129, 255))      # Декораторы

font = ('Ubuntu', fontsi)

# Паттерны для подсветки
repl = [
    # Ключевые слова Python
    (r'\b(print|and|as|assert|async|await|break|class|continue|del|finally|lambda|nonlocal|raise|yield|if|else|elif|for|in|return|with|from|import|try|except|is|not|or|pass|while|global|def|None|True|False)\b', keywords),

    # Строки
    (r'".*?"|\'.*?\'', string),

    # Комментарии
    (r'#.*?$', comments),

    # Функции и классы
    (r'\b(def|class)\b\s+\w+', function),

    # Константы и специальные значения
    (r'\b(None|True|False|Ellipsis|NotImplemented)\b', values),

    # Операторы
    (r'\b(and|or|not|is|in)\b', operators),

    # Операции присваивания
    (r'=', red),

    # Арифметические операторы
    (r'[\+\-\*/%]', arithmetic),

    # Сравнительные операторы
    (r'==|!=|<=|>=|<|>', comparison),

    # Логические операторы
    (r'\b(and|or|not)\b', logical),

    # Встроенные функции
    (r'\b(abs|all|any|ascii|bin|bool|breakpoint|bytearray|bytes|callable|chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|sum|super|tuple|type|vars|zip|__import__)\b', builtin_functions),

    # Числа
    (r'\b\d+\b', numbers),

    # Идентификаторы переменных
    (r'\b[a-zA-Z_]\w*\b', variables),

    # Декораторы
    (r'@\w+', decorators)
]

keywords_list = [
    'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 
    'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 
    'except', 'finally', 'for', 'from', 'global', 'if', 'import', 
    'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 
    'raise', 'return', 'try', 'while', 'with', 'yield',
    'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 
    'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr', 
    'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter', 'float', 
    'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 
    'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 
    'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 
    'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 
    'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 
    'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip', '__import__'
]

def changes(event=None):
    global previousText
    if code_menu.get('1.0', END) == previousText:
        return

    for tag in code_menu.tag_names():
        code_menu.tag_remove(tag, "1.0", "end")

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, code_menu.get('1.0', END)):
            code_menu.tag_add(f'{i}', start, end)
            code_menu.tag_config(f'{i}', foreground=color)
            i += 1

    previousText = code_menu.get('1.0', END)

def show_suggestions(event=None):
    changes()
    global suggestion_prefix
    cursor_pos = code_menu.index(INSERT)
    cursor_line = code_menu.get("insert linestart", "insert lineend")
    line_start = code_menu.index(f"insert linestart")
    line_text = code_menu.get(line_start, cursor_pos)

    if '.' in line_text:
        suggestion_prefix = line_text.split('.')[-1].strip()
    else:
        suggestion_prefix = line_text.strip()

    if not suggestion_prefix:
        suggestions_box.place_forget()
        return
    
    matching_keywords = [word for word in keywords_list if word.startswith(suggestion_prefix)]
    suggestion_count = len(matching_keywords)

    if matching_keywords:
        suggestions_box.delete(0, END)
        for word in matching_keywords:
            suggestions_box.insert(END, word)

        # Position the suggestions box under the cursor
        x, y, _, _ = code_menu.bbox(INSERT)
        if y is not None:
            suggestions_box.place(x=x + 50, y=y, anchor='nw')  # Adjust y + 20 as needed
        else:
            suggestions_box.place_forget()
    else:
        suggestions_box.place_forget()
    changes()

def select_suggestion(event=None):
    changes()
    selected = suggestions_box.curselection()
    if selected:
        suggestion = suggestions_box.get(selected[0])
        cursor_pos = code_menu.index(INSERT)
        line_start = code_menu.index(f"insert linestart")
        line_text = code_menu.get(line_start, cursor_pos)

        if '.' in line_text:
            prefix = line_text.split('.')[-1].strip()
        else:
            prefix = line_text.strip()

        new_line_text = line_text.replace(prefix, suggestion, 1)
        code_menu.delete(line_start, cursor_pos)
        code_menu.insert(line_start, new_line_text)
        
        # Move cursor after the inserted text
        cursor_pos = code_menu.index(INSERT)
        code_menu.mark_set(INSERT, f"{line_start}+{len(suggestion)}c")  # Move cursor after the inserted text
        
        # Force update and redraw to ensure highlighting
        code_menu.update_idletasks()
        changes()
        show_suggestions()  # Show updated suggestions
        suggestions_box.place_forget()

def open_project():
    folder_path = filedialog.askdirectory(title="Выберите папку проекта")
    if folder_path:
        update_files_repo(folder_path)

def update_files_repo(folder_path):
    global current_path
    current_path = folder_path
    files_repo.delete(0, END)

    if os.path.dirname(folder_path) != folder_path:
        files_repo.insert(END, "..")

    for item in os.listdir(folder_path):
        files_repo.insert(END, item)

def search_re(pattern, text):
    matches = []
    lines = text.splitlines()

    for i, line in enumerate(lines):
        for match in re.finditer(pattern, line):
            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches

def create_new_file(event=None):
    save_file()
    code_menu.delete('1.0', END)
    root.title('Unnamed - LowStudio')

def undo(event=None):
    code_menu.undo()

def redo(event=None):
    pass

def select_all(event=None):
    code_menu.delete(0.0)

def change_light():
    pass

def changefont(event):
    global fontsi
    global font
    if event.delta > 0:
        if fontsi < 50:
            fontsi += 2
            font = ('Ubuntu', fontsi)
            print("+ 2")
            code_menu.config(font=font)
            root.update()
            root.update_idletasks()
            print("Updated")
        else:
            pass
    else:
        fontsi -= 2
        font = ('Ubuntu', fontsi)
        print("-2")
        code_menu.config(font=font)
        root.update()
        root.update_idletasks()
        print("Updated")

def changefontoutput(event=None):
    global fontsi
    global font
    if event.delta > 0:
        if fontsi < 30:
            fontsi += 2
            font = ('Ubuntu', fontsi)
            print("+ 2")
            code_menu.config(font=font)
            root.update()
            root.update_idletasks()
            print("Updated")
        else:
            pass
    else:
        fontsi -= 2
        font = ('Ubuntu', fontsi)
        print("-2")
        code_menu.config(font=font)
        root.update()
        root.update_idletasks()
        print("Updated")

def set_file_path(path):
    global file_path
    file_path=path
    root.title(path)
    changes()

def open_file(event=None):
    path = askopenfilename(filetypes=[('Python Files','*.py')])
    pathName = os.path.basename(path)
    print(pathName)
    with open(path, 'r') as file:
        code = file.read()
        code_menu.delete('1.0', END)
        code_menu.insert('1.0', code)
        root.title(path + ' - LowStudio')
        set_file_path(path)
    changes()
    if pathName != '':
        label.configure(text=pathName)
    else:
        label.configure(text='Untitled')

def on_item_double_click(event):
    selected_item = files_repo.get(files_repo.curselection())
    selected_path = os.path.join(current_path, selected_item)
    if os.path.isdir(selected_path):
        update_files_repo(selected_path)
    else:
        with open(selected_path, 'r') as file:
            code = file.read()
            code_menu.delete('1.0', END)
            code_menu.insert('1.0', code)
            root.title(os.path.basename(selected_path) + ' - LowStudio')
            set_file_path(selected_path)
            label.configure(text=os.path.basename(selected_path))
            changes()

def create_venv(event=None):
    pass

def save_file(event=None):
    if file_path=='':
       path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
       path=file_path
    with open(path, 'w') as file:
        code = code_menu.get('1.0', END)
        file.write(code)
        set_file_path(path)
        root.title(path + ' - LowStudio')
    changes()

def start_file(event=None):
    if file_path =='':
        messagebox.showerror("LowStudio", "Try to save your code ( Ctrl + s ).")
        return
    global console
    console.configure(state="normal")
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
    output , error = process.communicate()
    console.insert('1.0', error)
    console.insert('1.0', output)
    console.configure(state="disabled")
    changes()

def clear_cons(event=None):
    console.delete(1.0, END)
    changes()

def stop_file(event=None):
    if file_path=='':
        messagebox.showerror('LowStudio', 'Try to save file Ctrl+s')
    else:
         messagebox.showinfo('LowStudio', 'File Stop')

def save_as_file(event=None):
    if file_path == '':
        file_path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        file_path = path
    with open(file_path, 'g') as file:
        code = console.get('1.0', END)
        file.write(code)
        set_file_path(file_path)
        root.title(path + ' - LowStudio')

def about_us(event=None):
    messagebox.showinfo('LowStudio', 'Мы два кодера интузиаста которые любят программирование, и пишут разные проекты помогая развивать айти')

# Code menu
code_menu = Text(root, font=float, undo=True, selectbackground='#696969', inactiveselectbackground='#b8b4b4', fg='#e1e6e2')
code_menu.place(x=50, y=30, width=1166,height=738)
code_menu.configure(bg="#262625",undo=True)

# 2 window
os.system('py loading.py')

#File Menu
file_menu = Frame(root, bg='#696969')
file_menu.place(x=50, y=0, width=200, height=30)
label = Label(root, text='Untitled *', bg='#696969', font='Ubuntu')
label.place(x=50, y=5, width=100, height=16)

#File repository show
files_repo = Listbox(root, width="100", height="768", background="#2e2e2e", foreground="#e3e3e3")
files_repo.place(x=1216, y=0)

#Console
console = Text(root, selectbackground='#bab0af', inactiveselectbackground='#b8b4b4', font="Arial", bg="#262625", fg='#f5ed05')
console.place(x=50,y=510,width=1166,height=258)
console.configure(state="disabled")

# Button menu
button_menu = Frame(root, bg='#606060')
button_menu.place(x=1, y=0, width=50,height=768)

# Suggestions box
suggestions_box = Listbox(root, font=('Arial', 10), width=30, height=suggestion_count*5)
suggestions_box.place_forget()  # Hide initially

# Menu
menu = Menu()
file_menu = Menu(menu, tearoff=0)
oformlenie_menu = Menu(menu, tearoff=0)
edit_menu = Menu(menu, tearoff=0)
Tools_menu = Menu(menu, tearoff=0)
run_menu = Menu(menu, tearoff=0)
setting_menu = Menu(menu, tearoff=0)
other_menu = Menu(menu, tearoff=0)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Edit", menu=edit_menu)
menu.add_cascade(label="Run", menu=run_menu)
menu.add_command(label="Exit", command=root.destroy)
menu.add_cascade(label="Colors", menu=oformlenie_menu)
menu.add_cascade(label="Tools", menu=Tools_menu)
Tools_menu.add_command(label="Create Venv", command=create_venv)
edit_menu.add_command(label="Undo - Ctrl + Z", command=undo)
edit_menu.add_command(label="Redo - Ctrl + Y", command=redo)
edit_menu.add_command(label='Select All - Ctrl+A', command=select_all)

file_menu.add_command(label="New File - Ctrl + N", command=create_new_file)
file_menu.add_command(label="Open - Ctrl + O", command=open_file)
file_menu.add_command(label="Save - Ctrl + S", command=save_file)
file_menu.add_command(label="Save as - Ctrl + shift + S", command=save_as_file)
file_menu.add_command(label="Open Project", command=open_project)
file_menu.add_cascade(label='Settings - Ctrl + Alt + S', menu=setting_menu)

setting_menu.add_command(label='about Us', command=about_us)

run_menu.add_command(label='Run - F5', command=start_file)
run_menu.add_command(label='Clear - F6', command=clear_cons)

oformlenie_menu.add_command(label="Change Colors", command=change_light)

root.bind('<F6>', clear_cons)
root.bind('<Control-n>', create_new_file)
root.bind('<F5>', start_file)
root.bind('<Control-s>', save_file)
root.bind('<Control-o>', open_file)
code_menu.bind('<Control-MouseWheel>', changefont)
console.bind('<Control-MouseWheel>', changefontoutput)
code_menu.bind('<Control-+>', changefont)
console.bind('<Control-+>', changefontoutput)
code_menu.bind('<KeyRelease>', changes)
code_menu.bind('<KeyRelease>', show_suggestions)
suggestions_box.bind('<Double-1>', select_suggestion)
suggestions_box.bind('<Tab>', select_suggestion)

files_repo.bind('<Double-1>', on_item_double_click)

from PIL import ImageTk

def resize_image(image_path, width, height):
    image = Image.open(image_path)
    image = image.resize((width, height))
    return ImageTk.PhotoImage(image)

logo_size = (20, 20)
button_image_size = (20, 20)

img_logo = resize_image('Assets/LOGO.png', *logo_size)
img_stop = resize_image('Assets/Stop.png', *button_image_size)
img_play = resize_image('Assets/play.png', *button_image_size)

logo = Label(button_menu,bd=0, height=30, width=30, image=img_logo)
logo.pack()

button_stop = Button(button_menu,border=0,activebackground="#606060", height=30, width=30, image=img_stop, bg='#606060', command=stop_file)
button_play = Button(button_menu,border=0,activebackground="#606060", height=30, width=30, image=img_play, bg='#606060', command=start_file)
button_stop.pack()
button_play.pack()

root.config(menu=menu)

root.mainloop()