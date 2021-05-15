#aqui estarn todas las rutas que tienen que ver con la aplicacion covid

from covid import app

import csv, json


@app.route('/provincias')
def provincias():
    fichero = open('data/provincias.csv', 'r', encoding='utf8')
    csvreader= csv.reader(fichero, delimiter=',')

    lista = []
    for registro in csvreader:
        dic={'codigo': registro[0], 'valor': registro[1]}
        lista.append(dic)
    
    fichero.close()
    print(lista)
    return json.dumps(lista)

@app.route('/provincia/<codigoProvincia>') #para meter un parametro variable <>
def laprovincia(codigoProvincia):
    fichero = open('data/provincias.csv', 'r', encoding='utf8')
    dictreader= csv.DictReader(fichero,fieldnames=['codigo','provincia'])
    for registro in dictreader:
        if registro['codigo']==codigoProvincia:
            return registro['provincia']

    fichero.close()
    return 'La provincia no existe. Largo de aquí!'

#@app.route('/casos/<year>/<mes>/<dia>')
#def casos(year, mes, dia):
    