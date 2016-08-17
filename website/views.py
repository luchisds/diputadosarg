# -*- coding: utf-8 -*-
#Python modules
import os
import re
import csv
#Django functions
from django.shortcuts import render
from django.http import JsonResponse
#Django models
from models import Asistencias
#Json serializers
from django.core import serializers
import json
#Dependencies
import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

app_path = os.path.dirname(os.path.realpath(__file__))

def MainApi(request):
	#Cantidad de sesiones
	cantidad_sesiones = 8
	periodo = 134
	slug_sesiones = 'Se realizaron 7 Sesiones que comprenden 7 reuniones (incluye 1 Sesión Informativa) + 1 Asamblea Legislativa. TOTAL: 8 REUNIONES'

	sesiones = list()
	with open(app_path+'/static/tabula-PRESENTISMO_2016_0716.csv', 'rb') as f:
		reader = csv.reader(f)
		reader.next()
		for row in reader:
			sesiones.append({'fecha':row[0], 'sesion':row[1], 'presente':row[2], 'ausente':row[3], 'licencia':row[4], 'mo':row[5]})

	return JsonResponse({'periodo':periodo, 'cantidad_sesiones':cantidad_sesiones,'slug_sesiones':slug_sesiones,'sesiones':sesiones})


def DiputadosApi(request):
	html = requests.get('http://www.diputados.gov.ar/diputados/listadip.html')
	soup = BeautifulSoup(html.text, 'html5lib')
	data = soup.find('table',{'id':'tablesorter'}).findAll('tr')[1:]

	tmp_dict = {}
	diputados = []

	for diputado in data:
		datos = diputado.findAll('td')
		img = datos[0].img.attrs['src']
		if datos[1].find('a'):
			url_diputado = datos[1].a.attrs['href']
			nombre = datos[1].a.get_text().strip()
		else:
			nombre = datos[1].get_text().strip()
			url_diputado = ''
		id_diputado = url_diputado.split('/')[2]
		distrito = datos[2].get_text().strip()
		ini_mandato = datos[3].get_text().strip()
		fin_mandato = datos[4].get_text().strip()
		bloque = datos[5].get_text().strip()

		# Correcciones para matchear "bloque" diputados con "bloque" asistencias
		if bloque == 'UCR':
			bloque = 'UNION CIVICA RADICAL'
		elif bloque == 'PROYECTO SUR - UNEN':
			bloque = 'PROYECTO SUR'
		elif bloque == 'BRIGADIER GENERAL JUAN BAUTISTA BUSTOS':
			bloque = 'BG JUAN B. BUSTOS'
		elif bloque == 'FRENTE CIVICO Y SOCIAL DE CATAMARCA':
			bloque = 'FTE. CIVICO Y SOCIAL DE CATAMARCA'
		elif bloque == 'DEMOCRATA PROGRESISTA':
			bloque = 'PARTIDO DEMOCRATA PROGRESISTA'
		elif bloque == 'MOV POP NEUQUINO':
			bloque = 'MOVIMIENTO POPULAR NEUQUINO'
		elif bloque == 'LIBERTAD VALORES Y CAMBIO':
			bloque = 'LIBERTAD, VALORES Y CAMBIO'
		elif bloque == 'FRENTE DE IZQUIERDA Y DE LOS TRABAJADORES':
			bloque = 'FTE. DE IZQUIERDA Y DE LOS TRABAJADORES'
		# Correccion para matchear "nombre" diputados con "nombre" asistencias
		if nombre == 'SOSA, SOLEDAD':
			nombre = 'SOSA CAPURRO, VICTORIA SOLEDAD'

		tmp_dict = {'id':id_diputado,'nombre':nombre.upper(),'bloque':bloque.upper(),'distrito':distrito,'ini':ini_mandato,'fin':fin_mandato,'img':img,'url':url_diputado}
		diputados.append(tmp_dict)

	return JsonResponse(diputados, safe=False)


def DiputadoApi(request, id):
	html = requests.get('http://www.diputados.gov.ar/diputados/'+id)
	soup = BeautifulSoup(html.text, 'html5lib')
	info = soup.find('div', {'class':'detalleDip container appInvisible'})

	img = info.find('div',{'class':'verticalPad'}).find('img',{'class':'img-circle'}).attrs['src']
	cargo = info.h2.get_text().strip()
	nombre = info.h1.get_text().strip()
	bloque = info.find('div',{'class':'col-sm-12 col-md-4'}).contents[4].strip()
	email = info.find('a').get_text().strip()
	tel = info.findAll('div', {'class':'col-sm-12 col-md-2 verticalPad'})[1].contents[4].replace(u'Teléfono:','').strip()
	distrito_escudo = info.find('div', {'class':'col-sm-12 col-md-2 distrito'}).img.attrs['src'].strip()
	distrito = info.find('div', {'class':'col-sm-12 col-md-2 distrito'}).div.get_text().strip()

	diputado = {'id':id,'nombre':nombre,'bloque':bloque,'distrito':distrito,'cargo':cargo,'email':email,'tel':tel,'img':img,'distrito_escudo':distrito_escudo}

	return JsonResponse(diputado, safe=False)


def DiputadoProyectosApi(request, id):
	html = requests.get('http://www.diputados.gov.ar/diputados/'+id+'/listadodeproy.html?size=1000')
	soup = BeautifulSoup(html.text, 'html5lib')
	info = soup.find('table', {'id':'tabla-proyectos'}).findAll('tr')[1:]

	tmp_dict = {}
	proyectos = []

	for proyecto in info:
		datos = proyecto.findAll('td')
		expediente_url = datos[0].a.attrs['href']
		id_proyecto = re.search('id=([0-9]+)', datos[0].a.attrs['href']).group(1)
		expediente = datos[0].a.get_text()
		tipo = datos[1].get_text()
		sumario = datos[2].get_text()
		fecha = datos[3].get_text()

		tmp_dict = {'expediente':expediente,'fecha':fecha,'tipo':tipo,'sumario':sumario,'expediente_url':expediente_url,'id_proyecto':id_proyecto,'id':id}
		proyectos.append(tmp_dict)

	return JsonResponse(proyectos, safe=False)


def ProyectoApi(request, id):

	html = requests.get('http://www.diputados.gov.ar/proyectos/proyecto.jsp?id='+id)
	soup = BeautifulSoup(html.text, 'html5lib')
	content = soup.find('div', {'id':'proyecto-tab'}).find('div',{'class':'tab-content'})

	texto = content.find('div',{'id':'texto'}).get_text()

	fundamentos = unidecode(content.find('div',{'id':'fundamentos'}).get_text())

	data_firmantes = content.find('div',{'id':'firmantes'}).find('table').findAll('tr')
	firmantes = []
	for firmante in data_firmantes[1:]:
		datos = firmante.findAll('td')
		nombre = datos[0].get_text()
		distrito = datos[1].get_text()
		bloque = datos[2].get_text()
		firmantes.append({'firmante':nombre,'distrito':distrito,'bloque':bloque})

	comision = []
	data_tramite = soup.find('div', {'id':'tramites'}).find('table')
	titulo_tramite = data_tramite.caption.get_text().strip()
	for t in data_tramite.findAll('tr')[1:]:
		datos = t.findAll('td')
		comision.append(datos[0].get_text())

	proyecto = {'texto':texto,'fundamentos':fundamentos,'firmantes':firmantes,'tramite':{'titulo':titulo_tramite,'comisiones':comision}}

	return JsonResponse(proyecto, safe=False)


def DiputadoComisionesApi(request, id):
	html = requests.get('http://www.diputados.gov.ar/diputados/'+ id +'/comisiones.html')
	soup = BeautifulSoup(html.text, 'html5lib')
	info = soup.find('table', {'id':'tablaComisiones'}).findAll('tr')[1:]

	comisiones = []

	for c in info:
		datos = c.findAll('td')
		comision = datos[0].a.get_text()
		cargo = datos[1].get_text().strip()
		comisiones.append({'comision':comision,'cargo':cargo})

	return JsonResponse({'id':id,'comisiones':comisiones}, safe=False)


def AsistenciasApi(request):
	html = requests.get('http://www.diputados.gov.ar/diputados/listadip.html')
	soup = BeautifulSoup(html.text, 'html5lib')
	data = soup.find('table',{'id':'tablesorter'}).findAll('tr')[1:]

	tmp_dict = {}
	diputados = []

	for diputado in data:
		datos = diputado.findAll('td')
		if datos[1].find('a'):
			url_diputado = datos[1].a.attrs['href']
			nombre = datos[1].a.get_text()
		else:
			nombre = datos[1].get_text()
			url_diputado = ''
		id_diputado = url_diputado.split('/')[2]
		bloque = datos[5].get_text()

		# Correcciones para matchear "bloque" diputados con "bloque" asistencias
		if bloque == 'UCR':
			bloque = 'UNION CIVICA RADICAL'
		elif bloque == 'PROYECTO SUR - UNEN':
			bloque = 'PROYECTO SUR'
		elif bloque == 'BRIGADIER GENERAL JUAN BAUTISTA BUSTOS':
			bloque = 'BG JUAN B. BUSTOS'
		elif bloque == 'FRENTE CIVICO Y SOCIAL DE CATAMARCA':
			bloque = 'FTE. CIVICO Y SOCIAL DE CATAMARCA'
		elif bloque == 'DEMOCRATA PROGRESISTA':
			bloque = 'PARTIDO DEMOCRATA PROGRESISTA'
		elif bloque == 'MOV POP NEUQUINO':
			bloque = 'MOVIMIENTO POPULAR NEUQUINO'
		elif bloque == 'LIBERTAD VALORES Y CAMBIO':
			bloque = 'LIBERTAD, VALORES Y CAMBIO'
		elif bloque == 'FRENTE DE IZQUIERDA Y DE LOS TRABAJADORES':
			bloque = 'FTE. DE IZQUIERDA Y DE LOS TRABAJADORES'


		if nombre.find(' ',nombre.find(', ')+2) == -1:
			nuevo_nombre = nombre.upper()
		else:
			nuevo_nombre = nombre[:nombre.find(' ',nombre.find(', ')+2)].upper()

		#print 'DP: '+nuevo_nombre

		asistencia = Asistencias.objects.filter(nombre_match=nuevo_nombre, bloque=bloque)
		if asistencia:
			for obj in asistencia:
				presente = obj.presente
				ausente = obj.ausente
				licencia = obj.licencia
				mo = obj.mo
				#print 'AS: '+obj.nombre_match
		else:
			presente = None
			ausente = None
			licencia = None
			mo = None

		tmp_dict = {'id':id_diputado,'nombre':nombre.upper(),'bloque':bloque.upper(),'presente':presente,'ausente':ausente,'licencia':licencia,'mo':mo}
		diputados.append(tmp_dict)

	return JsonResponse(diputados, safe=False)


def AsistenciasUpdate(request):

	def make_int(num):
		if num == '':
			return 0
		else:
			return int(num)


	asistencias = []

	with open(app_path+'/static/tabula-ESTADISTICAS_2016_0716.csv', 'rb') as f:
		reader = csv.reader(f)
		#Pasa al segundo registro porque el primero contiene los nombres de columnas
		reader.next()
		for row in reader:
			# Unidecode toma los caracteres Unicode y devuelve su equivalente en ASCII, ej = 'á' devuelve 'a'
			# ord() devuelve el numero de caracter Unicode  |  Á=193  É=201  Í=205  Ó=211  Ú=218  Ì=204
			bloque = ''.join(unidecode(c) if ord(c)==193 or ord(c)==201 or ord(c)==205 or ord(c)==211 or ord(c)==218 or ord(c)==204 else c for c in row[0].decode('utf8').upper() or ord(c)==218).replace('\r', ' ')
			nombre = ''.join(unidecode(c) if ord(c)==193 or ord(c)==201 or ord(c)==205 or ord(c)==211 or ord(c)==218 or ord(c)==204 else c for c in row[1].decode('utf8').upper()).split('\r')
			
			observacion = ''
			if len(nombre) > 1:
				for e in nombre[1:]:
					observacion += ' ' + e
				observacion = observacion.replace('OBSERVACION: ','').strip()

			nombre = nombre[0].strip().replace('-',' ')

			# En el PDF de Asistencias figuran como bloque "Frente para la Victoria - PJ"
			# Pero en el sitio de diputados son parte del "Frente de la Concordia Misionero"
			if nombre == 'CLOSS, MAURICE FABIAN' or nombre == 'FRANCO, JORGE DANIEL' or nombre == 'RISKO, SILVIA LUCRECIA':
				bloque = 'FRENTE DE LA CONCORDIA MISIONERO'
			# En el PDF de Asistencias figura como "Frente para la Victoria - PJ"
			elif nombre == 'CARLOTTO, REMO GERARDO' or nombre == 'DE PONTI, LUCILA MARIA' or nombre == 'FERREYRA, ARACELI SUSANA DEL ROSARIO' or nombre == 'GROSSO, LEONARDO' or nombre == 'GUZMAN, ANDRES ERNESTO' or nombre == 'HORNE, SILVIA RENEE':
				bloque = 'PERONISMO PARA LA VICTORIA'
			# En el sitio de Diputados el bloque figura con la palabra CAMBIO en su nombre, en vez de CAMBIOS
			elif bloque == 'LIBERTAD, VALORES Y CAMBIOS':
				bloque = 'LIBERTAD, VALORES Y CAMBIO'

			#nombre_match
			if nombre.find(' ',nombre.find(', ')+2) == -1:
				nuevo_nombre = nombre
			else:
				nuevo_nombre = nombre[:nombre.find(' ',nombre.find(', ')+2)]

			updated_values = {'nombre':nombre,'bloque':bloque,'nombre_match':nuevo_nombre,'presente':make_int(row[3].decode('utf8')),'ausente':make_int(row[4].decode('utf8')),'licencia':make_int(row[5].decode('utf8')),'mo':make_int(row[6].decode('utf8')),'observacion':observacion}
			obj, created = Asistencias.objects.update_or_create(nombre=nombre, bloque=bloque, defaults=updated_values)
			asistencias.append({'objeto':serializers.serialize('json',[obj,]),'creado':created})

	return JsonResponse(asistencias, safe=False)

##########################


##########################

def Index(request):
	return render(request, 'index.html')
