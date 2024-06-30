from fastapi import FastAPI, UploadFile, File
import os
import shutil
from pywhispercpp.model import Model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["Content-Disposition"],
)

w = Model('medium')
UPLOAD_DIR="/tmp"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)
    
@app.post('/transcribe')
async def transcriptions(file: UploadFile = File(...)):
    filename = file.filename
    fileobj = file.file
    upload_name = os.path.join(UPLOAD_DIR, filename)
    upload_file = open(upload_name, 'wb+')
    shutil.copyfileobj(fileobj, upload_file)
    upload_file.close()
    
    result = w.transcribe(upload_name)
    text = ' '.join(s.text for s in result)
    
    return text
