import requests
from datetime import date
import matplotlib.pyplot as plt
from tabulate import tabulate

username = 'marcos'
password = 'password123'



def cargar_distribuidor():
	'''
	Permite cargar un nuevo distribuidor
	'''
	try:
		post_data = {
			'razon_social': input('Razon Social: '),
			'tfno': int(input('Telefono: ')),
			'direccion': input('Direccion: '),
			'email': input('Email: ')
		}
	except:
		print('Se ha introducido un valor erroneo')

	r = requests.post('http://127.0.0.1:8000/distribuidores/', data=post_data, auth=(username, password))
	
	if r.status_code == 201:
		print('Se ha cargado un nuevo distribuidor al sistema.')
	else:
		print('No se ha podido cargar el distribuidor')


def cargar_equipo():
	'''
	Permite cargar un nuevo equipo
	'''
	TIPO_CHOICES = ['ventilacion', 'ecografia', 'cirugia', 'monitoreo', 'diagnostico por imagenes']
	SECTOR_CHOICES = ['guardia', 'UTI', 'UCO', 'quirofano', 'rayos', 'taller']

	distribuidores = requests.get('http://127.0.0.1:8000/distribuidores/', auth=(username, password)).json()
	DISTRIBUIDORES_CHOICES = [dist['razon_social'] for dist in distribuidores]

	post_data = {
		'marca': input('Marca: '),
		'modelo': input('Modelo: '),
		'numero_serie': int(input('Numero de serie: ')),
		'tipo': input(str(TIPO_CHOICES) + ': \n'),
		'sector': input(str(SECTOR_CHOICES) + ': \n'),
		'fecha_mantenimiento_anual': date.today(),
		'operativo': True,
		}

	distribuidor = input(str(DISTRIBUIDORES_CHOICES) + ': \n')
	post_data['distribuidor'] = [dist['url'] for dist in distribuidores if dist['razon_social'] == distribuidor][0]

	r = requests.post('http://127.0.0.1:8000/equipos/', data=post_data, auth=(username,password))
	if r.status_code == 201:
		print('Se a cargado un nuevo equipo correctamente')
	else:
		print('Se ha producido un error')


def historial_reparaciones(ns):
	'''
	Muestra una tabla con el historial de reparaciones
	del equipo seleccionado. 
	'''	
	constancias = requests.get(f"http://127.0.0.1:8000/constancias-service/?equipo={ns}", auth=(username, password)).json()
	tabla_equipos = [[const['fecha'], const['falla'], const['observaciones']] for const in constancias]
	headers= ['fecha', 'falla', 'observaciones']

	print('\n' + tabulate(tabla_equipos, headers, tablefmt="github"))


def grafico_operativos():
	'''
	Muestra un grafico con la cantidad de equipos
	operativos y no operativos
	'''
	equipos_json = requests.get('http://127.0.0.1:8000/equipos/', auth=(username,password))
	equipos_list = equipos_json.json()

	n_operativos=0
	for equipo in equipos_list:
		if equipo['operativo']:
			n_operativos += 1


	estado = ['Operativos', 'No Operativos']
	cantidad = [n_operativos, len(equipos_list)-n_operativos]

	plt.bar(estado, cantidad)
	plt.show()


def arreglos_pendientes():
	'''
	Entrega un listado de las constancias de 
	service que estan abiertas
	'''
	constancias = requests.get('http://127.0.0.1:8000/constancias-service/', auth=(username, password)).json()

	for constancia in constancias:
		if constancia['cerrada'] == False:
			equipo = requests.get(constancia['equipo'], auth=(username, password)).json()

			print(f""" -------------------
				\nconstancia numero: {constancia['id']}
				\nequipo: {equipo['marca']} {equipo['modelo']} {equipo['numero_serie']}
				\nresponsable: {constancia['responsable']} 
				\nfalla: {constancia['falla']} 
				\nobservaciones; {constancia['observaciones']}\n""")


def cambio_de_estado(ns, nuevo_estado):
	'''
	Modifica el estado 'operativo/no operativo' del equipo correspondiente
	al numero de serie pasado en el parametro 'ns'. Si nuevo_estado es TRUE
	el equipo pasa a estar operativo. Si es FALSE, lo contrario.
	Adicionalmente se genera una constancia de service.
	'''
	equipo_data = requests.get(f"http://127.0.0.1:8000/equipos/{ns}/", auth=(username, password)).json()
	equipo_data['operativo'] = nuevo_estado
	r = requests.put(f"http://127.0.0.1:8000/equipos/{ns}/", data=equipo_data , auth=(username,password))

	# Si el equipo vuelve a estar operativo se busca la constancia de service correspondiente para cerrarla
	if nuevo_estado:
		constancias = requests.get(f"http://127.0.0.1:8000/constancias-service/?equipo={ns}", auth=(username, password)).json()
		lista_const = [(const['id'], const['falla']) for const in constancias if const['cerrada']==False]
		_id = int(input('Introduzca id de la constancia de service correspondiente:\n' + str(lista_const) +'\n' ))

		const_data = requests.get(f"http://127.0.0.1:8000/constancias-service/{_id}/", auth=(username, password)).json()
		const_data['cerrada'] = True
		const_data['observaciones'] = input('Obervaciones respecto a la reparacion: ')
		requests.put(f"http://127.0.0.1:8000/constancias-service/{_id}/", data=const_data, auth=(username, password))

	# Si el equipo pasa a estar no operativo, se crea una nueva constancia de service
	else:
		print("generando constancia de service...")
		post_data = {
			'equipo': equipo_data['url'],
			'responsable': input("responsable: "),
			'falla': input("falla: "),
			'observaciones': input("observaciones: "),
			'cerrada': False
			}

		requests.post("http://127.0.0.1:8000/constancias-service/", data=post_data, auth=(username,password))

	if r.status_code == 200:
		if nuevo_estado:
			print(f"Equipo {ns} esta nuevamente en servicio")
		else:
			print(f"Equipo {ns} esta fuera de servicio")
	else:
		print('No se pudo realizar la accion')


def equipo_no_operativo(ns):
	'''
	Llama a la funcion cambio_de_estado para actualizar
	el estado del equipo a No Operativo
	'''
	cambio_de_estado(ns, False)


def equipo_operativo(ns):
	'''
	Llama a la funcion cambio_de_estado para actualizar
	el estado del equipo a No Operativo pasando como parametro
	el numero de serie del mismo.
	'''
	cambio_de_estado(ns, True)


def mantenimientos_anuales():
	equipos = requests.get('http://127.0.0.1:8000/mantenimiento/', auth=(username, password)).json()
	lista_equipos = [[eq['marca'], eq['modelo'], eq['numero_serie'], eq['fecha_mantenimiento_anual']] for eq in equipos]
	headers = ['marca', 'modelo', 'numero_serie', 'ultimo mantenimiento']

	print('\n' + tabulate(lista_equipos, headers, tablefmt="github"))


def mantenimiento_realizado(ns):
	equipo_data = requests.get(f"http://127.0.0.1:8000/equipos/{ns}/", auth=(username, password)).json()
	equipo_data['fecha_mantenimiento_anual'] = date.today()
	requests.put(f"http://127.0.0.1:8000/equipos/{ns}/", data=equipo_data , auth=(username, password))

	print('Mantenimiento anual cargado exitosamente')