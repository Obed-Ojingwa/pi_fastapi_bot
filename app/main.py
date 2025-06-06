
### File: app/main.py

from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .pi_worker import process_all_seeds
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/templates"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def form_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/transfer")
async def transfer(request: Request, bg: BackgroundTasks):
    data = await request.json()
    seeds = [s.strip() for s in data["seeds"].split(",") if s.strip()]
    destination = data["owner"]
    amount = float(data["amount"])

    results = await process_all_seeds(seeds, destination, amount)
    return JSONResponse({"results": results})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

