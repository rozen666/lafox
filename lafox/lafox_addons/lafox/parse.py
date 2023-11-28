#! -*- coding: utf-8 -*-
import psycopg2
import xlrd
import base64


def cast_str_to_int( s ):
    mto = str(s).split('.')[0]
    l = len(mto) - 1
    suma = 0
    for letra in mto:
        n = (10**l)*(ord(letra) - 48)
        l -= 1
        suma += n
    return suma


def cargar_MA( nombre_archivo ):

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
        v3 = hoja.cell_value( rowx=r, colx=3 )
        v4 = hoja.cell_value( rowx=r, colx=4 )
        v5 = hoja.cell_value( rowx=r, colx=5 )        
        v6 = hoja.cell_value( rowx=r, colx=6 )        
        v7 = hoja.cell_value( rowx=r, colx=7 )        
        v8 = hoja.cell_value( rowx=r, colx=8 )        
        v9 = hoja.cell_value( rowx=r, colx=9 )        
        v10 = hoja.cell_value( rowx=r, colx=10 )        
        v11 = hoja.cell_value( rowx=r, colx=11 )        
        v12 = hoja.cell_value( rowx=r, colx=12 )        
        v13 = hoja.cell_value( rowx=r, colx=13 ) 
        v14 = hoja.cell_value( rowx=r, colx=14 )       

        d = {
            'CLAVE':v0,
            'CODE_BARRAS': v1,
            'DESCRIPCION': v2,
            'PIEZAS': v3,
            'UNIDDAD': v4,
            'IMAGEN': v5,
            'GPO_PRECIO': v6,
            'REFERENCIA': v7,
            'GPO_INVENTARIO': v8,
            'MONEDA': v9,
            'IVA': v10,
            'PRECIO_BASE': v11,
            'OBSERVACION': v12,
            'BLOQUEAR': v13,
            'PROVEEDOR': v14,
            }
        
        lista_dicc.append( d )
        r += 1
    	
    return lista_dicc

def cargar_PT( nombre_archivo ):

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
        v3 = hoja.cell_value( rowx=r, colx=3 )
        v4 = hoja.cell_value( rowx=r, colx=4 )
        v5 = hoja.cell_value( rowx=r, colx=5 )        
        v6 = hoja.cell_value( rowx=r, colx=6 )        
        v7 = hoja.cell_value( rowx=r, colx=7 )        
        v8 = hoja.cell_value( rowx=r, colx=8 )        
        v9 = hoja.cell_value( rowx=r, colx=9 )        
        v10 = hoja.cell_value( rowx=r, colx=10 )        
        v11 = hoja.cell_value( rowx=r, colx=11 )        
        v12 = hoja.cell_value( rowx=r, colx=12 )        
        v13 = hoja.cell_value( rowx=r, colx=13 )        
        v14 = hoja.cell_value( rowx=r, colx=14 )        
        v15 = hoja.cell_value( rowx=r, colx=15 )        
        v16 = hoja.cell_value( rowx=r, colx=16 )        
        v17 = hoja.cell_value( rowx=r, colx=17 )        
        v18 = hoja.cell_value( rowx=r, colx=18 )        
        v19 = hoja.cell_value( rowx=r, colx=19 )        
        v20 = hoja.cell_value( rowx=r, colx=20 )        
        v21 = hoja.cell_value( rowx=r, colx=21 )        
        v22 = hoja.cell_value( rowx=r, colx=22 )        
        v23 = hoja.cell_value( rowx=r, colx=23 )        
        v24 = hoja.cell_value( rowx=r, colx=24 )        
        v25 = hoja.cell_value( rowx=r, colx=25 )        
        v26 = hoja.cell_value( rowx=r, colx=26 )        
        v27 = hoja.cell_value( rowx=r, colx=27 ) 
        v28 = hoja.cell_value( rowx=r, colx=28 )
        v29 = hoja.cell_value( rowx=r, colx=29 )
        v30 = hoja.cell_value( rowx=r, colx=30 )

    
        d = {
            'DEPARTAMENTO': v0,
            'CLAVE':v1,
            'NOMBRE': v2,
            'DIRECCION': v3,
            'EXTERIOR':v4,
            'INTERIOR':v5,
            'COLONIA': v6,
            'CIUDAD_DELEG': v7,
            'ZIP': v8,
            'ESTADO': v9,
            'PAIS': v10,
            'LADA': v11,
            'TELEFONO': v12,
            'MOBILE': v13,
            'EMAIL': v14,
            'VENDEDOR': v15,
            'MEDIO_CONTACTO': v16,
            'REFERENCIA': v17,
            'OBSERVACION': v18,
            'RFC': v19,
            'METODO_PAGO': v20,
            'FISICA_MORAL': v21,
            'MONEDA': v22,
            'LIMITE_CREDITO': v23,
            'DIAS_CREDITO': v24,
            'ESCALA_PRECIOS': v25,
            'SALDO_PENDIENTE': v26,
            'PROMEDIO_COMPRA_M': v27,
            'COMPRA_MAYOR': v28,
            'ULT_COMPRA': v29,
            'PUNTUALIDAD_PAGO': v30,

            # 'TELEFONO3': v13,
            # 'TELEFONO3':v12,

            }
        
        lista_dicc.append( d )
        r += 1
        
    return lista_dicc
# print cargar_PT( "lAYOUT CLIENTES  15.xlsx" )[0]



def cargar_CO( nombre_archivo ):

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
        v3 = hoja.cell_value( rowx=r, colx=3 )
        v4 = hoja.cell_value( rowx=r, colx=4 )
        v5 = hoja.cell_value( rowx=r, colx=5 ) 
        v6 = hoja.cell_value( rowx=r, colx=5 )       

        d = {

            'MODELO': v0,
            'DESCRIPCION': v1,
            'REFERENCIA': v2,
            'PIEZAS_PA': v3,
            'COSTO': v4,
            'PVF': v5,
            'UNI': v6,
            }


        lista_dicc.append( d )
        r += 1
        
    return lista_dicc



def cargar_delete( nombre_archivo ):

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

        # Funcion para quitar parentesis del archivo excel
        # f_code = v0.find(" (")
        # r_code = v0[:f_code]
       

        d = {

            'NAME': v0,

            }


        lista_dicc.append( d )
        r += 1
        
    return lista_dicc


