import streamlit as st
import subprocess
from PIL import Image
import os
import time
import re

def run_your_code(image_path):
    command = f"python yolov5/segment/predict.py --weights yolov5/best.pt --img 320 --source {image_path} --hide-labels=True --line-thickness"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    #classes_info = result.stdout.split('\n')
    #return classes_info
    # Display the result in the Streamlit app
    #st.text(result.stdout)
    #st.text(result.stderr)
    #st.text(result.stderr)

    # Extract and display the number of classes dynamically
    matches = re.findall(r"(\d+) Class (\d+)", result.stderr)
    class_number = 0
    totall_trees = 0
    if matches:
        total_trees = sum(int(class_number) for _, count in matches)
        for i, match in enumerate(matches, start=1):
            class_number, count = map(int, match)
            #st.text(f"Number of Trees {count}s: {class_number}")
            totall_trees += class_number
        
        # Display the total number of trees
        st.title(f"Total Number of Trees: {totall_trees}")

#def detect_new_folders(directory, last_check_time):
def detect_new_folders(detect_directory_path):
    try:
        # List all items in the directory
        items = os.listdir(detect_directory_path)

        # Filter out only directories
        folders = [item for item in items if os.path.isdir(os.path.join(detect_directory_path, item))]

        if folders:
            # Return the name of the last folder
            return folders[-1]
        else:
            return None
    except OSError as e:
        print(f"Error accessing directory: {e}")
        return None

st.title("Avalanche Detection")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Add a button to run the YOLOv5 code with the uploaded image
    if st.button("Detect Avalanche"):
        # Save the uploaded image to a temporary file
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)
        last_check_time = time.time()
        # Run the YOLOv5 code with the temporary image path
        run_your_code(temp_image_path)
        #st.text("Classes Information:")
        #for class_info in classes_info:
        #    st.text(class_info)

        # Check for new folders in the 'detect' directory
        detect_directory_path = "yolov5/runs/predict-seg"
        # Set this to the time of the last check

        new_folders = detect_new_folders(detect_directory_path)

        if new_folders:
            #st.text(f"New folders detected in 'detect' directory: {new_folders}")
            #first_folder = new_folders[0]
            image_dir = f"{detect_directory_path}/{new_folders}/temp_image.jpg"
            st.text(image_dir)
            st.image(image_dir, caption="Uploaded Image.", use_column_width=True)
        else:
            st.text("No new folders.")

        #image = Image.open(uploaded_file)
        
