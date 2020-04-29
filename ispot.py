 
# -*- coding: utf-8 -*-


import os
import helps
import tkinter
import tkinter.filedialog

import pytesseract
from PIL import Image
from PIL import ImageTk


def windowSize():
	global window
	global fonts
	global filename

	window = tkinter.Tk()
	fonts = 'Arial', 10
	filename = None

	window.title('Squirrel')
	window.geometry('500x400')
	window.geometry('+400+150')
	# window.attributes('-alpha', 0.9)
	window.iconbitmap('./spot.ico')


def photoFrame():
	global frame
	global background

	frame = (tkinter.Label(window, text='Photos', anchor='center', 
			width=1920, height=1080, bg='#121a2f', fg='#ad6152', 
			font=('Arial', 40), image=None))
	frame.pack()

	background = Image.open('./background.jpg', 'r')
	background = ImageTk.PhotoImage(background)
	frame.config(image=background)


class MenuBar(object):
	def __init__(self, menubar=None, _window=None):       
		self.menubar = tkinter.Menu(window)
		self._window = window.config(menu=self.menubar)

	def photoBar(self):
		photo = tkinter.Menu(self.menubar, tearoff=0)
		photo.add_command(label=' Get Text... ', command=textSpot, font=(fonts))

		photo.add_command(label=' Save ', command=saveAsFile, font=(fonts))

		self.menubar.add_cascade(label=' Photos ', menu=photo)

	def fileBar(self):
		fileoption = tkinter.Menu(self.menubar, tearoff=0)
		
		fileoption.add_command(label=' Open Photo... ', command=openDialog,
							   font=(fonts))

		fileoption.add_command(label=' Close Photo ', command=closePhotos, font=(fonts))
		fileoption.add_separator()
		fileoption.add_command(label=' Quit ', command=quit, font=(fonts))

		self.menubar.add_cascade(label=' Files ', menu=fileoption)

	def editBar(self):
		editoption = tkinter.Menu(self.menubar, tearoff=0)
		editoption.add_command(label=' Undo ', font=(fonts))

		editoption.add_command(label=' Redo ', font=(fonts))

		editoption.add_separator()
		editoption.add_command(label=' Cut ', font=(fonts))

		editoption.add_command(label=' Copy ', font=(fonts))
		
		editoption.add_command(label=' Paste ', font=(fonts))

		self.menubar.add_cascade(label=' Edit ', menu=editoption)

	def viewBar(self):
		view = tkinter.Menu(self.menubar, tearoff=0)
		view.add_command(label=' Zoom In ', font=(fonts))
		view.add_command(label=' Zoom Out ', font=(fonts))
		view.add_command(label=' Real ', command=originalImage,  
						 font=(fonts))
		self.menubar.add_cascade(label=' View ', menu=view)

	def helpBar(self):
		_window = tkinter.Menu(self.menubar, tearoff=0)
		_window.add_command(label=' Help... ', command=helps.helps,
							font=(fonts))
		self.menubar.add_cascade(label=' Help ', menu=_window)


def openDialog():
	global filename
	
	filename = (tkinter.filedialog.askopenfilename(title='Open Photos', 
				filetypes=[('All Files', '*'), ('Photos', '*.jpg *.png')]))

	openPhotos(filename)


def openPhotos(photoname):
	global newsize

	try:
		photo = Image.open(photoname, 'r')
		photo_width, photo_height = photo.size
		
		if photo_width > 500 or photo_height > 400:
			
			newsize = photo.resize(photoResize(photo_width, 
								   photo_height, 500, 400))
			newsize = ImageTk.PhotoImage(newsize)
		else:
			newsize = ImageTk.PhotoImage(photo)
		frame.config(image=newsize)
	except:
		print('No File Selected')


def closePhotos():
	global background
	
	filename = None
	background = Image.open('./background.jpg', 'r')
	background = ImageTk.PhotoImage(background)
	frame.config(image=background)


def photoResize(photo_width, photo_height, box_width, box_height):

	box_width = box_width / photo_width
	box_height = box_height / photo_height
	min_size = min(box_width, box_height)
	_width = int(min_size * photo_width)
	_height = int(min_size * photo_height)

	return _width, _height


def originalImage():
	global photo
	
	try:
		photo = Image.open(filename, 'r')
		photo = ImageTk.PhotoImage(photo)
		frame.config(image=photo)
	except:
		print('No Photos Opened')


def textBox():
	global text

	textWindow = tkinter.Toplevel(window)
	textWindow.title('Text')
	textWindow.geometry('500x400')
	textWindow.geometry('+920+150')
	textWindow.resizable(False, False)
	textWindow.transient(window)
	textWindow.iconbitmap('./spot.ico')

	ybar = tkinter.Scrollbar(textWindow, orient='vertical')
	ybar.pack(fill='y', side='right')

	text = (tkinter.Text(textWindow, width=290, height=140, 
			fg='#131313', bg='#f2f2f2', selectbackground='#222222', 
			yscrollcommand=ybar.set, font=(fonts)))
	text.pack()

	ybar.config(command=text.yview)


def textSpot():
	try:
		image = Image.open(filename)
		_text = pytesseract.image_to_string(image, lang='chi_sim')
		if _text == '':
			textBox()
			text.insert('end', '\n\t\t\tNot recognized')
		else:
			textBox()
			text.insert('end', _text)
	except:
		print('No Photos Opened')
		print('test: 2019.9')


def saveAsDialog():
	global path

	saveasname = (tkinter.filedialog.asksaveasfilename(title='Save As', 
				 initialdir=r'C:\ ibook', filetypes=[('All Files', '*'), 
				 ('Text', '*.txt')], initialfile='', defaultextension='.txt'))

	path = saveasname


def saveAsFile():
	try:
		saveAsDialog()
		file = open(path, 'w')
		saveas = text.get(1.0, 'end')
		file.write(saveas)
		file.close()
	except:
		print('No get Content')


if __name__ == '__main__':
	windowSize()
	photoFrame()
	MenuBar = MenuBar()
	MenuBar.photoBar()
	MenuBar.fileBar()
	MenuBar.editBar()
	MenuBar.viewBar()
	MenuBar.helpBar()

	window.mainloop()
