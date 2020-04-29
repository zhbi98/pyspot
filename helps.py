
# -*- coding: utf-8 -*-


'''\t\t  Squirrel Help\n

\t\tSquirrel Version

   \tSquirrel Version 1.0
      \tCopyright (C)2019.Python.Org
        \tPower by H.C.S
'''


import tkinter


def helps():
    helpWindow = tkinter.Toplevel()
    helpWindow.title('Help')
    helpWindow.geometry('500x400')
    helpWindow.geometry('+920+150')
    helpWindow.resizable(False, False)
    helpWindow.transient()
    helpWindow.iconbitmap('./spot.ico')

    ybar = tkinter.Scrollbar(helpWindow, orient='vertical')
    ybar.pack(fill='y', side='right')

    doc = (tkinter.Text(helpWindow, width=290, height=140, 
           fg='#131313', bg='#f2f2f2', selectbackground='#222222', 
           yscrollcommand=ybar.set, font=('Arial', 12, 'bold')))
    doc.pack()
    doc.insert('end', __doc__)

    ybar.config(command=doc.yview)
