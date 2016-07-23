from __future__ import unicode_literals

from django.db import models

import datetime

class Asistencias(models.Model):
	#No indico clave primaria ya que uso unique_together. Dejo a Django crear su propio pk_id
	bloque = models.CharField(max_length=100)
	nombre = models.CharField(max_length=100)
	nombre_match = models.CharField(max_length=100)
	presente = models.IntegerField()
	ausente = models.IntegerField()
	licencia = models.IntegerField()
	mo = models.IntegerField()
	update_date = models.DateField(auto_now=True)
	observacion = models.CharField(max_length=100)

	class Meta:
		#Con unique_together le decimos que no se puede haber repeticiones en el conjunto de campos "nombre" y "bloque"
		#Actua como una clave primaria compuesta
		unique_together=('nombre', 'bloque')
		verbose_name_plural = 'Asistencias'