from fastapi import FastAPI,UploadFile, File
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os 

app = FastAPI()

# เพิ่ม middleware เพื่ออนุญาตให้เข้าถึงจาก origin ของคุณ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

class PredictionResult(BaseModel):
    predictions: str
    accuracy: float

@app.get("/")
def hello():
    return {"API":"API is working fine"}

@app.post("/predict")
async def upload_image(img_file:UploadFile =File(...)):

    if '.jpg' in img_file.filename or '.jpeg' in img_file.filename or '.png' in img_file.filename:
        file_save_path="./images/"+img_file.filename
        if os.path.exists("./images") == False:
            os.makedirs("./images")

        with open(file_save_path, "wb") as f:
            f.write(img_file.file.read())

        if os.path.exists(file_save_path):
            # return {"image_path":file_save_path,"message": "Image saved successfully"}

            predictions = "normal"
            accuracy = 100

            result = PredictionResult(predictions=predictions, accuracy=accuracy)
            return result
        else:
            return {"error":"Image Not saved !!!"}
    else:
        return {"error": "File Type is not valid please upload only jpg,jpeg and png"}

if __name__=="__main__":
    uvicorn.run(app)
