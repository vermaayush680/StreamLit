import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from tensorflow import keras
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from keras.preprocessing import image
from PIL import Image
import streamlit as st

def load_image(image_file):
	img = Image.open(image_file)
	return img

def check(img):

    lr = keras.models.load_model('weights.h5')
    print('loaded')
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

    a=  img
    #a = img.decode('utf-8', 'ignore') 
    a= a.resize((256,256))
    predic = full_pipeline.predict(a)
    return(predic)

def main():
    # giving a title
    st.title('African Wildlife Animal Classifier')
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
    # code for Prediction
    prediction = ''

    # creating a button for Prediction
    
    if st.button('Predict'):
        if image_file is not None:
            # To See details
            file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
            st.write(file_details)
            img = load_image(image_file)
            st.image(img,width=256)
            prediction = check(img)
            
        st.success(prediction)
if __name__ == '__main__':
    main()
