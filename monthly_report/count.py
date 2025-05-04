import os

def count_images_in_folders(folders, image_extensions=None):
    base_path = os.getcwd()  # Automatically use the current directory

    if image_extensions is None:
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

    image_counts = {}

    for folder in folders:
        folder_path = os.path.join(base_path, folder)
        count = 0
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                ext = os.path.splitext(filename)[1]
                if ext in image_extensions:
                    count += 1
        image_counts[folder] = count

    return image_counts

# Example usage
folders = ["civil", "hvac", "electric", "garden", "cleaning", "mech"]
result = count_images_in_folders(folders)
print(result)
