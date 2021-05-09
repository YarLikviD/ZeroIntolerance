from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return FileResponse('app/static/index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
