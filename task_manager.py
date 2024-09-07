import hashlib
from tinydb import TinyDB, Query
from getpass import getpass
import os
import re

db = TinyDB('db.json')
Task = Query()
User = Query()

def register():
    User = Query()
    username = input("Introduce tu nombre de usuario: ")
    password = input("Introduce tu contraseña: ")
    md5_password = hashlib.md5(password.encode()).hexdigest()

    if db.search(User.nombre == username):
        print("El usuario ya existe. Intenta con otro nombre de usuario.")
        return
        
    db.insert({'nombre': username, 'contraseña': md5_password})
    print("Usuario registrado exitosamente!")

def go_back_to_menu():
    pattern_out = re.compile(r"^(s|si|sí)$", re.IGNORECASE)
    while True:
        choice = input("Volver a menú (S/N): ")
        if pattern_out.match(choice):
            os.system('cls')
            main_menu()

def authenticate():
    users_table = db.table('users')
    user = input("Usuario: ")
    password = getpass("Contraseña: ")
    md5_password = hashlib.md5(password.encode()).hexdigest()
    result  = users_table.search((User.nombre == user) & (User.password == md5_password))
    if result:
        print("Acceso concedido\n")
    else:
        print("Acceso denegado")
        exit()

def add_task():
    os.system('cls')
    title = input("Titulo de la tarea: ")
    description = input("Descripcion de la tarea: ")
    due_date = input("Fecha de vencimiento (yyyy-mm-dd): ")
    tag = input("Etiqueta: ")
    db.insert({
        'title': title,
        'description': description,
        'due_date': due_date,
        'tag': tag,
        'status': 'Pendiente'
    })
    print(f"Tarea '{title}' añadida.\n")
    go_back_to_menu()

def show_tasks():
    os.system('cls')
    tasks = db.all()
    if tasks:
        for task in tasks:
            print(f"{task['title']} - {task['status']} - {task['due_date']} - {task['tag']}")
    else:
        print("No hay tareas registradas.\n")
    go_back_to_menu()

def update_task_status():
    os.system('cls')
    title = input("Ingrese el título de la tarea a actualizar: ")
    new_status = input("Nuevo estado (Pendiente, En progreso, Completada): ")
    if new_status in ['Pendiente', 'En progreso', 'Completada']:
        updated = db.update({'status': new_status}, Task.title == title)
        if updated:
            print(f"Estado de '{title}' actualizado a {new_status}.\n")
        else:
            print("Tarea no encontrada.\n")
    else:
        print("Estado no valido. Los estados válidos son 'Pendiente', 'En progreso', 'Completada'.\n")
    go_back_to_menu()

def main_menu():
    while True:    
        
        print("1. Añadir tarea")
        print("2. Mostrar tareas")
        print("3. Actualizar estado de tarea")
        print("4. Salir")
        choice = input("Seleccione una opcion: ")
        if choice == '1':
            add_task()
        elif choice == '2':
            show_tasks()
        elif choice == '3':
            update_task_status()
        elif choice == '4':
            print("Saliendo del sistema.")
            break
        else:
            print("Opcion no válida. Intente de nuevo.\n")

if __name__ == '__main__':
    print("Bienvenido al Sistema de Gestion de Tareas")
    authenticate()
    main_menu()