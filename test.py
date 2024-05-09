import streamlit as st
import subprocess
from PIL import Image

def run_your_code(image_path):
    command = f"python yolov5/segment/predict.py --weights yolov5/best.pt --img 320 --source {image_path} --hide-labels"
    #          f"python yolov5/segment/predict.py --weights /best (3).pt --img 320 --source {image_path}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Display the result in the Streamlit app
    st.text(result.stdout)
    st.text(result.stderr)

    # Display the annotated image
    #annotated_image_path = image_path.replace('.jpg', '_detected.jpg')  # Adjust the path as per your naming convention
    #annotated_image = Image.open(annotated_image_path)
    #st.image(annotated_image, caption="Annotated Image.", use_column_width=True)

st.title("Run YOLOv5 Code with Image Upload")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Check if a file is uploaded
if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

    # Add a button to run the YOLOv5 code with the uploaded image
    if st.button("Run YOLOv5 Code"):
        # Save the uploaded image to a temporary file
        temp_image_path = "temp_image.jpg"
        image.save(temp_image_path)

        # Run the YOLOv5 code with the temporary image path
        run_your_code(temp_image_path)
