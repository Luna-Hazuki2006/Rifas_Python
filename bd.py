import pymongo

cliente = pymongo.MongoClient('mongodb+srv://lunahazuki2006:cXU0lYhSncWZ12FM@cluster0.owjghpf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

db = cliente.Rifas

Tickets = db.Tickets
Rifas = db.Rifas
