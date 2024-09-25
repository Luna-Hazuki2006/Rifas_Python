from bd import Rifas, Jugadores
from Rifa.schemas import Rifa, EmailSchema
from Ticket.schemas import Ticket
from datetime import datetime
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from secrets import choice

conf = ConnectionConfig(
    MAIL_USERNAME = "empresamariamoonlit72@gmail.com",
    MAIL_PASSWORD = "qmoz cnct ebek jnkn",
    MAIL_FROM = "empresamariamoonlit72@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_FROM_NAME="Rifas rápidas",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

porcia = 'https://static.wixstatic.com/media/28278e_0be5524cac4f423982fde05be7123be0~mv2.jpg/v1/fill/w_700,h_560,al_c,q_85,enc_auto/28278e_0be5524cac4f423982fde05be7123be0~mv2.jpg'

def registrar_rifas(rifa : Rifa): 
    if Rifas.find_one({'codigo' : rifa.codigo}): 
        return 'Ese código ya existe, ¡intente otro!'
    for i in range(rifa.primer_numero, rifa.cantidad_tickets + rifa.primer_numero): 
        ticket = Ticket(numero=i)
        rifa.tickets.append(dict(ticket))
    if Rifas.insert_one(dict(rifa)).inserted_id: 
            # if Tickets.insert_one(dict(ticket)).inserted_id: continue
            # return 'Hubo un problema en la creación de tickets'
        return rifa
    return 'No se pudo registrar la rifa'

def buscar_tiempo(fecha : datetime): 
    if fecha <= datetime.now(): return False
    tiempo = fecha - datetime.now()
    if tiempo.seconds < 0: 
        return False
    if tiempo.days < 1: 
        data = (tiempo.seconds / 60) / 60
        tiempo = f'{data} horas'
    else: 
        tiempo = f'{tiempo.days} días'
    return tiempo

def buscar_rifa(codigo : str): 
    este = Rifas.find_one({'codigo': codigo})
    este = Rifa(
        codigo=este['codigo'], 
        premio=este['premio'], 
        creador=este['creador'], 
        inicio=este['inicio'], 
        final=este['final'], 
        cantidad_tickets=este['cantidad_tickets'], 
        primer_numero=este['primer_numero'], 
        sorteo=este['sorteo'], 
        monto_venta=este['monto_venta'], 
        participantes=este['participantes'], 
        tickets=este['tickets'], 
        ganado=este['ganado']
    )
    return este

async def sortear_rifa(codigo : str): 
    if Rifas.find_one({'codigo': codigo}) == None: return False
    rifa = buscar_rifa(codigo)
    ganador = choice(rifa.tickets)
    i = rifa.tickets.index(ganador)
    rifa.tickets[i]['ganador'] = True
    rifa.ganado = True
    Rifas.replace_one({'codigo': codigo}, dict(rifa))
    for esto in rifa.participantes: 
        jugador = Jugadores.find_one({'cedula': esto})
        emailFinal = EmailSchema(
            email= [
                jugador['correo']
            ]
        )
        if ganador['estatus'] == False: 
            html = f"""
<h1>Fin de la rifa</h1>
<p>
    Gracias por jugar en la rifa {rifa.codigo} <br>
    Tristemente como en la vida, esta rifa no tuvo un ganador. <br>
    ¡Pero no te desanimes! Puedes seguir jugando en https://rifas-python.onrender.com/ <br>
    <img src="{porcia}" alt="{porcia}">
</p>
"""
        elif ganador['estatus'] != jugador['cedula']: 
            html = f"""
<h1>Fin de la rifa</h1>
<p>
    Gracias por jugar en la rifa {rifa.codigo} <br>
    Tristemente como en la vida, usted no ha ganado en esta rifa. <br>
    ¡Pero no te desanimes! Puedes seguir jugando en https://rifas-python.onrender.com/ <br>
    <img src="{porcia}" alt="{porcia}">
</p>
"""
        elif ganador['estatus'] == jugador['cedula']: 
            html = f'''
<h1>¡Fin de la rifa!</h1>
<p>
    Gracias por jugar en la rifa {rifa.codigo} <br>
    Hay veces que uno gana y otras en las que se pierde... ¡Y usted ganó! <br>
    ¡Ahora puede disfrutar de su premio! <br>
    <img src="{rifa.premio}" alt="{rifa.premio}">
    ¿Quieres volver a ganar? Puedes seguir jugando en https://rifas-python.onrender.com/
</p>
'''
        else: 
            html = f'''
<h1>¡Fin de la rifa!</h1>
<p>
    ... Y algo muy extrañó acaba de pasar <br>
    <img src="{porcia}" alt="{porcia}">
    Juega más en https://rifas-python.onrender.com/
</p>
'''
        message = MessageSchema(
            subject="Fin de la rifa",
            recipients=emailFinal.model_dump().get('email'),
            body=html,
            subtype=MessageType.html)

        fm = FastMail(conf)
        print("Avisos fastmail: ", fm)
        await fm.send_message(message)
    return rifa

def listar_rifas(): 
    lista = []
    for esto in Rifas.find({}): 
        lista.append(buscar_rifa(esto['codigo']))
    return lista

def listar_rifas_actuales(): 
    hoy = datetime.now()
    lista = []
    for esto in Rifas.find({}): 
        if hoy < esto['final']: 
            lista.append(buscar_rifa(esto['codigo']))
    return lista 

def listar_rifas_creadas(creador : str): 
    lista = []
    for esto in Rifas.find({'creador': creador}): 
        lista.append(buscar_rifa(esto['codigo']))
    return lista

def listar_rifas_participadas(participante : str): 
    lista = []
    for esto in Rifas.find({'participantes': [participante]}): 
        lista.append(buscar_rifa(esto['codigo']))
    return lista

def revisar_codigo(codigo : str): 
    if Rifas.find_one({'codigo' : codigo}): return False
    return True