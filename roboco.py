"""
Provides a GUI for very basic robocopy commands. Allows users to copy 
directories and or sub-directories in restart or backup mode. 
from bradhamson / roboco.py on GITHUB. https://github.com/bradhamson/roboco.py. 
-- updated for Python 3; 
-- added an option for mirror (/MIR); 
-- widened the window; 
-- added a Clear button; 
-- to added a checkbox to save output to file in robocoPY/log directory. 
++ TO DO: add a button to pull the last log file up into an editor.
          -- add method to discover an editor
          -- add method to give the file to that editor for viewing

Install location is expected to be <install root>/robocoPY with subdirectories src and log
...\robocoPY
...\robocoPY\src\roboco.py
...\robocoPy\log\log<datestamp>.log
"""

import os
import datetime
from subprocess import call
from tkinter import *
from tkinter import filedialog
#from pip._vendor.pyparsing import line
#from tkinter import tkFileDialog
#from tkFileDialog import askdirectory

class App(object):

    def __init__(self, master):
        frame = Frame(master, width=2000, height=500)
        # frame.pack(expand=YES)
        frame.grid(sticky=N+S+E+W)
        frame.grid_columnconfigure(0, weight=1)
        # buttons
        self.source_button = Button(frame, text='...',          command=self.get_source_dir)
        self.destination_button = Button(frame, text='...',
            command=self.get_dest_dir)
        self.cancel_button = Button(frame, text='Exit', command=frame.quit)
        self.copy_button = Button(frame, text='Copy', width = 20, command=self.copy)
        self.clear_button = Button(frame, text='Clear', width = 10, command=self.clearEntry)
        self.source_button.grid(row=0, column=2, sticky=W, ipadx=3)
        self.destination_button.grid(row=1, column=2, sticky=W, ipadx=3)
        self.cancel_button.grid(row=5, column=3, sticky=E, ipadx=10)
        self.copy_button.grid(row=5, column=1, sticky=W, ipadx=10)
        self.clear_button.grid(row=5, column=0, sticky=W, ipadx=10)

        # entry
        self.source = Entry(frame, width=45, bd=2)
        self.destination = Entry(frame, width=45, bd=2)
        self.source.grid(row=0, column=1, sticky=E+W, ipady=2)
        self.destination.grid(row=1, column=1, sticky=E+W, ipady=2)

        # checks
        self.recursive_var = BooleanVar()
        self.recursive_var.set(True)
        self.restart_var = BooleanVar()
        self.mirror_var  = BooleanVar()
        self.mirror_var.set(True)
        self.savefile_var = BooleanVar()
        self.savefile_var.set(False)
        self.recurse = Checkbutton(frame, text='Copy Sub-Directories',
            variable=self.recursive_var) # /e
        self.restart = Checkbutton(frame, text='Restart Mode',
            variable=self.restart_var) #/zb
        self.mirror  = Checkbutton(frame, text='Mirror',
            variable=self.mirror_var)   # /MIR
        self.savefile = Checkbutton(frame, text='Log Output',
            variable=self.savefile_var) # for mirroring output to a file
        self.recurse.grid( row=3, column=0, sticky=W)
        self.restart.grid( row=3, column=1, sticky=W)
        self.mirror.grid(  row=3, column=2, sticky=W)
        self.savefile.grid(row=3, column=3, sticky=W)

        # labels
        Label(frame, text='Source Directory').grid(row=0, sticky=W)
        Label(frame, text='Destination Directory').grid(row=1, sticky=W)
        
        # logging
        self.outputfile = ''
        outputfilepath = os.path.dirname(__file__).replace(r'\src', r'\log') + '\\'
        if not os.path.isdir(outputfilepath): # make sure that the directory exists
            outputfilepath = os.path.dirname(__file__) + r'\log' + '\\'
        self.outputfilepath = outputfilepath

    def get_source_dir(self):
        source_dir = filedialog.askdirectory(mustexist=True,
            title='Select Source Directory')
        self.source.delete(0, len(self.source.get()))
        self.source.insert(0,
            str('"{}"').format(source_dir.replace('/', '\\')))
        return source_dir

    def get_dest_dir(self):
        dest_dir = filedialog.askdirectory(mustexist=True,
            title='Select Destinatoin Directory')
        self.destination.delete(0, len(self.destination.get()))
        self.destination.insert(0,
            str('"{0}\\{1}"').format(dest_dir.replace('/', '\\'),
                os.path.basename(self.source.get().replace('"', ''))))
        return dest_dir

    def clearEntry(self):
        self.source.delete(0, len(self.source.get()))
        self.destination.delete(0, len(self.destination.get()))

    def get_args(self):
        option_list = []
        r = self.recursive_var.get()
        b = self.restart_var.get()
        m = self.mirror_var.get()
        s = self.savefile_var.get()
        if r:
            option_list.append(r'/E')
        if b:
            option_list.append(r'/Z')
        if m:
            option_list.append(r'/MIR')
        if s:
            outputfilename = r'log_' + datetime.datetime.now().strftime('%d-%b-%g_%I-%M-%S') + '.log'
            self.outputfile = self.outputfilepath + outputfilename
            #print(self.outputfile)
            option_list.append(r'/tee /log:' + self.outputfile)
        return (' '.join(option_list))

    def build_cmd(self):
        cmd = 'robocopy {0} {1} {2}'.format(self.source.get(),
            self.destination.get(), self.get_args())
        return cmd

    def copy(self):
        call(self.build_cmd())

if __name__ == '__main__':
    root = Tk()
    root.wm_title('Roboco.py - A robocopy GUI')
    app = App(root)
    root.mainloop()
    root.destroy()
