#aqui estarn todas las rutas que tienen que ver con la aplicacion covid

from covid import app

import csv, json

from flask import render_template, request #va a buscar el fichero template


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
    
@app.route('/casos/<int:year>', defaults={'mes':None, 'dia':None})
@app.route('/casos/<int:year>/<int:mes>', defaults={'dia':None})
@app.route('/casos/<int:year>/<int:mes>/<int:dia>')
def casos(year, mes, dia=None):
    if not mes: #tambien se podría poner if dia==None
        fecha = '{:04d}'.format(year)
    elif not dia:
        fecha = '{:04d}-{:02d}'.format(year, mes)
    else:
        fecha= '{:04d}-{:02d}-{:02d}'.format(year, mes, dia) #d es de numero entero, tipo digito. que ponga dos de ocupar dos ditios, y el 0 de delante para que si no son 2 que sea 0 y el valor
    
    #fecha=f'{year}-{mes:02d}-{dia:02d}' esto es lo mismo de lo de arriba
    #tambien con el modulo datetime se puede validar la fecha

    fichero = open('data/casos_diagnostico_provincia.csv', 'r')
    dictreader= csv.DictReader(fichero)

    #se crea el diccionario que se va a querer representar
    res= {
            'num_casos': 0,
    'num_casos_prueba_pcr':0,
    'num_casos_prueba_test_ac': 0,
    'num_casos_prueba_ag': 0,
    'num_casos_prueba_elisa': 0,
    'num_casos_prueba_desconocida': 0

    }

    for registro in dictreader:
        if fecha in registro['fecha']: #se pone in en vez de == para que sea si esta ahi, o si esta en parte
            for clave in res:
                res[clave] += int(registro[clave]) #se utiliza clave en ambas porque es el mismo nombre

        elif registro['fecha']> fecha:
            break #para acortar

    fichero.close()
    
    return json.dumps(res) #se nevia una cadena de etxto pero se pasa luego al json

@app.route('/incidenciadiaria', methods = ['GET', 'POST'])
def incidencias():
    if request.method =='GET':
        return render_template("alta.html")

    #hay que validar la informacion de llegada
    #que los valores de los casos sean numeros y enteros positivos
    valores = request.form

    try:
        valores.num_casos_prueba_pcr = int( valores.num_casos_prueba_pcr)
    except:
        return render_template("alta.html", PCR="valor no valido" )

    #que el total de casos sea la suma del resto de casos
    #que la provincia sea correcta
    #que la fecha no sea futura ni anterior a fecha covid
    #que la fecha sea correcta en formato y supongo que en valor
    return 'se ha hecho un post'

'''
MI CODIGO

@app.route('/casos/<int:year>/<int:mes>/<int:dia>')
def casos(year, mes, dia):
    fichero= open('data/casos_diagnostico_provincia.csv')
    dictreader= csv.DictReader(fichero)
    numero_casos = 0
    num_pcr=0
    num_test_ac= 0
    num_prueba_ag= 0
    num_prueba_elisa= 0
    num_prueba_desconocida= 0

    if len(str(year)) !=4 or str(year) not in '2020, 2021':
        return 'fecha incorrecta'
  
    if str(mes) not in '123456789101112' or dia>31 or dia<1:
        return 'fecha incorrecta'

    #PODRIA HACERSE LA FECHA CON UN FORMAT METIENDO DENTRO LO DE .2 DE DOS DIGITOS

    if len(str(mes)) <2 and str(mes)[0] != 0:
        mes= '0'+str(mes)

    if len(str(dia)) <2 and str(dia)[0] != 0 :
        dia= '0'+str(dia)

    fecha=str(year)+'-'+str(mes)+'-'+str(dia)
    
    for registro in dictreader:

        if registro['fecha']== fecha:
            numero_casos += int(registro['num_casos'])
            num_pcr += int(registro['num_casos_prueba_pcr'])
            num_test_ac += int(registro['num_casos_prueba_test_ac'])
            num_prueba_ag += int(registro['num_casos_prueba_ag'])
            num_prueba_elisa += int(registro['num_casos_prueba_elisa'])
            num_prueba_desconocida += int(registro['num_casos_prueba_desconocida'])

    fichero.close()

    if numero_casos == 0:
        return 'No hay datos de ese dia o la fecha es incorrecta'
    
    return 'El número total de casos ese dia es:{} \n\n Dividios en:\n Pruebas pcr:{} Pruebas test: {} Pruebas ag: {} Pruebas elisa:{} Otras: {}'.format(numero_casos, num_pcr,num_test_ac, num_prueba_ag, num_prueba_elisa, num_prueba_desconocida)
'''