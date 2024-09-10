import os

# List of directories to count images in
directories = ['mech', 'hvac', 'civil', 'electric', 'garden', 'cleaning']

# Supported image file extensions
image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')

def count_images_in_directory(directory):
    """Count the number of image files in a given directory."""
    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(image_extensions):
                count += 1
    return count

def count_images_in_directories(root_directory):
    """Return a dictionary with the count of images in each subdirectory."""
    image_count_dict = {}
    for directory in directories:
        full_path = os.path.join(root_directory, directory)
        if os.path.exists(full_path):
            image_count_dict[directory] = count_images_in_directory(full_path)
        else:
            image_count_dict[directory] = 0  # If the directory does not exist, count is 0
    return image_count_dict

# Running the program from the daily report root directory
if __name__ == "__main__":
    root_directory = os.getcwd()  # Get the current working directory
    image_counts = count_images_in_directories(root_directory)
    print(image_counts)
