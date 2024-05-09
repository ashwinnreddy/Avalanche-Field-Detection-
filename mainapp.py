import streamlit as st
from roboflow import Roboflow
import supervision as sv
import cv2
import numpy as np
import PIL


def main():
    st.title("Avalanche Prediction")

    # Initialize Roboflow client
    rf = Roboflow(api_key="pjZtbsAzjhkBsKvruel1")
    project = rf.workspace().project("avalert")
    model = project.version(1).model

    # File uploader for user to upload an image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    # st.text(uploaded_file.name)

    if uploaded_file is not None:
        # Display the uploaded image
        uploaded_image = PIL.Image.open(uploaded_file)
        st.image(uploaded_image, caption="Uploaded Image",
                    use_column_width=True)
        if st.button("Predict"):

            result = model.predict(uploaded_file.name, confidence=40).json()

            labels = [item["class"] for item in result["predictions"]]

            detections = sv.Detections.from_roboflow(result)

            label_annotator = sv.LabelAnnotator()
            mask_annotator = sv.MaskAnnotator()

            # image = cv2.imread("your_image.jpg")

            annotated_image = mask_annotator.annotate(
                scene=uploaded_image, detections=detections)
            annotated_image = label_annotator.annotate(
                scene=annotated_image, detections=detections, labels=labels)

            sv.plot_image(image=annotated_image, size=(16, 16))

            # Display the annotated image
            st.image(annotated_image, caption='Annotated Image', use_column_width=True)

if __name__ == "__main__":
    main()
