 # -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today OpenERP SA (<http://www.openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Code create by: Ing. Luis J. Ortega 24/09/2018
#    for creation of invoice with pack 3.3
#
##############################################################################
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from openerp import SUPERUSER_ID
from openerp import models, fields, api, tools
from openerp import http
from openerp.osv import osv
import os
import subprocess
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from datetime import date, timedelta, datetime as dt
from xml.etree import cElementTree
from xml.etree.cElementTree import Element
from xml.etree.cElementTree import SubElement
from suds.client import Client
import base64
import number_to_letter

import datetime
import xml.etree.ElementTree as ET
import logging
_logger = logging.getLogger(__name__)

# ODOO_HOME = "/opt/odoo/extra_addons"
ODOO_HOME = "/opt/lafox/odoo/extra_addons/"

TYPE_SELECT_VF=[
            ('VENTA','Venta'),
            ('FACTURA','Factura'),
            ]

TIPO_COMPROBANTE_LISTA = [
            ('I','INGRESO'),
            ('E','EGRESO'),
            ('T','TRASLADO'),
            ('N','NÓMINA'),
            ('P','PAGO'),
            ]

METODO_PAGO_SELECTION = [
            ('01','01/Efectivo'),
            ('02','02/Cheque Nominativo'),
            ('03','03/Transferencia Electrónica de Fondos'),
            ('04','04/Tarjetas de Crédito'),
            ('05','05/Monederos Electrónicos'),
            ('06','06/Dinero Electrónico'),
            # ('07','07/Tarjetas Digitales'),
            ('08','08/Vales de Despensa'),
            # ('09','09/Bienes'),
            # ('10','10/Servicio'),
            # ('11','11/Por cuenta de Tercero'),
            ('12','12/Dacioń de Pago'),
            ('13','13/Pago por Subrogación'),
            ('14','14/Pago por Consignación'),
            ('15','15/Condonación'),
            # ('16','16/Cancelación'),
            ('17','17/Compensación'),
            ('23','23/Novación'),
            ('24','24/Confusuón'),
            ('25','25/Remisión de deuda'),
            ('26','26/Prescripción o caducidad'),
            ('27','27/A satisfacción del acreedor'),
            ('28','28/Tarjeta de Débito'),
            ('29','29/Tarjeta de Servicios'),
            ('30','30/Aplicacion de Anticipos'),
            ('31','29/Intermediario de Pago'),
            # ('98','98/No Aplica (NA)'),
            ('99','99/Otros'),
        ]           
        
FORMA_PAGO_SELECTION = [
            ('PUE','Pago en una sola exhibición'),
            ('PPD','Pago en parcialidades o diferido'),
        ]

ACCOUNT_STATE = [
            ('draft','Borrador'),
            ('open','Abierto'),
            ('paid','Pagado'),
            ('cancel','Cancelado'),

        ]

REGIMEN_FISCAL = [
            ('601','General de Ley Personas Morales'),
            ('603','Personas Morales con Fines no Lucrativos'),
            ('605','Sueldos y Salarios e Ingresos Asimilados a Salarios'),
            ('606','Arrendamiento'),
            ('608','Demás ingresos'),
            ('609','Consolidación'),
            ('610','Residentes en el Extranjero sin Establecimiento Permanente en México'),
            ('611','Ingresos por Dividendos (socios y accionistas)'),
            ('612','Personas Físicas con Actividades Empresariales y Profesionales'),
            ('614','Ingresos por intereses'),
            ('616','Sin obligaciones fiscales'),
            ('620','Sociedades Cooperativas de Producción que optan por diferir sus ingresos'),
            ('621','Incorporación Fiscal'),
            ('622','Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras'),
            ('623','Opcional para Grupos de Sociedades'),
            ('624','Coordinados'),
            ('628','Hidrocarburos'),
            ('607','Régimen de Enajenación o Adquisición de Bienes'),
            ('629','De los Regímenes Fiscales Preferentes y de las Empresas Multinacionales'),
            ('630','Enajenación de acciones en bolsa de valores'),
            ('615','Régimen de los ingresos por obtención de premios'),
            ]   

USO_CFDI = [
            ('G01','Adquisición de mercancias'),
            ('G02','Devoluciones, descuentos o bonificaciones'),
            ('G03','Gastos en general'),
            ('I01','Construcciones'),
            ('I02','Mobilario y equipo de oficina por inversiones'),
            ('I03','Equipo de transporte'),
            ('I04','Equipo de computo y accesorios'),
            ('I05','Dados, troqueles, moldes, matrices y herramental'),
            ('I06','Comunicaciones telefónicas'),
            ('I07','Comunicaciones satelitales'),
            ('I08','Otra maquinaria y equipo'),
            ('D01','Honorarios médicos, dentales y gastos hospitalarios.'),
            ('D02','Gastos médicos por incapacidad o discapacidad'),
            ('D03','Gastos funerales.'),
            ('D04','Donativos.'),
            ('D05','Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación).'),
            ('D06','Aportaciones voluntarias al SAR.'),
            ('D07','Primas por seguros de gastos médicos.'),
            ('D08','Gastos de transportación escolar obligatoria.'),
            ('D09','Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.'),
            ('D10','Pagos por servicios educativos (colegiaturas)'),
            ('P01','Por definir'),
            ]

class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    # FUNCION PARA OBTNER EL TOTAL LETRA Y CENTAVOS
    @api.multi
    @api.depends('amount_total')
    def _get_importe_letra(self):
        dic = {}
        decimal = self.get_centavos_letra(self.amount_total)
        importeletra = (number_to_letter.to_word(int(self.amount_total)) + " MXN " + decimal + "/100 ").upper()
        self.total_con_letra = str(importeletra)
        dic[self.id] = importeletra
        return dic

    def get_centavos_letra(self, cantidad):
        centavos = ""
        cantidad_str = str(cantidad)
        cantidad_splitted = cantidad_str.split('.')
        if len(cantidad_splitted) > 1:
            if len(cantidad_splitted[1]) == 1:
                centavos = cantidad_splitted[1] + "0"
            else:
                centavos = cantidad_splitted[1]
        else:
            centavos = "00"
        return centavos

    # DEFAULT PARA OBTENER EL SALDO PENDIENTE
    @api.multi
    @api.depends('amount_total')
    def _compute_saldo_pend(self):
        total_pen = 0
        for invoice in self:
            suma = 0
        for pagos in self.env['lafox.recibo.electronico.pago'].search([('invoice_id', '=', self.id)]):
            suma =  suma + pagos.monto_pago
        
        total_pen = float(invoice.amount_total) - float(suma)
        invoice.saldo_pediente = total_pen
        return total_pen
        # for invoice in self:
        #     print invoice
        #     suma = 0
        # for pagos in self.env['lafox.recibo.electronico.pago'].search([('invoice_id', '=', invoice.id)]):
        #     print pagos
        #     suma =  suma + pagos.monto_pago

        # total_pen = float(invoice.amount_total) - float(suma)
        # invoice.saldo_pediente = total_pen
        # return total_pen

    @api.onchange('tipo_venta')
    def _onchange_number_folio(self):
        if self.tipo_venta == 'FACTURA':
            folio = 1
            folios = self.search([('folio', '!=', '')], order='folio desc')
            if folios:
                folio = int(folios[0].folio) + 1
            self.folio = folio

    # FIELDS PARA FACTURACION
    tipo_venta = fields.Selection(TYPE_SELECT_VF, string='Tipo de Venta')
    lugar_exp = fields.Char(string='Lugar de Expedicón', index=True, default='CUAUHTEMOC, CDMX')
    fecha_certificacion = fields.Datetime(string='Fecha y Hora de Certificación', index=True)
    fecha_emision = fields.Datetime(string='Fecha y Hora de Emsión', index=True)
    tipo_comprobante = fields.Selection(TIPO_COMPROBANTE_LISTA, string='Tipo de Comprobante', index=True)
    folio_fiscal = fields.Char(string='Folio Fiscal', index=True)
    serie = fields.Char(string='Serie', index=True, default='L')
    folio = fields.Char(string='Folio', index=True)
    no_serie_csd_sat = fields.Char(string='NO. Serie CSD de SAT', index=True)
    no_serie_csd_emisor = fields.Char(string='NO. Serie CSD de Emisor', index=True)
    RfcProvCertif = fields.Char(string='RfcProvCertif', index=True)
    metodo_pago = fields.Selection(METODO_PAGO_SELECTION, string='Metodo de Pago', index=True)
    forma_pago = fields.Selection(FORMA_PAGO_SELECTION, string='Forma de Pago', index=True)
    total_con_letra = fields.Char(string='Total con Letra', index=True, compute='_get_importe_letra', store=True)
    cadena_original_s = fields.Char(string='Cadena Original Del Complemento De Certificación Digital Del SAT:', index=True)
    sello_digita_emisor = fields.Char(string='Sello Digital Del Emisor', index=True)
    sello_digita_sat = fields.Char(string='Sello Digital Del SAT', index=True)
    state_ac = fields.Selection(ACCOUNT_STATE, string="Estado", default='draft')
    bind = fields.Boolean (string = "Timbrado", invisible='True')
    xml_64 = fields.Binary(string="XML timbrado",)
    xml_64_cancelado = fields.Binary(string="XML Cancelado",)
    name_facturacion = fields.Char(string='nombre', index=True)
    pass_facturacion = fields.Char(string='pass', index=True)
    qr= fields.Char(string='Codigo QR', size=120)
    acuse = fields.Binary(string="Acuse",)
    regimen_fiscal = fields.Selection(REGIMEN_FISCAL, string='Regimen Fiscal')
    uso_cfdi = fields.Selection(USO_CFDI, string='Uso CFDI')
    comentarios = fields.Text(string='Información Adicional', index=True)
    saldo_pediente = fields.Float(string='Saldo Pendiente', compute='_compute_saldo_pend',store=True)
    monto_pagado = fields.Float(string='Monto Pagado')

    #Field para colocar el estatus de la factura
    factura_estatus = fields.Char(string='Estatus de la factura')
    #FIeld para colocar el numero de seguimiento de la factura
    n_seguimiento = fields.Char(string= 'Numero de seguimiento')
    #Field para ver el estado de la solicitud
    estado_soli = fields.Char(string='Estado de la solicitud')
    #Field para saber el UUID relacionado con la factura
    uuid_relacionado =fields.Text(string='UUID Relacionados')

    _sql_constraints = [
        ('folio', 'UNIQUE (folio)',  'Ya existe una factura con este folio favor de verificar!')
    ]

    
    #FUNCION PARA TIMBRAR EL XML 
    def _binding(self,cr,uid,path,invoice_id):
        invoice_fac = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=None)
        id_company=invoice_fac.company_id
        certificadoEmisor = id_company.cer
        LlavePrivadaEmisor = id_company.key
        llavePrivadaEmisorPassword = id_company.jpassword
        USER = id_company.usr_proveedor
        PASS = id_company.psw_proveedor

        # print '\t======tibrado productivo======'
        # WSDL = 'http://ws.rfacil.com/InterconectaWs.svc?wsdl'

        print '\t======tibrado pruebas======'
        WSDL = 'http://wspruebas.rfacil.com/InterconectaWs.svc?wsdl'
        # USER = 'PIGE691013RPA_34'
        # PASS = '348647913486479134864791'

        content = open(path, "r")
        content = content.read()
        content = content.decode("utf-8")
        client = Client(url=WSDL)
        content = content and content.replace('&', '&amp;').replace('"', '&quot;').replace('"', '&apos;').replace('<', '&lt;').replace('>', '&gt;')

        response = client.service.timbrarEnviaCFDIxp33(USER,PASS,certificadoEmisor,LlavePrivadaEmisor,llavePrivadaEmisorPassword,content)
        
        if response.numError != 0:
            error = 'Error %s : %s' % (response.numError, response.ErrorMessage)
            raise osv.except_osv('Error', error)

        else:

            xml_encoded = base64.b64decode(response.XML)
            cadena=xml_encoded

            num_cadena5= cadena.find("NoCertificado=") + (len('NoCertificado='))+1
            cadena_15 = cadena[num_cadena5:].find("Sello=")- 2
            noCertificado =  cadena[num_cadena5:][:cadena_15]

            num_cadena6= cadena.find("NoCertificadoSAT=") + (len('NoCertificadoSAT='))+1
            cadena_16 = cadena[num_cadena6:].find("SelloSAT=")- 2
            noCertificadoSAT =  cadena[num_cadena6:][:cadena_16]

            num_cadena7= cadena.find("RfcProvCertif=") + (len('RfcProvCertif='))+1
            cadena_17 = cadena[num_cadena7:].find("SelloCFD=")- 2
            RfcProvCertif =  cadena[num_cadena7:][:cadena_17]

            dic = {}
            
            #~Formato de respuesta pruebas (INICIO)
            dic['cadena_original_s'] = response["CadenaOriginal"]
            dic['fechaHoraTimbrado'] = response["FechaHoraTimbrado"]
            dic['folioCodCancelacion'] = response["FolioCodCancelacion"]
            dic['folio_fiscal'] = response["FolioUUID"]
            dic['sello_digita_emisor'] = response["SelloDigitalEmisor"]
            dic['sello_digita_sat'] = response["SelloDigitalTimbreSAT"]
            #~Formato de respuesta pruebas (FIN)
            
            dic['no_serie_csd_emisor'] = noCertificado
            dic['no_serie_csd_sat'] = noCertificadoSAT
            dic['RfcProvCertif'] = RfcProvCertif

            dic['XML'] = response["XML"]
            xml = response["XML"]
            vals_xml ={}
            vals_xml['xml_64'] =  response["XML"]
            xml_updt_id = self.pool.get('account.invoice').write(cr,uid, invoice_id, vals_xml)

            account_update = self.pool.get('account.invoice').write(cr,uid, invoice_id, dic)

            return dic

    # FUNCION PARA GENERAL EL XML A TIMBRAR
    def _generate_xml(self, cr, uid, invoice_ids, noseal, context=None):
        for invoice in noseal['invoice']:
            
            for co in noseal['company']:
                com = self.pool.get('res.company').browse(cr, SUPERUSER_ID, co.id, context=context)
                cert = com.cer
                calle = com.street
                calle2 = com.street2
                ciudad =com.city
                zip_co = com.zip
                estado_n = com.state_id.name
                country_n = com.country_id.name
                LugarE = '%s , %s , %s ,%s , %s , %s , %s' % (str(calle),str(calle2),str(zip_co),str(ciudad),str(ciudad),str(estado_n),str(country_n))
                LugarE = LugarE.decode("utf-8")
           
           #self.pool.get(res_partner) para forma de pago y num cuenta de pago
           
            sello = noseal['sello']
            noseal_fecha = noseal['date_1'][0:10]+"T"+noseal['date_1'][11:] 
            noseal_certificado = noseal['certificado']

            header = {
                'xmlns:cfdi': 'http://www.sat.gob.mx/cfd/3',
                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance' ,
                'xsi:schemaLocation': 'http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd', #TODO:'http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv32.xmlnscfdi', #hacer dinamico para acpetar una direccion mas
                
                'Version': '3.3',
                'Serie': noseal['serie'],
                'Folio': noseal['folio'],
                'Fecha': noseal_fecha,
                'Sello': sello,
                'FormaPago':noseal['metodoDePago'], 
                'NoCertificado':noseal_certificado,
                'Certificado': cert,
                'SubTotal':str(("%.2f" % invoice.amount_untaxed)) ,
                'Moneda':"MXN" ,
                'TipoCambio':"1" ,
                'Total':str(("%.2f" % invoice.amount_total)) ,
                'TipoDeComprobante':noseal['tipo_comprobante'],
                'MetodoPago': noseal['forma_pago'],
                'LugarExpedicion':str(zip_co) , #direccion de la res_company (emisor)
                }

        Comprobante = Element( 'cfdi:Comprobante', header )
        company_id = com
          
        if not company_id.rfc:
            raise osv.except_osv('Error', 'La compañia %s no tiene RFC definido'%company_id.name)
        elif not company_id.partner_id.street:
            raise osv.except_osv('Error', 'La compañia %s no tiene calle definida'%company_id.name)
        elif not company_id.street2:
            raise osv.except_osv('Error', 'La compañia %s no tiene No. exterior definido'%company_id.name)
        elif not company_id.partner_id.state_id.name:
            raise osv.except_osv('Error', 'La compañia %s no tiene el estado definido'%company_id.name)
        elif not company_id.city:
            raise osv.except_osv('Error', 'La compañia %s no tiene el municipio definida'%company_id.name)
        elif not company_id.partner_id.country_id.name:
            raise osv.except_osv('Error', 'La compañia %s no tiene el Pais definido'%company_id.name)
        elif not company_id.zip:
            raise osv.except_osv('Error', 'La compañia %s no tiene el codigo postal definido'%company_id.name)
        else:
            emisor = SubElement( Comprobante, 'cfdi:Emisor', Rfc=company_id.rfc ,Nombre=company_id.fiscal_name, RegimenFiscal=invoice.regimen_fiscal )
 
        for partner_id in noseal['partner']:
           
            if not partner_id.rfc_cliente:
                raise osv.except_osv('Error', 'El cliente %s no tiene RFC definido'%partner_id.name)
            elif not partner_id.street:
                raise osv.except_osv('Error', 'El cliente %s no tiene ninguna calle definida'%partner_id.name)
            elif not partner_id.street2:
                raise osv.except_osv('Error', 'El cliente %s no tiene No. exterior definido'%partner_id.name)
            elif not partner_id.city:
                raise osv.except_osv('Error', 'El cliente %s no tiene municipio definido'%partner_id.name)
            elif not partner_id.state_id.name:
                raise osv.except_osv('Error', 'El cliente %s no tiene estado definido'%partner_id.name)
            elif not partner_id.country_id.name:
                raise osv.except_osv('Error', 'El cliente %s no tiene pais definido'%partner_id.name)
            elif not partner_id.zip:
                raise osv.except_osv('Error', 'El cliente %s no tiene codigo postal definido'%partner_id.name)            
            else:
                nombre_r = partner_id.name
                receptor = SubElement( Comprobante, 'cfdi:Receptor', Rfc=partner_id.rfc_cliente , Nombre=nombre_r, UsoCFDI = invoice.uso_cfdi)
                
                conceptos = SubElement( Comprobante, 'cfdi:Conceptos' )
                for concept in invoice.invoice_line:
                    descripcion = concept.name
                    importe = concept.price_subtotal
                    concepto = SubElement( conceptos, 'cfdi:Concepto', ClaveProdServ=str(concept.clave_prod_serv), ClaveUnidad=str(concept.clave_unidad), Cantidad= str(concept.quantity), Unidad='Pieza', Descripcion=descripcion, ValorUnitario=str(("%.2f" % concept.price_unit)), Importe=str(("%.2f" % importe)))
                    concepto_i = SubElement( concepto, 'cfdi:Impuestos', )
                    traslados = SubElement( concepto_i, 'cfdi:Traslados')
                    tax_import = concept.price_subtotal * concept.invoice_line_tax_id.amount

                    traslado = SubElement( traslados, 'cfdi:Traslado', Impuesto="002", TipoFactor="Tasa", Base=str(("%.2f" % importe)), TasaOCuota="0.160000", Importe=str(("%.2f" % tax_import)))

                    if concepto is None:
                        raise osv.except_osv('Error', 'El cliente %s no tiene lineas'%partner_id.name)

        impuestos = SubElement( Comprobante, 'cfdi:Impuestos', TotalImpuestosTrasladados=str(("%.2f" % invoice.amount_tax)))
        traslados = SubElement( impuestos, 'cfdi:Traslados')
        traslado = SubElement( traslados, 'cfdi:Traslado', Impuesto="002", TipoFactor="Tasa", TasaOCuota="0.160000", Importe=str(("%.2f" % invoice.amount_tax)))
  
        output_file = open(ODOO_HOME+"facturacion_3_3/facturacion/invoices/original_string"+'/'+str(noseal.get('xmlname'))+'.xml', 'wb')
        xml_path = str(noseal['path'])+'/'+str(noseal.get('xmlname'))+'.xml'
        output_file.write( '<?xml version="1.0" encoding="UTF-8"?>' )  

        output_file.write( cElementTree.tostring( Comprobante ) )
        output_file.close() 

        return xml_path

    # FUNCION PARA LA CREACION DEL XML
    def bind_buttom(self, cr, uid,ids, context=None):
        
        original_path = ODOO_HOME + '/facturacion_3_3/facturacion/invoices/original_string'
        seal_path = ODOO_HOME + '/facturacion_3_3/facturacion/invoices/original_string'
        xsltpath = ODOO_HOME + '/facturacion_3_3/facturacion/invoices/SAT/cadenaoriginal_3_3/cadenaoriginal_3_3.xslt'
        infopath = ODOO_HOME + '/facturacion_3_3/facturacion/invoices/info'

        if context is None:
            context = {}
        for invoice in self.browse(cr, SUPERUSER_ID, ids, context=context):
            if invoice.bind == True:
                raise osv.except_osv('Error 901', 'La Factura que esta enviando ya fue previamente timbrada')
            if invoice.amount_total <= 0:
                raise osv.except_osv('Error en el Total', 'La Factura no puede ser timbrada en cantidades negativas o con un total de 0.0 pesos')

            invoices = {}
            company_id = invoice.company_id
            if not company_id.rfc:
                raise osv.except_osv('Error', 'La compañia %s no tiene RFC definido'%company_id.name)
            elif not company_id.partner_id.street:
                raise osv.except_osv('Error', 'La compañia %s no tiene calle definida'%company_id.name)
            elif not company_id.street2:
                raise osv.except_osv('Error', 'La compañia %s no tiene No. exterior definido'%company_id.name)
            elif not company_id.partner_id.state_id.name:
                raise osv.except_osv('Error', 'La compañia %s no tiene el estado definido'%company_id.name)
            elif not company_id.city:
                raise osv.except_osv('Error', 'La compañia %s no tiene el municipio definida'%company_id.name)
            elif not company_id.partner_id.country_id.name:
                raise osv.except_osv('Error', 'La compañia %s no tiene el Pais definido'%company_id.name)
            elif not company_id.zip:
                raise osv.except_osv('Error', 'La compañia %s no tiene el codigo postal definido'%company_id.name)

            partner_id = invoice.partner_id
            if not partner_id.rfc_cliente:
                raise osv.except_osv('Error', 'El cliente %s no tiene RFC definido'%partner_id.name)
            elif not partner_id.street:
                raise osv.except_osv('Error', 'El cliente %s no tiene ninguna calle definida'%partner_id.name)
            elif not partner_id.street2:
                raise osv.except_osv('Error', 'El cliente %s no tiene No. exterior definido'%partner_id.name)
            elif not partner_id.city:
                raise osv.except_osv('Error', 'El cliente %s no tiene municipio definido'%partner_id.name)
            elif not partner_id.state_id.name:
                raise osv.except_osv('Error', 'El cliente %s no tiene estado definido'%partner_id.name)
            elif not partner_id.country_id.name:
                raise osv.except_osv('Error', 'El cliente %s no tiene pais definido'%partner_id.name)
            elif not partner_id.zip:
                raise osv.except_osv('Error', 'El cliente %s no tiene codigo postal definido'%partner_id.name)
            elif len(partner_id.rfc_cliente)> 13:
                raise osv.except_osv('Error: RFC Mal Invalido', 'El cliente %s tiene un RFC con más caracteres de los permitidos'%partner_id.name)
            elif len(partner_id.rfc_cliente)<= 11:
                raise osv.except_osv('Error: RFC Mal Invalido', 'El cliente %s tiene un RFC con menos caracteres de los permitidos'%partner_id.name)


            keypem = infopath+'/'+company_id.rfc+'/'+company_id.rfc+'.key.pem'
            cerpem = infopath+'/'+company_id.rfc+'/'+company_id.rfc+'.cer.pem'

            if not os.path.exists(ODOO_HOME + 'facturacion_3_3/facturacion/invoices/info/'+str(company_id.rfc)):
                if not company_id.key:
                    raise osv.except_osv('Error', 'El archivo .key de la compañia %s no fue encontrado'%company_id.name)

                mkpath = ODOO_HOME + 'facturacion_3_3/facturacion/invoices/info/'+str(company_id.rfc)
                mkpathp = subprocess.Popen(['mkdir','-m','757',mkpath], stdout=subprocess.PIPE).communicate()[0]
                mkpathproc = repr(mkpathp)

                get_key = open(ODOO_HOME + "facturacion_3_3/facturacion/invoices/info/"+str(company_id.rfc)+"/"+str(company_id.rfc)+".key", "wb")
                get_key.write(company_id.key.decode('base64'))
                get_key.close()

                key_path = ODOO_HOME + "facturacion_3_3/facturacion/invoices/info/"+str(company_id.rfc)+"/"+str(company_id.rfc)+".key"
                output_keypem = ODOO_HOME + "facturacion_3_3/facturacion/invoices/info/"+str(company_id.rfc)+"/"+str(company_id.rfc)+".key.pem"

                key_proc1 = subprocess.Popen(shlex.split('openssl pkcs8 -inform DER -in '+key_path+' -out '+output_keypem+' -passin pass:'+company_id.jpassword),stdout=subprocess.PIPE)
                key_proc2 = subprocess.Popen(shlex.split('grep a'),stdin=key_proc1.stdout, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                key_proc1.stdout.close()

                if not company_id.cer:
                    raise osv.except_osv('Error', 'El archivo .cer de la compañia %s no fue encontrado'%company_id.name)

                get_key = open(ODOO_HOME + "facturacion_3_3/facturacion/invoices/info/"+str(company_id.rfc)+"/"+str(company_id.rfc)+".cer", "wb")
                get_key.write(company_id.cer.decode('base64'))
                get_key.close()
                
                cer_path = ODOO_HOME + "facturacion_3_3/facturacion/invoices/info/"+str(company_id.rfc)+"/"+str(company_id.rfc)+".cer"
                p = subprocess.Popen(["openssl", "x509", "-inform", "DER","-outform","PEM","-in",cer_path,"-pubkey"], stdout=subprocess.PIPE)
                (output, err) = p.communicate()

                get_key = open(ODOO_HOME + "facturacion_3_3/facturacion/invoices/info/"+str(company_id.rfc)+"/"+str(company_id.rfc)+".cer.pem", "w")
                get_key.write(output)
                get_key.close()


            else:
                pass

            xmlname = str(invoice.company_id.rfc)+'-'+str(invoice.serie)+'-'+str(invoice.folio)
            if os.path.isfile('%s/%s.xml' % (original_path,xmlname)):
                print '%s/%s.xml' % (original_path,xmlname)

            cerpem = infopath+'/'+company_id.rfc+'/'+company_id.rfc+'.cer'
            # cerpem = infopath+'/'+company_id.rfc+'/'+company_id.rfc+'.cer.pem'
            nocert = subprocess.Popen(['openssl','x509','-in',cerpem,'-inform','der','-outform','pem', '-out',cerpem+"_1.pem"], stdout=subprocess.PIPE).communicate()[0]
            nocert = subprocess.Popen(['openssl','x509','-in',cerpem+"_1.pem",'-serial','-noout'], stdout=subprocess.PIPE).communicate()[0]
            cert = repr(nocert)
            cert = cert and cert.replace('serial=', '').replace('33', 'B').replace('3', '').replace('B', '3').replace(' ', '').replace('&#10;', '').replace('\r', '').replace('\n', '').replace('\r\n', '').replace('\\n', '').replace('\"', '').replace('\'', '') or ''
            
            date_format = 'T%H:%M:%S'
            date_1 = invoice.fecha_emision
            date_1 = str(fields.datetime.now() - timedelta(hours=6))
            date_1 = date_1[0:19]
            date_noseal = date_1[0:10]+"T"+date_1[11:]
            
            #~generar xml sin sello
            info_no_seal = {}
            info_no_seal ['company'] = [company_id] #invoice.company_id
            info_no_seal ['partner'] = [invoice.partner_id]
            info_no_seal ['invoice_line'] = [invoice.invoice_line]
            info_no_seal ['invoice'] = [invoice]
            info_no_seal ['path'] = original_path
            info_no_seal ['xmlname'] = xmlname
            info_no_seal ['folio'] = invoice.folio
            info_no_seal ['serie'] = invoice.serie
            info_no_seal ['forma_pago'] = invoice.forma_pago
            info_no_seal ['metodoDePago'] = invoice.metodo_pago
            info_no_seal ['tipo_comprobante'] = invoice.tipo_comprobante
            info_no_seal ['sello'] = ''
            info_no_seal ['certificado'] = cert
            info_no_seal ['date_1'] = date_noseal
            xml_path = self._generate_xml(cr, uid, ids, info_no_seal, context=context)

            p1 = subprocess.Popen(['xsltproc',xsltpath,xml_path], stdout=subprocess.PIPE) #Set up the echo command and direct the output to a pipe 
            p2 = subprocess.Popen(['openssl','dgst','-sha256','-sign',keypem], stdin=p1.stdout, stdout=subprocess.PIPE) #send p1's output to p2
            p3 = subprocess.Popen(['openssl','enc','-base64','-A'], stdin=p2.stdout, stdout=subprocess.PIPE) #send p1's output to p2
            p1.stdout.close() #make sure we close the output so p2 doesn't hang waiting for more input
            output = p3.communicate()[0]

            xml_addenda = {}
            xml_addenda ['company'] = [company_id] #original -> company_id
            xml_addenda ['partner'] = [invoice.partner_id]
            xml_addenda ['invoice_line'] = [invoice.invoice_line]
            xml_addenda ['invoice'] = [invoice]
            xml_addenda ['path'] = seal_path
            xml_addenda ['xmlname'] = xmlname
            xml_addenda ['folio'] = invoice.folio
            xml_addenda ['serie'] = invoice.serie           
            xml_addenda ['forma_pago'] = invoice.forma_pago           
            xml_addenda ['metodoDePago'] = invoice.metodo_pago           
            xml_addenda ['tipo_comprobante'] = invoice.tipo_comprobante
            xml_addenda ['sello'] = output
            xml_addenda ['certificado'] = cert       
            xml_addenda ['date_1'] = date_noseal
            xml_seal_path = self._generate_xml(cr, uid, ids, xml_addenda, context=context)

            bind_xml = self._binding(cr,uid,xml_seal_path,invoice.id)
            try:
                uuid = str(bind_xml['folio_fiscal'])
                cOriginal = str(bind_xml['cadena_original_s'])
            except:
                raise osv.except_osv('Error', bind_xml)
            uuid = bind_xml['folio_fiscal']
            qr_total = '%017.6f' % invoice.amount_total

            qr = '?re=%s&rr=%s&tt=%s&id=%s' % (company_id.rfc,invoice.partner_id.rfc_cliente,qr_total,uuid)
            qr = qr.encode("utf-8")            
        return self.write(cr, uid, ids, { 'state_ac': 'open', 'bind': True, 'qr':qr})

    # def button_cancelar(self, cr, uid , ids, context=None):               
    #     if isinstance(ids, (int, long)):
    #         ids = [ids]
    #     if context is None:
    #        context = {}
        
    #     for invoice_id in ids:
            
    #         #Datos de account_invoice
    #         datos_account_invoice = self.browse(cr, uid, invoice_id, context=context)

    #         if datos_account_invoice.state_ac == 'cancel':
    #             raise osv.except_osv('Alerta', 'La factura ya está cancelada')
            
    #         if datos_account_invoice.bind: #Sólo si la factura ya está timbrada se manda llamar a rfacil

    #             # print '\t======tibrado productivo======'
    #             # WSDL = 'http://ws.rfacil.com/InterconectaWs.svc?wsdl'


    #             print '\t======tibrado pruebas======'
    #             WSDL  = 'http://wspruebas.rfacil.com/InterconectaWs.svc?wsdl'

    #             invoice_fac = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=None)
    #             id_company=invoice_fac.company_id

    #             USER = id_company.usr_proveedor 
    #             PASS = id_company.psw_proveedor
    #             certificadoEmisor = id_company.cer
    #             LlavePrivadaEmisor = id_company.key
    #             llavePrivadaEmisorPassword = id_company.jpassword
               
            
                # cbi_id = self.pool.get('account.invoice').search(cr, uid, [('id', '=', ids[0])])
                # bytesXmlCFDI = (self.pool.get('account.invoice').browse(cr, uid, cbi_id, context=context).xml_64).decode('base64')
                # bytesXmlCFDI = str(bytesXmlCFDI.decode("utf-8"))
                # bytesXmlCFDI = bytesXmlCFDI and bytesXmlCFDI.replace('&', '&amp;').replace('"', '&quot;').replace('"', '&apos;').replace('<', '&lt;').replace('>', '&gt;')

    #             client = Client(url=WSDL)

                # _logger.info("response (en button_cancelar): %r", bytesXmlCFDI)
                # src_tstamp_str = tools.datetime.now().strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
                # src_format = tools.misc.DEFAULT_SERVER_DATETIME_FORMAT
                # dst_format = DEFAULT_SERVER_DATETIME_FORMAT #format you want to get time in. 
                # dst_tz_name = self.pool.get('res.users').browse(cr, uid, uid, context=context).tz or 'Mexico/General'
                # _now = tools.misc.server_to_local_timestamp(src_tstamp_str, src_format, dst_format, dst_tz_name)
                
    #             fecha_solicitud = _now # time.strftime(DEFAULT_SERVER_DATETIME_FORMAT) # fields.datetime.now()
    #             response = client.service.cancelaCFDI33(USER,PASS,certificadoEmisor,LlavePrivadaEmisor,llavePrivadaEmisorPassword,bytesXmlCFDI)
    #             _logger.info("response (en button_cancelar): %r", response)
                
    #             vals = {
    #                 'state_ac': 'cancel',
    #                 'amount_total': 0,
    #                 'amount_untaxed':0,
    #                 'amount_tax':0,
    #                 'folioCodCancelacion': getattr(response, 'FolioCodCancelacion', False),
    #                 'xml_64_cancelado': getattr(response, 'XML', False),
    #                 'acuse': getattr(response, 'Acuse', False),
    #             }
                
                
    #             _logger.info("type(acuse): %r", type(vals['acuse']))
    #             signatureValueText = ""
    #             link_acuse = ""
    #             folio = datos_account_invoice.folio
    #             name = datos_account_invoice.partner_id.name + str(fields.date.today()) + folio
    #             name = name and name.replace(' ', '_')
                
    #             fechaHoraCancelacion = ''
                
    #             if vals['acuse']:
    #                 acuse_decoded = vals['acuse'].decode('base64')
    #                 _logger.info("acuse_decoded: %r", acuse_decoded)
                    
    #                 # link_acuse = "http://201.150.42.66:8069/jemil/static/cancelacion/acuses/acuse_"+name+".xml"
    #                 new_f = open(ODOO_HOME+"/facturacion_3_3/facturacion/static/cancelacion/acuses/acuse_"+name+".xml", "wb")
    #                 new_f.write(acuse_decoded)
    #                 new_f.close()
                    
    #                 acuse_tree = ET.fromstring(acuse_decoded)
    #                 #~ _logger.info("acuse_tree: %r", acuse_tree)
    #                 exprSignatureValue = './/{http://www.w3.org/2000/09/xmldsig#}SignatureValue'
    #                 signatureValueElem = acuse_tree.find(exprSignatureValue)
    #                 signatureValueText = signatureValueElem.text
    #                 _logger.info("signatureValueText: %r", signatureValueText)
                    
    #                 exprCFDResult = './/{http://cancelacfd.sat.gob.mx}CancelaCFDResult'
    #                 CFDResultElem = acuse_tree.find(exprCFDResult)
    #                 fechaHoraCancelacion = CFDResultElem.attrib['Fecha'][:19].replace('T', ' ')
                
    #             link_xml_cancelado = ""
    #             if vals['xml_64_cancelado']:
    #                 xml_cancelado_decoded = vals['xml_64_cancelado'].decode('base64')
                    
    #                 # link_xml_cancelado = "http://201.150.42.66:8069/jemil/static/cancelacion/cancel_"+name+".xml"
    #                 new_f = open(ODOO_HOME+"/facturacion_3_3/facturacion/static/cancelacion/cancel_"+name+".xml", "wb")
    #                 new_f.write(xml_cancelado_decoded)
    #                 new_f.close()
                    
                    
    #             if response.numError != 201:
    #                 raise osv.except_osv(response.numError, response.ErrorMessage)
    #                 return error

    #             template = self.pool.get('ir.model.data').get_object(cr, SUPERUSER_ID, 'jemil', 'mail_factura_cancelada_1')
    #             context['nombre_from']='Facturacion Jemil'
    #             context['correo_from']='facturacion@jemil.mx'
    #             nombre = self.pool.get('res.users').browse(cr, uid, uid, context=None)
    #             context['admon']=nombre.name
    #             context['folio']=datos_account_invoice.folio
    #             context['folio_fiscal']=datos_account_invoice.folio_fiscal
    #             context['rfc_emisor']=id_company.rfc
    #             context['fecha_solicitud']= fecha_solicitud
    #             context['fecha_cancelacion']= fechaHoraCancelacion
    #             context['sello']= signatureValueText
    #             context['empresa']=datos_account_invoice.partner_id.name
    #             context['descarga_xml_acuse']= link_acuse
    #             context['descarga_xml_cancelado']= link_xml_cancelado
    #             # context['receptor_email']="leticia@jemil.mx, admon1@jemil.mx, admon2@jemil.mx, admon3@jemil.mx, rosy@jemil.mx, emilio@jemil.mx, gruposydemas@gmail.com"
    #             # context['receptor_name']='leticia@jemil.mx, admon1@jemil.mx, admon2@jemil.mx, admon3@jemil.mx, rosy@jemil.mx, emilio@jemil.mx'

    #             _logger.info("Antes de envío de correo de cancelación -> context:%r", context)
    #             self.pool['email.template'].send_mail(cr, SUPERUSER_ID, template.id, ids[0], force_send=True, raise_exception=True, context=context)
    #             _logger.info("Después de envío de correo de cancelación -> context:%r", context)
    #             return self.write(cr, uid, ids, vals)
    #         else:
    #             raise osv.except_osv(("¡Error!"), ('Esta factura no ha sido timbrada o fue actualizada después de timbrar.'))


    def button_estatus(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
            if context is None:
                context = {}

        for invoice_id in ids:

            #DATOS de account in voice

            datos_account_invoice = self.browse(cr, uid, invoice_id, context=context)

            if datos_account_invoice.state_ac == 'cancel':
                raise osv.except_osv('Alerta', 'La factura ya esta cancelada')

            if datos_account_invoice.bind: #Solo si la factura se encuentra timbrada se llama a rfacil

                print '\t========Timbrado de pruebas========'
                WSDL = 'http://wspruebas.rfacil.com/wsCancela33.svc?wsdl'

                invoice_fac = self.pool.get('account.invoice').browse(cr,uid, invoice_id, context=None)
                id_company = invoice_fac.company_id


                #Fields que se necesitan para cancelar la factura y timbrado de la misma, en dado caso que no este timbrada
                USER = id_company.usr_proveedor
                PASS = id_company.psw_proveedor
                certificadoEmisor = id_company.cer
                LlavePrivadaEmisor = id_company.key
                llavePrivadaEmisorPassword = id_company.jpassword

                rfc_emisor = id_company.rfc
                RFC_Receptor = datos_account_invoice.partner_id.rfc_cliente
                UUID = datos_account_invoice.folio_fiscal
                Monto = datos_account_invoice.amount_total
                SelloEmisor = datos_account_invoice.sello_digita_emisor
                estatus = datos_account_invoice.factura_estatus
                estado_soli = datos_account_invoice.estado_soli
                n_seguimiento = datos_account_invoice.n_seguimiento
                state_ac = datos_account_invoice.state_ac
                forma_pago = datos_account_invoice.forma_pago

                #Instrucciones para buscar el XML a cancelar

                cbi_id = self.pool.get('account.invoice').search(cr, uid, [('id', '=', ids[0])])
                bytesXmlCFDI = (self.pool.get('account.invoice').browse(cr, uid, cbi_id, context=context).xml_64).decode('base64')
                bytesXmlCFDI = str(bytesXmlCFDI.decode("utf-8"))
                bytesXmlCFDI = bytesXmlCFDI and bytesXmlCFDI.replace('&', '&amp;').replace('"', '&quot;').replace('"', '&apos;').replace('<', '&lt;').replace('>', '&gt;')

                client= Client(url=WSDL)


                #Instrucciones para traer la fecha del dia en el que se realiza el proceso

                _logger.info("response (en button_estatus): %r", bytesXmlCFDI)
                src_tstamp_str = tools.datetime.now().strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
                src_format = tools.misc.DEFAULT_SERVER_DATETIME_FORMAT
                dst_format = DEFAULT_SERVER_DATETIME_FORMAT #format you want to get time in. 
                dst_tz_name = self.pool.get('res.users').browse(cr, uid, uid, context=context).tz or 'Mexico/General'
                _now = tools.misc.server_to_local_timestamp(src_tstamp_str, src_format, dst_format, dst_tz_name)


                #Peticion para leer datos que se enviaran al Soap de Rfacil en response mediante ConsultaQR


                fecha_solicitud = _now
                digits = SelloEmisor[336:344] #rango para sacar los ultimos ocho digitos del SelloEmisor
                digits2 = digits
                print digits2
                response = client.service.ConsultaQr(USER, PASS, rfc_emisor, RFC_Receptor, UUID, Monto, digits)
                _logger.info("response (en button_estatus): %r", response)

                if response.Estado == "Cancelado":
                        datos_account_invoice.state_ac = 'cancel'
                        fecha_solicitud = _now
                        response = client.service.RegistraSolicitud(USER, PASS, certificadoEmisor, LlavePrivadaEmisor, llavePrivadaEmisorPassword, bytesXmlCFDI)
                        _logger.info("response (en _button_cancel_factura): %r", response)



                        vals = {

                        'state_ac':'cancel',
                        'amount_total': 0,
                        'amount_untaxed': 0,
                        'amount_tax': 0,
                        'FolioCodCancelacion': getattr(response, 'FolioCodCancelacion', False),
                        'xml_64_cancelado': getattr(response, 'XML', False),
                        'acuse': getattr(response, 'Acuse', False),
                        }


                        _logger.info("type(acuse): %r", type(vals['acuse']))
                        signatureValueText = ''
                        link_acuse = ''
                        folio = datos_account_invoice.folio
                        name = datos_account_invoice.partner_id.name + str(fields.date.today()) + folio
                        name and name.replace('','_')

                        fechaHoraCancelacion = ''


                        if vals['acuse']:
                            # acuse_decoded = vals['acuse'].decode('base64')
                            acuse_decoded = vals['acuse']
                            _logger.info("acuse_decoded: %r", acuse_decoded)

                            # link_acuse = "http://201.150.42.66:8069/jemil/static/cancelacion/acuses/acuse_"+name+".xml"
                            new_f = open(ODOO_HOME+"facturacion_3_3/facturacion/invoices/cancelacion/acuses/acuse_"+name+".xml", "wb")
                            new_f.write(acuse_decoded)
                            new_f.close()
                            print acuse_decoded

                            acuse_tree = ET.fromstring(acuse_decoded)
                            #~ _logger.info("acuse_tree: %r", acuse_tree)
                            exprSignatureValue = './/{http://www.w3.org/2000/09/xmldsig#}SignatureValue'
                            signatureValueElem = acuse_tree.find(exprSignatureValue)
                            signatureValueText = signatureValueElem.text
                            _logger.info("signatureValueText: %r", signatureValueText)
                            


                            exprCFDResult = './/{http://wspruebas.rfacil.com/wsCancela33.svc?wsdl'  #Timbrado de cancelacion de prueba
                            # exprCFDResult = './/{http://cancelacfd.sat.gob.mx}CancelaCFDResult'
                            CFDResultElem = acuse_tree.find(exprCFDResult)
                            # fechaHoraCancelacion = CFDResultElem.attrib['Fecha'][:19].replace('T', ' ')

                            # Codigo para crear el xml
                        
                        link_xml_cancelado = ""
                        if vals['xml_64_cancelado']:
                            xml_cancelado_decoded = vals['xml_64_cancelado'].decode('base64')
                            
                            # link_xml_cancelado = "http://201.150.42.66:8069/jemil/static/cancelacion/cancel_"+name+".xml"
                            new_f = open(ODOO_HOME+"/facturacion_3_3/facturacion/invoices/cancelacion/cancel_"+name+".xml", "wb")
                            new_f.write(xml_cancelado_decoded)
                            new_f.close()

                #Instruccion que verifica el estatus que tiene la factura y la guarda en el campo factura_estatus
                elif response.ResultadoCodigo == 'S-0':
                    vals = {}
                    vals['factura_estatus'] = response["EsCancelable"]
                    factura_estatus = self.pool.get('account.invoice').write(cr,uid, invoice_id, vals)

                elif response.ResultadoCodigo == '206':
                    vals = {}
                    vals['factura_estatus'] = response["EsCancelable"]
                    vals['n_seguimiento'] = response['Rastreo']
                    n_seguimiento = self.pool.get('account.invoice').write(cr,uid, invoice_id, vals)   

                elif response.EsCancelable == "No cancelable":
                    vals = {}
                    vals['factura_estatus'] = response['EsCancelable']
                    factura_estatus = self.pool.get('account.invoice').write(cr,uid, invoice_id, vals)


                else:
                    error = 'Error %s : %s' % (response.ResultadoCodigo, response.ResultadoDescripcion)
                    raise osv.except_osv('Error', error)



    # def button_cancel_f_ppd(self, cr, uid, ids, context=None):
    #     if isinstance(ids, (int, long)):
    #         ids = [ids]
    #         if context is None:
    #             context = {}

    #     for invoice_id in ids:

    #         #DATOS de account in voice

    #         datos_account_invoice = self.browse(cr, uid, invoice_id, context=context)

    #         if datos_account_invoice.state_ac == 'cancel':
    #             raise osv.except_osv('Alerta', 'La factura ya esta cancelada')

    #         if datos_account_invoice.bind: #Solo si la factura se encuentra timbrada se llama a rfacil

    #             print '\t========Timbrado de pruebas========'
    #             WSDL = 'http://wspruebas.rfacil.com/wsCancela33.svc?wsdl'

    #             invoice_fac = self.pool.get('account.invoice').browse(cr,uid, invoice_id, context=None)
    #             id_company = invoice_fac.company_id


    #             #Fields que se necesitan para cancelar la factura y timbrado de la misma, en dado caso que no este timbrada
    #             USER = id_company.usr_proveedor
    #             PASS = id_company.psw_proveedor
    #             certificadoEmisor = id_company.cer
    #             LlavePrivadaEmisor = id_company.key
    #             llavePrivadaEmisorPassword = id_company.jpassword

    #             rfc_emisor = id_company.rfc
    #             RFC_Receptor = datos_account_invoice.partner_id.rfc_cliente
    #             UUID = datos_account_invoice.folio_fiscal
    #             Monto = datos_account_invoice.amount_total
    #             SelloEmisor = datos_account_invoice.sello_digita_emisor
    #             estatus = datos_account_invoice.factura_estatus
    #             estado_soli = datos_account_invoice.estado_soli
    #             n_seguimiento = datos_account_invoice.n_seguimiento
    #             state_ac = datos_account_invoice.state_ac
    #             forma_pago = datos_account_invoice.forma_pago

    #             #Instrucciones para buscar el XML a cancelar

    #             cbi_id = self.pool.get('account.invoice').search(cr, uid, [('id', '=', ids[0])])
    #             bytesXmlCFDI = (self.pool.get('account.invoice').browse(cr, uid, cbi_id, context=context).xml_64).decode('base64')
    #             bytesXmlCFDI = str(bytesXmlCFDI.decode("utf-8"))
    #             bytesXmlCFDI = bytesXmlCFDI and bytesXmlCFDI.replace('&', '&amp;').replace('"', '&quot;').replace('"', '&apos;').replace('<', '&lt;').replace('>', '&gt;')

    #             client= Client(url=WSDL)


    #             #Instrucciones para traer la fecha del dia en el que se realiza el proceso

    #             _logger.info("response (en button_estatus): %r", bytesXmlCFDI)
    #             src_tstamp_str = tools.datetime.now().strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
    #             src_format = tools.misc.DEFAULT_SERVER_DATETIME_FORMAT
    #             dst_format = DEFAULT_SERVER_DATETIME_FORMAT #format you want to get time in. 
    #             dst_tz_name = self.pool.get('res.users').browse(cr, uid, uid, context=context).tz or 'Mexico/General'
    #             _now = tools.misc.server_to_local_timestamp(src_tstamp_str, src_format, dst_format, dst_tz_name)


    #             #Peticion para leer datos que se enviaran al Soap de Rfacil en response mediante ConsultaQR


    #             fecha_solicitud = _now
    #             digits = SelloEmisor[336:344] #rango para sacar los ultimos ocho digitos del SelloEmisor
    #             digits2 = digits
    #             print digits2
    #             response = client.service.ConsultaQr(USER, PASS, rfc_emisor, RFC_Receptor, UUID, Monto, digits)
    #             _logger.info("response (en button_estatus): %r", response)


    #             if response.Estado == "Cancelado":
    #                     datos_account_invoice.state_ac = 'cancel'








    #Boton para Cancelar la factura una vez que ya tenga un estatus de cancelable con/sin aceptacion
    def button_cancel_factura(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
            if context is None:
                context = {}

        for invoice_id in ids:

            #DATOS de account in voice

            datos_account_invoice = self.browse(cr, uid, invoice_id, context=context)

            if datos_account_invoice.state_ac == 'cancel':
                raise osv.except_osv('Alerta', 'La factura ya esta cancelada')

            if datos_account_invoice.bind: #Solo si la factura se encuentra timbrada se llama a rfacil

                print '\t========Timbrado de pruebas========'
                WSDL = 'http://wspruebas.rfacil.com/wsCancela33.svc?wsdl'

                invoice_fac = self.pool.get('account.invoice').browse(cr,uid, invoice_id, context=None)
                id_company = invoice_fac.company_id

                #Fields que se necesitan para cancelar la factura y timbrado de la misma, en dado caso que no este timbrada
                USER = id_company.usr_proveedor
                PASS = id_company.psw_proveedor
                certificadoEmisor = id_company.cer
                LlavePrivadaEmisor = id_company.key
                LlavePrivadaEmisorPassword = id_company.jpassword

                rfc_emisor = id_company.rfc
                RFC_Receptor = datos_account_invoice.partner_id.rfc_cliente
                UUID = datos_account_invoice.folio_fiscal
                Monto = datos_account_invoice.amount_total
                SelloEmisor = datos_account_invoice.sello_digita_emisor
                estatus = datos_account_invoice.factura_estatus
                estado_soli = datos_account_invoice.estado_soli
                n_seguimiento = datos_account_invoice.n_seguimiento
                state_ac = datos_account_invoice.state_ac



                #Instrucciones para buscar el XML a cancelar

                cbi_id = self.pool.get('account.invoice').search(cr, uid, [('id', '=', ids[0])])
                bytesXmlCFDI = (self.pool.get('account.invoice').browse(cr, uid, cbi_id, context=context).xml_64).decode('base64')
                bytesXmlCFDI = str(bytesXmlCFDI.decode("utf-8"))
                bytesXmlCFDI = bytesXmlCFDI and bytesXmlCFDI.replace('&', '&amp;').replace('"', '&quot;').replace('"', '&apos;').replace('<', '&lt;').replace('>', '&gt;')

                client= Client(url=WSDL)

                #Instrucciones para traer la fecha del dia en el que se realiza el proceso

                _logger.info("response (en _button_cancel_factura): %r", bytesXmlCFDI)
                src_tstamp_str = tools.datetime.now().strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
                src_format = tools.misc.DEFAULT_SERVER_DATETIME_FORMAT
                dst_format = DEFAULT_SERVER_DATETIME_FORMAT #format you want to get time in. 
                dst_tz_name = self.pool.get('res.users').browse(cr, uid, uid, context=context).tz or 'Mexico/General'
                _now = tools.misc.server_to_local_timestamp(src_tstamp_str, src_format, dst_format, dst_tz_name)


                #SI el campo factura_estatus es cancelable sin aceptacion, se cancelara la factura
                if estatus == 'Cancelable sin aceptación':
                    datos_account_invoice.state_ac = 'cancel'
                    fecha_solicitud = _now
                    response = client.service.RegistraSolicitud(USER, PASS, certificadoEmisor, LlavePrivadaEmisor, LlavePrivadaEmisorPassword, bytesXmlCFDI)
                    _logger.info("response (en _button_cancel_factura): %r", response)



                    vals = {

                    'state_ac':'cancel',
                    'amount_total': 0,
                    'amount_untaxed': 0,
                    'amount_tax': 0,
                    'FolioCodCancelacion': getattr(response, 'FolioCodCancelacion', False),
                    'xml_64_cancelado': getattr(response, 'XML', False),
                    'acuse': getattr(response, 'Acuse', False),
                    }


                    _logger.info("type(acuse): %r", type(vals['acuse']))
                    signatureValueText = ''
                    link_acuse = ''
                    folio = datos_account_invoice.folio
                    name = datos_account_invoice.partner_id.name + str(fields.date.today()) + folio
                    name and name.replace('','_')

                    fechaHoraCancelacion = ''


                    if vals['acuse']:
                        # acuse_decoded = vals['acuse'].decode('base64')
                        acuse_decoded = vals['acuse']
                        _logger.info("acuse_decoded: %r", acuse_decoded)

                        # link_acuse = "http://201.150.42.66:8069/jemil/static/cancelacion/acuses/acuse_"+name+".xml"
                        new_f = open(ODOO_HOME+"facturacion_3_3/facturacion/invoices/cancelacion/acuses/acuse_"+name+".xml", "wb")
                        new_f.write(acuse_decoded)
                        new_f.close()
                        print acuse_decoded

                        acuse_tree = ET.fromstring(acuse_decoded)
                        #~ _logger.info("acuse_tree: %r", acuse_tree)
                        exprSignatureValue = './/{http://www.w3.org/2000/09/xmldsig#}SignatureValue'
                        signatureValueElem = acuse_tree.find(exprSignatureValue)
                        signatureValueText = signatureValueElem.text
                        _logger.info("signatureValueText: %r", signatureValueText)
                        


                        exprCFDResult = './/{http://wspruebas.rfacil.com/wsCancela33.svc?wsdl'  #Timbrado de cancelacion de prueba
                        # exprCFDResult = './/{http://cancelacfd.sat.gob.mx}CancelaCFDResult'
                        CFDResultElem = acuse_tree.find(exprCFDResult)
                        # fechaHoraCancelacion = CFDResultElem.attrib['Fecha'][:19].replace('T', ' ')

                        # Codigo para crear el xml
                    
                    link_xml_cancelado = ""
                    if vals['xml_64_cancelado']:
                        xml_cancelado_decoded = vals['xml_64_cancelado'].decode('base64')
                        
                        # link_xml_cancelado = "http://201.150.42.66:8069/jemil/static/cancelacion/cancel_"+name+".xml"
                        new_f = open(ODOO_HOME+"/facturacion_3_3/facturacion/invoices/cancelacion/cancel_"+name+".xml", "wb")
                        new_f.write(xml_cancelado_decoded)
                        new_f.close()


                    #Funcion para enviar un Email a el cliente de que la factura fue cancelada
                        

                    # template = self.pool.get('ir.model.data').get_object(cr, SUPERUSER_ID, 'lafox', 'template_email_cancelado')
                    # context['nombre_from']='Facturacion Lafox'
                    # context['correo_from']='facturacion@lafox.mx'
                    # nombre = self.pool.get('res.users').browse(cr, uid, uid, context=None)
                    # context['admon']=nombre.name
                    # context['folio']=datos_account_invoice.folio
                    # context['folio_fiscal']=datos_account_invoice.folio_fiscal
                    # context['rfc_emisor']=id_company.rfc
                    # context['RFC_Receptor'] = datos_account_invoice.partner_id.rfc_cliente
                    # context['Monto'] = datos_account_invoice.amount_total
                    # context['fecha_solicitud']= fecha_solicitud
                    # context['fecha_cancelacion']= fechaHoraCancelacion
                    # context['sello']= signatureValueText
                    # context['empresa']=datos_account_invoice.partner_id.name
                    # context['descarga_xml_acuse']= link_acuse
                    # context['descarga_xml_cancelado']= link_xml_cancelado
                    # # context['receptor_email']="leticia@jemil.mx, admon1@jemil.mx, admon2@jemil.mx, admon3@jemil.mx, rosy@jemil.mx, emilio@jemil.mx, gruposydemas@gmail.com"
                    # # context['receptor_name']='leticia@jemil.mx, admon1@jemil.mx, admon2@jemil.mx, admon3@jemil.mx, rosy@jemil.mx, emilio@jemil.mx'

                    # _logger.info("Antes de envío de correo de cancelación -> context:%r", context)
                    # self.pool['email.template'].send_mail(cr, SUPERUSER_ID, template.id, ids[0], force_send=True, raise_exception=True, context=context)
                    # _logger.info("Después de envío de correo de cancelación -> context:%r", context)
                    # return self.write(cr, uid, ids, vals)



                #Si el campo factura_estatus es cancelable con aceptacion, se solicitara la peticion para este tipo de cancelaciones
                else:
                    estatus == 'Cancelable con aceptacion'
                    fecha_solicitud = _now
                    response = client.service.RegistraSolicitud(USER, PASS, certificadoEmisor, LlavePrivadaEmisor, LlavePrivadaEmisorPassword, bytesXmlCFDI)
                    _logger.info("response (en _button_cancel_factura): %r", response)


                    #Imprime el codigo de rastreo que envia el SAT en el campo n_rastreo
                    if response.ResultadoCodigo == 'S-206':
                        vals = {}
                        vals['n_seguimiento'] = response["Rastreo"]
                        n_seguimiento = self.pool.get('account.invoice').write(cr,uid, invoice_id, vals)


                    #Muestra la informacion de si la factura se cancelo o lanzo algun otro codigo diferente

                    else:
                        response.ResultadoCodigo != 'S-201'
                        error = 'Error %s : %s' % (response.ResultadoCodigo, response.ResultadoDescripcion)
                        return error


    #Boton para consultar el estatus de la cancelacion de factura

    def button_consul_estatus(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
            if context is None:
                context = {}

        for invoice_id in ids:

            #DATOS de account in voice

            datos_account_invoice = self.browse(cr, uid, invoice_id, context=context)

            if datos_account_invoice.state_ac == 'cancel':
                raise osv.except_osv('Alerta', 'La factura ya esta cancelada')

            if datos_account_invoice.bind: #Solo si la factura se encuentra timbrada se llama a rfacil

                print '\t========Timbrado de pruebas========'
                WSDL = 'http://wspruebas.rfacil.com/wsCancela33.svc?wsdl'

                invoice_fac = self.pool.get('account.invoice').browse(cr,uid, invoice_id, context=None)
                id_company = invoice_fac.company_id


                #campo que contiene el numero de seguimiento a verificar
                USER = id_company.usr_proveedor
                PASS = id_company.psw_proveedor
                segui = datos_account_invoice.n_seguimiento
                RFC_Receptor = datos_account_invoice.partner_id.rfc_cliente
                UUID = datos_account_invoice.folio_fiscal
                SelloEmisor = datos_account_invoice.sello_digita_emisor
                estatus = datos_account_invoice.factura_estatus
                estado_soli = datos_account_invoice.estado_soli
                n_seguimiento = datos_account_invoice.n_seguimiento
                state_ac = datos_account_invoice.state_ac


                client= Client(url=WSDL)
                #Instrucciones para traer la fecha del dia en el que se realiza el proceso

                _logger.info("response (en button_consul_estatus): %r")
                src_tstamp_str = tools.datetime.now().strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
                src_format = tools.misc.DEFAULT_SERVER_DATETIME_FORMAT
                dst_format = DEFAULT_SERVER_DATETIME_FORMAT #format you want to get time in. 
                dst_tz_name = self.pool.get('res.users').browse(cr, uid, uid, context=context).tz or 'Mexico/General'
                _now = tools.misc.server_to_local_timestamp(src_tstamp_str, src_format, dst_format, dst_tz_name)


                fecha_solicitud = _now
                response = client.service.SeguimientoSolicitud(USER, PASS, n_seguimiento)
                _logger.info("response (en button_consul_estatus): %r", response)


                #Si el ResultadoCodigo es R-1011 se manda la solicitud para que sea cancelado

                if response.ResultadoCodigo == 'R-1011':
                    vals = {}
                    vals['estado_soli'] = response["Estatus"]
                    n_estatus = self.pool.get('account.invoice').write(cr,uid, invoice_id, vals)

                    #Valores para crear el xml, dependiendo el estatus en el que se encuentre
                    if response.Estatus != 'Rechazado':
                        datos_account_invoice.state_ac = 'cancel'
                        vals = {

                        'state_ac':'cancel',
                        'amount_total': 0,
                        'amount_untaxed': 0,
                        'amount_tax': 0,
                        'FolioCodCancelacion': getattr(response, 'FolioCodCancelacion', False),
                        'xml_64_cancelado': getattr(response, 'XML', False),
                        'acuse': getattr(response, 'Acuse', False),
                        }


                        _logger.info("type(acuse): %r", type(vals['acuse']))
                        signatureValueText = ''
                        link_acuse = ''
                        folio = datos_account_invoice.folio
                        name = datos_account_invoice.partner_id.name + str(fields.date.today()) + folio
                        name and name.replace('','_')

                        fechaHoraCancelacion = ''


                        if vals['acuse']:
                            # acuse_decoded = vals['acuse'].decode('base64')
                            acuse_decoded = vals['acuse']
                            _logger.info("acuse_decoded: %r", acuse_decoded)

                            # link_acuse = "http://201.150.42.66:8069/jemil/static/cancelacion/acuses/acuse_"+name+".xml"
                            new_f = open(ODOO_HOME+"facturacion_3_3/facturacion/invoices/cancelacion/acuses/acuse_"+name+".xml", "wb")
                            new_f.write(acuse_decoded)
                            new_f.close()
                            print acuse_decoded

                            acuse_tree = ET.fromstring(acuse_decoded)
                            #~ _logger.info("acuse_tree: %r", acuse_tree)
                            exprSignatureValue = './/{http://www.w3.org/2000/09/xmldsig#}SignatureValue'
                            signatureValueElem = acuse_tree.find(exprSignatureValue)
                            signatureValueText = signatureValueElem.text
                            _logger.info("signatureValueText: %r", signatureValueText)
                            


                            exprCFDResult = './/{http://wspruebas.rfacil.com/wsCancela33.svc?wsdl'  #Timbrado de cancelacion de prueba
                            # exprCFDResult = './/{http://cancelacfd.sat.gob.mx}CancelaCFDResult'
                            CFDResultElem = acuse_tree.find(exprCFDResult)
                            # fechaHoraCancelacion = CFDResultElem.attrib['Fecha'][:19].replace('T', ' ')


                            #Codigo para crear el xml

                            link_xml_cancelado = ""
                    if vals['xml_64_cancelado']:
                        xml_cancelado_decoded = vals['xml_64_cancelado'].decode('base64')
                        
                        # link_xml_cancelado = "http://201.150.42.66:8069/jemil/static/cancelacion/cancel_"+name+".xml"
                        new_f = open(ODOO_HOME+"/facturacion_3_3/facturacion/invoices/cancelacion/cancel_"+name+".xml", "wb")
                        new_f.write(xml_cancelado_decoded)
                        new_f.close()


                else:
                    response.ResultadoCodigo != 'R-1011'
                    error = 'Error %s : %s' % (response.ResultadoCodigo, response.ResultadoDescripcion)
                    return error
                    


account_invoice()



class account_invoice_line(models.Model):
    _name = "account.invoice.line"
    _inherit="account.invoice.line"

    clave_prod_serv = fields.Char(string='Clave del Servicio/Producto')
    clave_unidad = fields.Char(string='Clave de Unidad')

account_invoice_line()


class lafox_recibo_electronico_pago(models.Model):
    _name='lafox.recibo.electronico.pago'

    @api.multi
    @api.depends('fecha')
    def _compute_montopago(self):  
        active_model = self.env['account.invoice'].browse(self._context.get('active_id'))   
        res = str (active_model.saldo_pediente)

        return res

    # CREACION DE XML PARA LOS RECIBOS ELECTRONICOS DE PAGO
    def _generate_xml_recibo(self,noseal):
        print noseal
        monto_r = str("{0:.2f}".format(float(noseal['Monto'])))
        saldoAnt = str("{0:.2f}".format(float(noseal['Total'])))
        residuo = str("{0:.2f}".format(float(noseal['Total']) - float(monto_r)))
        for co in noseal['company']:
            com = co.id
            zip_co = co.zip
            company_p = co.rfc
            name_p = co.fiscal_name
            

        header = {
            'xmlns:cfdi': 'http://www.sat.gob.mx/cfd/3',
            'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance' ,
            'xsi:schemaLocation': 'http://www.sat.gob.mx/cfd/3 http://www.sat.gob.mx/sitio_internet/cfd/3/cfdv33.xsd',
            'Version': '3.3',
            'Serie': noseal['serie'],
            'Folio': noseal['folio'],
            'Fecha': noseal['date_1'],
            'Sello': '',
            'NoCertificado':'',
            'Certificado': '',
            'SubTotal': noseal['SubTotal'] ,
            'Moneda':"XXX" ,
            # 'TipoCambio':"1" ,
            'Total':noseal['SubTotal'] ,
            'TipoDeComprobante':noseal['tipo_comprobante'],
            'LugarExpedicion':str(zip_co) , #direccion de la res_company (emisor)
            }
        Comprobante = Element( 'cfdi:Comprobante', header )
        output_file = open(ODOO_HOME+"facturacion_3_3/facturacion/recibos/original_string"+'/'+str(noseal.get('xmlname'))+'.xml', 'wb')
        xml_path = str(noseal['path'])+'/'+str(noseal.get('xmlname'))+'.xml'
        output_file.write( '<?xml version="1.0" encoding="UTF-8"?>' )  

        relacion_uid = SubElement( Comprobante, 'cfdi:CfdiRelacionados ', TipoRelacion='09' )
        relacion_uid_i = SubElement( relacion_uid, 'cfdi:CfdiRelacionado', UUID=self.folio_cfdi )
        emisor = SubElement( Comprobante, 'cfdi:Emisor', Rfc=company_p ,Nombre=name_p, RegimenFiscal=noseal['RegimenFiscal'] )
        for partner_id in noseal['partner']:
            receptor = SubElement( Comprobante, 'cfdi:Receptor', Rfc=partner_id.rfc_cliente , Nombre=partner_id.name, UsoCFDI = 'P01')
            # receptor = SubElement( Comprobante, 'cfdi:Receptor', Rfc=partner_id.razon_social , Nombre=partner_id.name, UsoCFDI = noseal['UsoCFDI'])

        header_pagos ={
            'xmlns:xsi':"http://www.w3.org/2001/XMLSchema-instance",
            'xmlns:pago10':"http://www.sat.gob.mx/Pagos",
            'xsi:schemaLocation': "http://www.sat.gob.mx/Pagos http://www.sat.gob.mx/sitio_internet/cfd/Pagos/Pagos10.xsd",
            'Version':"1.0"
        }
        conceptos = SubElement( Comprobante, 'cfdi:Conceptos' )
        concepto = SubElement( conceptos, 'cfdi:Concepto', ClaveProdServ='84111506', ClaveUnidad='ACT', Cantidad= '1', Descripcion='Pago', ValorUnitario='0', Importe='0')

        pagos_com = SubElement( Comprobante, 'cfdi:Complemento' )
        pagos = SubElement( pagos_com, 'pago10:Pagos', header_pagos)
        pago = SubElement( pagos, 'pago10:Pago',FechaPago=noseal['date_1'], FormaDePagoP=noseal['FormaDePagoP'],  MonedaP="MXN", Monto=monto_r, NumOperacion=str(noseal['NumOperacion']).zfill(2) )
        pago1 = SubElement( pago, 'pago10:DoctoRelacionado', IdDocumento=self.folio_cfdi, Serie='H', Folio= noseal['folio'], MonedaDR='MXN', MetodoDePagoDR="PPD", NumParcialidad="1", ImpSaldoAnt=saldoAnt, ImpPagado=monto_r, ImpSaldoInsoluto=residuo )


        output_file.write( cElementTree.tostring( Comprobante ) )
        output_file.close()
        return xml_path

    @api.onchange('cfdi')
    def _onchange_montopago(self):
        original_path = ODOO_HOME + 'facturacion_3_3/facturacion/recibos/original_string'
        seal_path = ODOO_HOME + 'facturacion_3_3/facturacion/invoices/original_string'
        xsltpath = ODOO_HOME + 'facturacion_3_3/facturacion/invoices/SAT/cadenaoriginal_3_3/cadenaoriginal_3_3.xslt'
        infopath = ODOO_HOME + 'facturacion_3_3/facturacion/invoices/info'
        self.fecha = fields.Date.today()

        for invoice in self:
            active_model = self.env['account.invoice'].browse(self._context.get('active_id')) 
            client = active_model.partner_id
            folio_fiscal = active_model.folio_fiscal
            company_id = active_model.company_id
            date_1 = self.fecha
            xmlname = 'PAGO-'+str(active_model.company_id.rfc)+'-'+'G'+'-'+str(active_model.folio)
        if self.cfdi != False:
            pagos_ids = self.search([('invoice_id', '=', active_model.id)], order='fecha desc')
            if not pagos_ids :
                NoOperacion = str(1).zfill(2) 
            else:
                NoOperacion = str(pagos_ids[0].numero_pago).zfill(2) 

            self.show = True
            data = base64.decodestring(self.cfdi)
            forma_pago = self.forma_pago
            date_format = 'T%H:%M:%S'
            date_1 = str(fields.datetime.now() - timedelta(hours=6))
            date_1 = date_1[0:19]
            date_noseal = date_1[0:10]+"T"+date_1[11:]

            info_pago = {}
            info_pago['company'] = [company_id] 
            info_pago['partner'] = [active_model.partner_id]
            info_pago['invoice_line'] = [active_model.invoice_line]
            info_pago['invoice'] = [active_model.id]
            info_pago['path'] = original_path
            info_pago['xmlname'] = xmlname
            info_pago['folio'] = active_model.folio
            info_pago['serie'] = 'G'
            info_pago['Total'] = str(active_model.amount_total)
            info_pago['Monto'] = str(self.monto_pago)
            info_pago['SubTotal'] = '0'
            info_pago['Moneda'] = 'XXX'
            info_pago['tipo_comprobante'] = 'P'
            info_pago['NoCertificado'] = ''
            info_pago['Certificado'] = ''
            info_pago['Sello'] = ''
            info_pago['NumOperacion'] = NoOperacion
            info_pago['FormaDePagoP'] = str(forma_pago)
            info_pago['RegimenFiscal'] = active_model.regimen_fiscal
            info_pago['UsoCFDI'] = active_model.uso_cfdi
            info_pago['date_1'] = date_noseal
            xml_info = self._generate_xml_recibo(info_pago)
            self.xml_recibo = xml_info

        # self.monto_pago = monto
        self.cliente = client
        self.folio_cfdi = folio_fiscal
        active_model.monto_pago = self.monto_pago
        

    cfdi = fields.Binary(string='CFDI')
    xml_recibo = fields.Binary(string='XML Recibo Electrónico')
    acuse_recibo = fields.Binary(string='Acuse Recibo Electrónico')
    show = fields.Boolean(string = 'Show')
    monto_pago = fields.Float(string='Monto Pagado', default=_compute_montopago)
    fecha = fields.Datetime(string='Fecha Pago', required='True')
    cliente = fields.Many2one('res.partner',string='Cliente', readonly=True)
    folio_cfdi = fields.Char(string='Folio CFDI')
    forma_pago = fields.Selection(METODO_PAGO_SELECTION, string='Metodo de Pago', required='True')
    invoice_id = fields.Many2one('account.invoice',string='ID Factura')
    numero_pago = fields.Integer(string='Número de Pago')

    # FUNCION PARA OBTENER RECIBO ELECTRONICO DE PAGO
    @api.multi
    def button_recibo_electronico_pago(self):
        if self.xml_recibo == None:
            raise osv.except_osv(("¡Aviso!"),('No se ha cargado ningun archivo de tipo xlm, favor de revisar y volver a subir el CFDI'))
        else:
            invoice_fac = self.env['account.invoice'].browse(self._context.get('active_id'))
            id_company=invoice_fac.company_id
            certificadoEmisor = id_company.cer
            LlavePrivadaEmisor = id_company.key
            llavePrivadaEmisorPassword = id_company.jpassword
            USER = id_company.usr_proveedor
            PASS = id_company.psw_proveedor

            # print '\t======tibrado productivo======'
            # WSDL = 'http://ws.rfacil.com/InterconectaWs.svc?wsdl'

            print '\t======tibrado pruebas======'
            WSDL = 'http://wspruebas.rfacil.com/InterconectaWs.svc?wsdl'
            # USER = 'PIGE691013RPA_34'
            # PASS = '348647913486479134864791'

            content = open(self.xml_recibo, "r")
            content = content.read()
            content = content.decode("utf-8")
            client = Client(url=WSDL)
            content = content and content.replace('&', '&amp;').replace('"', '&quot;').replace('"', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
            response = client.service.timbrarEnviaCFDIxp33(USER,PASS,certificadoEmisor,LlavePrivadaEmisor,llavePrivadaEmisorPassword,content)
            print response
            if response.numError != 0:
                raise osv.except_osv(response.numError, response.ErrorMessage)
                return error

            xml_encoded = base64.b64decode(response.XML)
            cadena=xml_encoded
            self.acuse_recibo = response.XML
            self.invoice_id = invoice_fac.id
            if self.monto_pago > invoice_fac.saldo_pediente:
                raise osv.except_osv(("¡Alerta!"),('El monto que ingreso supera el total del pago de la Factura.'))
            if self.monto_pago == invoice_fac.saldo_pediente:
                invoice_fac.write({'state_ac': 'paid'})


    def enviar_factura(self, cr, uid,ids, context=None):
        xml_att = self.pool.get('account.invoice').browse(cr, uid, ids[0])
        bytesXmlCFDI = (self.pool.get('account.invoice').browse(cr, uid, ids[0], context=context).xml_64).decode('base64')
        bytesXmlCFDI = str(bytesXmlCFDI.decode("utf-8"))
        folio = xml_att.folio
        name = xml_att.partner_id.name + str(fields.date.today()) + folio
        name = name and name.replace(' ', '_') 
        # logo = "http://201.150.42.66:8069/jemil/static/src/img/"+xml_att.company_id.logo_emisor
        # link = "http://201.150.42.66:8069/jemil/static/src/"+name+".xml"
        # new_f = open(ODOO_HOME+"/jemil_addons/jemil/static/src/"+name+".xml", "wb")  
        new_f = open("/opt/odoo/extra_addons/facturacion_3_3/static/src/"+name+".xml", "wb")  
        new_f.write(bytesXmlCFDI)
        new_f.close()

        servidor_id = self.pool.get('ir.mail_server').search(cr, uid, [('smtp_user', '=', 'facturacion@jemil.mx')])[0]
        servidor = self.pool.get('ir.mail_server').browse(cr, uid, servidor_id)
        model_data_template_id = self.pool.get('ir.model.data').search(cr, uid, [('module', '=', 'jemil'), ('name', '=', 'template_envio_fact')])[0]
        model_data_template = self.pool.get('ir.model.data').browse(cr, uid, model_data_template_id)
        template_id = model_data_template.res_id
        report_id = self.pool.get('ir.actions.report.xml').search(cr, uid, [('name','=','Factura'), ('report_name', '=', 'Factura')])[0]
        self.pool.get('email.template').write(cr, SUPERUSER_ID, template_id, {'mail_server_id': servidor.id, 'report_template': report_id}, context=context )
        context["receptor_email"] = "leticia@jemil.mx, admon1@jemil.mx, admon2@jemil.mx, admon3@jemil.mx"
        context['correo_from']="Facturacion@jemil.mx"
        # context['descarga_xml']= link
        # context['logo']= logo
        # self.pool['email.template'].send_mail(cr, uid, template_id, ids[0], force_send=True, context=context)

        # if xml_att.partner_id.id != False:
        #     mails_id = self.pool.get('jemil.oficina').search(cr, uid, [('empresa_2','=',xml_att.partner_id.id)])
        #     mails_ids = self.pool.get('jemil.oficina').browse(cr, uid, mails_id)
                
        #     if mails_ids :
        #         print mails_ids
        #         mail_r = mails_ids[0].email
        #         if mail_r :
        #             context["receptor_email"] = mail_r.strip()
        #         self.pool['email.template'].send_mail(cr, uid, template_id, ids[0], force_send=True, context=context)

        # if xml_att.partner_id.correo_vendedor != False:
        #     context["receptor_email"] = xml_att.partner_id.correo_vendedor.email
        #     self.pool['email.template'].send_mail(cr, uid, template_id, ids[0], force_send=True, context=context)


        #Misael Flores
