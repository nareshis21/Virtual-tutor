import tempfile
import streamlit as st
from PIL import Image
import os
from utils.ingest1 import create_vector_database

def process_uploaded_file():
    st.title("Upload File to Chat")
    uploaded_file = st.file_uploader("File upload", type="pdf")
    if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
    #with open(path, "wb") as f:
    #    f.write(uploaded_file.getvalue())
        print(path)    
        st.write("Document uploaded successfully!")
        # Display the uploaded document
        st.write("Preview of the document:")
        st.write(uploaded_file)

        # Button to start parsing and vector database creation
        if st.button("Start Processing"):
            # Placeholder for processing logic
            st.write("Processing...")

            # Placeholder for progress bar
            with st.spinner('Processing...'):
                # Call your function to parse data and create vector database
                create_vector_database(path)

            st.success("Processing completed!")

            # Display success message
            st.write("Vector database created successfully!")

            # Show success image
            success_image = Image.open("success_image.jpg")
            st.image(success_image, caption="Success!", use_column_width=True)

    # Add a footer
    #st.text("Built with Streamlit")
