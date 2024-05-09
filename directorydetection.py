import os

def get_last_folder(directory_path):
    try:
        # List all items in the directory
        items = os.listdir(directory_path)

        # Filter out only directories
        folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]

        if folders:
            # Return the name of the last folder
            return folders[-1]
        else:
            return None
    except OSError as e:
        print(f"Error accessing directory: {e}")
        return None

# Specify the directory path you want to check
directory_path = 'yolov5/runs/predict-seg'

# Call the function to get the name of the last folder
last_folder = get_last_folder(directory_path)

if last_folder is not None:
    print(f"Name of the last folder in {directory_path}: {last_folder}")
else:
    print("Folder detection failed.")
