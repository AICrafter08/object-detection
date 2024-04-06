import os

# Define the base directory
base_dir = "/content/folder1"

# Define the subdirectories containing images and labels
subdirectories = ['train', 'valid', 'test']

# Iterate through each subdirectory
for subdir in subdirectories:
    labels_dir = os.path.join(base_dir, subdir, 'labels')
    
    # Iterate through each text file in the labels directory
    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(labels_dir, filename)
            
            # Read the content of the file
            with open(file_path, 'r') as file:
                content = file.readlines()
            # print(content)
            
            # Modify the label in the content
            modified_content = []
            for line in content:
                values = line.split()
                if len(values) > 0:
                    values[0] = '11'
                    modified_content.append(' '.join(values) + '\n')
            # print(modified_content)
            # Write the modified content back to the file
            with open(file_path, 'w') as file:
                file.writelines(modified_content)

# create fodler2 correctly folder structure
import os
import shutil
import random

# Define the paths for the original images and labels directory
original_images_dir = '/content/folder2/export/images'
original_labels_dir = '/content/folder2/export/labels'

# Define the paths for the new train, validation, and test directories
new_structure = {
    'train': {
        'images': '/content/folder3/train/images',
        'labels': '/content/folder3/train/labels'
    },
    'val': {
        'images': '/content/folder3/valid/images',
        'labels': '/content/folder3/valid/labels'
    },
    'test': {
        'images': '/content/folder3/test/images',
        'labels': '/content/folder3/test/labels'
    }
}

# Create directories if they don't exist
for directory_type in new_structure.values():
    for directory_path in directory_type.values():
        os.makedirs(directory_path, exist_ok=True)

# Get list of all files in the original images directory
files = os.listdir(original_images_dir)

# Shuffle the files randomly
random.shuffle(files)

# Define the split ratios
train_split_ratio = 0.7
val_split_ratio = 0.15
test_split_ratio = 0.15

# Split the files into train, validation, and test sets
train_split = int(len(files) * train_split_ratio)
val_split = int(len(files) * val_split_ratio)

train_files = files[:train_split]
val_files = files[train_split:train_split + val_split]
test_files = files[train_split + val_split:]

# Function to copy files from one directory to another
def copy_files(files, source_dir, dest_dir):
    for file in files:
        image_file = os.path.join(original_images_dir, file)
        label_file = os.path.join(original_labels_dir, file.replace('.jpg', '.txt'))
        shutil.copy(image_file, dest_dir['images'])
        shutil.copy(label_file, dest_dir['labels'])

# Copy files to the new directory structure
copy_files(train_files, original_images_dir, new_structure['train'])
copy_files(val_files, original_images_dir, new_structure['val'])
copy_files(test_files, original_images_dir, new_structure['test'])


import os
import shutil

# Define the paths for folder1, folder2, and folder4
folder1_path = 'folder1'
folder2_path = 'folder3'
folder4_path = 'folder4'

# Create directories if they don't exist
for directory_type in ['train', 'valid', 'test']:
    os.makedirs(os.path.join(folder4_path, directory_type, 'images'), exist_ok=True)
    os.makedirs(os.path.join(folder4_path, directory_type, 'labels'), exist_ok=True)

# Function to merge files from folder1 and folder2 and copy to folder4
def merge_and_copy(folder1, folder2, folder4):
    for directory_type in ['train', 'valid', 'test']:
        for image_label_type in ['images', 'labels']:
            folder1_files = os.listdir(os.path.join(folder1, directory_type, image_label_type))
            folder2_files = os.listdir(os.path.join(folder2, directory_type, image_label_type))
            for file in folder1_files:
                src_file = os.path.join(folder1, directory_type, image_label_type, file)
                dst_file = os.path.join(folder4, directory_type, image_label_type, file)
                shutil.copy(src_file, dst_file)
            for file in folder2_files:
                src_file = os.path.join(folder2, directory_type, image_label_type, file)
                dst_file = os.path.join(folder4, directory_type, image_label_type, file)
                shutil.copy(src_file, dst_file)


# Merge and copy files from folder1 and folder2 to folder4
merge_and_copy(folder1_path, folder2_path, folder4_path)

print("Files merged and copied successfully.")

print(len(os.listdir('/content/folder1/train/images')), len(os.listdir('/content/folder3/train/images')),len(os.listdir('/content/folder4/train/images')))
# (465, 20860, 21325)
print(len(os.listdir('/content/folder1/test/images')), len(os.listdir('/content/folder3/test/images')),len(os.listdir('/content/folder4/test/images')))
# (67, 4470, 4537)
print(len(os.listdir('/content/folder1/valid/images')), len(os.listdir('/content/folder3/valid/images')),len(os.listdir('/content/folder4/valid/images')))
# (133, 4470, 4603)
