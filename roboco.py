"""
Provides a GUI for very basic robocopy commands. Allows users to copy 
directories and or sub-directories in restart or backup mode.
"""

import os
from subprocess import call
from Tkinter import *
from tkFileDialog import askdirectory

class App(object):

	def __init__(self, master):

		frame = Frame(master)
		frame.pack(expand=YES)
		# buttons
		self.source_button = Button(frame, text='...', 
			command=self.get_source_dir)
		self.destination_button = Button(frame, text='...',
			command=self.get_dest_dir)
		self.cancel_button = Button(frame, text='Cancel', command=frame.quit)
		self.copy_button = Button(frame, text='Copy', command=self.copy)
		self.source_button.grid(row=0, column=2, sticky=W, ipadx=3)
		self.destination_button.grid(row=1, column=2, sticky=W, ipadx=3)
		self.cancel_button.grid(row=5, column=0, sticky=E, ipadx=10)
		self.copy_button.grid(row=5, column=1, sticky=W, ipadx=10)

		# entry
		self.source = Entry(frame)
		self.destination = Entry(frame)
		self.source.grid(row=0, column=1, sticky=E, ipady=2)
		self.destination.grid(row=1, column=1, sticky=E, ipady=2)

		# checks
		self.rec_var = BooleanVar()
		self.restart_var = BooleanVar()
		self.recurse = Checkbutton(frame, text='Copy Sub-Directories', 
			variable=self.rec_var) # /e
		self.restart = Checkbutton(frame, text='Restart Mode', 
			variable=self.restart_var) #/zb
		self.recurse.grid(row=3, sticky=W)
		self.restart.grid(row=3, column=1)

		# labels
		Label(frame, text='Source Directory').grid(row=0, sticky=W)
		Label(frame, text='Destination Directory').grid(row=1, sticky=W)

	def get_source_dir(self):
		source_dir = askdirectory(mustexist=True, 
			title='Select Source Directory')
		self.source.delete(0, len(self.source.get()))
		self.source.insert(0, 
			str('"{}"').format(source_dir.replace('/', '\\')))
		return source_dir

	def get_dest_dir(self):
		dest_dir = askdirectory(mustexist=True, 
			title='Select Destinatoin Directory')
		self.destination.delete(0, len(self.destination.get()))
		self.destination.insert(0, 
			str('"{0}\\{1}"').format(dest_dir.replace('/', '\\'),
				os.path.basename(self.source.get().replace('"', ''))))
		return dest_dir

	def get_args(self):
		r = self.rec_var.get()
		b = self.restart_var.get()
		if r and not b:
			return r'/e'
		elif b and not r:
			return r'/zb'
		elif r and b:
			return r'/e /zb'
		else:
			return ''

	def build_cmd(self):
		cmd = 'robocopy {0} {1} {2}'.format(self.source.get(), 
			self.destination.get(), self.get_args())
		return cmd

	def copy(self):
		call(self.build_cmd())
		
if __name__ == '__main__':
	root = Tk()
	app = App(root)
	root.mainloop()
	root.destroy()
