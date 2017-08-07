import tkinter as tk
from tkinter import ttk
import serial # requires installing
import serial.tools.list_ports
from time import sleep, time
import threading 
from PIL import Image, ImageTk # requires installing
import logging
import queue
import os
import subprocess
from tkinter import filedialog
import sys

from pygments import lex
from pygments.lexers import PythonLexer

import blockly_window


# tkinter on scrollbar instead of loo 60ms!!!
# every single fucking tab!!!!

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s',
                    )

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def center_window(window):
    window.update_idletasks()
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    window.geometry("%dx%d+%d+%d" % (size + (x, y)))

class NotebookTab(ttk.Frame):
    def __init__(self, master, title, file):
        super().__init__(master)
        self.master = master   
        self.title = title
        self.file = file

        self.rowconfigure(0, weight=1) 
        self.columnconfigure(1, weight=1)

        self.text_area = tk.Text(self)
        self.text_area.grid(row=0, column=1, sticky="nsew")

        self.y_scrollbar = tk.Scrollbar(self)
        self.y_scrollbar.config(command=self.text_area.yview)
        self.y_scrollbar.grid(row=0, column=2, sticky="nsew")
        self.x_scrollbar = tk.Scrollbar(self)
        self.x_scrollbar.config(command=self.text_area.xview, orient=tk.HORIZONTAL)
        self.x_scrollbar.grid(row=1, column=1, sticky="nsew")

        self.line_numbers = tk.Canvas(self, width=28)
        self.line_numbers.grid(row=0, column=0, sticky="ns")

        self.text_area.config(
            # bg="black",  # background color
            # fg="green",  # default text color
            wrap=tk.NONE,  # allows lines to be infinitely long
            yscrollcommand=self.y_scrollbar.set,
            xscrollcommand=self.x_scrollbar.set,
            font="{fixedsys} 12",
            # insertbackground="white",  # cursor color
        )

        self.last_line_number = None
        self.update_line_numbers()

        self.text_area.bind("<Tab>", self._tab_event)
        # self.text_area.bind("<Shift-ISO_Left_Tab>", self._shift_tab_event)
        self.text_area.bind("<Control-a>", self._control_a_event)
        self.text_area.bind("<Control-A>", self._control_a_event)
        self.text_area.bind("<Key>", self._key_event)
        self.text_area.bind("<KeyRelease>", self._release_key)

        if file:
            with open(file, "r") as f:
                file_content = f.read()
                file_content = file_content.replace("\t", 4*" ")
            self.text_area.insert("1.0", file_content)
            self.python_lexer()

    def _set_text_tags(self):
        self.text_area.tag_config("Token.Text", foreground="black") 
        self.text_area.tag_config("Token.Error", foreground="red") 
        self.text_area.tag_config("Token.Keyword", foreground="blue") 
        self.text_area.tag_config("Token.Operator", foreground="green") 
        self.text_area.tag_config("Token.Comment", foreground="grey") 
        self.text_area.tag_config("Token.Name", foreground="black") 

    def _key_event(self, event):
        if self.text_area.edit_modified():
            self.master.tab(self.master.select(), text=self.title+" *")

    def _release_key(self, event):
        self.python_lexer()

    def python_lexer(self):
        for tag in self.text_area.tag_names():
            self.text_area.tag_delete(tag)
        self._set_text_tags()
        data = self.text_area.get("1.0", "end-1c")
        self.text_area.mark_set("range_start", "1.0")
        print("------------------")
        for token, content in lex(data, PythonLexer()):
            master_token = ".".join(str(token).split(".")[0:2])
            self.text_area.mark_set("range_end", "range_start + %dc" % len(content))
            self.text_area.tag_add(str(master_token), "range_start", "range_end")
            print(token, len(content), content.encode())
            self.text_area.mark_set("range_start", "range_end")

    def _tab_event(self, event):
        self.text_area.insert(tk.INSERT, " " * 4)
        self._key_event(event)
        return 'break'

    def _shift_tab_event(self, event):
        return 'break'

    def _control_a_event(self, event):
        self.text_area.tag_add("sel", "1.0", "end")
        return 'break'

    def update_line_numbers(self):
        line = self.text_area.index('@0,0')
        if (self.last_line_number != line) or (self.last_line_number is None):
            self.line_numbers.delete("all")

            while True:
                dline = self.text_area.dlineinfo(line)
                if dline is None:
                    break
                y = dline[1]
                linenum = str(line).split(".")[0]
                self.line_numbers.create_text(2, y, anchor="nw", text=linenum)
                line = self.text_area.index("%s+1line" % line)

            self.last_line_number = line

    def save_file(self):
        if self.file and os.path.exists(self.file):
            with open(self.file, "w") as f:
                f.write(self.text_area.get(1.0, tk.END)[:-1]) # Text.get adds \n to the end, so this must be cut with [:-1]
            self.master.tab(self.master.select(), text=self.title)
        else:
            self.file = filedialog.asksaveasfilename(initialdir = "",title = "Save File",filetypes = (("python files","*.py"),("all files","*.*")))
            with open(self.file, "w") as f:
                f.write(self.text_area.get(1.0, tk.END))
            self.title = os.path.basename(self.file)
            self.master.tab(self.master.select(), text=self.title)


class SerialSetupWindow(tk.Toplevel):
    def __init__(self, master, command):
        super().__init__(master)
        self.title("Connect to Serial Device")
        self.attributes("-topmost", True)
        self.grab_set()
        self.minsize(400, 100)
        self.columnconfigure(0, weight=1)
        self.resizable(0, 0) # disable resizing by user
        self.command = command
        self.usb_devices = None
        self.buttons = []

        center_window(self)
        self.update_serial_devices()

    def button_pressed(self, device):
        self.command(device)
        self.grab_release() # to return to normal
        self.destroy()

    def get_serial_devices(self):
        ports = list(serial.tools.list_ports.comports()) # get all serial devices
        return [dev.device for dev in ports if "USB" in dev.hwid] # return a list of their names (COMx or dev/ttyUSBx)
        # return [dev.device for dev in ports]

    def update_serial_devices(self):
        usb_devices = self.get_serial_devices()
        if usb_devices != self.usb_devices:
            self.usb_devices = usb_devices
            for button in self.buttons:
                button.grid_forget()
            self.buttons = []
            for i, device in enumerate(self.usb_devices):
                self.buttons.append(tk.Button(self, text=device, command=lambda dev=device: self.button_pressed(dev)))
                self.buttons[-1].grid(sticky="ew")

        self.after(1000, self.update_serial_devices)


class Editor(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.repl = None
        self.u_serial = None

        self.tab_close_style()  # for tab closing

        self.notebook_tabs = []
        self.notebook = ttk.Notebook(self, style="ButtonNotebook") # 'style' for tab closing
        self.notebook.pressed_index = None  # for tab closing
        self.notebook.bind("<ButtonPress-1>", self.btn_press)  # for tab closing
        self.notebook.bind("<ButtonRelease-1>", self.btn_release)  # for tab closing
        self.notebook.grid(row=0, sticky="nsew")
        self.notebook.columnconfigure(0, weight=1)
        self.notebook.rowconfigure(0, weight=1)
        self.new_tab()

        self.line_number_update_timer()

        self.repl_visible = False
        
        self.setup_device()

    def tab_close_style(self): # for tab closing
        self.i1 = tk.PhotoImage("img_close", file=resource_path(os.path.join("img", "close.gif")))
        self.i2 = tk.PhotoImage("img_closeactive",
            file=resource_path(os.path.join("img", "close_active.gif")))
        self.i3 = tk.PhotoImage("img_closepressed",
            file=resource_path(os.path.join("img", "close_pressed.gif")))

        style = ttk.Style()

        style.element_create("close", "image", "img_close",
            ("active", "pressed", "!disabled", "img_closepressed"),
            ("active", "!disabled", "img_closeactive"), border=8, sticky='')

        style.layout("ButtonNotebook", [("ButtonNotebook.client", {"sticky": "nswe"})])
        style.layout("ButtonNotebook.Tab", [
            ("ButtonNotebook.tab", {"sticky": "nswe", "children":
                [("ButtonNotebook.padding", {"side": "top", "sticky": "nswe",
                                             "children":
                    [("ButtonNotebook.focus", {"side": "top", "sticky": "nswe",
                                               "children":
                        [("ButtonNotebook.label", {"side": "left", "sticky": ''}),
                         ("ButtonNotebook.close", {"side": "left", "sticky": ''})]
                    })]
                })]
            })]
        )

    def btn_release(self, event):  # for tab closing
        x, y, widget = event.x, event.y, event.widget

        if not widget.instate(['pressed']):
            return



        elem =  widget.identify(x, y)
        index = widget.index("@%d,%d" % (x, y))

        if "close" in elem and widget.pressed_index == index:
            widget.forget(index)
            widget.event_generate("<<NotebookClosedTab>>")

        widget.state(["!pressed"])
        self.notebook_tabs.pop(widget.pressed_index)
        widget.pressed_index = None
        if len(self.notebook_tabs) == 0:
            self.new_tab()

    def btn_press(self, event):  # for tab closing
        x, y, widget = event.x, event.y, event.widget
        elem = widget.identify(x, y)
        index = widget.index("@%d,%d" % (x, y))

        if "close" in elem:
            widget.state(['pressed'])
            widget.pressed_index = index

    def setup_device(self):
        SerialSetupWindow(self, self.connect)

    def blockly(self):
        blockly_window.BlocklyThread(self.blockly_run)

    def blockly_run(self, code):
        print("=== Blockly Code: ===\n{}\n=== END ===".format(code))
        self.u_serial.run("print('sadasdasd')\n".encode())
        self.u_serial.run(code.encode())

    def connect(self, device):
        if self.repl:
            self.repl.disconnect()
        if self.u_serial:
            self.u_serial.close()
        self.u_serial = uSerial(device)
        self.repl = Repl(self, self.u_serial)
        self.toggle_repl(True) # set REPL to visible
        self.master.update_title(device)
        self.master.bottom_status_bar.change_status(device)
        self.master.tool_bar.update_device_image(alert=False)
        self.master.root.lift() # After connecting to a device, ensure the Editor is on the top

    def line_number_update_timer(self):
        self.selected_tab_object().update_line_numbers()
        self.master.after(60, self.line_number_update_timer)

    def _add_tab(self, title, file):
        new_tab = NotebookTab(self.notebook, title, file)
        self.notebook_tabs.append(new_tab)
        self.notebook.add(new_tab, text=title)
        self.notebook.select(new_tab)

    def selected_tab_index(self):
        return self.notebook.index(self.notebook.select())

    def selected_tab_object(self):
        return self.notebook_tabs[self.selected_tab_index()]

    def run_tab(self):
        self.set_repl_visible()
        if self.u_serial:
            self.u_serial.run(self.selected_tab_object().text_area.get(1.0, tk.END).encode())

    def new_tab(self, title="untitled", file=None):
        if len(self.notebook_tabs) < 10:
            self._add_tab(title, file)

    def toggle_repl(self, visibility=None):
        if not self.repl:
            return
        
        if visibility is None:    
            if self.repl_visible:
                self.set_repl_invisible()
            else:
                self.set_repl_visible()
        elif visibility:
            self.set_repl_visible()
        else:
            self.set_repl_invisible()

    def set_repl_visible(self):
        if not self.repl:
            return

        self.repl_visible = True
        self.repl.grid(row=1, sticky="we")

    def set_repl_invisible(self):
        if not self.repl:
            return
        
        self.repl_visible = False
        self.repl.grid_remove()

    def save_file(self):
        self.selected_tab_object().save_file()

    def load_file(self):
        file_path = filedialog.askopenfilename(initialdir = "",title = "Load file",filetypes = (("python files","*.py"),("all files","*.*")))
        if os.path.exists(file_path):
            self.new_tab(file=file_path, title=os.path.basename(file_path))


class FileManager(tk.Frame):
    def __init__(self, master, u_serial):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.t = tk.Text(self)
        self.t.grid(row=0, sticky="nsew")


class Repl(tk.Frame):
    def __init__(self, master, u_serial):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.repl_text_field = tk.Text(self)
        self.repl_text_field.grid(row=0, column=0, sticky="ew")
        self.repl_scrollbar = tk.Scrollbar(self)
        self.repl_scrollbar.grid(row=0, column=1, sticky="ns")
        self.repl_scrollbar.config(command=self.repl_text_field.yview)
        self.repl_stop = self.repl_text_field.index("end")
        self.send_queue = queue.Queue()

        self.repl_text_field.config(
            height=15,
            yscrollcommand=self.repl_scrollbar.set,
            # background="black",
            # foreground="yellow",
            # insertbackground="white",  # cursor color
        )


        self.repl_text_field.bind("<Key>", self._key_event)
        self.repl_text_field.bind("<Control-a>", self._ctrl_a_event)
        self.repl_text_field.bind("<Control-A>", self._ctrl_a_event)
        self.repl_text_field.bind("<Control-b>", self._ctrl_b_event)
        self.repl_text_field.bind("<Control-B>", self._ctrl_b_event)
        self.repl_text_field.bind("<Control-c>", self._ctrl_c_event)
        self.repl_text_field.bind("<Control-C>", self._ctrl_c_event)
        self.repl_text_field.bind("<Control-d>", self._ctrl_d_event)
        self.repl_text_field.bind("<Control-D>", self._ctrl_d_event)
        self.repl_text_field.bind("<Control-e>", self._ctrl_e_event)
        self.repl_text_field.bind("<Control-E>", self._ctrl_e_event)

        self.serial_thread = SerialThread(self, u_serial)

    def _key_event(self, event):
        if event.keysym == "Left" and self.repl_text_field.compare(self.repl_text_field.index(tk.INSERT), '==', self.repl_stop):
            return "break"
        if event.keysym == "BackSpace" and self.repl_text_field.compare(self.repl_text_field.index(tk.INSERT), '==', self.repl_stop):
            return "break"
        if event.keysym == "Up":
            return "break"
        if self.repl_text_field.compare(self.repl_text_field.index(tk.INSERT), '<', self.repl_stop):
            self.repl_text_field.mark_set("insert", self.repl_stop)
            return "break"
        if event.keysym == "Tab":
            self.repl_text_field.insert(tk.INSERT, " " * 4)
            return 'break'
        if event.keysym == "Return":
            to_send = self.repl_text_field.get(self.repl_stop, tk.END).rstrip()
            to_send += "\r"
            to_send = to_send.encode()
            self.repl_text_field.delete(self.repl_stop, tk.END)
            self.send_queue.put(to_send)
            return "break" 

    def _ctrl_a_event(self, event):
        self.send_queue.put(chr(1).encode())
        return "break"

    def _ctrl_b_event(self, event):
        self.send_queue.put(chr(2).encode())
        return "break"

    def _ctrl_c_event(self, event):
        self.send_queue.put(chr(3).encode())
        return "break"

    def _ctrl_d_event(self, event):
        self.send_queue.put(chr(4).encode())
        return "break"

    def _ctrl_e_event(self, event):
        self.send_queue.put(chr(5).encode())
        return "break"

    def disconnect(self, wait_for_thread_join=True):
        self.grid_remove()
        self.serial_thread.isRunning = False
        if wait_for_thread_join:
            self.serial_thread.join()
        self.master.u_serial.close()
        self.master.u_serial = None
        self.master.master.update_title(None)
        self.master.master.tool_bar.update_device_image(alert=True)
        self.master.master.bottom_status_bar.change_status(None)
        self.master.repl = None


class Toolbar(tk.Frame):
    def __init__(self, master):
        super().__init__(master, borderwidth=2, height=False)

        self.images = {}
        self.buttons = {}
        self.labels = {}

        self._add_button("new", "New", resource_path(os.path.join("img", "new.png")))
        self._add_button("load_file", "Load", resource_path(os.path.join("img", "load_file.png")))
        self._add_button("save_file", "Save", resource_path(os.path.join("img", "save.png")))
        self._add_separator("separator_1")
        self._add_separator("separator_2")
        self._add_button("run", "Run", resource_path(os.path.join("img", "run.png")))
        self._add_button("repl", "REPL", resource_path(os.path.join("img", "repl.png")))
        self._add_button("files", "Storage", resource_path(os.path.join("img", "files.png")))
        self._add_button("device", "Connect", resource_path(os.path.join("img", "device_alert.png")))
        self._load_image(resource_path(os.path.join("img", "device.png")))
        self._add_button("blockly", "Blockly", resource_path(os.path.join("img", "blockly.png")))


    def _load_image(self, img_file):
        # Load the image first as PNGs and use ImageTk to convert
        # them to usable Tkinter image.
        img = Image.open(img_file)
        img = img.resize((40, 40), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        
        # The image must be stored somewhere forever
        self.images[img_file] = img
        return self.images[img_file]

    def _add_button(self, name, label_text, img_file):
        new_button = tk.Button(self, image=self._load_image(img_file), border=0)
        new_button.grid(row=0, column=len(self.buttons))

        new_label = tk.Label(self, text=label_text)
        new_label.grid(row=1, column=len(self.buttons))

        self.buttons[name] = new_button
        self.labels[name] = new_label

    def _add_separator(self, name):
        new_separator = ttk.Separator(self,orient=tk.VERTICAL)
        new_separator.grid(row=0, column=len(self.buttons), sticky="ns")
        self.buttons[name] = new_separator

    def update_device_image(self, alert):
        if alert:
            self.buttons["device"].config(image=self.images[resource_path(os.path.join("img", "device_alert.png"))])
        else:
            self.buttons["device"].config(image=self.images[resource_path(os.path.join("img", "device.png"))])


class uSerial(serial.Serial):
    def __init__(self, port):
        super().__init__(port, baudrate=115200, timeout=.2)
        self.write(b'\r\x03\x03') # ctrl-C twice: interrupt any running program
        self.write(b'\x04') # ctrl-D: soft reset
        sleep(.2) # wait for the device to send a reply
        self.flushInput() # flush the reply

    def run(self, command):
        self.enter_raw_repl()
        self.exec(command)
        self.exit_raw_repl()

    def run_file(self, filename):
        with open(filename, 'rb') as f:
            pyfile = f.read()
        self.run(pyfile)

    def enter_raw_repl(self):
        self.write(b'\r\x03\x03') # ctrl-C twice: interrupt any running program

        self.flushInput()

        self.write(b'\r\x01') # ctrl-A: enter raw REPL
        sleep(.1)
        self.write(b'\x04') # ctrl-D: soft reset
        sleep(.5)

    def exit_raw_repl(self):
        self.write(b'\r\x02') # ctrl-B: enter friendly REPL

    def exec(self, command):
        command_bytes = command.strip() + b"\n\r"

        # write command
        for i in range(0, len(command_bytes), 256):
            self.write(command_bytes[i:min(i + 256, len(command_bytes))])
            sleep(0.01)
        self.write(b'\x04')


class SerialThread(threading.Thread):

    def __init__(self, repl, u_serial):
        super().__init__()
        self.name = "SerialThread"
        self.repl = repl
        self.u_serial = u_serial
        self.isRunning = True
        self.start()

    def run(self):
        logging.info('SerialThread Started')
        
        if self.u_serial.is_open:
            logging.info("Serial opened")
        else:
            logging.critical("Serial could not be open")
            return

        self.u_serial.write(b'\x04') # soft reset - the reply is the first thing printed in the REPL area
        
        while self.isRunning:
            try:
                incoming_bytes = []
                if not self.repl.send_queue.empty():
                    message = self.repl.send_queue.get()
                    self.u_serial.write(message)
                if self.u_serial.inWaiting():
                    while self.u_serial.inWaiting():
                        incoming_bytes.append(self.u_serial.read(1))
                    for index, byte in enumerate(incoming_bytes):
                        if ord(byte) < 128:
                            incoming_bytes[index] = byte.decode()
                        else:
                            incoming_bytes[index] = "$"

                    incoming_message = "".join(incoming_bytes).replace("\r", "")
                    self.repl.repl_text_field.insert(tk.END, incoming_message)
                    self.repl.repl_text_field.mark_set(tk.INSERT, tk.END)
                    self.repl.repl_text_field.see(tk.END)
                    # if self.text_color == "grey":
                    #     self.repl.repl_text_field.tag_add("grey", self.repl.repl_stop, tk.END)
                    #     self.repl.repl_text_field.tag_config("grey", foreground="grey")
                    self.repl.repl_stop = self.repl.repl_text_field.index("end-1c")
                else:
                    sleep(.01)
            except Exception as e:
                print("Serial Thread Exception !!!")
                self.isRunning = False
                self.repl.disconnect(False)


        return

class StatusBar(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self)
        self.label.grid()
        self.change_status()

    def change_status(self, new_device=None):
        self.device_name = new_device
        if self.device_name is None:
            self.label.config(text="Not connected. Try the 'Connect' button in the toolbar.")
        else:
            self.label.config(text="Connected to: {}".format(self.device_name))

class Application(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.title = "MicroPython Editor"
        self.root = root

        root.minsize(500, 500) # main window can not be smaller than 500x500 px
        
        # Set main window size to 60% of the screen size
        width = root.winfo_screenwidth() * .6
        height = root.winfo_screenheight() * .6
        root.geometry(str(int(width)) + "x" + str(int(height)))
        
        center_window(root) # center main window
        root.protocol("WM_DELETE_WINDOW", self.close_event)

        # makes the area in the main window scalable
        root.rowconfigure(0, weight=1) 
        root.columnconfigure(0, weight=1)

        self.rowconfigure(1, weight=1) # make the 2nd row (Editor) scalable
        self.columnconfigure(0, weight=1) # make the 1st (and only) column scalable
        self.grid(sticky="nsew") # expand Application Frame to the whole window

        self.update_title(None) # set main window title to the default setting

        self.tool_bar = Toolbar(self)
        self.tool_bar.grid(row=0, sticky="w")
    
        self.editor = Editor(self)
        self.editor.grid(row=1, sticky="nsew")

        self.bottom_status_bar = StatusBar(self)
        self.bottom_status_bar.grid(row=2, sticky="ew")

        # Bind Tool Bar buttons with functions from self.editor
        self.tool_bar.buttons["run"].config(command=self.editor.run_tab)
        self.tool_bar.buttons["new"].config(command=self.editor.new_tab)
        self.tool_bar.buttons["repl"].config(command=self.editor.toggle_repl)
        self.tool_bar.buttons["load_file"].config(command=self.editor.load_file)
        self.tool_bar.buttons["save_file"].config(command=self.editor.save_file)
        self.tool_bar.buttons["device"].config(command=self.editor.setup_device)
        self.tool_bar.buttons["blockly"].config(command=self.editor.blockly)

    def update_title(self, device=None):
        if device:
            self.root.title("{} - {}".format(self.title, device))
        else:
            self.root.title(self.title)

    def close_event(self):
        if self.editor.repl:
            self.editor.repl.disconnect()
        self.root.destroy()


def run():
    root = tk.Tk()
    app = Application(root)
    app.mainloop()

if __name__ == "__main__":
    run()
