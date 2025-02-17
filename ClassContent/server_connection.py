import requests
import random
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

url = 'http://localhost:8080/tienda/run-sql-query/'



def insertar_fibonacci(n=100):
    a,b = 0,1

    for i in range(0, n):
        err = random.randrange(-1000,1000)/1000
        a, b = b, a+b
        a_err = a+err

        make_query(f'INSERT INTO tienda_fibonacci (Fibonaccic, Conruido, Error) VALUES ({a}, {a_err}, {err});')


def make_query(query):
    data = {
    'query': query
    }
    try:
        response = requests.post(url, json=data)
        res = []
        if response.status_code == 200:
            result = response.json()
            print("Query Result:")
            for row in result:
                res.append(row)

            return res
        else:
            print(f"Failed to execute query. Status code: {response.status_code}")
            print(f"Error: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


#insertar_fibonacci(100)
#make_query("SELECT * FROM tienda_fibonacci")

def graficar_datos():
    resultados = make_query("SELECT * FROM tienda_fibonacci")
    
    n = []
    Fibonacci = []
    Conruido = []
    Error = []
    # Procesar los resultados

    #print(resultados)
    for fila in resultados:
        n.append(fila['id'])             # ID (n)
        Fibonacci.append(fila['fibonaccic'])     # Serie de Fibonacci
        Conruido.append(fila['conruido'])      # Valor serie con ruido
        Error.append(fila['error'])         # Error
    # Cerrar la conexión
    # Graficar los resultados
    plt.figure(figsize=(10, 6))
    # Graficar serie de Fibonacci
    plt.plot(n, Fibonacci, label="Serie (Fibonacci)", marker='o')
    plt.plot(n, Conruido, label="Con error (Conerror)", marker='x')
    # Graficar error
    plt.plot(n, Error, label="Error", linestyle='--', color='red')
    # Personalización del gráfico
    plt.title("SERIE DE FIBONACCI")
    plt.xlabel("ID (n)")
    plt.ylabel("Valores de la serie")
    plt.legend()
    plt.grid(True)
    # Mostrar el gráfico
    plt.show()




def limpiar_canvas():
    for widget in frame_canvas.winfo_children():
        widget.destroy()

# Función para leer y graficar los datos de la tabla regfibonacci
def graficar_interfaz():
    try:
        # Limpiar el canvas antes de dibujar el nuevo gráfico
        limpiar_canvas()

        resultados = make_query("SELECT * FROM tienda_fibonacci")

        # Listas para almacenar los datos
        n = []
        Fibonacci = []
        Conruido = []
        Error = []

        for fila in resultados:
            n.append(fila['id'])             # ID (n)
            Fibonacci.append(fila['fibonaccic'])     # Serie de Fibonacci
            Conruido.append(fila['conruido'])      # Valor serie con ruido
            Error.append(fila['error'])     
        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(8, 6))

        # Graficar Serie de Fibonacci y Serie de Fibonacci con Ruido
        ax.plot(n, Fibonacci, label="Serie (Fibonacci)", marker='o')
        ax.plot(n, Conruido, label="Con ruido (Conerror)", marker='x')

        # Graficar error
        ax.plot(n, Error, label="Error", linestyle='--', color='red')

        # Personalización del gráfico
        ax.set_title("SERIE DE FIBONACCI")
        ax.set_xlabel("ID (n)")
        ax.set_ylabel("Valores de La Serie")
        ax.legend()
        ax.grid(True)

        # Mostrar el gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, master=frame_canvas)
        canvas.draw()
        canvas.get_tk_widget().pack()

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Crear la ventana principal con Tkinter
root = Tk()
root.title("SERIE DE FIBONACCI")
root.geometry("800x600")

# Frame para entradas de datos
frame_inputs = Frame(root)
frame_inputs.pack(pady=10)

# Etiquetas y entradas de datos
Label(frame_inputs, text="Número de términos").grid(row=1, column=0, padx=5, pady=5)
entry_terminos = Entry(frame_inputs)
entry_terminos.grid(row=1, column=1, padx=5, pady=5)

# Frame para los botones
frame_botones = Frame(root)
frame_botones.pack(pady=10)

# Botón para insertar valores
btn_insertar = Button(frame_botones, text="Insertar valores", command=insertar_fibonacci)
btn_insertar.grid(row=0, column=0, padx=5)

# Botón para graficar datos
btn_graficar = Button(frame_botones, text="Graficar datos", command=graficar_datos)
btn_graficar.grid(row=0, column=1, padx=5)

# Frame para gráficos
frame_canvas = Frame(root)
frame_canvas.pack(pady=20)

# Ejecutar la aplicación
root.mainloop()

# Ejemplo de uso del script
if __name__ == "__main__":
    graficar_interfaz()
