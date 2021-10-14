from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo
from concurrent.futures import ThreadPoolExecutor
import requests
import urllib.parse
import base64
import binascii
from tkinter.ttk import Progressbar,Scrollbar
from requests.api import head
import itertools
from tkinter.scrolledtext import ScrolledText
root = Tk()
root.title("PyIntruder v0.3")
root.geometry("1100x650")

root.minsize(1100, 650)
root.maxsize(1100, 650)
img = PhotoImage(file='burp.png')
root.tk.call('wm', 'iconphoto', root._w, img)
# Exception classes
class Unknown_request(Exception):
    pass
class no_threads(Exception):
    pass
class greater_zero(Exception):
    pass
class no_position(Exception):
    pass
class no_wordlist(Exception):
    pass

#Main Variables
var_url =""
var_data=""
var_headers={}
var_req_method = ""

var_from_numbers = 0
var_to_numbers = 0
var_step_numbers = 1
var_min_length = 1
var_max_length = 1
var_bruteforce_charset=""
root_filename = ""
button_place = ''
payload_list=""
loading_bar=""
second_frame=""
uen = StringVar()
urlencode_var=""
percent_increase=0
h=0
encoding_var = ""
option_var = ""
prefix_var = ""
suffix_var = ""
listbox=""
searchbox=""
maindict = {}
def update(data):
    global listbox,maindict
    listbox.delete(0,END)
    for m in data:
        listbox.insert(END,m)

def search(event):
    global searchbox,maindict
    typed_text=searchbox.get()
    data_find=[]
    if typed_text == "":
        data_find=[l for l in maindict]
    else:
        for l in maindict:
            if typed_text.lower() in maindict[l].lower():
                data_find.append(l)

    update(data_find)

def show_data(event):
    global maindict,listbox
    payload=listbox.get(ANCHOR)
    payload=payload[0:15].strip()
    dta = maindict[payload]
    x=Toplevel()
    x.geometry("900x600")
    x.title("Response")
    textbox=ScrolledText(x,wrap=WORD,height=34,width=120,fg='#660066')
    textbox.pack()
    textbox.insert(INSERT,dta)
    textbox.config(state=DISABLED)
    x.minsize(900,600)
    x.maxsize(900,600)
def req_get(list_payload):
        global button_place,maindict,root
        global var_url
        global var_headers
        global var_data,var_req_method
        global urlencode_var
        global encoding_var
        global option_var,listbox
        global prefix_var,suffix_var,percent_increase,loading_bar,second_frame,payload_list,h
        tempvar=payload_list.index(list_payload)
        list_payload=str(list_payload)
        tempvariable=list_payload
        if option_var == 1:
            list_payload = prefix_var+list_payload+suffix_var
            tempvariable=list_payload
            if encoding_var == "Base64":
                list_payload = base64.b64encode(list_payload.encode()).decode()
            elif encoding_var == "Hex":
                list_payload = binascii.hexlify(list_payload.encode()).decode()
            elif encoding_var == "ASCII Numbers":
                list_payload = ''.join(str(ord(c)) for c in list_payload)
        elif option_var == 2:
            if encoding_var == "Base64":
                list_payload = base64.b64encode(list_payload.encode()).decode()
            elif encoding_var == "Hex":
                list_payload = binascii.hexlify(list_payload.encode()).decode()
            elif encoding_var == "ASCII Numbers":
                list_payload = ''.join(str(ord(c)) for c in list_payload)
            list_payload = prefix_var+list_payload+suffix_var
        reqdata = var_data.replace("@@@@@@",list_payload)
        if urlencode_var == "url_encode":
            reqdata=urllib.parse.quote(reqdata, safe='')
        var_headers_temp=var_headers.copy()
        for i in var_headers_temp:
            var_headers_temp[i] = var_headers_temp[i].replace("@@@@@@",list_payload)
        if var_req_method=="GET":
            r =requests.get(var_url,params=reqdata,headers=var_headers_temp)
        elif var_req_method=="POST":
            r=requests.post(var_url,data=reqdata,headers=var_headers_temp)
        maindict[list_payload] = r.text
        txt=tempvariable+" "*(97-len(list_payload))+str(len(r.text))+" "*(40-len(str(len(r.text))))+str(r.status_code)
        listbox.insert(END,txt)
        h+=percent_increase
        loading_bar["value"] = h
        root.update_idletasks()

def extractrequest(web_request):
    g=open("temp.txt",'w+')
    g.write(web_request)
    g.close()
    f=open("temp.txt","r")
    listdata1=f.readlines()
    listdata=[]
    for i in listdata1:
      tv=str(i).replace("\n","")
      if tv!="":
        listdata.append(tv)
    req_type=listdata[0]
    host=listdata[1]
    headerslist={}

    if "POST" in req_type:
        req_method="POST"
        fullurl=req_type[4:-9]
        data=listdata[-1]
        for i in range(2,len(listdata)-2): 
            spoint=listdata[i].find(":")
            headerslist[listdata[i][:spoint]]=listdata[i][spoint+2:].rstrip("\n")
            

    elif "GET" in req_type:
        req_method="GET"
        getfind=req_type.find("?")
        if getfind == -1:
            fullurl=req_type[3:-9]
        else:
            fullurl=req_type[3:getfind]
        data=req_type[getfind+1:-9]

        for i in range(2,len(listdata)-1):       
            spoint=listdata[i].find(":")
            headerslist[listdata[i][:spoint]]=listdata[i][spoint+2:].rstrip("\n") 
    else:
        try:
            raise Unknown_request
        except Unknown_request:
            messagebox.showwarning("Warning","Unable To Detect Request Type")
            return

    f.close()
    url="http://"+host[5:].strip()+fullurl.strip()
    headerslist.pop("",None)
    return req_method,url,headerslist,data


def mainattack():
    global button_place
    global var_url
    global var_headers
    global var_data
    global var_req_method
    global urlencode_var
    global encoding_var
    global option_var,listbox,searchbox
    global prefix_var,suffix_var,loading_bar,second_frame,h
    main_request = Request_Text_Area.get("1.0",END)
    var_req_method,var_url,var_headers,var_data = extractrequest(main_request)
    for temp_replace in var_headers:
        temp_var = var_headers[temp_replace]
        if "§" in temp_var:
            position1 = temp_var.find("§",0)
            position2 = temp_var.find("§",position1+1)
            position2 = position2 +1
            temp_var = temp_var.replace(temp_var[position1:position2],"@@@@@@")
            var_headers[temp_replace] = temp_var
    for i in range(10):
        if "§" in var_data:
            position1 = var_data.find("§",0)
            position2 = var_data.find("§",position1+1)
            position2 = position2 +1
            var_data = var_data.replace(var_data[position1:position2],"@@@@@@")
        else:
            break

    attack_type = combo_box1.get()
    urlencode_var=uen.get()
    encoding_var = combo_box2.get()
    option_var = opt1.get()
    prefix_var = prefix.get()
    suffix_var = suffix.get()
    button_place = Toplevel()
    button_place.geometry("700x700")
    button_place.title("Attack Box")
    button_place.minsize(700,700)
    button_place.maxsize(700,700)
    Label(button_place,text="Attacking").pack()
    loading_bar=Progressbar(button_place,orient=HORIZONTAL,length=400,mode="determinate")
    loading_bar.pack()
    Label(button_place,text="Payload"+" "*90+"Length"+" "*40+"Status Code",borderwidth=2,relief=SOLID).pack(side=TOP,anchor="w")
    main_frame = Frame(button_place)
    my_scrollbar=ttk.Scrollbar(main_frame,orient=VERTICAL)
    main_frame.pack(fill=BOTH,expand=1)
    listbox=Listbox(main_frame,width=80,height=33,yscrollcommand=my_scrollbar.set)
    my_scrollbar.config(command=listbox.yview)
    my_scrollbar.pack(side=RIGHT,fill=Y)
    listbox.bind("<Double-1>",show_data)
    searchbox=Entry(button_place,width=45)
    listbox.pack()
    Label(button_place,text="Search :",fg="green").place(x=210,y=667)
    searchbox.place(x=280,y=665)
    searchbox.bind("<KeyRelease>",search)
    
    global payload_list
    if attack_type == "Numbers":
        global var_from_numbers
        global var_to_numbers
        global var_step_numbers
        global percent_increase
        payload_list=[x for x in range(var_from_numbers,var_to_numbers+1,var_step_numbers)]
        percent_increase=100/len([x for x in range(var_from_numbers,var_to_numbers+1,var_step_numbers)])
        h=0
        execute=ThreadPoolExecutor(max_workers=Threads_Button.get())
        execute.map(req_get,[x for x in range(var_from_numbers,var_to_numbers+1,var_step_numbers)])
        execute.shutdown(wait=False)
    elif attack_type == "Wordlist":
        global root_filename
        f1 = open(root_filename,"r")
        pay = f1.readlines()
        payload_list=[]
        for i in pay:
            payload_list.append(i.rstrip("\n"))
        percent_increase=100/len(payload_list)
        h=0
        execute=ThreadPoolExecutor(max_workers=Threads_Button.get())
        execute.map(req_get,payload_list)
        execute.shutdown(wait=False)
    elif attack_type=="BruteForce":
        global var_bruteforce_charset,var_max_length,var_min_length
        payload_list=[]
        for x in range(var_min_length,var_max_length+1):
            for y in itertools.product(var_bruteforce_charset,repeat=x):
                payload_list.append("".join(y))
        percent_increase=100/len(payload_list)
        h=0
        execute=ThreadPoolExecutor(max_workers=Threads_Button.get())
        execute.map(req_get,payload_list)
        execute.shutdown(wait=False)
def start_attack():
    global var_from_numbers
    global var_to_numbers
    global var_step_numbers
    global var_min_length
    global var_max_length
    global var_bruteforce_charset
    attack_type = combo_box1.get()
    try:
        attack_threads = Threads_Button.get()
        if attack_threads == 0:
            raise no_threads
    except no_threads:
        messagebox.showwarning("Warning","Please Select Some Threads")
        return
    if attack_type == "Numbers" :
        try:
            var_from_numbers = int(from_entry.get())
            var_to_numbers = int(to_entry.get())
            var_step_numbers = int(step_entry.get())
            if var_to_numbers < 1 or var_step_numbers < 1:
                raise greater_zero
            if "§" not in Request_Text_Area.get("1.0",END):
                raise no_position
            mainattack()
        except ValueError:
            messagebox.showwarning("Warning","Please enter numbers only")
            return
        except greater_zero:
            messagebox.showwarning("Warning","Enter Number Greater Than Zero")
            return
        except no_position:
            messagebox.showwarning("Warning","Please Add Position in Box")
    elif attack_type == "BruteForce":
        try:
            var_min_length = int(min_entry.get())
            var_max_length = int(max_entry.get())
            var_bruteforce_charset=charset.get()
            if var_min_length < 1 or var_max_length < 1:
                raise greater_zero
            if "§" not in Request_Text_Area.get("1.0",END):
                raise no_position
            mainattack()
        except ValueError:
            messagebox.showwarning("Warning","Please enter numbers")
            return
        except greater_zero:
            messagebox.showwarning("Warning","Enter Number Greater Than Zero")
            return
        except no_position:
            messagebox.showwarning("Warning","Please Add Position in Box")
    else:
        try:
            a = root_filename
            if "§" not in Request_Text_Area.get("1.0",END):
                raise no_position
            if "/" not in a:
                raise no_wordlist
            mainattack()
        except no_position:
            messagebox.showwarning("Warning","Please Add Position in Box")
        except no_wordlist:
            messagebox.showwarning("Warning","Please Specify Wordlist")
def add_position():
    if Request_Text_Area.selection_get():
       #Replacing Before and After With Unicode Character 
        Request_Text_Area.insert("sel.first","§")
        Request_Text_Area.insert("sel.last","§")
        temp=Request_Text_Area.get("1.0",END)
        Request_Text_Area.delete(1.0, END)
        Request_Text_Area.insert(1.0,temp.replace("§§",'§')[:-1])
    else:
        pass

def clear_position():
    temp=Request_Text_Area.get("1.0",END)
    Request_Text_Area.delete(1.0, END)
    Request_Text_Area.insert(1.0,temp.replace("§",'')[:-1])

# Function for Paste button

def paste():
    pst = Request_Text_Area.index(INSERT)
    try:
        clip = root.clipboard_get()
        Request_Text_Area.insert(pst, clip)
    except:
        messagebox.showwarning("Warning","Nothing is in the clipboard")
# Function for Clear button


def clear():
    Request_Text_Area.delete(1.0, END)

# Function for choosing file button


def choosefile():
    global root_filename
    root_filename = filedialog.askopenfilename(
        initialdir="~/", title="Select a file", filetypes=(("Text files", "*.txt"), ("All files*", "*")))
    file_label = Label(root, text=root_filename, width=40, fg="red")
    file_label.place(x=580, y=465)
# Function for Combo-Box for Payloads

def comboclk(event):
    #Recieve Value From Drop Down List
    attack_type = combo_box1.get()

    #Disabling Each Parameter 

    choose_file.config(state=DISABLED)
    min_entry.config(state=DISABLED)
    max_entry.config(state=DISABLED)
    
    charset.config(state=DISABLED)
    from_entry.config(state=DISABLED)
    
    to_entry.config(state=DISABLED)
    step_entry.config(state=DISABLED)
    
    if attack_type == "Wordlist" :
       choose_file.config(state=NORMAL)

    if attack_type == "BruteForce" :
       min_entry.config(state=NORMAL)
       max_entry.config(state=NORMAL)
       charset.config(state=NORMAL)     

    if attack_type == "Numbers" :
       from_entry.config(state=NORMAL)
       to_entry.config(state=NORMAL)
       step_entry.config(state=NORMAL)
       
# Function for Help menu item

def info():
    msg = '''About PyIntruder v0.6  

This tool will help you to
send your requests faster
than ever you've used.More
features will be added in
the future.This is
absolutely free of cost. 
    
    Developed by:
        Yash Bansal
        Sagnik Haldar'''
    messagebox.showinfo(title='Details', message=msg)

def usage():
    msg="www.google.com"
    help_window = Toplevel()
    help_lbl = Label(help_window,text=msg)
    help_lbl.pack()


menu_button = Menu(root)
root.config(menu=menu_button)

# Help menu item
help_menu = Menu(menu_button, tearoff="off")
menu_button.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Usage", command=usage)
help_menu.add_command(label="About Me", command=info)


# Requests LabelFrame
frame_requests = LabelFrame(root, text="Requests", padx=260, pady=640, borderwidth=6)
frame_requests.pack(padx=10, pady=10, side=LEFT)
dummy_request_frame = Label(frame_requests, text="",)
dummy_request_frame.grid(row=0, column=0)

# Text-Area for Requests
Request_Text_Area = Text(root, width=60, height=31, bg="#ffffcc")
Request_Text_Area.place(x=30, y=50)

# Paste Button

paste_button = Button(root, text="Paste", command=paste,
                 borderwidth=2, bg="#ff751a", fg="white", activebackground='#ff751a')
paste_button.place(x=275, y=570, height=25, width=75)

# Clear Button
clear_button = Button(root, text="Clear", command=clear,
                 borderwidth=2, bg="#ff751a", fg="white", activebackground='#ff751a')

clear_button.place(x=195, y=570, height=25, width=75)


# Options LabelFrame
Options_Frame = LabelFrame(root, text="Options", padx=260, pady=640, borderwidth=6)
Options_Frame.pack(padx=10, pady=10, side=RIGHT)
Dummy_Options_Frame = Label(Options_Frame, text="",)
Dummy_Options_Frame.grid(row=0, column=0)

# Select Threads Button
Threads_Button = Scale(root, from_=0, to=100, orient=HORIZONTAL)
Threads_Button.place(x=960, y=32)

Select_Threads_Label = Label(root, text="Select Threads", fg='green')
Select_Threads_Label.place(x=858, y=53)


# Position Button and Frame

position_frame = LabelFrame(root, text="Positions",
                            padx=80, pady=30, borderwidth=6)
position_frame.place(x=600, y=98)
Dummy_position_frame = Label(position_frame, text="",)
Dummy_position_frame.grid(row=0, column=0)

button_add_position = Button(root, text=" Add Position ",
                          borderwidth=2, bg="#ff751a", activebackground='#ff751a', height=1,command=add_position)
button_add_position.place(x=625, y=120)
button_clear_position = Button(root, text="Clear Position",
                            borderwidth=2, bg="#ff751a", activebackground='#ff751a', height=1,command=clear_position)
button_clear_position.place(x=625, y=160)

# BruteForce Frame

bruteforce_frame = LabelFrame(
    root, text="BruteForce", padx=130, pady=35, borderwidth=6)
bruteforce_frame.place(x=790, y=95)
label_BruteForce = Label(bruteforce_frame, text="",)
label_BruteForce.grid(row=0, column=0)

# BruteForce Charset

charset = Entry(root, width=30, bg="#ffff99", fg="green",state=DISABLED)
charset.get()
charset.place(x=805, y=120)
charset.insert(0, "Enter The Charset")

# Min Length

min_label = Label(root, text="Min Length:", fg="green")
min_label.place(x=870, y=145)

min_entry = Entry(root, width=3, bg="#ffff99",state=DISABLED)
min_entry.get()
min_entry.place(x=950, y=143)

# Max Length

max_label = Label(root, text="Max Length:", fg="green")
max_label.place(x=870, y=172)

max_entry = Entry(root, width=3, bg="#ffff99",state=DISABLED)
max_entry.get()
max_entry.place(x=950, y=173)


# Prefix

prefix = Entry(root, width=15, bg="#ffff99")
prefix.get()
prefix.place(x=680, y=320)

Prefix_Label = Label(root, text="Prefix:", fg="green")
Prefix_Label.place(x=630, y=320)

# Suffix

suffix = Entry(root, width=15, bg="#ffff99")
suffix.get()
suffix.place(x=680, y=350)

Suffix_Label = Label(root, text="Suffix:", fg="green")
Suffix_Label.place(x=630, y=350)

# Number Frame

number_frame = LabelFrame(root, text="Numbers",
                          padx=80, pady=60, borderwidth=6)
number_frame.place(x=875, y=300)

Dummy_number_frame = Label(number_frame, text="",)
Dummy_number_frame.grid(row=0, column=0)

# From Starting

from_label = Label(root, text="From:", fg="green")
from_label.place(x=890, y=342)

from_entry = Entry(root, width=12, bg="#ffff99",state=DISABLED)
from_entry.get()
from_entry.place(x=930, y=345)

# To Numbers

to_label = Label(root, text="To:", fg="green")
to_label.place(x=890, y=372)

to_entry = Entry(root, width=12, bg="#ffff99",state=DISABLED)
to_entry.get()
to_entry.place(x=930, y=373)

# Step

step_label = Label(root, text="Step:", fg="green")
step_label.place(x=890, y=402)

step_entry = Entry(root, width=12, bg="#ffff99",state=DISABLED)
step_entry.get()
step_entry.place(x=930, y=402)

# Url Encode CheckBox

chk = Checkbutton(root, text="URL Encode characters?",
                  variable=uen, onvalue="url_encode", offvalue="not_encode")
chk.deselect()
chk.place(x=630, y=390)

# Choose File
choose_file = Button(root, text="Choose Wordlist", command=choosefile,
                     borderwidth=2, bg="#ff751a", fg="white", activebackground='#ff751a', height=1)
choose_file.place(x=665, y=420)

# Combo Box for Selecting Payloads

Payloads = [
    "Wordlist",
    "Numbers",
    "BruteForce"
]

# ComboBox

combo_box1 = ttk.Combobox(root, values=Payloads)
combo_box1.current(0)
combo_box1['state'] = 'readonly'
combo_box1.bind("<<ComboboxSelected>>", comboclk)
combo_box1.pack(fill='none', expand='False')
combo_box1.place(x=742, y=53, height=20, width=95)

Label_Select_Payload = Label(root, text="Select Payload Type", fg="green")
Label_Select_Payload.place(x=600, y=53)

# Combo Box for Selecting encoding Types

Encodings = [
    "None",
    "Base64",
    "Hex",
    "ASCII Numbers"
]

# ComboBox 2

combo_box2 = ttk.Combobox(root, values=Encodings)
combo_box2.current(0)
combo_box2['state'] = 'readonly'
combo_box2.bind("<<ComboboxSelected>>")
combo_box2.pack(fill='none', expand='False')
combo_box2.place(x=840, y=250, height=20, width=118)

Label_Select_Encoding = Label(root, text="Select Encoding Type", fg="green")
Label_Select_Encoding.place(x=690, y=250)

opt1= IntVar()
opt1.set(1)
Radiobutton(root,text="Suffix/Prefix --> Encode",variable=opt1,value=1).place(x=600,y=495)
Radiobutton(root,text="Encode --> Suffix/Prefix",variable=opt1,value=2).place(x=600,y=520)

start_attack_button = Button(root,text="Start Attack",bg="#ff751a",activebackground="#ff751a",command=start_attack)
start_attack_button.place(x=960,y=550)

mainloop()
