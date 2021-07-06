import tkinter as tk
from tkinter import ttk, filedialog
from tkinter.constants import E
from widgets import timeEntry
from os import system
from time import sleep
from datetime import date, datetime
##import re

def load_settings():
    with open('launch settings.ini', 'r') as setting:
        paraStr = setting.read()
        paras = paraStr.split('\n')
        print(paras)
    return paras

def save_settings(settings):
    with open('launch settings.ini', 'w') as setting:
        setStr = '\n'.join(settings)
        setting.write(setStr)
        
    
class scheduler(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Launch Scheduler')
        self.resizable(0, 0)
        self.autoConfirm = 1
        self.bind('<Button>', lambda event: self.active())
        self.bind('<Escape>', lambda event: self.destroy())
        self.after(1000, self.auto_confirm)

        self.settings = load_settings()
        self.timeout = int(self.settings[3])
        self.count = self.timeout
        print(self.timeout)
        self.mainFrame = tk.LabelFrame(self, text='Launch configuration')
        self.mainFrame.pack(fill='both', expand=True, padx=8, pady=7)
        
        frame_1 = tk.Frame(self.mainFrame)
        frame_1.pack(anchor='w')
        
        tk.Label(frame_1, text='set launch time:').pack(side='left')
        self.timeEntry = timeEntry(frame_1)
        self.timeEntry.set_value(['%.2d'%int(self.settings[0]), '%.2d'%int(self.settings[1])])
        self.timeEntry.pack(padx=5, pady=3, side='left')

        frame_2 = tk.Frame(self.mainFrame)
        frame_2.pack(anchor='w')

        tk.Label(frame_2, text='set launch path:').pack(side='left')
        self.pathEntry = ttk.Entry(frame_2, font=('consolas', 11))
        self.pathEntry.insert(0, self.settings[2])
        self.pathEntry.pack(side='left', padx=5, pady=3)
        
        frame_3 = tk.Frame(self.mainFrame)
        frame_3.pack(anchor='w')

        self.fileSelect = ttk.Button(frame_3, text='Select path', command=self.get_path)
        self.fileSelect.pack(padx=5, pady=3, side='left')
        self.confirmBtn = ttk.Button(frame_3, text='Confirm(%s)'%self.timeout, command=self.confirm)
        # self.confirmBtn.grab_set()
        self.confirmBtn.focus_set()
        self.confirmBtn.pack(padx=5, pady=3, side='left')
        self.cancelBtn = ttk.Button(frame_3, text='Cancel', command=self.destroy)
        self.cancelBtn.pack(padx=5, pady=3, side='left')

    def active(self):
        self.autoConfirm = 0
        # print('N')
        self.unbind('<Button>')

    def auto_confirm(self):
        if self.count == 0:
            self.confirm()
        elif not self.autoConfirm:
            # print('Y')
            self.confirmBtn['text'] = 'Confirm'
            return None
        else:
            self.count -= 1
            self.confirmBtn['text'] = 'Confirm(%d)' % self.count
            self.after(1000, self.auto_confirm)
        

    def get_path(self):
        path = tk.filedialog.askopenfilename()
        if path:
            self.pathEntry.delete(0, tk.END)
            self.pathEntry.insert(0, path)
            self.path = path
            print(self.path)
        else:
            print(None)

    def confirm(self):
        setTime = self.timeEntry.get_entry()
        path = self.pathEntry.get()
        if setTime == None or path == '':
            self.pathEntry.insert(0, self.settings[2])
            return None

        self.settings[0], self.settings[1] = map(str, setTime)
        self.path = path
        self.settings[2] = self.path
        save_settings(self.settings)

        today = date.today()

        launchTime = datetime(today.year, today.month, today.day, int(self.settings[0]), int(self.settings[1]))
        print(launchTime)
        print(datetime.now())
        countdown = (launchTime-datetime.now()).seconds

        # print(countdown)
        # print(countdown.seconds)
        self.destroy() 
        sleep(countdown)
        system('start "" "%s"' % self.path)

if __name__ == '__main__':
##    load_settings()
##    save_settings(['12','12','22'])
    app = scheduler()
    app.mainloop()