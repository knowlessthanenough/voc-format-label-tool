import argparse
import os
import shutil

# Create an argument parser
parser = argparse.ArgumentParser(description='Combine multiple jetson nano voc xml data txt files into one.')

# Add the arguments
parser.add_argument('folders', metavar='folder', nargs=1,
                    help='a folder contain all data need to be combined')

# Parse the arguments
args = parser.parse_args()

# Get the path from the user
folder_path = args.folders[0]
print(folder_path)

# Check that the path exists
if not os.path.exists(folder_path):
    print(f'{folder_path} does not exist')
    exit()

# Check if the combined_file directory already exists
save_path = os.path.dirname(folder_path)
combined_path = os.path.join(save_path, 'combined_file')
if os.path.exists(combined_path):
    print(f'The directory {combined_path} already exists, please delete it first.')
    exit()

# Create the combined_file directory
os.makedirs(os.path.join(combined_path, 'ImageSets', 'Main'), exist_ok=True)

# Get a list of all the subdirectories in the path
files_list = [name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
print('those are folder going to combine: ', files_list)

# Combine the train files
train_save_path = os.path.join(combined_path, 'ImageSets', 'Main', 'train.txt')
with open(train_save_path, 'w') as outfile:
    for folder_name in files_list:
        filename = os.path.join(folder_path, folder_name, 'ImageSets', 'Main', 'train.txt')
        with open(filename, 'r') as infile:
            contents = infile.read()
            outfile.write(contents)

# Combine the test files
test_save_path = os.path.join(combined_path, 'ImageSets', 'Main', 'test.txt')
with open(test_save_path, 'w') as outfile:
    for folder_name in files_list:
        filename = os.path.join(folder_path, folder_name, 'ImageSets', 'Main', 'test.txt')
        with open(filename, 'r') as infile:
            contents = infile.read()
            outfile.write(contents)

# Combine the trainval files
trainval_save_path = os.path.join(combined_path, 'ImageSets', 'Main', 'trainval.txt')
with open(trainval_save_path, 'w') as outfile:
    for folder_name in files_list:
        filename = os.path.join(folder_path, folder_name, 'ImageSets', 'Main', 'trainval.txt')
        with open(filename, 'r') as infile:
            contents = infile.read()
            outfile.write(contents)

# Combine the val files
val_save_path = os.path.join(combined_path, 'ImageSets', 'Main', 'val.txt')
with open(val_save_path, 'w') as outfile:
    for folder_name in files_list:
        filename = os.path.join(folder_path, folder_name, 'ImageSets', 'Main', 'val.txt')
        with open(filename, 'r') as infile:
            contents = infile.read()
            outfile.write(contents)

print('train.txt, test.txt, trainval.txt, val.txt are combined successfully')

# Combine all Annotations folder together
Annotations_output_path = os.path.join(combined_path, 'Annotations')
os.makedirs(Annotations_output_path, exist_ok=True)
# Loop over each Annotations folder
for folder_name in files_list:
    Annotations_input_path = os.path.join(folder_path, folder_name, 'Annotations')
    # Loop over each voc xml file in the Annotations
    for filename in os.listdir(Annotations_input_path):
        # Get the full path to the input file
        input_path = os.path.join(Annotations_input_path, filename)

        # Get the full path to the output file
        output_path = os.path.join(Annotations_output_path, filename)

        # Copy the file to the output folder
        shutil.copy(input_path, output_path)

print(f"Annotations file from {', '.join(files_list)} have been combined into {Annotations_output_path}.")

# Combine all JPEGImages folder together
JPEGImages_output_path = os.path.join(combined_path, 'JPEGImages')
os.makedirs(JPEGImages_output_path, exist_ok=True)
# Loop over each JPEGImages folder
for folder_name in files_list:
    JPEGImages_input_path = os.path.join(folder_path, folder_name, 'JPEGImages')
    # Loop over each image in the folder
    for filename in os.listdir(JPEGImages_input_path):
        # Get the full path to the input
        input_path = os.path.join(JPEGImages_input_path, filename)

        # Get the full path to the output
        output_path = os.path.join(JPEGImages_output_path, filename)

        # Copy the file to the output folder
        shutil.copy(input_path, output_path)

print(f"JPEG Images from {', '.join(files_list)} have been combined into {JPEGImages_output_path}.")
