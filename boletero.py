import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime
from reportlab.pdfgen import canvas

# 🔹 BD
conn = sqlite3.connect("boletero.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS boletos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT,
    nombre TEXT,
    apellido TEXT,
    precio REAL,
    fecha TEXT
)
""")
conn.commit()

# 🔹 FUNCIONES

def registrar():
    dni = entry_dni.get()
    nombre = entry_nombre.get()
    apellido = entry_apellido.get()
    precio = entry_precio.get()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if dni == "" or nombre == "":
        messagebox.showerror("Error", "Complete datos")
        return

    cursor.execute("INSERT INTO boletos VALUES (NULL,?,?,?,?,?)",
                   (dni, nombre, apellido, precio, fecha))
    conn.commit()

    generar_pdf(dni, nombre, apellido, precio, fecha)
    mostrar_tabla()
    limpiar()

def generar_pdf(dni, nombre, apellido, precio, fecha):
    c = canvas.Canvas(f"boleto_{dni}.pdf")
    c.drawString(100, 750, "BOLETO")
    c.drawString(100, 720, f"DNI: {dni}")
    c.drawString(100, 700, f"Nombre: {nombre} {apellido}")
    c.drawString(100, 680, f"Precio: S/ {precio}")
    c.drawString(100, 660, f"Fecha: {fecha}")
    c.save()

def mostrar_tabla():
    for row in tabla.get_children():
        tabla.delete(row)

    cursor.execute("SELECT * FROM boletos")
    for row in cursor.fetchall():
        tabla.insert("", tk.END, values=row)

def limpiar():
    entry_dni.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_precio.delete(0, tk.END)

# 🔹 INTERFAZ
ventana = tk.Tk()
ventana.title("Boletero Experto")
ventana.geometry("600x500")

tk.Label(ventana, text="DNI").pack()
entry_dni = tk.Entry(ventana)
entry_dni.pack()

tk.Label(ventana, text="Nombre").pack()
entry_nombre = tk.Entry(ventana)
entry_nombre.pack()

tk.Label(ventana, text="Apellido").pack()
entry_apellido = tk.Entry(ventana)
entry_apellido.pack()

tk.Label(ventana, text="Precio").pack()
entry_precio = tk.Entry(ventana)
entry_precio.pack()

tk.Button(ventana, text="Registrar Boleto", command=registrar).pack(pady=10)

# 🔹 TABLA
tabla = ttk.Treeview(ventana, columns=("ID","DNI","Nombre","Apellido","Precio","Fecha"), show="headings")

for col in ("ID","DNI","Nombre","Apellido","Precio","Fecha"):
    tabla.heading(col, text=col)

tabla.pack(expand=True, fill="both")

mostrar_tabla()

ventana.mainloop()