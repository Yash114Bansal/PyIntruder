from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from json import loads
show_list_box=""
show_search_box=""
json_data={}
def openfile():
    global json_data,show_list_box
    show_list_box.delete(0, END)
    filename = filedialog.askopenfilename(title="Select a file", filetypes=(("Json files", "*.json"), ("All files*", "*")))
    try:
        f0=open(filename,"r")
        data=f0.read()
        data=loads(data)
        json_data=data
        f0.close()
    except:
        messagebox.showerror("Error", "Can not Identify PyIntruder Data")
    for i in json_data:
        txt = i+" "*(94-len(i)-len(json_data[i][1])) + (json_data[i][0]) + " "*(40-len(str(json_data[i][0]))) + json_data[i][1]
        show_list_box.insert(END, txt)

def show_data(event):
    global json_data, show_list_box
    payload = show_list_box.get(ANCHOR)
    payload = payload[0:15].strip()
    dta = json_data[payload][2]
    header_dta=json_data[payload][2]
    x = Toplevel()
    x.geometry("900x600")
    x.title("Response")
    textbox = ScrolledText(x, wrap=WORD, height=34, width=120, fg='#660066')
    textbox.pack()
    textbox.insert(INSERT, dta)
    textbox.config(state=DISABLED)
    x.minsize(900, 500)
    x.maxsize(900, 600)
def update(data):
    global show_list_box, json_data
    show_list_box.delete(0, END)
    for m in data:
        to_insert=m+" "*(97-len(m)) + str(json_data[m][0]) + " "*(40-len(str(json_data[m][0]))) + str(json_data[m][1])
        show_list_box.insert(END, to_insert)


def search(event):
    global show_search_box, json_data
    given_text = show_search_box.get()
    data_find = []
    if given_text == "":
        data_find = [l for l in json_data]

    else:
        for l in json_data:
            if given_text.lower() in json_data[l][2].lower():
                data_find.append(l)

    update(data_find)
def showdatamain():
    global show_search_box,show_list_box
    show_root = Tk()
    show_root.geometry("700x700")
    show_root.title("Attack Box")
    show_root.minsize(700, 700)
    show_root.maxsize(700, 700)
    Label(show_root, text="Attacking").pack()
    Label(show_root, text="Payload" + " "*90 + "Length"+" "*40 + "Status Code", borderwidth=2, relief=SOLID).pack(side=TOP, anchor="w")
    frame0 = Frame(show_root)
    scrollbar0 = ttk.Scrollbar(frame0, orient=VERTICAL)
    frame0.pack(fill=BOTH, expand=1)
    show_list_box = Listbox(frame0, width=80, height=32, yscrollcommand=scrollbar0.set)
    scrollbar0.config(command=show_list_box.yview)
    scrollbar0.pack(side=RIGHT, fill=Y)
    show_list_box.bind("<Double-1>", show_data)
    show_search_box = Entry(show_root, width=45)
    show_list_box.pack()
    Label(show_root, text="Search :", fg="green").place(x=210, y=637)
    show_search_box.place(x=275, y=634)
    show_search_box.bind("<KeyRelease>", search)
    menu_button = Menu(show_root)
    show_root.config(menu=menu_button)

    # Help menu item
    help_menu = Menu(menu_button, tearoff="off")
    menu_button.add_cascade(label="Menu", menu=help_menu)
    help_menu.add_command(label="Open File", command=openfile)
    mainloop()
