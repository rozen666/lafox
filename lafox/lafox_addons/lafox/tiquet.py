#! -*- coding: utf-8 -*-
from xhtml2pdf import pisa
import psycopg2
import os
import webbrowser

# Postgres
PSQL_HOST = "localhost"
PSQL_PORT = "5432"
PSQL_USER = "odoo"
PSQL_PASS = "password"
PSQL_DB   = "LaFox"

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
outputFilename = "test.pdf"

def convertHtmlToPdf(sourceHtml, outputFilename,id_account):
	valor = "<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"
	valor_dev = "<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>"+"<tr><td>"+""+"</td><td>" 

	try:
	    # Conectarse a la base de datos
	    connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (PSQL_HOST, PSQL_PORT, PSQL_USER, PSQL_PASS, PSQL_DB)
	    conn = psycopg2.connect(connstr)

	    # Abrir un cursor para realizar operaciones sobre la base de datos
	    cur = conn.cursor()
	    cur_line = conn.cursor()
	    cur_dev = conn.cursor()

	    # Ejecutar una consulta SELECT
	    sqlquery = "SELECT total_con_letra,amount_total,fecha_venta,nomenclatura FROM account_invoice WHERE ID ="+str(id_account)
	    sql_line = "SELECT clave_prod, name, cantidad_producto, quantity, price_unit_des, price_unit,monto_pago FROM account_invoice_line INNER JOIN product_product ON account_invoice_line.product_id =product_product.id  WHERE invoice_id ="+str(id_account)
	    sql_devo = "SELECT clave_prod, description, product_uom_qty, piezas_qty, precio_mov, precio_lst,amount FROM lafox_devolucion_account INNER JOIN product_product ON lafox_devolucion_account.product_id =product_product.id  WHERE account_id ="+str(id_account)
	    
	    cur.execute(sqlquery)
	    cur_line.execute(sql_line)
	    cur_dev.execute(sql_devo)

	    # Obtener los resultados como objetos Python
	    row = cur.fetchall()
	    row_line = cur_line.fetchall()
	    row_devo = cur_dev.fetchall()

	    # Recuperar datos del objeto Python
	    # for data in row:
	    print '****************************'
	    print '****************************'
	    print row
	    print row[0][0]
	    print '****************************'
	    print '****************************'

	    if row_line:
	    	valor = ""
		for line in row_line:
			valor = valor + "<tr><td bgcolor='#ffffff' style='font-size:9px'>"+line[0]+"</td><td bgcolor='#ffffff' style='font-size:9px' >"+line[1]+"</td><td bgcolor='#ffffff'>"+str(line[2])+"</td><td bgcolor='#ffffff'>"+str(line[3])+"</td><td bgcolor='#ffffff'>"+str(line[4])+"</td><td bgcolor='#ffffff'>"+str(line[5])+"</td><td bgcolor='#ffffff'>"+str(line[6])+"</td></tr>"
	    if row_devo:
	    	valor_dev = ""
	    	for line in row_devo:
		    	valor_dev = valor_dev + "<tr><td bgcolor='#ffffff' style='font-size:9px'>"+line[0]+"</td><td bgcolor='#ffffff' style='font-size:9px' >"+line[1]+"</td><td bgcolor='#ffffff'>"+str(line[2])+"</td><td bgcolor='#ffffff'>"+str(line[3])+"</td><td bgcolor='#ffffff'>"+str(line[4])+"</td><td bgcolor='#ffffff'>"+str(line[5])+"</td><td bgcolor='#ffffff'>"+str(line[6])+"</td></tr>"
	    

	except:
	    print("Error de base de datos")
	
	html = """<!doctype html>
	<html lang='en'>
	  <head>
	  </head>
	<table style='width: 999px;'>
	<tbody>
	<tr>
	<td><img src='http://lafox.com.mx/images/logo-2015-azul-horizontal.gif?crc=4277878345' alt='' width='233' height='98' /></td>
	<td>
	<table height='71'>
	<tbody>
	<tr>
	<td><span>Palma 31 4o Piso, Col Centro<br />Deleg. Cuauhtemoc, M&eacute;xico, Ciudad de M&eacute;xico, 06000 (55)5512-7614, 5518-2628 Fax 55127614</span></td>
	</tr>
	<tr>
	<td></td>
	</tr>
	</tbody>
	</table>
	</td>
	<td>
	<table height='286'>
	<tbody>
	<tr>
	<td>
	<pre>
	<p align='left'><strong>Tipo de Cambio:         """+str(row[0][2][:10])+"""</strong> </p>
	<p align='left'><strong>$ 18.50                 """+str(row[0][3])+"""</strong> </p>
	<p align='left'>                        Agente:Gaby</p>
	</pre>
	</td>
	</tr>
	<tr>
	<td>
	<p><strong>Maria Jose Estrada Bautista</strong></p>
	<p>ARTURO DEL CASTILLO S/N N Ext PALMILLAS MIXQUIAHUALA DE JUAREZ,HGO, HIDALGO CP 42700</p>
	<p>5534447040&nbsp; 7721438928</p>
	</td>
	</tr>
	</tbody>
	</table>
	</td>
	</tr>
	</tbody>
	</table>
	<p></p>
	<table align='center'>
	<tbody>
	<tr>
	<td bgcolor='#f6ae1d ' align='center'>
	<table>
	<tbody>
	<tr>
	<td>DEVOLUCION</td>
	</tr>
	<tr>
	<td>
	<table>
	<tbody>
	<tr>
	<td >Clave</td>
	<td >Descrpci&oacute;n</td>
	<td >Cantidad</td>
	<td >Prec Lista</td>
	<td >Precio</td>
	<td >Importe</td>
	</tr>
	</tbody>
	</table>
	<table>
	<tbody>
	"""+valor_dev+"""
	</tr>
	</tbody>
	</table>
	</td>
	</tr>
	</tbody>
	</table>
	</td>
	</tr>
	</tbody>
	</table>
	<br>
	<table align='center'>
	<tbody>
	<tr>
	<td bgcolor='#f6ae1d' align='center'>
	<table>
	<tbody>
	<tr>
	<td>VENTA</td>
	</tr>
	<tr>
	<td>
	<table>
	<tbody>
	<tr>
	<td >Clave</td>
	<td >Descrpci&oacute;n</td>
	<td >Cantidad</td>
	<td >Prec Lista</td>
	<td >Precio</td>
	<td >Importe</td>
	</tr></tbody>
	</table>
	<table>
	<tbody>
	"""+valor+"""
	</tr>
	</tbody>
	</table>
	</td>
	</tr>
	</tbody>
	</table>
	</td>
	</tr>
	</tbody>
	</table>
	<br>

	<table align='center'>
	<tbody>
	<tr>
	<td bgcolor='#f6ae1d' align='center'>
	<table>
	<tbody>
	<tr>
	<td></td>
	</tr>
	<tr>
	<td>
	<table>
	<tbody>
	<tr>
	<td ><strong>Total:</strong></td>
	<td ></td>
	<td ></td>
	<td ></td>
	<td ></td>
	<td ></td>
	<td >Importe</td>
	</tr>
	</tbody>
	</table>
	<table>
	<tbody>
	<tr>
	<td style='font-size:9px'>"""+row[0][0]+"""</td>
	<td >1</td>
	<td >2</td>
	<td >3</td>
	<td >4</td>
	<td >5</td>
	<td >"""+str(row[0][1])+"""</td>
	</tr>
	</tbody>
	</table>
	</td>
	</tr>
	</tbody>
	</table>
	</td>
	</tr>
	</tbody>
	</table>
	<br>
	<table align='right' bgcolor="#f6ae1d" width="290" height="20" >
	<tbody>
	<tr bgcolor="#f6ae1d">
	<td  bgcolor="#f6ae1d">Descripci&oacuten</td>
	<td  bgcolor="#f6ae1d">Banco Referencia</td>
	<td  bgcolor="#f6ae1d">Importe</td>
	</tr>
	</tbody>
	</table>
	<table align='right' bgcolor="#f6ae1d" width="290" height="18" >
	<tbody>
	<tr>
	<td >Efectivo</td>
	<td >Ref Banc</td>
	<td >"""+str(row[0][1])+"""</td>
	</tr>
	</tbody>
	</table>
	<p></p>
	</html>"""
	print html
	resultFile = open(outputFilename, "w+b")
	pisaStatus = pisa.CreatePDF(html,dest=resultFile)
	resultFile.close()
	webbrowser.open_new_tab("http://192.168.1.100:8069/lafox/static/src/PDF/test2018-12-04.pdf")
	return resultFile
	# return pisaStatus.err

if __name__=="__main__":
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)