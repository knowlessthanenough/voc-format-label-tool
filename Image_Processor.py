import tkinter as tk
from PIL import ImageTk, Image
import cv2
import glob
import sys
import shutil
import os
import functools


# Callback function for image selection.
def click(name):
    global image, current_file_index, image_list, photo, photo_resize, photo_final
    global photo_label, photo_title, xml_name, xml
    cv2_array = cv2.imread(name)
    image_list_id = 0
    for check_file_name in image_list:
        if check_file_name == name:
            current_file_index = image_list_id
        image_list_id = image_list_id + 1
    xml_name = name.replace("JPEGImages", "Annotations")
    xml_name = xml_name.replace(".jpg", ".xml")
    starting_line = 20
    next_object_line_difference = 12
    name_starting_line = 15
    count = 0
    with open(xml_name, "r") as xml:

        lines = xml.readlines()
        for number in lines:
            count = count + 1
        number_of_boxes = int(count - 15) / 12
        i = 0
        while i < number_of_boxes:
            name = lines[name_starting_line + next_object_line_difference * i].replace("<name>", "") \
                .replace("</name>", "").replace(" ", "").replace("\n", "")
            name = str(name)
            xmin = lines[starting_line + next_object_line_difference * i].replace("<xmin>", "") \
                .replace("</xmin>", "").replace(" ", "")
            xmin = int(xmin)
            ymin = lines[starting_line + 1 + next_object_line_difference * i].replace("<ymin>", "") \
                .replace("</ymin>", "").replace(" ", "")
            ymin = int(ymin)
            xmax = lines[starting_line + 2 + next_object_line_difference * i].replace("<xmax>", "") \
                .replace("</xmax>", "").replace(" ", "")
            xmax = int(xmax)
            ymax = lines[starting_line + 3 + next_object_line_difference * i].replace("<ymax>", "") \
                .replace("</ymax>", "").replace(" ", "")
            ymax = int(ymax)
            i = i + 1
            color = (0, 0, 255)
            if name == "stand":
                color = (0, 255, 0)  # Green
            elif name == "swim":
                color = (255, 0, 0)  # Blue
            elif name == "wave":
                color = (0, 130, 130)  # Yellow
            elif name == "drown":
                color = (0, 0, 255)  # Red
            elif name == "under":
                color = (130, 0, 130)  # Purple
            cv2.rectangle(cv2_array, (xmin - 3, ymin - 3), (xmax - 3, ymax - 3), color, 2)
            correct_color_array = cv2.cvtColor(cv2_array, cv2.COLOR_BGR2RGB)
            cv2_image = Image.fromarray(correct_color_array)

    photo = cv2_image
    width = int(window.winfo_screenwidth() * 0.6)
    height = int(width * 720 / 1280)
    photo_resize = photo.resize((width, height))
    photo_final = ImageTk.PhotoImage(photo_resize)
    photo_label = tk.Label(image, image=photo_final)
    photo_title = tk.Label(image, text=name, bg="light blue", font=("Arial", 12))
    photo_title.grid(row=1, column=1)
    photo_label.grid(row=2, column=1, sticky="ns")


# Callback function for button "Correct".
def correct():
    global current_file_index, image_list, xml_name, xml, path

    # Change button background color to green after pressing "Correct".
    button_list[current_file_index].configure(bg="green")

    # Copy all the respective files.
    input_labels = str(path + "/labels.txt")
    output_labels = str(path + "/output/labels.txt")
    open(output_labels, "a")
    shutil.copy2(input_labels, output_labels)

    output_file_name = xml_name.replace("Annotations", "output/Annotations")
    open(output_file_name, "a")
    shutil.copy2(xml_name, output_file_name)

    image_copy = image_list[current_file_index].replace("JPEGImages", "output/JPEGImages")
    open(image_copy, "a")
    shutil.copy2(image_list[current_file_index], image_copy)

    image_name = image_list[current_file_index].replace(path, "").replace("/JPEGImages/", "").replace(".jpg", "")
    ImageSets_path = str(path + "/output/ImageSets/Main/")

    # Check whether the respective files are already there.
    exist = False
    f = open(ImageSets_path + "test.txt", "r")
    lines = f.readlines()
    for line in lines:
        if line == image_name + "\n" or line == image_name:
            exist = True
    f.close()

    # Copy the file name onto the txt file.
    f = open(ImageSets_path + "test.txt", "a")
    if os.stat(ImageSets_path + "test.txt").st_size == 0:
        f.write(image_name)  # Prevent creating newline at the end.
    else:
        if exist == False:
            f.write("\n" + image_name)
    f.close()

    # create 3 more copies with the same content, but different file name
    shutil.copy(ImageSets_path + "test.txt", ImageSets_path + "train.txt")
    shutil.copy(ImageSets_path + "test.txt", ImageSets_path + "trainval.txt")
    shutil.copy(ImageSets_path + "test.txt", ImageSets_path + "val.txt")

    # Go to the next image on the list.
    if current_file_index < len(image_list) - 1:
        current_file_index = current_file_index + 1
    click(image_list[current_file_index])


# Callback function for button "Wrong".
def wrong():
    global current_file_index, image_list

    # Change the color of the button to red if "Wrong" is pressed.
    button_list[current_file_index].configure(bg="red")

    # Skip to the next image on the list.
    if current_file_index < len(image_list) - 1:
        current_file_index = current_file_index + 1
    click(image_list[current_file_index])


def delete():
    global current_file_index, image_list, xml_name, xml, path

    # Delete everything related to current selected photo. Easy to correct misclick.
    output_file_name = xml_name.replace("Annotations", "output/Annotations")
    if os.path.isfile(output_file_name):
        os.remove(output_file_name)

    image_copy = image_list[current_file_index].replace("JPEGImages", "output/JPEGImages")
    if os.path.isfile(image_copy):
        os.remove(image_copy)

    image_name = image_list[current_file_index].replace(path, "").replace("/JPEGImages/", "").replace(".jpg", "")
    ImageSets_path = str(path + "/output/ImageSets/Main/")
    # Check whether the respective line of text is already there.
    f = open(ImageSets_path + "test.txt", "r")
    lines = f.readlines()
    f = open(ImageSets_path + "test.txt", "w")
    for line in lines:
        if line.strip("\n") != image_name:
            f.write(line)
    f.close()

    # create 3 more copies with the same content, but different file name
    shutil.copy(ImageSets_path + "test.txt", ImageSets_path + "train.txt")
    shutil.copy(ImageSets_path + "test.txt", ImageSets_path + "trainval.txt")
    shutil.copy(ImageSets_path + "test.txt", ImageSets_path + "val.txt")

    button_list[current_file_index].configure(bg="purple")


# Frame setup and configuration details.
window = tk.Tk()
window.title("Image Verification")

window.rowconfigure(0, minsize=300, weight=1)
window.columnconfigure(2, minsize=100, weight=1)

buttons = tk.Frame(window, relief=tk.RAISED, bd=2, bg="pink")
btn_title = tk.Label(buttons, text="List of Images", bg="pink", font=("Arial", 15, "bold"), pady=10)
btn_title.grid(row=0, column=0)


def scrollable_frame(name):
    pass


# scrollable frame for buttons.
frame_container = tk.Frame(window)
canvas_container = tk.Canvas(frame_container, height=500)
frame2 = tk.Frame(canvas_container)
myscrollbar = tk.Scrollbar(frame_container, orient="vertical", command=canvas_container.yview)
canvas_container.create_window((0, 0), window=frame2, width=int(window.winfo_screenwidth() * 0.25), anchor="n")

image = tk.Frame(window, bg="light blue", bd=2)
image_title = tk.Label(image, text="Image", bg="light blue", font=("Arial", 15, "bold"))
image_title.grid(row=0, column=0)

confirm = tk.Frame(window, relief=tk.RAISED, bd=2, bg="light green", width=100, )
correct_button = tk.Button(confirm, text="Correct", command=correct, padx=10, pady=10,
                           font=("Arial", 12, "bold"), fg="green")
wrong_button = tk.Button(confirm, text="Wrong", command=wrong, padx=10, pady=10, font=("Arial", 13, "bold"), fg="red")
delete_button = tk.Button(confirm, text="Delete", command=delete, padx=10, pady=10, font=("Arial", 12, "bold"),
                          fg="purple")
correct_button.grid(row=0, column=0, pady=50)
wrong_button.grid(row=1, column=0, pady=50)
delete_button.grid(row=2, column=0, pady=50)

# Creating list of image presented in the specific directory. (Inside "Sample", in the current directory.)
current_file_index = 0
image_list = []
button_list = []
path = str(sys.argv[1])
path = path.replace("\\", "/")
for file_name in glob.glob(path + "/JPEGImages/*.jpg"):
    image_list.append(file_name)

for item in image_list:
    short_file_name = item.replace(path, "")
    button_list.append(current_file_index)
    button_list[current_file_index] = tk.Button(frame2, text=short_file_name, command=lambda item=item: click(item),
                                                padx=2)
    button_list[current_file_index].pack(fill=tk.X)
    current_file_index = current_file_index + 1

frame2.update()
canvas_container.configure(yscrollcommand=myscrollbar.set, scrollregion=canvas_container.bbox("all"))

canvas_container.grid(row=0, column=0, sticky="ns", padx=5, pady=10)
myscrollbar.grid(row=1, column=0, sticky="ns")

# Create directory for future output.
if not os.path.exists(path + "/output"):
    os.mkdir(path + "/output")
    os.mkdir(path + "/output/Annotations")
    os.mkdir(path + "/output/ImageSets")
    os.mkdir(path + "/output/ImageSets/Main")
    open(path + "/output/ImageSets/Main/test.txt", "a")
    open(path + "/output/ImageSets/Main/train.txt", "a")
    open(path + "/output/ImageSets/Main/trainval.txt", "a")
    open(path + "/output/ImageSets/Main/val.txt", "a")
    os.mkdir(path + "/output/JPEGImages")

# Present the first image of the list.
current_file_index = 0
first_file_name = image_list[0]
click(first_file_name)

# Finish the window setup.
image.grid(row=0, column=1, sticky="nsew")
confirm.grid(row=0, column=2, sticky="nse")
frame_container.grid(row=0, column=0, sticky="nsew")

window.mainloop()
