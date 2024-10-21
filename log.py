import datetime

def Print(msg):
    # Obtener el timestamp actual
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Imprimir el resultado
    print(f"{timestamp} - {msg}")