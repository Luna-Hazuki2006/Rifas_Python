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

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.middleware("http")
async def create_auth_header(request: Request, call_next,):
    '''
    Check if there are cookies set for authorization. If so, construct the
    Authorization header and modify the request (unless the header already
    exists!)
    '''
    if ("Authorization" not in request.headers 
        and "Authorization" in request.cookies
        ):
        access_token = request.cookies["Authorization"]
        
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer {access_token}".encode(),
            )
        )
    elif ("Authorization" not in request.headers 
        and "Authorization" not in request.cookies
        ): 
        request.headers.__dict__["_list"].append(
            (
                "authorization".encode(),
                 f"Bearer 12345".encode(),
            )
        )
        
    response = await call_next(request)
    return response    

@app.get("/")
async def obtener(request : Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/cambio')
async def mandar(request : Request): 
    pass