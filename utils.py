import numpy as np
import pandas as pd
import streamlit as st

from PIL import Image

def visualization_results(input_format, threshold):
    data = []
    
    input_format = dict(sorted(input_format.items(), key=lambda item: item[1], reverse=True))

    col1, col2 = st.columns([1, 1])
    count = 0
    for i in input_format.items():
        if i[1] >= threshold / 100:
            count += 1
            df = pd.DataFrame()
            data.append([i[0].split('/')[len(i[0].split('/'))-1], i[1]])
            df = df.append(data)
            df = df.rename(columns={0: "Image", 1: "Cosine distance"})

    if count == 0:
        st.info(f"No images for {threshold} or above cosine distance, %")
    else:
        for _, i in enumerate(input_format.items(), 1):
            with col1:
                try:
                    if i[1] >= threshold / 100:
                        not_corr_path = i[0].split('/')
                        path_to_image = '/app/indexes/' + '/'.join([not_corr_path[-i] for i in range(1,4)][::-1])
                        image = Image.open(path_to_image)
                        caption = f"{path_to_image.split('/')[len(path_to_image.split('/'))-1]}, {i[1]}"
                        st.image(image, caption=caption)
                except:
                    pass
            with col2:
                if _ == 1:
                    st.write("Output cosine distance")
                    st.dataframe(df.style.text_gradient(axis=0, cmap='Spectral'))
