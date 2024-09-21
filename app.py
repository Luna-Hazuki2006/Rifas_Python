from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, status, Response, Form, Depends
# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from cliente import router as cliente
from administradores import router as adminis
from Rifa import router as rifas
from Ticket import router as ticket
from login.login import No_Cliente_Exception, No_Administrador_Exception, LoginExpired, RequiresLoginException, AuthHandler

app = FastAPI()

auth_handler = AuthHandler()

app.mount("/static", StaticFiles(directory="./static"), name="static")

templates = Jinja2Templates(directory="./templates")

app.include_router(cliente.router, prefix='/clientes', tags=['Clientes'])
app.include_router(adminis.router, prefix='/admins', tags=['Administradores'])
app.include_router(rifas.router, prefix='/rifas', tags=['Rifas'])
app.include_router(ticket.router, prefix='/tickets', tags=['Tickets'])

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

@app.exception_handler(RequiresLoginException)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return templates.TemplateResponse("message-redirection.html", {"request": request, "message": exc.message, "path_route": exc.path_route, "path_message": exc.path_message})

@app.exception_handler(LoginExpired)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return templates.TemplateResponse("message-redirection.html", {"request": request, "message": exc.message, "path_route": exc.path_route, "path_message": exc.path_message})

@app.exception_handler(No_Administrador_Exception)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return templates.TemplateResponse("message-redirection.html", {"request": request, "message": exc.message, "path_route": exc.path_route, "path_message": exc.path_message})

@app.exception_handler(No_Cliente_Exception)
async def exception_handler(request: Request, exc: RequiresLoginException) -> Response:
    return templates.TemplateResponse("message-redirection.html", {"request": request, "message": exc.message, "path_route": exc.path_route, "path_message": exc.path_message})

@app.get("/")
async def obtener(request : Request): 
    lista = rifas.servicio.listar_rifas_actuales()
    return templates.TemplateResponse('index.html', {
        'request': request, 'rifas': lista, 'token': None})

@app.post('/cambio')
async def mandar(request : Request): 
    pass

@app.post('/cerrar_sesion')
async def cerrar_sesion(request : Request, response : Response, info = Depends(auth_handler.auth_wrapper)): 
    lista = rifas.servicio.listar_rifas_actuales()
    response = templates.TemplateResponse('index.html', {
        'request': request, 'rifas': lista, 'token': info})
    response.delete_cookie(key="Authorization")
    return response