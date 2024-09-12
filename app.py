from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, status, Response, Form
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from cliente import router as cliente
from administradores import router as adminis
from Rifa import router as rifas
from Ticket import router as ticket

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="./templates")

app.include_router(cliente.router, prefix='/clientes', tags=['Clientes'])
app.include_router(adminis.router, prefix='/admins', tags=['Administradores'])
app.include_router(rifas.router, prefix='/rifas', tags=['Rifas'])
app.include_router(ticket.router, prefix='/tickets', tags=['Tickets'])

@app.get("/")
async def obtener(request : Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/cambio')
async def mandar(request : Request): 
    pass