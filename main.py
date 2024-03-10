from fastapi import FastAPI, UploadFile, File
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastai.vision.all import load_learner, PILImage
import os 

app = FastAPI()

# เพิ่ม middleware เพื่ออนุญาตให้เข้าถึงจาก origin ของคุณ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

# model_path = "cctv_model.pth.pth"  # Adjust the path accordingly
# learn = load_learner(model_path)

class PredictionResult(BaseModel):
    predictions: str
    accuracy: float

@app.get("/")
def hello():
    return {"API":"API is working fine"}

@app.post("/predict")
async def upload_image(img_file: UploadFile = File(...)):

    if '.jpg' in img_file.filename or '.jpeg' in img_file.filename or '.png' in img_file.filename:
        file_save_path = "./images/" + img_file.filename
        if os.path.exists("./images") == False:
            os.makedirs("./images")

        with open(file_save_path, "wb") as f:
            f.write(img_file.file.read())

        if os.path.exists(file_save_path):
            # สร้างข้อมูลการทำนาย
            result = PredictionResult(predictions="violence", accuracy=100)
            # ส่งข้อมูลการทำนายกลับไปยังไคลเอนต์
            return result
    return {"error": "Invalid image format"}


if __name__=="__main__":
    uvicorn.run(app)
