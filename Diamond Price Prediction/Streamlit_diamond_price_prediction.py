import pickle
import pandas as pd
import numpy as np
import streamlit as st

## import Pickle Files
with open ('pipline.pkl','rb') as f:
    pipeline= pickle.load(f)

with open('preprocessor.pkl','rb') as f:
    preprocessor=pickle.load(f)

with open('KMeans.pkl','rb') as f:
    kmeans=pickle.load(f)

st.title('💍DIAMOND PRICE PREDICTION SYSTEM💍')
st.header("📝Instructions")
st.markdown("#### 🗄️Enter the values below for the Price Prediction")
##Data Input
cut=st.selectbox('Cut',['Fair','Good','Very Good','Premium','Ideal'])
color=st.selectbox('Color',['J','I','H','G','F','E','D'])
clarity=st.selectbox('Clarity',['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF'])
carat_category=st.selectbox('Carat Category',['light','medium','heavy'])
carat=st.number_input('Carat',0.2,2.0)
depth=st.number_input('Depth',55.0,65.0,step=0.5)
table=st.number_input('Table',50.0,65.0,step=0.5)
x=st.number_input('x',3.5,10.0,step=0.5)
y=st.number_input('y',3.5,10.0,step=0.5)
z=st.number_input('z',1.0,6.0,step=0.5)
volume=st.number_input('Volume',30,350,step=10)
price_per_carat=st.number_input('Price Per Carat',1000,9000,step=100)
dimension_ratio=st.number_input('Dimension Ratio',1.500,1.700)

input_df=pd.DataFrame({'carat':[carat],
                        'cut':[cut],
                        'color':[color],
                        'clarity':[clarity],
                        'depth':[depth],
                        'table':[table],
                        'x':[x],
                        'y':[y],
                        'z':[z],
                        'volume':[volume],
                        'price_per_carat':[price_per_carat],
                        'dimension_ratio':[dimension_ratio],
                        'carat_category':[carat_category]})

## Regression										
predict_price=st.button("Predict Price")
if predict_price:
    regression_output=pipeline.predict(input_df)
    price_output=np.round(np.expm1(regression_output),2)
    st.write("Diamond Price:",price_output)

## Clustering
predict_cluster=st.button('Predict Cluster')
if predict_cluster:
    pre_input_data=preprocessor.transform(input_df)
    cluster_num=kmeans.predict(pre_input_data)
    if cluster_num==0:
        cluster_name="Premium Heavy Diamonds"
    elif cluster_num==1:
        cluster_name="Affordable Small Diamonds"
    st.write('Cluster Name:',cluster_name)
    st.write('Cluster Number:',cluster_num)

# Feedback
st.markdown("#### Rating:")
feedback=st.feedback("stars")
if feedback is not None:
    st.markdown("##### 💐Thank You for Rating✨")