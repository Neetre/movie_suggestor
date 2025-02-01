from fastapi import FastAPI, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from movies import get_similar, get_recommendations
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://film.figliolo.it"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/similar")
async def similar(request: Request, title: str = Form(...)):
    recommendations = get_recommendations(title)
    if isinstance(recommendations, pd.Series):
        recommendations = recommendations.tolist()
    return JSONResponse(content=recommendations)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8011)
