from fastapi import FastAPI, Form,Request
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class PredictionForm(BaseModel):
    gender: str = Field(..., min_length=1) 
    ethnicity: str = Field(..., min_length=1) 
    parental_level_of_education: str = Field(..., min_length=1)  
    lunch: str = Field(..., min_length=1) 
    test_preparation_course: str = Field(..., min_length=1) 
    reading_score: float = Field(..., ge=0, le=100) # Score should be between 0 and 100
    writing_score: float = Field(..., ge=0, le=100) 




@app.get('/',response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("index.html",{"request": request})
@app.get('/predictdata',response_class=HTMLResponse)
async def predict_landing(request:Request):
    return templates.TemplateResponse("home.html",{"request": request})

@app.post('/predictdata',response_class=HTMLResponse)
async def  predict_datapoint(
    request: Request,
    gender:str = Form(...),
    ethnicity: str = Form(...),
    parental_level_of_education: str = Form(...),
    lunch: str = Form(...),
    test_preparation_course: str = Form(...),
    reading_score: float = Form(...),
    writing_score: float = Form(...),

):
    data = CustomData(
        gender=gender,
        race_ethnicity=ethnicity,
        parental_level_of_education=parental_level_of_education,
        lunch=lunch,
        test_preparation_course=test_preparation_course,
        reading_score=reading_score,
        writing_score=writing_score,
    )
    pred_df=data.get_data_as_data_frame()
    predict_pipeline=PredictPipeline()
    results=predict_pipeline.predict(pred_df)
    return templates.TemplateResponse("home.html", {"request": request, "results": results[0]})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)