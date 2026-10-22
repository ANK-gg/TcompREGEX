from flask import Flask, render_template, request
import re

app = Flask(__name__)

# Expresiones regulares para cada campo del ticket de estacionamiento
PATRONES = {
    'Nombre de dueño': r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$',
    'Tipo de vehiculo': r'^[A-Za-záéíóúÁÉÍÓÚñÑ\s]+$',
    'Modelo de auto': r'^[A-Za-z0-9\s\-]+$',
    'Matricula': r'^([A-Z]{3})(-?)([0-9]{3})$',
    'Fecha': r'^\d{4}-\d{2}-\d{2}$'
}

def analizar_linea(linea):
    if ':' not in linea:
        return None
    
    clave, valor = linea.split(':', 1)
    clave = clave.strip()
    valor = valor.strip()
    
    if clave in PATRONES:
        es_valido = bool(re.match(PATRONES[clave], valor.upper() if clave == 'Matricula' else valor))
        mensaje = "Formato correcto" if es_valido else "Error de formato o caracteres inválidos"
        return {'clave': clave, 'valor': valor, 'valido': es_valido, 'mensaje': mensaje}
    
    return {'clave': clave, 'valor': valor, 'valido': False, 'mensaje': 'Campo no reconocido en el lenguaje'}

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    if request.method == 'POST':
        archivo = request.files.get('archivo')
        if archivo and archivo.filename.endswith('.txt'):
            lineas = archivo.read().decode('utf-8').splitlines()
            for linea in lineas:
                if linea.strip():
                    resultado = analizar_linea(linea)
                    if resultado:
                        resultados.append(resultado)
                        
    return render_template('index.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True, port=5000)