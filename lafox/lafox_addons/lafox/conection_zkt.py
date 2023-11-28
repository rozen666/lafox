# -*- coding: utf-8 -*-
###############################################################################
# Created on 27/03/2018 by Ing. Luis Ortega.
###############################################################################
__author__ = 'axcg'

import sys
import time
from zklib import zklib, zkconst
import xmlrpclib

usuario='admin'
password='admin'
odoourl = 'http://localhost:8069'
dbname='LaFox'
modulo = 'lafox'
servicio = 'value_assistence'

machine_ip = '192.168.1.201'
port = 4370
attendance = []

zk = zklib.ZKLib(machine_ip, int(port))
res = zk.connect()
print res
if res == True:
	print zk.enableDevice()
	print zk.disableDevice()
	print zk.version()
	print zk.osversion()
	print zk.deviceName()
	# print zk.setUser(uid=3, userid='3', name='BPMTech', password='1111', role=zkconst.LEVEL_USER)
	# zk.enableDevice()
	# zk.disconnect()
	zk.getAttendance()
	# print zk.getAttendanceclear()
	attendance = zk.getAttendance()
	zk.enableDevice()
	zk.disconnect()
lista_user = []
if ( attendance ):
	for registros in attendance:
		if registros[0] != '':
			lista_user.append(registros)

def conexion():
    try:
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(odoourl))
        uid = common.authenticate(dbname, usuario, password, {})
        models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(odoourl))
    
        idmodule=models.execute_kw(dbname, uid, password,'ir.module.module', 'search',[[['name', '=', modulo]]])[0]
        serv = models.execute(dbname, uid, password, 'hr.asistencia.employee', servicio,1,lista_user) 

        print serv
    
    except xmlrpclib.Fault as error:
        print "Error: "+error.faultString
        print error.faultCode

    print "Fin de la conexion"
        
conexion()

		
		# print "Clear Attendance:", zk.clearAttendance()