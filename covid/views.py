#aqui estarn todas las rutas que tienen que ver con la aplicacion covid

from covid import app

@app.route('/')
def index():
    return 'Flask está funcionado desde views'