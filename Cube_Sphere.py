from tkinter import *
from pathlib import Path
from tkinter.filedialog import askopenfilename
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import math

# Variables
parent_folder = Path(os.path.dirname(os.path.abspath(__file__))).parent
file_name = parent_folder  # Cubemap image variable. Default is current dir
width = 2.0  # Aspect ratio
height = 1.5  # Aspect ratio


# Functions
def get_filename(event):
    global file_name
    file_name = askopenfilename()
    entry_select.delete(0, END)
    entry_select.insert(0, file_name)
    label_progress['text'] = 'Ready'


def generate(event):
    # Signal that we started the process
    global label_progress
    label_progress['text'] = 'Processing...'
    # Read width and height
    global height
    height = float(entry_height.get())
    global width
    width = float(entry_width.get())
    # Read Image
    path = str(parent_folder) + '/Sphere_Images'
    if not os.path.exists(path):
        os.mkdir(path)
    img = Image.open(file_name)
    # Generate image
    new_img_array = generate_sphere(img)
    # Save Image
    img_path = path + '/generated_image.png'
    new_img = Image.fromarray(new_img_array.astype(np.uint8))
    new_img.save(img_path)
    # plt.axis('off')
    # # Display fig
    # new_img_array = new_img_array.astype(dtype=np.uint8)
    # plt.imshow(new_img_array, cmap='gray', vmin=0, vmax=255)
    # # Save fig
    # plt.savefig(img_path, bbox_inches=0)
    # Signal that we're done
    label_progress['text'] = 'Done'


def generate_sphere(image):
    image_array = np.asarray(image)
    # Create the new array for the sphere image
    h = int(len(image_array)*height)
    w = int(len(image_array[0])*width)
    sphere_image = np.empty((h, w, 3), dtype=np.uint8)
    # Calculate the dimensions for the cube faces
    cube_width = len(image_array[0]) / 4  # Number of faces on the x axis
    cube_height = len(image_array) / 3  # Number of faces on the y axis

    for j in range(len(sphere_image)):  # Bottom-up
        v = 1 - j / len(sphere_image)
        theta = v * math.pi

        for i in range(len(sphere_image[0])):  # Left to right
            u = i / len(sphere_image[0])
            phi = u * 2 * math.pi
            # Initialize the unit vector
            x = math.sin(phi) * math.sin(theta) * -1
            y = math.cos(theta)
            z = math.cos(phi) * math.sin(theta) * -1

            a = max(abs(x), abs(y), abs(z))

            # Initialize the vector parallel to the unit vector lying on one of the cube faces
            xa = x / a
            ya = y / a
            za = z / a

            if xa == 1:
                # Right face
                xPixel = ((((za + 1) / 2) - 1) * cube_width)
                xOffset = 2 * cube_width  # Offset
                yPixel = ((((ya + 1) / 2)) * cube_height)
                yOffset = cube_height  # Offset
            elif xa == -1:
                # Left face
                xPixel = ((((za + 1) / 2)) * cube_width)
                xOffset = 0;
                yPixel = ((((ya + 1) / 2)) * cube_height)
                yOffset = cube_height
            elif ya == 1:
                # Upper face
                xPixel = ((((xa + 1) / 2)) * cube_width)
                xOffset = cube_width
                yPixel = ((((za + 1) / 2) - 1) * cube_height)
                yOffset = 2 * cube_height
            elif ya == -1:
                # Lower face
                xPixel = ((((xa + 1) / 2)) * cube_width)
                xOffset = cube_width
                yPixel = ((((za + 1) / 2)) * cube_height)
                yOffset = 0
            elif za == 1:
                # Front face
                xPixel = ((((xa + 1) / 2)) * cube_width)
                xOffset = cube_width
                yPixel = ((((ya + 1) / 2)) * cube_height)
                yOffset = cube_height
            elif (za == -1):
                # Back face
                xPixel = ((((xa + 1) / 2) - 1) * cube_width)
                xOffset = 3 * cube_width
                yPixel = ((((ya + 1) / 2)) * cube_height)
                yOffset = cube_height
            else:
                print("Unknown face, something went wrong")
                xPixel = 0
                yPixel = 0
                xOffset = 0
                yOffset = 0

            xPixel = abs(xPixel)
            yPixel = abs(yPixel)

            xPixel = xPixel + xOffset
            yPixel = yPixel + yOffset
            if yPixel >= len(image_array) or xPixel >= len(image_array[0]):
                continue
            tmp = image_array[int(yPixel)][int(xPixel)]
            sphere_image[j][i] = tmp
    return sphere_image.astype(int)


# Main window
root = Tk()
# Labels and buttons and entries and others
label_select = Label(root, text="Select Cubemap image")
button_select = Button(root, text="Browse")  # , command=askopenfilename)
button_select.bind("<Button-1>", get_filename)
entry_select = Entry(root)
entry_select.insert(END, file_name)
label_aspect_ratios = Label(root, text="Select aspect ratios for result image compared to original")
label_height = Label(root, text="Height")
label_width = Label(root, text="Width")
entry_height = Entry(root)
entry_height.insert(END, str(height))
entry_width = Entry(root)
entry_width.insert(END, str(width))
button_generate = Button(root, text="Generate Panorama")
button_generate.bind("<Button-1>", generate)
label_progress = Label(root, text="Waiting for image")
# Pack
label_select.grid(row=0, columnspan=2, sticky=W)
button_select.grid(row=1, column=1)
entry_select.grid(row=1, columnspan=1, column=0, sticky=EW)
label_aspect_ratios.grid(row=2, columnspan=2, column=0)
label_height.grid(row=3, columnspan=1, column=0)
label_width.grid(row=3, columnspan=1, column=1)
entry_height.grid(row=4, columnspan=1, column=0)
entry_width.grid(row=4, columnspan=1, column=1)
button_generate.grid(row=5, column=0, columnspan=2, sticky=SW)
label_progress.grid(row=6, column=0, columnspan=2, sticky=SW)
# Include main window in main loop
root.columnconfigure(0, weight=1)
root.mainloop()




# # Buttons
# button2 = Button(top_frame, text="Button 2", fg="yellow")
# button3 = Button(top_frame, text="Button 3", fg="blue")
# button4 = Button(bottom_frame, text="Button 4", fg="green")
# # Pack 'em
# button1.pack(side=LEFT)
# button2.pack(side=LEFT)
# button3.pack(side=LEFT)
# button4.pack()
#
# # # Labels
# # label_1 = Label(root, text="One", bg="red", fg="yellow")
# # label_2 = Label(root, text="Two", bg="green", fg="white")
# # label_3 = Label(root, text="Three", bg="blue", fg="orange")
# # # Pack
# # label_1.pack()
# # label_2.pack(fill=X)
# # label_3.pack(side=LEFT, fill=Y)
#
