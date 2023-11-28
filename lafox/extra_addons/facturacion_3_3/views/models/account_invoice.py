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

# ODOO_HOME = "/opt/odoo/"
ODOO_HOME = "/opt/Lafox/odoo/"

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

    # FIELDS PARA FACTURACION
    tipo_venta = fields.Selection(TYPE_SELECT_VF, string='Tipo de Venta')
    lugar_exp = fields.Char(string='Lugar de Expedicón', index=True, default='CUAUHTEMOC, CDMX')
    fecha_certificacion = fields.Datetime(string='Fecha y Hora de Certificación', index=True)
    fecha_emision = fields.Datetime(string='Fecha y Hora de Emsión', index=True)
    tipo_comprobante = fields.Selection(TIPO_COMPROBANTE_LISTA, string='Tipo de Comprobante', index=True)
    folio_fiscal = fields.Char(string='Folio Fiscal', index=True)
    serie = fields.Char(string='Serie', index=True)
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

account_invoice()

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
        # print noseal
        monto_r = str("{0:.2f}".format(float(noseal['Monto'])))
        saldoAnt = str("{0:.2f}".format(float(noseal['Total'])))
        residuo = str("{0:.2f}".format(float(noseal['Monto']) - float(monto_r)))
        for co in noseal['company']:
            print co
            # com = self.pool.get('res.company').browse(cr, SUPERUSER_ID, co.id, context=context)
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
            receptor = SubElement( Comprobante, 'cfdi:Receptor', Rfc=partner_id.razon_social , Nombre=partner_id.name, UsoCFDI = 'P01')
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
            # monto = active_model.saldo_pediente
            client = active_model.partner_id
            folio_fiscal = active_model.folio_fiscal
            company_id = active_model.company_id
            date_1 = self.fecha
            xmlname = 'PAGO-'+str(active_model.company_id.rfc)+'-'+'G'+'-'+str(active_model.folio)
        # self.monto_pago = monto
        if self.cfdi != False:
            pagos_ids = self.search([('invoice_id', '=', active_model.id)], order='fecha desc')
            if not pagos_ids :
                NoOperacion = str(1).zfill(2) 
            else:
                NoOperacion = str(pagos_ids[0].numero_pago).zfill(2) 

            self.show = True
            data = base64.decodestring(self.cfdi)
            forma_pago = self.forma_pago
            # print datas
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
            print info_pago
            xml_info = self._generate_xml_recibo(info_pago)
            self.xml_recibo = xml_info
            print xml_info

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
    forma_pago = fields.Selection(FORMA_PAGO_SELECTION, string='Forma de Pago', required='True')
    invoice_id = fields.Many2one('account.invoice',string='ID Factura')
    numero_pago = fields.Integer(string='Número de Pago')

    # FUNCION PARA OBTENER RECIBO ELECTRONICO DE PAGO
    @api.multi
    def button_recibo_electronico_pago(self):
        if self.xml_recibo == None:
            raise osv.except_osv(("¡Aviso!"),('No se ha cargado ningun archivo de tipo xlm, favor de revisar y volver a subir el CFDI'))
        else:
            print self.xml_recibo
            # invoice_fac = self.pool.get('account.invoice').browse(cr, uid, invoice_id, context=None)
            invoice_fac = self.env['account.invoice'].browse(self._context.get('active_id'))
            print invoice_fac 
            # id_company = self.company_id
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
            print content
            content = content and content.replace('&', '&amp;').replace('"', '&quot;').replace('"', '&apos;').replace('<', '&lt;').replace('>', '&gt;')
            response = client.service.timbrarEnviaCFDIxp33(USER,PASS,certificadoEmisor,LlavePrivadaEmisor,llavePrivadaEmisorPassword,content)
            # print response
            xml_encoded = base64.b64decode(response.XML)
            cadena=xml_encoded
            print cadena
            self.acuse_recibo = response.XML
            self.invoice_id = invoice_fac.id
            # invoice_fac.write({'monto_pagado': self.monto_pago})
            if self.monto_pago > invoice_fac.saldo_pediente:
                raise osv.except_osv(("¡Alerta!"),('El monto que ingreso supera el total del pago de la Factura.'))

            if self.monto_pago == invoice_fac.saldo_pediente:
                invoice_fac.write({'state_ac': 'paid'})

