"""
Provides a GUI for very basic robocopy commands. Allows users to copy 
directories and or sub-directories in restart or backup mode.
"""

import os
import sys
from Tkinter import *
from tkFileDialog import askdirectory

class App(object):

	def __init__(self, master):

		frame = Frame(master)
		frame.pack(expand=YES)
		# buttons
		self.source_button = Button(frame, text='...', 
			command=self.get_dir)
		self.destination_button = Button(frame, text='...',
			command=self.get_dir)
		self.cancel_button = Button(frame, text='Cancel', command=frame.quit)
		self.copy_button = Button(frame, text='Copy', command=self.copy())
		self.source_button.grid(row=0, column=2, sticky=W, ipadx=3)
		self.destination_button.grid(row=1, column=2, sticky=W, ipadx=3)
		self.cancel_button.grid(row=5, column=0, sticky=E, ipadx=10)
		self.copy_button.grid(row=5, column=1, sticky=W, ipadx=10)

		# bars
		self.source = Entry(frame)
		self.destination = Entry(frame)
		self.source.grid(row=0, column=1, sticky=E, ipady=2)
		self.destination.grid(row=1, column=1, sticky=E, ipady=2)

		# checks
		self.rec_var = IntVar()
		self.restart_var = IntVar()
		self.recurse = Checkbutton(frame, text='Copy Sub-Directories', 
			variable=self.rec_var) # /e
		self.restart = Checkbutton(frame, text='Restart Mode', 
			variable=self.restart_var) #/zb
		self.recurse.grid(row=3, sticky=W)
		self.restart.grid(row=3, column=1)

		# labels
		Label(frame, text='Source Directory').grid(row=0, sticky=W)
		Label(frame, text='Destination Directory').grid(row=1, sticky=W)

	def get_dir(self):
		return askdirectory(mustexist=True, title='Select Directory')

	def build_cmd(self):
		# get variable from entries and checks, format into a robocopy
		# command, return a string
		# 'robocopy {0} {1} {2}{3}'.format(source, destination, subs, res)
		pass

	def source(self):
		# open explorer, pass directory to entry
		pass

	def destination(self):
		# open explorer, pass directory to entry
		pass

	def copy(self):
		# command = self.build_cmd()
		# sys.execute_command(command)
		pass


if __name__ == '__main__':
	root = Tk()
	app = App(root)
	root.mainloop()
	root.destroy()
