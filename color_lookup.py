import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Create the main window
root = tk.Tk()
img=''
root.title("GUI")
image_id=''
# Create a label widget
label = tk.Label(root, text="Hello!")
label.pack()
canvas = tk.Canvas(root,width=0,height=0)
canvas.pack()

def resize_image(img,max_width,max_height):
    ratio = min(max_width / img.width, max_height / img.height)
    if img.width>img.height:
        width=max_width
        height=int(ratio*width)
    else:
        height=max_height
        width=int(ratio*height)

    return img.resize((width,height),Image.Resampling.LANCZOS)

# Create a button widget
def on_button_click():
    global canvas, image_id
    #Get image from dir
    img = filedialog.askopenfilename(title="Select an image", filetypes=(("Image files", ["*.png"]), ("All files", "*.*")))
    if img:
        img = Image.open(img)
        img = resize_image(img,700,700)
        img = ImageTk.PhotoImage(img)
        if image_id:
            canvas.itemconfig(image_id, image=img)  # Update image
            canvas.config(width=min(img.width(),700),height=min(img.height(),700))


        else:
            canvas_image_id = canvas.create_image(0, 0, anchor=tk.NW, image=img)
            canvas.config(width=min(img.width(),700),height=min(img.height(),700))
        canvas.image = img
        canvas.pack()

button = tk.Button(root, text="Choose Image", command=on_button_click)
button.pack()

# Run the GUI application




def main():
    root.mainloop()
    return 0

if __name__=='__main__':
    main()