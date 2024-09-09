import hashlib
from tinydb import TinyDB, Query
from getpass import getpass
import os
import re
from datetime import datetime

db = TinyDB('db.json')
Task = Query()
User = Query()
users_table = db.table('users')
tasks_table = db.table('tasks')
archived_tasks = db.table('archived_tasks')

def register():
    os.system('cls')
    print('Crear cuenta')
    User = Query()
    username = input("Introduce tu nombre de usuario: ")
    password = getpass("Introduce tu contraseña: ")
    md5_password = hashlib.md5(password.encode()).hexdigest()

    # Buscar si el usuario ya existe en la tabla de usuarios
    if users_table.search(User.nombre == username):
        print("El usuario ya existe. Intenta con otro nombre de usuario.")
        input("Presione enter para continuar.")
        return

    # Insertar el nuevo usuario en la tabla de usuarios
    users_table.insert({'nombre': username, 'password': md5_password})
    os.system('cls')
    print("Usuario registrado exitosamente!")
    input("Presione enter para continuar.")

def authenticate():
    os.system('cls')
    print("Inicio de sesión")
    user = input("Usuario: ")
    password = getpass("Contraseña: ")
    md5_password = hashlib.md5(password.encode()).hexdigest()
    result  = users_table.search((User.nombre == user) & (User.password == md5_password))
    if result:
        print("Acceso concedido\n")
        input("Presione enter para continuar.")
    else:
        print("Acceso denegado")
        exit()

def add_task():
    os.system('cls')
    title = input("Titulo de la tarea: ")
    description = input("Descripcion de la tarea: ")
    due_date = input("Fecha de vencimiento (yyyy-mm-dd): ")
    etiquetas = ['dummy','urgente', 'trabajo', 'personal', 'otros']
    print("1. urgente")
    print("2. trabajo")
    print("3. personal")
    print("4. otros")
    tag = input("Seleccione etiqueta: ")
    tasks_table.insert({
        'title': title,
        'description': description,
        'due_date': due_date,
        'tag': etiquetas[int(tag)],
        'status': 'Pendiente'
    })
    print(f"Tarea '{title}' añadida.\n")
    input("Presione enter para continuar.")

def show_tasks():
    os.system('cls')
    tasks = tasks_table.all()
    if tasks:
        for task in tasks:
            print(f"{task['title']} - {task['status']} - {task['due_date']} - {task['tag']}")
    else:
        print("No hay tareas registradas.\n")
    input("Presione enter para continuar.")

def update_task_status():
    os.system('cls')
    statuses = ["Pendiente", "En progreso", "Completada"]
    
    title = input("Ingrese el título de la tarea a actualizar: ")
    result = tasks_table.search(Task.title == title)
    if not result:
        print("No se ha encontrado una tarea con este título")
        input("Presione enter para continuar.")
        return

    while True:
        os.system('cls')
        for (i, item) in enumerate(statuses, start=1):
            print(str(i)+".", item)
        choice = int(input("Seleccione el nuevo estado: "))
        if choice in list( range( 1, len(statuses) + 1) ):
            break
        os.system('cls')
        print("Opción inválida.")
        input("Presione enter para continuar.")

    updated = tasks_table.update({'status': statuses[choice-1]}, Task.title == title)
    if updated:
        print(f"Estado de '{title}' actualizado a {statuses[choice-1]}.\n")
    else:
        print("Ha ocurrido un error.\n")
    input("Presione enter para continuar.")

def delete_task():
    pattern_out = re.compile(r"^(s|si|sí)$", re.IGNORECASE)
    while True:
        # Obtener todos los elementos de la tabla
        tasks = tasks_table.all()
        os.system('cls')
        if tasks:
            t = []
            for task in tasks:
                print(f"{task['title']} - {task['status']} - {task['due_date']} - {task['tag']}")
                t.append(task['title'])

            choice = input("Ingrese título de tarea a eliminar: ")
            if (choice in t):
                erase = input("Eliminar tarea permanentemente? (S/N): ")
                if pattern_out.match(erase):
                    tasks_table.remove(Task.title == choice)
                    os.system('cls')
                    print('Tarea Eliminada')
                    input("Presione enter para continuar.")
                    return
                else:
                    task_to_move = tasks_table.get(Task.title == choice)
                    archived_tasks.insert(task_to_move)
                    tasks_table.remove(Task.title == choice)
                    os.system('cls')
                    print('Tarea guardada en papelera')
                    input("Presione enter para continuar.")
                    return
            else:
                print("No se ha encontrado la tarea")
                choice = input("Volver a menú (S/N): ")
                if pattern_out.match(choice):
                    os.system('cls')
                    return
        
        else:
            print("No hay tareas registradas.\n")
            input("Presione enter para continuar.")
            return

def filter():
    while True:
        os.system('cls')
        print("Elija un parámetro por el que filtrar")
        print("1. Fecha de vencimiento")
        print("2. Etiqueta")
        print("3. Estado")
        print("4. Título")
        print("5. Volver al menú")

        choice = input("Seleccione una opcion: ")
        if choice == '1':
            filter_by_date()
        elif choice == '2':
            filter_by_tag()
        elif choice == '3':
            filter_by_state()
        elif choice == '4':
            filter_by_title()
        elif choice == '5':
            break
        else:
            print("Opcion no válida. Intente de nuevo.\n")

def filter_by_date():
    os.system('cls')
    date_pattern = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")
    
    from_date = input("Desde la fecha (yyyy-mm-dd): ")
    while not date_pattern.match(from_date):
        print("Formato de fecha inválido. Inténtalo de nuevo.")
        from_date = input("Desde la fecha (yyyy-mm-dd): ")
    
    to_date = input("Hasta la fecha (yyyy-mm-dd): ")
    while not date_pattern.match(to_date):
        print("Formato de fecha inválido. Inténtalo de nuevo.")
        to_date = input("Hasta la fecha (yyyy-mm-dd): ")
    
    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
    to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
    
    def search_by_date(date):
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        return from_date_obj <= date_obj <= to_date_obj

    result = tasks_table.search(Task.due_date.test(search_by_date))
    sorted_tasks = sorted(result, key=lambda x: datetime.strptime(x['due_date'], "%Y-%m-%d"))

    os.system('cls')
    if result:
        print("Tareas encontradas:")
        for task in sorted_tasks:
            print(f"{task['title']} - {task['status']} - {task['due_date']} - {task['tag']}")
    else:
        print("No se encontraron tareas dentro de este rango de fechas.")
    input("Presione enter para continuar.")

def filter_by_tag():
    os.system('cls')
    tag = input("Ingrese una etiqueta: ")

    result = tasks_table.search(Task.tag == tag)
    sorted_tasks = sorted(result, key=lambda x: datetime.strptime(x['due_date'], "%Y-%m-%d"))

    os.system('cls')
    if result:
        print("Tareas encontradas:")
        for task in sorted_tasks:
            print(f"{task['title']} - {task['status']} - {task['due_date']} - {task['tag']}")
    else:
        print("No se encontraron tareas con esa etiqueta.")
    input("Presione enter para continuar.")

def filter_by_state():
    os.system('cls')
    statuses = ["Pendiente", "En progreso", "Completada", "Atrasada"]
    
    for (i, item) in enumerate(statuses, start=1):
        print(str(i)+".", item)
    choice = int(input("Seleccione una opcion: "))

    result = tasks_table.search(Task.status == statuses[choice-1])
    sorted_tasks = sorted(result, key=lambda x: datetime.strptime(x['due_date'], "%Y-%m-%d"))

    os.system('cls')
    if result:
        print("Tareas encontradas:")
        for task in sorted_tasks:
            print(f"{task['title']} - {task['status']} - {task['due_date']} - {task['tag']}")
    else:
        print("No se encontraron tareas con ese estado.")
    input("Presione enter para continuar.")

def filter_by_title():
    os.system('cls')
    title = input("Ingrese el título de la tarea: ")

    result = tasks_table.search(Task.title.matches(title, flags=re.IGNORECASE))
    sorted_tasks = sorted(result, key=lambda x: datetime.strptime(x['due_date'], "%Y-%m-%d"))

    os.system('cls')
    if result:
        print("Tareas encontradas:")
        for task in sorted_tasks:
            print(f"{task['title']} - {task['status']} - {task['due_date']} - {task['tag']}")
    else:
        print("No se encontraron tareas con ese título.")
    input("Presione enter para continuar.")

def update_overdue_tasks():
    today = datetime.now()

    tasks = tasks_table.all()

    for task in tasks:
        due_date = datetime.strptime(task['due_date'], "%Y-%m-%d")
        if due_date < today:
            tasks_table.update({'status': 'Atrasada'}, doc_ids=[task.doc_id])

def main_menu():
    while True:     
        os.system('cls')
        print("Sistema de Gestion de Tareas")
        print("1. Añadir tarea")
        print("2. Mostrar tareas")
        print("3. Actualizar estado de tarea")
        print("4. Buscar tareas")
        print("5. Borrar tareas")
        print("6. Salir")
        choice = input("Seleccione una opcion: ")
        if choice == '1':
            add_task()
        elif choice == '2':
            show_tasks()
        elif choice == '3':
            update_task_status()
        elif choice == '4':
            filter()
        elif choice == '5':
            delete_task()
        elif choice == '6':
            print("Saliendo del sistema.")
            exit()
        else:
            print("Opcion no válida. Intente de nuevo.\n")

def user_decision():
    while True:
        os.system('cls')
        print("Sistema de Gestion de Tareas")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        choice = input("Seleccione una opcion: ")
        if choice == '1':
            authenticate()
            return
        elif choice == '2':
            register()
        elif choice == '3':
            print("Saliendo del sistema.")
            exit()
        else:
            os.system('cls')
            print("Opcion no válida. Intente de nuevo.\n")
            input("Presione enter para continuar.")
            

if __name__ == '__main__':
    update_overdue_tasks()
    user_decision()
    main_menu()