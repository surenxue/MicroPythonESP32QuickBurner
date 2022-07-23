import tkinter as tk
from tkinter import ttk
import serial.tools.list_ports
import json
import icon
# import espProsess
import espTest
import os

root = tk.Tk()
root.title("选择镜像烧录")

global_options = {
    "port_discribe_list" : [],
    "temp_ports_list": [],
    "last_port"      : 0,
    "skin_mode"      : "Classic",
    "selected_bin"   : None,
    "status_line"    : "",
    "Bin_list"       : None,
    "ChipType"       : "ESP32"
}



def gridWidgets():
    frameTree.pack(padx=10)
    frameLower.pack(padx=10)
    framePort.grid(row=0, column=0)
    sb.pack(side=tk.RIGHT,fill=tk.Y)
    sb1.pack(side=tk.BOTTOM,fill=tk.X)
    tree.pack(padx=0, pady=0)
    NowBin.pack(pady=5, anchor=tk.W)
    comboPort.grid(row=0, column=0)
    BurnButton.grid(row=1, column=1)
    frameChip.grid(row=0, column=1)
    NowState.pack(pady=5, anchor=tk.W)
    strChosen.pack()

def init_funcs():
    """启动时运行的动作"""
    fresh_files()
    load_config()
    NowBin.configure(text=f"当前选择: {global_options['selected_bin']}")

def fresh_files():
    """刷新目录下的文件"""
    tree.delete(0, tk.END)
    for i in os.listdir():
        if os.path.isfile(i) and i.endswith(".bin"):
            tree.insert(tk.END, i)
    global_options["Bin_list"] = list(tree.get(0, tk.END))

def fresh_ports():
    """选择一个端口"""
    ports = []
    global_options["temp_ports_list"].clear()
    for i in serial.tools.list_ports.comports():
        ports.append(i.description)
        global_options["temp_ports_list"].append(i.name)
    comboPort['values'] = ports
    global_options["port_discribe_list"] = ports

class redirect:
    """将烧录的输出信息重定向到用户界面底部"""
    def write(self, string:str):
        if string == -1:
            BurnButton.config(state="normal")
        elif string == 1:
            BurnButton.config(state="disabled")
            global_options["status_line"] = ""
            NowState.configure(text=global_options["status_line"])
        else:
            global_options["status_line"] += string
            lines = global_options["status_line"].split("\n")
            temp_lines = []
            for i in lines:
                if i:
                    temp_lines.append(i)
            if len(temp_lines) > 4:
                global_options["status_line"] = temp_lines[-4]+"\n"+\
                    temp_lines[-3]+"\n"+temp_lines[-2]+"\n"+temp_lines[-1]
            NowState.configure(text=global_options["status_line"])
    def flush(*args):
        pass
    def isatty(*args):
        pass

def burn_file():
    """烧录文件"""
    file_name = global_options["selected_bin"]
    if file_name is not None and comboPort.current() != -1:
        global_options["last_port"] = comboPort.current()
        port = global_options["temp_ports_list"][comboPort.current()]
        # print(file_name, port)
        r = redirect()
        if global_options["ChipType"] == "ESP32":
            start = '0x1000'
        else:
            start = '0x0000'
        espTest.erase_flash(port, stdout=r)
        espTest.write_flash(port, file_name, stdout=r, start=start)
    save_config()

def set_Bin(*args):
    try:
        file_name = tree.get(0, tk.END)[tree.curselection()[0]]
    except Exception as e:
        file_name = None
    NowBin.configure(text=f"当前选择: {file_name}")
    global_options["selected_bin"] = file_name

def load_config():
    try:
        with open("config.json", 'r') as js_file:
            temp_options = json.load(js_file)
    except BaseException as e:
        with open("config.json", 'w') as js_file:
            js_string = json.dumps(global_options, sort_keys=True, indent=4, separators=(',', ': '))
            js_file.write(js_string)
            temp_options = global_options
    fresh_ports()
    if temp_options["temp_ports_list"] == global_options["temp_ports_list"]:
        if temp_options["temp_ports_list"]:
            comboPort.set(global_options["port_discribe_list"][temp_options["last_port"]])
    if temp_options["Bin_list"] == global_options["Bin_list"]:
        global_options['selected_bin'] = temp_options["selected_bin"]
        NowBin.configure(text=f"当前选择: {global_options['selected_bin']}")
    
    try:
        for k, i in enumerate(strChosen['values']):
            if i == temp_options['ChipType']:
                strChosen.current(k)
                global_options["ChipType"] = i
    except:
        pass

def save_config():
    with open("config.json", 'w') as js_file:
        js_string = json.dumps(global_options, sort_keys=True, indent=4, separators=(',', ': '))
        js_file.write(js_string)

def get_icon():
    if os.path.exists("temp.ico"):
        root.iconbitmap("temp.ico")
    else:
        root.iconbitmap(icon.write_icon())

def setChipType(*args):
    global global_options
    global_options["ChipType"]=chipTypeTkVar.get()
        
frameTree = tk.LabelFrame(root,text="选择镜像文件")
NowBin    = tk.Label(frameTree, text="当前选择:")
sb = tk.Scrollbar(frameTree)
sb1 = tk.Scrollbar(frameTree, orient=tk.HORIZONTAL)
tree = tk.Listbox(frameTree, width=30, 
    xscrollcommand=sb1.set,
    yscrollcommand=sb.set, )
tree.bind('<Button-1>', set_Bin)
sb.config(command=tree.yview)
sb1.config(command=tree.xview)
frameLower = tk.Frame(root)
framePort = tk.LabelFrame(frameLower,text="选择端口")
frameChip = tk.LabelFrame(frameLower,text="芯片型号")
portIndex = tk.StringVar()
comboPort = ttk.Combobox(framePort, width=20, textvariable=portIndex, 
                state='readonly', postcommand=fresh_ports)

comboPort['values'] = []
BurnButton = ttk.Button(frameLower, width=8, text="烧录", command=burn_file)
NowState   = tk.Label(root, text="欢迎使用")

# 信号发送方式列表
chipTypeTkVar = tk.StringVar()
strChosen = ttk.Combobox(frameChip, width=10, textvariable=chipTypeTkVar, state='readonly')
strChosen['values'] = ["ESP32", "ESP32C3",'ESP32S2', "ESP32S3", "ESP8266"]  # 设置下拉列表的值
strChosen.current(0)
strChosen.bind('<<ComboboxSelected>>', setChipType)



def main():
    get_icon()
    init_funcs()
    gridWidgets()
    root.mainloop()

if __name__ == "__main__":
    main()