import cv2
import ImageProcessor
import ImageEditor
import tkinter.filedialog as dialog

filename = dialog.askopenfilename(initialdir='C:/')
if filename:
    img = ImageProcessor.getMarkedImage(filename)
    img = ImageEditor.editImage(img)
    img = ImageProcessor.analyseImage(img)

cv2.waitKey(0)
cv2.destroyAllWindows()
