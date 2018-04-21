import tkinter.filedialog as dialog


def getPath():
    filename = dialog.askopenfilename(initialdir='C:/')
    return filename
