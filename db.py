from tkinter import *
import sqlite3 

root = Tk()
root.title('Hola mundo: todo list')
root.geometry('400x400')

#REALIZANDO CONEXION CON SQLITE3 
conn = sqlite3.connect('todo.db') 

#CREANDO EL CURSOR CON SQLITE3, CON EL CUAL PODEMOS EJERCER LLAMADOS A LAS BASES DE DATOS
c = conn.cursor()

#CREANDO LAS REGLAS DE LAS TABLAS CON SQLITE3 
c.execute("""
    CREATE TABLE if not exists todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        description TEXT NO NULL,
        completed BOOLEAN NOT NULL
    );
""")

conn.commit()

#CREANDO UNA FUNCION PARA ELIMINAR LAS TAREAS 
def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id,))
        conn.commit()
        render_todos()

    return _remove

#FUNCION PARA MARCAR LAS TAREAS COMO COMPLETADAS AQUI APLICAMOS UNA TECNICA LLAMADA CURRYING DONDE ANIDAMOS FUNCIONES PARA PODER EVITAR ERRORES CON EL USO DE LAMBDA
def complete(id):
    def _complete():
        todo = c.execute("SELECT * from todo WHERE id = ?", (id,)).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?", (not todo[3], id))
        conn.commit()
        render_todos()

    return _complete

#RENDERIZANDO LOS TODOS
def render_todos():
    rows = c.execute("SELECT * FROM todo").fetchall()

    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#99A3A4' if completed else "#555555"
        ck = Checkbutton(frame, text=description, fg=color, width=42, anchor='w', command=complete(id))
        ck.grid(row=i, column=0, sticky='w')
        btn = Button(frame, text="Eliminar", command=remove(id))
        btn.grid(row=i, column=1)
        ck.select() if completed else ck.deselect()

#CREANDO FUNCION PARA AGREGAR TAREAS
def addTodo():
    todo = e.get()
    if todo:
        c.execute("""
                  INSERT INTO todo (description, completed) VALUES (?,?)
                  """, (todo, False))
        conn.commit()
        e.delete(0, END)
        render_todos()
    else:
        pass


#CREANDO LA PARTE VISUAL DE LA APLICACION
l = Label(root, text='Tarea')
l.grid(row=0, column=0)

e = Entry(root, width=40)
e.grid(row=0,column=1)

btn = Button(root, text='Agregar', command=addTodo)
btn.grid(row=0, column=2)

#CREANDO EL FRAME
frame = LabelFrame(root, text='Mis tareas', padx=5, pady=5)
frame.grid(row=1, column=0, columnspan=3, sticky='nswe', padx=5)

e.focus()

root.bind('<Return>', lambda x: addTodo())

render_todos()

root.mainloop()

