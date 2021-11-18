#!/bin/python3
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar, Scrollbar
from tkinter.filedialog import asksaveasfile
from concurrent.futures import ThreadPoolExecutor
from json import dumps
from sys import path
import requests
from urllib.parse import quote
from base64 import b64encode
from binascii import hexlify
from requests.api import head
from itertools import product
from os import remove
path.insert(1,"/opt/PyIntruder")
from ShowJson import *
root = Tk()
root.title("PyIntruder")
root.geometry("1100x650")
root.minsize(1100, 650)
root.maxsize(1100, 650)
img = PhotoImage(file='/opt/PyIntruder/PyI.png')
root.tk.call('wm', 'iconphoto', root._w, img)

# Exception classes


class Unknown_request(Exception):
    pass


class greater_zero(Exception):
    pass


class no_position(Exception):
    pass


class no_wordlist(Exception):
    pass


# Main Variables
var_url = ""
var_data = ""
var_headers = {}
var_req_method = ""
var_from_numbers = 0
var_to_numbers = 0
var_step_numbers = 1
var_min_length = 1
var_max_length = 1
var_bruteforce_charset = ""
root_filename = ""
button_place = ''
payload_list = ""
loading_bar = ""
second_frame = ""
uen = StringVar()
urlencode_var = ""
percent_increase = 0
h = 0
count=0
encoding_var = ""
option_var = ""
prefix_var = ""
suffix_var = ""
listbox = ""
searchbox = ""
response_headers=""
maindict = {}
#HTTP Status Codes
StatusCodes={"100":"CONTINUE","101":"SWITCHING_PROTOCOLS","200":"OK","201":"CREATED","202":"ACCEPTED","203":"NON_AUTHORITATIVE_INFORMATION","204":"NO_CONTENT","205":"RESET_CONTENT","206":"PARTIAL_CONTENT","207":"MULTI_STATUS","208":"ALREADY_REPORTED","226":"IM_USED","300":"MULTIPLE_CHOICES","301":"MOVED_PERMANENTLY","302":"FOUND","303":"SEE_OTHER","304":"NOT_MODIFIED","305":"USE_PROXY","306":"RESERVED","307":"TEMPORARY_REDIRECT","308":"PERMANENT_REDIRECT","400":"BAD_REQUEST","401":"UNAUTHORIZED","402":"PAYMENT_REQUIRED","403":"FORBIDDEN","404":"NOT_FOUND","405":"METHOD_NOT_ALLOWED","406":"NOT_ACCEPTABLE","407":"PROXY_AUTHENTICATION_REQUIRED","408":"REQUEST_TIMEOUT","409":"CONFLICT","410":"GONE","411":"LENGTH_REQUIRED","412":"PRECONDITION_FAILED","413":"REQUEST_ENTITY_TOO_LARGE","414":"REQUEST_URI_TOO_LONG","415":"UNSUPPORTED_MEDIA_TYPE","416":"REQUESTED_RANGE_NOT_SATISFIAB","417":"EXPECTATION_FAILED","418":"IM_A_TEAPOT","422":"UNPROCESSABLE_ENTITY","423":"LOCKED","424":"FAILED_DEPENDENCY","426":"UPGRADE_REQUIRED","428":"PRECONDITION_REQUIRED","429":"TOO_MANY_REQUESTS","431":"REQUEST_HEADER_FIELDS_TOO_LARGE","451":"UNAVAILABLE_FOR_LEGAL_REASONS","500":"INTERNAL_SERVER_ERROR","501":"NOT_IMPLEMENTED","502":"BAD_GATEWAY","503":"SERVICE_UNAVAILABLE","504":"GATEWAY_TIMEOUT","505":"VERSION_NOT_SUPPORTED","506":"VARIANT_ALSO_NEGOTIATES","507":"INSUFFICIENT_STORAGE","508":"LOOP_DETECTED","509":"BANDWIDTH_LIMIT_EXCEEDED","510":"NOT_EXTENDED","511":"NETWORK_AUTHENTICATION_REQUIRED"}

#Function to Update data while searching
def update(data):
    global listbox, maindict
    listbox.delete(0, END)
    for m in data:
        to_insert=m+" "*(97-len(m)) + str(maindict[m][0]) + " "*(40-len(str(maindict[m][0]))) + str(maindict[m][1])
        listbox.insert(END, to_insert)

#Search When Typed Something in searchbox
def search(event):
    global searchbox, maindict
    typed_text = searchbox.get()
    data_find = []
    if typed_text == "":
        data_find = [l for l in maindict]

    else:
        for l in maindict:
            if typed_text.lower() in maindict[l][2].lower():
                data_find.append(l)

    update(data_find)

#Function to show response
def show_data(event):
    global maindict, listbox,response_headers
    payload = listbox.get(ANCHOR)
    payload = payload[7:20].strip()
    dta = maindict[payload][2]
    x = Toplevel()
    x.geometry("900x600")
    x.title("Response")
    textbox = ScrolledText(x, wrap=WORD, height=34, width=120, fg='#660066')
    textbox.pack()
    for i in response_headers:
        to_insert=i+" : "+response_headers[i]+"\n"
        textbox.insert(INSERT,to_insert)
    textbox.insert(INSERT, "\n"+dta)
    textbox.config(state=DISABLED)
    x.minsize(900, 500)
    x.maxsize(900, 600)

#Function To Save Data
def save():
    global maindict
    file_name = filedialog.asksaveasfile(initialfile="save.json",defaultextension=".json",filetypes=[("json file","*.json")])
    try:
        file_name.write(dumps(maindict))
    except PermissionError:
        messagebox.showwarning("Warning", "Permission Denied")
    file_name.close()

def req_get(list_payload):
    #Windows
    global button_place, root,count
    #Request Material
    global var_url, var_headers, var_data, var_req_method,maindict
    #Encodings
    global urlencode_var,encoding_var
    global option_var, listbox,StatusCodes,prefix_var, suffix_var, percent_increase, loading_bar, second_frame, payload_list, h,response_headers
    tempvar = payload_list.index(list_payload)
    list_payload = str(list_payload)
    list_payload=list_payload.replace("\n",'')
    list_payload=list_payload
    tempvariable = list_payload
    #Suffix/Prefix --> Encode
    if option_var == 1:
        list_payload = prefix_var+list_payload+suffix_var
        tempvariable = list_payload
        if encoding_var == "Base64":
            list_payload = b64encode(list_payload.encode()).decode()

        elif encoding_var == "Hex":
            list_payload = hexlify(list_payload.encode()).decode()

        elif encoding_var == "ASCII Numbers":
            list_payload = ''.join(str(ord(c)) for c in list_payload)
    #Encode -->Suffix/Prefix1
    elif option_var == 2:
        if encoding_var == "Base64":
            list_payload = b64encode(list_payload.encode()).decode()

        elif encoding_var == "Hex":
            list_payload = hexlify(list_payload.encode()).decode()

        elif encoding_var == "ASCII Numbers":
            list_payload = ''.join(str(ord(c)) for c in list_payload)

        list_payload = prefix_var+list_payload+suffix_var
    #@@@@@@ is sign of Position Of Payload
    reqdata = var_data.replace("@@@@@@", list_payload)
    if urlencode_var == "url_encode":
        reqdata = quote(reqdata, safe='')
    #Creating Copy Of Header to preserve position
    var_headers_temp = var_headers.copy()
    for i in var_headers_temp:
        var_headers_temp[i] = var_headers_temp[i].replace("@@@@@@", list_payload)

    var_url1=var_url.replace("@@@@@@",list_payload)
    if var_req_method == "GET":
        r = requests.get(var_url1, params=reqdata, headers=var_headers_temp)

    elif var_req_method == "POST":
        r = requests.post(var_url1, data=reqdata, headers=var_headers_temp)
    #Adding Data To Our Dictionary
    maindict[list_payload] = [str(len(r.text)),str(r.status_code)+" "+StatusCodes[str(r.status_code)],r.text]
    response_headers = r.headers
    #Add Data In ListBox
    count+=1
    txt = str(count)+" "*10+tempvariable+" "*(84-len(list_payload)-len(str(count))-len(StatusCodes[str(r.status_code)])) + str(len(r.text)) + " "*(40-len(str(len(r.text)))) + str(r.status_code)+" "+StatusCodes[str(r.status_code)]
    listbox.insert(END, txt)
    #Updating Progressbar
    h += percent_increase
    loading_bar["value"] = h
    root.update_idletasks()

#Extracting Headers/Url/Data From Given Request
def extractrequest(web_request):
    g = open("temp.txt", 'w+')
    g.write(web_request)
    g.close()
    f = open("temp.txt", "r")
    listdata1 = f.readlines()
    listdata = []
    #Removing Blank Lines
    for i in listdata1:
        tv = str(i).replace("\n", "")
        if tv != "":
            listdata.append(tv)

    req_type = listdata[0]
    host = listdata[1]
    headerslist = {}
    #Extracting Headers and data
    if "POST" in req_type:
        req_method = "POST"
        fullurl = req_type[4:-9]
        data = listdata[-1]
        for i in range(2, len(listdata)-2):
            spoint = listdata[i].find(":")
            headerslist[listdata[i][:spoint]
                        ] = listdata[i][spoint+2:].rstrip("\n")

    elif "GET" in req_type:
        req_method = "GET"
        getfind = req_type.find("?")
        if getfind == -1:
            fullurl = req_type[3:-9]

        else:
            fullurl = req_type[3:getfind]

        data = req_type[getfind+1:-9]
        for i in range(2, len(listdata)-1):
            spoint = listdata[i].find(":")
            headerslist[listdata[i][:spoint]
                        ] = listdata[i][spoint+2:].rstrip("\n")

    else:
        try:
            raise Unknown_request

        except Unknown_request:
            messagebox.showwarning("Warning", "Unable To Detect Request Type")
            return

    f.close()
    #Deleting File 
    remove("temp.txt")
    url = "http://"+host[5:].strip()+fullurl.strip()
    headerslist.pop("", None)
    return req_method, url, headerslist, data


def mainattack():
    #Window
    global button_place
    #Requests Material
    global var_url,var_headers,var_data,var_req_method
    #Encodings
    global urlencode_var,encoding_var
    #Others
    global option_var, listbox, searchbox,prefix_var, suffix_var, loading_bar, second_frame, h
    main_request = Request_Text_Area.get("1.0", END)
    #Getting Data From extractrequest function
    var_req_method, var_url, var_headers, var_data = extractrequest(main_request)
    #Replacing Added Position With @@@@@@ To Replace with payload Easily
    #Headers
    for temp_replace in var_headers:
        temp_var = var_headers[temp_replace]
        if "§" in temp_var:
            position1 = temp_var.find("§", 0)
            position2 = temp_var.find("§", position1+1)
            position2 = position2 + 1
            temp_var = temp_var.replace(
                temp_var[position1:position2], "@@@@@@")
            var_headers[temp_replace] = temp_var
    #Get/Post Data
    for i in range(10):
        if "§" in var_data:
            position1 = var_data.find("§", 0)
            position2 = var_data.find("§", position1+1)
            position2 = position2 + 1
            var_data = var_data.replace(
                var_data[position1:position2], "@@@@@@")
    #URL
    for i in range(3):
        if  "§" in var_url:
            positiona1 = var_url.find("§", 0)
            positiona2 = var_url.find("§", positiona1+1)
            positiona2 = positiona2 + 1
            var_url = var_url.replace(
                var_url[positiona1:positiona2], "@@@@@@")
        else:
            break

    attack_type = combo_box1.get()
    urlencode_var = uen.get()
    encoding_var = combo_box2.get()
    option_var = opt1.get()
    prefix_var = prefix.get()
    suffix_var = suffix.get()
    #Creating pop up Window To Show Response 
    button_place = Toplevel()
    button_place.geometry("700x700")
    button_place.title("Attack Box")
    button_place.minsize(700, 700)
    button_place.maxsize(700, 700)
    Label(button_place, text="Attacking").pack()
    #Adding LoadingBar
    loading_bar = Progressbar(button_place, orient=HORIZONTAL, length=400, mode="determinate")
    loading_bar.pack()
    Label(button_place, text="No."+" "*10 + "Payload" + " "*70 + "Length"+" "*40 + "Status Code", borderwidth=2, relief=SOLID).pack(side=TOP, anchor="w")
    main_frame = Frame(button_place)
    #Adding ScrollBar To It
    my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL)
    main_frame.pack(fill=BOTH, expand=1)
    #Adding ListBox
    listbox = Listbox(main_frame, width=80, height=33, yscrollcommand=my_scrollbar.set)
    my_scrollbar.config(command=listbox.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    listbox.bind("<Double-1>", show_data)
    #Adding SearchBox
    searchbox = Entry(button_place, width=45)
    listbox.pack()
    Label(button_place, text="Search :", fg="green").place(x=210, y=667)
    searchbox.place(x=280, y=665)
    searchbox.bind("<KeyRelease>", search)  
    #Adding Save As Button
    Button(button_place,text="Save as",command=save).place(x=10,y=5)

    global payload_list
    if attack_type == "Numbers":
        global var_from_numbers
        global var_to_numbers
        global var_step_numbers
        global percent_increase
        payload_list = [x for x in range(var_from_numbers, var_to_numbers+1, var_step_numbers)]
        percent_increase = 100 / len([x for x in range(var_from_numbers, var_to_numbers+1, var_step_numbers)])
        h = 0
        #Running Attack with Threads
        execute = ThreadPoolExecutor(max_workers=Threads_Button.get())
        execute.map(req_get, [x for x in range(var_from_numbers, var_to_numbers+1, var_step_numbers)])
        execute.shutdown(wait=False)

    elif attack_type == "Wordlist":
        global root_filename
        f1 = open(root_filename, "r",errors="ignore")
        pay = f1.readlines()
        payload_list = pay
        #for i in pay:
            #payload_list.append(i.rstrip("\n"))
        percent_increase = 100/len(payload_list)
        h = 0
        execute = ThreadPoolExecutor(max_workers=Threads_Button.get())
        execute.map(req_get, payload_list)
        execute.shutdown(wait=False)

    elif attack_type == "BruteForce":
        global var_bruteforce_charset, var_max_length, var_min_length
        payload_list = []
        for x in range(var_min_length, var_max_length+1):
            for y in product(var_bruteforce_charset, repeat=x):
                payload_list.append("".join(y))

        percent_increase = 100/len(payload_list)
        h = 0
        execute = ThreadPoolExecutor(max_workers=Threads_Button.get())
        execute.map(req_get, payload_list)
        execute.shutdown(wait=False)


def start_attack():
    global var_from_numbers,var_to_numbers,var_step_numbers
    global var_min_length,var_max_length
    global var_bruteforce_charset,count
    count=0
    attack_type = combo_box1.get()
    attack_threads = Threads_Button.get()
    if attack_type == "Numbers":
        try:
            var_from_numbers = int(from_entry.get())
            var_to_numbers = int(to_entry.get())
            var_step_numbers = int(step_entry.get())
            if var_to_numbers < var_from_numbers:
                if var_step_numbers > 0:
                    var_step_numbers=-var_step_numbers
            if var_step_numbers == 0:
                raise greater_zero
                
            if "§" not in Request_Text_Area.get("1.0", END):
                raise no_position
            mainattack()

        except ValueError:
            messagebox.showwarning("Warning", "Please enter numbers only")
            return
        except greater_zero:
            messagebox.showwarning("Warning", "Please enter step greater than zero")
        except no_position:
            messagebox.showwarning("Warning", "Please Add Position in Box")

    elif attack_type == "BruteForce":

        try:
            var_min_length = int(min_entry.get())
            var_max_length = int(max_entry.get())
            var_bruteforce_charset = charset.get()
            if var_min_length < 1 or var_max_length < 1:
                raise greater_zero

            if "§" not in Request_Text_Area.get("1.0", END):
                raise no_position

            mainattack()

        except ValueError:
            messagebox.showwarning("Warning", "Please enter numbers")
            return

        except greater_zero:
            messagebox.showwarning("Warning", "Enter Number Greater Than Zero")
            return

        except no_position:
            messagebox.showwarning("Warning", "Please Add Position in Box")

    else:
        
        try:
            a = root_filename
            if "§" not in Request_Text_Area.get("1.0", END):
                raise no_position

            if "/" not in a:
                raise no_wordlist

            mainattack()

        except no_position:
            messagebox.showwarning("Warning", "Please Add Position in Box")

        except no_wordlist:
            messagebox.showwarning("Warning", "Please Specify Wordlist")


def add_position():
    try:
        if Request_Text_Area.selection_get():
        # Replacing Before and After With Unicode Character
            Request_Text_Area.insert("sel.first", "§")
            Request_Text_Area.insert("sel.last", "§")
            temp = Request_Text_Area.get("1.0", END)
            Request_Text_Area.delete(1.0, END)
            Request_Text_Area.insert(1.0, temp.replace("§§", '§')[:-1])

    except:
        messagebox.showwarning("Warning", "Nothing is selected")


def clear_position():
    temp = Request_Text_Area.get("1.0", END)
    Request_Text_Area.delete(1.0, END)
    Request_Text_Area.insert(1.0, temp.replace("§", '')[:-1])

# Function for Paste button


def paste():
    pst = Request_Text_Area.index(INSERT)
    try:
        clip = root.clipboard_get()
        Request_Text_Area.insert(pst, clip)

    except:
        messagebox.showwarning("Warning", "Nothing is in the clipboard")

# Function for Clear button

def clear():
    Request_Text_Area.delete(1.0, END)

# Function for choosing file button

def choosefile():
    global root_filename
    root_filename = filedialog.askopenfilename(initialdir="~/", title="Select a file", filetypes=(("Text files", "*.txt"), ("All files*", "*")))
    file_label = Label(root, text=root_filename, width=40, fg="red")
    file_label.place(x=580, y=465)

# Function for Combo-Box for Payloads

def comboclk(event):
    # Recieve Value From Drop Down List
    attack_type = combo_box1.get()

    # Disabling Each Parameter

    choose_file.config(state=DISABLED)
    min_entry.config(state=DISABLED)
    max_entry.config(state=DISABLED)

    charset.config(state=DISABLED)
    from_entry.config(state=DISABLED)

    to_entry.config(state=DISABLED)
    step_entry.config(state=DISABLED)

    if attack_type == "Wordlist":
        choose_file.config(state=NORMAL)

    if attack_type == "BruteForce":
        min_entry.config(state=NORMAL)
        max_entry.config(state=NORMAL)
        charset.config(state=NORMAL)

    if attack_type == "Numbers":
        from_entry.config(state=NORMAL)
        to_entry.config(state=NORMAL)
        step_entry.config(state=NORMAL)

# Function for Help menu item

def info():
    msg = '''About PyIntruder  

This tool will help you to
send your requests faster
than ever you've used.More
features will be added in
the future.This is
absolutely free of cost. 
    
    Developed by:
        Yash Bansal
        Sagnik Haldar
        Also... 0day Was Here'''
    messagebox.showinfo(title='Details', message=msg)


def usage():
    msg = "Please Refer To https://github.com/Yash114Bansal/PyIntruder"
    help_window = Toplevel()
    help_lbl = Label(help_window, text=msg)
    help_lbl.pack()


menu_button = Menu(root)
root.config(menu=menu_button)

# Help menu item
help_menu = Menu(menu_button, tearoff="off")
menu_button.add_cascade(label="Menu", menu=help_menu)
help_menu.add_command(label="Usage", command=usage)
help_menu.add_command(label="About Me", command=info)
help_menu.add_command(label="Show JSON", command=showdatamain)


# Requests LabelFrame
frame_requests = LabelFrame(root, text="Requests",
                            padx=260, pady=640, borderwidth=6)
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
Options_Frame = LabelFrame(
    root, text="Options", padx=260, pady=640, borderwidth=6)
Options_Frame.pack(padx=10, pady=10, side=RIGHT)
Dummy_Options_Frame = Label(Options_Frame, text="",)
Dummy_Options_Frame.grid(row=0, column=0)

# Select Threads Button
Threads_Button = Scale(root, from_=1, to=100, orient=HORIZONTAL)
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
                             borderwidth=2, bg="#ff751a", activebackground='#ff751a', height=1, command=add_position)
button_add_position.place(x=625, y=120)
button_clear_position = Button(root, text="Clear Position",
                               borderwidth=2, bg="#ff751a", activebackground='#ff751a', height=1, command=clear_position)
button_clear_position.place(x=625, y=160)

# BruteForce Frame

bruteforce_frame = LabelFrame(
    root, text="BruteForce", padx=130, pady=35, borderwidth=6)
bruteforce_frame.place(x=790, y=95)
label_BruteForce = Label(bruteforce_frame, text="",)
label_BruteForce.grid(row=0, column=0)

# BruteForce Charset

charset = Entry(root, width=30, bg="#ffff99", fg="green", state=DISABLED)
charset.get()
charset.place(x=805, y=120)
charset.insert(0, "Enter The Charset")

# Min Length

min_label = Label(root, text="Min Length:", fg="green")
min_label.place(x=870, y=145)

min_entry = Entry(root, width=3, bg="#ffff99", state=DISABLED)
min_entry.get()
min_entry.place(x=950, y=143)

# Max Length

max_label = Label(root, text="Max Length:", fg="green")
max_label.place(x=870, y=172)

max_entry = Entry(root, width=3, bg="#ffff99", state=DISABLED)
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

from_entry = Entry(root, width=12, bg="#ffff99", state=DISABLED)
from_entry.get()
from_entry.place(x=930, y=345)

# To Numbers

to_label = Label(root, text="To:", fg="green")
to_label.place(x=890, y=372)

to_entry = Entry(root, width=12, bg="#ffff99", state=DISABLED)
to_entry.get()
to_entry.place(x=930, y=373)

# Step

step_label = Label(root, text="Step:", fg="green")
step_label.place(x=890, y=402)

step_entry = Entry(root, width=12, bg="#ffff99", state=DISABLED)
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

opt1 = IntVar()
opt1.set(1)
Radiobutton(root, text="Suffix/Prefix --> Encode",variable=opt1, value=1).place(x=600, y=495)
Radiobutton(root, text="Encode --> Suffix/Prefix",variable=opt1, value=2).place(x=600, y=520)

start_attack_button = Button(root, text="Start Attack", bg="#ff751a",activebackground="#ff751a", command=start_attack)
start_attack_button.place(x=960, y=550)

mainloop()
