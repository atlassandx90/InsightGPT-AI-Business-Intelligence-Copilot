from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="InsightGPT API")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Welcome to InsightGPT API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)