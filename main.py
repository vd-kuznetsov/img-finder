import torch
import clip
import redis
import streamlit as st
import regex as re

from PIL import Image
from googletrans import Translator
from searchmodel import SearchModel
from embedder import EmbedderCLIP
from dummyindexer import DummyIndexer

from utils import visualization_results

st.set_page_config(page_title="Image Finder",
                   page_icon='⚙',
                   layout="centered",
                   initial_sidebar_state="expanded",
                   menu_items=None)
###

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def init_environment():
  clip_model = SearchModel(EmbedderCLIP(device='cpu'), DummyIndexer())
  db = redis.StrictRedis(host='redishost', charset="utf-8", decode_responses=True)
  
  if db.get('Tour') is None:
      db.set('Tour','trip')
      db.set('Trailer','trailer')
      db.set('Parking','traffic')
	
  return clip_model, db

clip_model, db = init_environment()
translator = Translator()
dict_indexer = {"Tour": db.get('Tour'), "Trailer": db.get('Trailer'), "Parking": db.get('Parking')}

###

with st.expander("About"):
    st.text("""
        Image Finder project.
        
        FAQ:
        1. Select preferred indexer
        2. Select text query or image method for processing
        3. Select output image count
        4. If you want to filter output results, you can use threshold slider
        5. The images will be print with sorting of cosine distance
        
        Models: CLIP
        
        Indexers:
        1. Tour - images from travel
        2. Trailer - video trailer a first film about Harry Potter
        3. Parking - a video where there is a fairly dense traffic of vehicles     
    """)

st.image(Image.open('assets/logo.png'))

indexer = st.selectbox(
    "Select usecase",
    ("Tour", "Trailer", "Parking")
)

st.caption(f"Current usecase: {indexer}")
option = st.selectbox(
    'What would you like to do?',
     ('Text query', 'Image')
)

if option == 'Text query':
    text = st.text_input('Input text query', value = 'Sunset')
else:
    file = st.file_uploader("Choose image", type=['jpeg', 'jpg', 'png'], accept_multiple_files=False)

values = st.slider('Select a range of sample images', 1, 10, 5)
threshold = st.slider('Select a threshold for output images, %', 1, 100, 10)

# Search
if st.button('Start processing'):
    indexer_name = dict_indexer.get(indexer)
    if option == 'Text query' and text:
        if re.findall(r'[а-яА-Я0-9]', text):
            text = translator.translate(text, src = 'ru', dest='en').text
        elif re.findall(r'[a-zA-Z0-9]', text):
            pass
        else:
            st.info(f"Error in query: {text}")
        
        if db.lrange(indexer_name, 0, -1) is None:
            db.lpush(indexer_name, text)
        else:
            db.rpush(indexer_name, text)
        
        st.write(f"Output images for text query: {text}")
        
        model_prefix = 'CLIP'
        clip_model.load_imgs(f"/app/indexes/{indexer_name}/images", model_prefix)
        clip_model.indexer.load(str(clip_model.features_path) + '/features.npy')
        
        query = clip_model.embedder.encode_text(text)
        input_data = clip_model.get_k_imgs(query, values)
        
        input_format = {}
        for i,j in zip(input_data[0], input_data[1]):
            input_format.update({str(j):i})
        
        visualization_results(input_format, threshold)
        st.write(f"Request history by {indexer_name}: {db.lrange(indexer_name, 0, -1)}")
        
    elif option == 'Image' and file is not None:
        model_prefix = 'CLIP'
        clip_model.load_imgs(f"/app/indexes/{indexer_name}/images", model_prefix)
        clip_model.indexer.load(str(clip_model.features_path) + '/features.npy')
        
        image = Image.open(file)
        query = clip_model.embedder.encode_imgs([image])
        st.image(image, caption=file.name)
        st.write(f"Output images for current input image: {file.name}")
        
        input_data = clip_model.get_k_imgs(query, values)
        
        input_format = {}
        for i,j in zip(input_data[0], input_data[1]):
            input_format.update({str(j):i})
        
        visualization_results(input_format, threshold)
        
    else:
        st.info("Error")
