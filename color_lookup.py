import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# Global variables
img = None  # Store the image for pixel access
tk_img = None  # Store the Tkinter image

def load_colors():
    colors={}
    with open('color_names.csv','r') as file:
        for line in file:
            colors[tuple(int(line.split(',')[1][1:-1][i:i + 2], 16) for i in (0, 2, 4))]=line.split(',')[0]
    return colors

def load_image():
    global img, tk_img  # Ensure global access
    file_path = filedialog.askopenfilename(title="Select an image",
                                           filetypes=[("Image files", "*.png;*.jpg;*.jpeg"), ("All files", "*.*")])
    if not file_path:
        return  # No file selected
    img = Image.open(file_path).convert("RGB")  # Store image (RGB mode)
    img = resize(700)
    tk_img = ImageTk.PhotoImage(img)  # Convert for Tkinter
    canvas.create_image(0, 0, anchor=tk.NW, image=tk_img)  # Draw image
    canvas.image = tk_img  # Keep reference to prevent garbage collection

def closest_point_numpy(target):
    global colors
    points = np.array(list(colors.keys()))
    distances = np.sum((points - np.array(target))**2, axis=1)
    closest = tuple(points[np.argmin(distances)])
    ints = [value.item() for value in closest]
    return colors.get(tuple(ints)), tuple(ints)

def get_pixel_color(event):
    global img  # Access stored image
    if img is None:
        return  # No image loaded

    x, y = event.x, event.y
    try:
        r, g, b = img.getpixel((x, y))  # Get RGB values
        match = closest_point_numpy([r, g, b])
        result.config(text = f"Closest match in colors is: {match[0]} / RGB({match[1]} / HEX #{match[1][0]:02x}{match[1][1]:02x}{match[1][2]:02x}")
        result.pack()

    except IndexError:
        print("Clicked outside the image bounds.")

def find_closest_color(color):
    global colors
    if colors.get((color[0],color[1],color[2])) is not None:
        return colors.get((color[0],color[1],color[2]))
    return "No perfect match"

def resize(max_size):
    global img
    ratio = min(img.width,img.height)/max(img.width,img.height)
    if img.width>img.height:
        img = img.resize([max_size,int(max_size*ratio)])
    elif img.height>img.width:
        img = img.resize([int(max_size * ratio),max_size])
    else:
        img = img.resize(max_size,max_size)
    return img

root = tk.Tk()
root.title("Image Pixel Reader")
canvas = tk.Canvas(root, width=700, height=700)
canvas.pack()
canvas.bind("<Button-1>", get_pixel_color)  # Bind click event to canvas
button = tk.Button(root, text="Choose Image", command=load_image)
button.pack()
result = tk.Label(root)
colors = load_colors()

def main():
    root.mainloop()

if __name__=='__main__':
    main()