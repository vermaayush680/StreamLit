import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
import pandas as pd
from tensorflow import keras
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from keras.preprocessing import image
from PIL import Image
import streamlit as st

#Function to load uploaded image
def load_image(image_file):
	img = Image.open(image_file)
	return img
# Function to check the image
def check():

    lr = keras.models.load_model('weights.h5')
    #Prediction Pipeline
    class Preprocessor(BaseEstimator, TransformerMixin):
        def fit(self,img_object):
            return self
        
        def transform(self,img_object):
            img_array = image.img_to_array(img_object)
            expanded = (np.expand_dims(img_array,axis=0))
            return expanded

    class Predictor(BaseEstimator, TransformerMixin):
        def fit(self,img_array):
            return self
        
        def predict(self,img_array):
            probabilities = lr.predict(img_array)
            predicted_class = ['Buffalo', 'Elephant', 'Rhino', 'Zebra'][probabilities.argmax()]
            return predicted_class

    full_pipeline = Pipeline([('preprocessor',Preprocessor()),
                            ('predictor',Predictor())])
    return full_pipeline

def output(full_pipeline,img):
   a=  img
   #a = img.decode('utf-8', 'ignore') 
   a= a.resize((256,256))
   predic = full_pipeline.predict(a)
   return(predic)

def main():
   # giving a title
   st.set_page_config(page_title='African Wildlife', page_icon='favicon.png')
   st.title('African Wildlife Animal Classifier')
   st.subheader('Upload either Buffalo/Elephant/Rhino/Zebra image for prediction')
   image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
   # code for Prediction
   prediction = ''

   # creating a button for Prediction

   if st.button('Predict'):
     if image_file is not None:
         # To See details
         with st.spinner('Loading Image and Model...'):
            full_pipeline = check()
         file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
         st.write(file_details)
         img = load_image(image_file)
         st.image(img,width=256)
         with st.spinner('Predicting...'):
            prediction = output(full_pipeline,img)
         st.success(prediction)
if __name__ == '__main__':
    main()
