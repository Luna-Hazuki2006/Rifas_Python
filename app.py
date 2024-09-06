from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, status, Response, Form
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="./templates")

@app.get("/")
async def obtener(request : Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/calculado')
async def mandar(request : Request): 
    pass