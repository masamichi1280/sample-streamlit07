import streamlit as st
import requests
import io
from PIL import Image
from PIL import ImageDraw

st.title('顔認識アプリ')

subscription_key  = '8a93ee1742524393b229b209595ede7e'

assert subscription_key 

face_api_url=  'https://20210701masa.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an image...", type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)

    with io.BytesIO() as output:
        img.save(output,format="JPEG")
        binary_img= output.getvalue()#バイナリ取得

    headers = {
        'Content-Type':'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }


    params = {
    'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,smile,facialHair,headPose,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    res= requests.post(face_api_url, params=params,headers=headers, data=binary_img)

    results= res.json()
    for result in results:
        
        rect=result['faceRectangle']


        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=5)



    st.image(img,caption='Uploaded Image.' ,use_column_width=True)

