import cv2
import ImageProcessor
import ImageEditor
import ImageImporter
import DataExporter
import tkinter as TK
import tkinter.messagebox
import os

filename = ""
img = None
helpText = "使用帮助：\n1.File->Import 导入待分析图片\n2.Run->Process&Edit 进入编辑界面，手动修正分析结果\n3.File->Export 导出分析结果的文本"
fileText = ""


def importImage():
    global filename, fileText, var
    filename = ImageImporter.getPath()
    if filename:
        name = os.path.basename(filename)
        path = os.path.dirname(filename)
        size = os.path.getsize(filename)
        fileText = "文件信息\n文件名：%s\n路径：%s\n大小：%d kB" % (name, path, size / 1024)
        var.set(fileText)
        print('imported')


def exportImage():
    global img, filename
    if img is not None:
        data = ImageProcessor.analyseImage(img)
        DataExporter.writeData(data)
        img = None
        filename = ""
        var.set(helpText)
        TK.messagebox.showinfo(title='Success', message='数据导出成功')
        print('data extracted')
    else:
        TK.messagebox.showinfo(title='Info', message='没有已导入的图片或图片未处理')


def process():
    global filename, img, fileText
    if filename:
        img = ImageProcessor.getMarkedImage(filename)
        img = ImageEditor.editImage(img)
        fileText += "\n分析完毕，可以导出"
        var.set(fileText)
        print('edited')
    else:
        TK.messagebox.showinfo(title='Info', message='没有已导入的图片')


top = TK.Tk()
top.title("MIRAS")
top.geometry('700x300')
menubar = TK.Menu(top)

filemenu = TK.Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Import', command=importImage)
filemenu.add_command(label='Export(txt)', command=exportImage)

runmenu = TK.Menu(menubar, tearoff=0)
menubar.add_cascade(label='Run', menu=runmenu)
runmenu.add_command(label='Process&Edit', command=process)

top.config(menu=menubar)

var = TK.StringVar()
var.set(helpText)
label = TK.Label(top,
                 textvariable=var,
                 font=('YaHei', 12), justify='left')
label.pack()

top.mainloop()
