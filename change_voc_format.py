import os
import shutil
import sys

# Replace input with the path to the data folder
input_file_name = sys.argv[1]
# input_file_name = '2_1_test'
xml_folder_path = input_file_name + "/Annotations/"
imagesets_folder_path = input_file_name + "/ImageSets/Main/"
image_folder_path = input_file_name + "/JPEGImages"

# Replace "path/to/folder" with the path to the folder you want to rename
old_folder_path = input_file_name + "/images"

# Replace "new_folder_name" with the new name you want to give to the folder
new_folder_path = input_file_name + "/JPEGimages"

# Rename the folder
os.rename(old_folder_path, new_folder_path)

print(f"Folder renamed from {old_folder_path} to {new_folder_path}")

# Define the line numbers to be deleted
lines_to_delete = [1, 9, 10, 12, 13, 14, 15]

# Loop through all files in the folder
for filename in os.listdir(xml_folder_path):
    file_path = os.path.join(xml_folder_path, filename)

    # Check if the file is a xml file
    if filename.endswith(".xml"):
        print(f"Processing file: {filename}")

        # Read the contents of the file
        with open(file_path, "r") as f:
            lines = f.readlines()

        # Delete the specified lines
        lines = [line for i, line in enumerate(lines, start=1) if i not in lines_to_delete]

        # Write the modified contents back to the file
        with open(file_path, "w") as f:
            f.writelines(lines)

        print(f"Deleted lines {lines_to_delete} from file: {filename}")

# create imagesets folder
os.makedirs(imagesets_folder_path)
# Create a new text file
with open(image_folder_path + "file_list.txt", "w") as f:
    # Loop through all files in the folder
    for filename in os.listdir(image_folder_path):
        # Get the filename without the extension
        name_without_extension = os.path.splitext(filename)[0]

        # Write the filename to the text file
        f.write(name_without_extension + "\n")

print("File list written to file_list.txt")

# copy rename txt file
file_list_location = image_folder_path + "file_list.txt"
output_folder_path = imagesets_folder_path
# Define the names of the output files
output_filenames = ["train.txt", "test.txt", "val.txt", "trainval.txt"]

# Open the input file and read its contents
with open(file_list_location, "r") as f:
    lines = f.readlines()

# Loop through the output filenames and copy the input file to each file
for filename in output_filenames:
    output_file_path = os.path.join(output_folder_path, filename)
    shutil.copyfile(file_list_location, output_file_path)

# Delete the input file
os.remove(file_list_location)

print("Input file copied to train.txt, test.txt, val.txt, and trainval.txt")
