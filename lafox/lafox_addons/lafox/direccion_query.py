#! -*- coding: utf-8 -*-
import psycopg2
import xlrd
import base64

def query_num_exint( nombre_archivo ):

    conexion = psycopg2.connect(host="localhost", database="lafox", user="odoo", password="admin")

    #Creacion del cursor con el objeto de conexion

    cur= conexion.cursor()


    #Leemos el archivo de excel

    archivo_excel_nombre = str(nombre_archivo)
    archivo = xlrd.open_workbook( archivo_excel_nombre )
    hoja = archivo.sheet_by_index(0)

    numero_registros = hoja.nrows
    #print "Numero de registros en la hoja: %d" % numero_registros
    r = 1
    lista_registros = []

    lista_dicc = []

    while r < numero_registros:

        v0 = hoja.cell_value( rowx=r, colx=0 )
        v1 = hoja.cell_value( rowx=r, colx=1 )
        v2 = hoja.cell_value( rowx=r, colx=2 )      

        d = {
            'CLAVE':v0,
            'INTERIOR': v1,
            'EXTERIOR': v2,
            }
        
        lista_dicc.append( d )
        r += 1
    	
    return lista_dicc

#Variables con los datos obtenidos del documento

clave = 'CLAVE'
interior = 'INTERIOR'
exterior = 'EXTERIOR'


#Ejecutamos una consulta

cur.execute( "update res_partner set num_interior= 'interior', num_exterior= 'exterior' where clave_cliente = 'CLAVE'" )

#Recorremos los resultados y los mostramos

for street in cur.fetchall():
	print street

conexion.close()

