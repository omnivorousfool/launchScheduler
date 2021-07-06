import tkinter as tk
import re

def convt_index(index):
    pos = [0,0]
    pos[0], pos[1] = map(int, index.split('.'))
    return pos

def convt_pos(pos):
    return '%d.%d' % (pos[0], pos[1])

class entry(tk.Text):
    def __init__(self, master=None, max=2, *args, **kw):
        super().__init__(master,  *args, **kw)
        self.master = master
        self.max_len = max
        self.configure(
                       wrap=tk.NONE,
                       height=1,
                       width=max,
                       bg='white',
                       fg='black',
                       insertbackground='black',
                       highlightcolor='black',
                       highlightbackground='white',
                       selectbackground='black',
                       selectforeground='white',
                       bd=0,
                       *args,
                       **kw
                       )
        self.bind('<Key>', lambda event: self.verify_len())
        self.bind('<KeyPress>', lambda event: self.verify_char(), '+')
        self.bind('<KeyRelease>', lambda event: self.verify_char(), '+')
        self.bind('<FocusOut>', lambda event: self.verify_char(delete=True))
        nnum = r'[^\d\n]'
        self.precomplied = re.compile(nnum)
        

    def verify_len(self):
        insert = self.get(1.0, convt_pos([1, self.max_len-1]))
        content = self.get(1.0, tk.END)
                    
        if len(content) > self.max_len:
            print(len(content))
            self.delete(1.0, tk.END)
            self.insert('insert', insert)
            print('insert', insert)
            
    def verify_char(self, delete=False):
        content = self.get(1.0, tk.END)
        
        num_find = re.search(self.precomplied, content)
        print(num_find)
        if num_find != None:
            print(self.index(tk.INSERT))
            insert = self.index(tk.INSERT)
            if delete:
                self.delete(1.0, tk.END)
            else:
                pos = convt_index(insert)
                pos[1] -= 1
                print(pos)
                self.delete(convt_pos(pos), insert)
            return True
        else:
            return False

    def get_value(self):
        return self.get(1.0, tk.END)

    def delAll(self):
        self.delete(1.0, tk.END)

        
class timeEntry(tk.Frame):
    def __init__(self, master=None, *args, **kw):
        super().__init__(master, bd=1, relief='solid', highlightbackground='grey', takefocus=True, *args, **kw)
##        self.bind('<FocusIn>', self.change_color)
##        self.bind('<FocusOut>', lambda event: self.config(bg='lightblue'))
##        self.bind('<Enter>', self.change_color)
        self.hEntry = entry(self, font=('consolas', 11))
        self.mEntry = entry(self, font=('consolas', 11))
        
        self.hEntry.pack(side='left', fill='both', expand=True)
        tk.Label(self, text=':', bd=0, bg='white').pack(side='left', fill='both', expand=True)
        self.mEntry.pack(side='left', fill='both', expand=True)

    def get_entry(self):
        try:
            hour = int(self.hEntry.get_value())
            mins = int(self.mEntry.get_value())
        except:
            return None
        if hour > 23 or mins > 59:
            self.hEntry.delAll()
            self.mEntry.delAll()
            return None
        else:
            return hour, mins

    def set_value(self, values):
        self.hEntry.insert(1.0, values[0])
        self.mEntry.insert(1.0, values[1])

    def change_color(self, event):
        print("Done")
        self['bg'] = 'blue'

##root = tk.Tk()
##timeEntry(root).pack(pady=10)
