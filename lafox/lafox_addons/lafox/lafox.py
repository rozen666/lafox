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
#    Code create by: Ing. Luis J. Ortega and Omar Ocampo 13/03/2018
#
##############################################################################
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from openerp import SUPERUSER_ID
from openerp import models, fields, api, tools
from openerp import http
from openerp.osv import osv
from openerp.exceptions import except_orm, Warning, RedirectWarning
import datetime as dt
import time
from datetime import time, datetime, date, timedelta
from openerp import _
import os
import xlrd
from xlrd import open_workbook
import base64
import time
import pytz
import calendar
from stdnum.mx.rfc import (validate,InvalidComponent,InvalidFormat,InvalidLength,InvalidChecksum)
from parse import cargar_MA,cargar_PT,cargar_CO, cargar_delete
import number_to_letter
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import itertools
from operator import itemgetter
import operator
from itertools import chain
from collections import defaultdict
import random
import openerp.addons.decimal_precision as dp
from openerp import api, fields, models, _
import xml.etree.ElementTree as ET
from suds.client import Client
from tiquet import convertHtmlToPdf
from xhtml2pdf import pisa
import os
import webbrowser
import logging
import requests
import json

_logger = logging.getLogger(__name__)



ODOO_HOME = "/opt/odoo/"
# ODOO_HOME = "/opt/Lafox/odoo"

LAFOX_SELECT_CRUDO_TERMINADO=[
            ('0','Accesorios'),
            ('1','Terminado'),
            ('2','Tienda 1'),
            ('3','Tienda 2'),
            ]
LAFOX_SELECT_PRODUCTO=[
            ('0','Accesorios'),
            ('1','Terminado'),
            ]
LAFOX_SELECT_CF=[
            ('0','CF1'),
            ('1','CF2'),
            ]
LAFOX_TIP_VENTA=[
            ('0','EFECTIVO'),
            ('1','CREDITO'),
            ]

LAFOX_SELECT_ESTATUS_PEDIDO=[
            ('P','PREPARACION'),
            ('E','ENVIADO'),
            ('R','RECIBIDO'),
            ]

LAFOX_TYPE_SELECT_VF=[
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
ACCOUNT_STATE = [
            ('draft','Borrador'),
            ('open','Abierto'),
            ('paid','Pagado'),
            ('cancel','Cancelado'),

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

LAFOX_SELECT_TIPO_CLIENTE=[
            ('0','Fisica'),
            ('1','Moral'),
]

SELECTION_MES = [
            ('01','ENERO'),
            ('02','FEBRERO'),
            ('03','MARZO'),
            ('04','ABRIL'),
            ('05','MAYO'),
            ('06','JUNIO'),
            ('07','JULIO'),
            ('08','AGOSTO'),
            ('09','SEPTIEMBRE'),
            ('10','OCTUBRE'),
            ('11','NOVIEMBRE'),
            ('12','DICIEMBRE'),
        ]
LAFOX_STATE_PRODUCT = [
            ('EXTRAORDINARIO','EXTRAORDINARIO'),
            ('BUENO','BUENO'),
            ('REGULAR','REGULAR'),
            ('MALO','MALO'),

]

LAFOX_SELECT_STATE_CLIENTE=[
            ('0','EN TIEMPO'),
            ('1','RETARDO SUAVE'),
            ('2','RETARDO DURO'),
            ('3','DESAYUNO'),
            ('4','DESAYUNO RETARDO'),
            ('5','COMIDA'),
            ('6','COMIDA RETARDO'),
            ('7','SALIDA'),
            ('8','FUERA DE HORARIO'),
]
LAFOX_PUNTUALIDAD_PAGO_CLIENTE = [
            ('EXTRAORDINARIO','EXTRAORDINARIO'),
            ('BUENO','BUENO'),
            ('REGULAR','REGULAR'),
            ('MALO','MALO'),
]
LAFOX_MEDIO_CONTACTO = [
            ('LLAMADA','LLAMADA'),
            ('REDES SOCIALES','REDES SOCIALES'),
            ('VISITA','VISITA'),
            ('OTRA','OTRA'),
]
LAFOX_UNIDAD_PRODUCTO = [
            ('G','G'),
            ('GR','GR'),
            ('PZ','PZ'),
            ('HILO', 'HL'),
            ('MT', 'MT'),
            ('PR', 'PR')
]
LAFOX_SOLICITUD_PRODUCTO =[
            ('BORRADOR', 'BORRADOR'),
            ('EN PROCESO', 'EN PROCESO'),
            ('CANCELADO', 'CANCELADO'),
            ('APROBADO', 'APROBADO')
]

LA_FOX_SELECT_MOV =[
            ('draft','Borrador'),
            ('confirmed','Confirmado'),
            ('aceptado','Aprobado'),
            ('cancelado','Cancelado'),
]

LA_FOX_BLOQUEAR =[
            ('1', 'SI'),
            ('0', 'NO'),
            ]
LAFOX_HR_ASISTECIA = [
            ('Oficina','Oficina'),
            ('OficinaFam','Oficina-Fam'),
            ('Fabrica','Fabrica'),
            ('FabricaFam','Fabrica-Fam')
            ]
LAFOX_CREDITO = [
            ('Credito','Credito'),
            ('Efectivo','Efectivo')
            ]

# Inicio de Clase para almacenes
class stock_warehouse(models.Model):
    _name = 'stock.warehouse'
    _inherit = 'stock.warehouse'

    # FIELDS PARA STOCK-WAREHOUSE

    # FUNCIONES PARA STOCK.WAREHOUSE
    # Función que permite redireccionar la vista a otro modelo
    def _get_act_window_dict(self, cr, uid, name, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.xmlid_to_res_id(cr, uid, name, raise_if_not_found=True)
        result = act_obj.read(cr, uid, [result], context=context)[0]
        return result

    # Funcion que permite visualizar el stock de los productos
    def action_open_quants_button(self, cr, uid, ids, context=None):
        result = self._get_act_window_dict(cr, uid, 'stock.product_open_quants', context=context)
        result['context'] = "{'search_default_locationgroup': 0, 'search_default_internal_loc': 1,'group_by':['product_id','location_id']}"
        return result

stock_warehouse()

class stock_location(osv.osv):
    _name = 'stock.location'
    _inherit = 'stock.location'

stock_location()

class stock_quant(osv.osv):
    _name = 'stock.quant'
    _inherit = 'stock.quant'

    # FUNCION PARA OBTENER AL RESPONSABLE QUE REALIZO EL MOVIMIENTO
    @api.multi
    @api.depends('create_date')
    def _compute_responsable_venta(self):
        datetime_object = datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S') + timedelta(seconds=01)
        class_obj = self.env['stock.move'].search([('create_date','>',self.create_date),('create_date','<',str(datetime_object))], limit=1)
        self.name_responsable = class_obj.responsable_id.id

    # FIELDS PARA STOCK.QUANT
    name_responsable = fields.Many2one('res.users',string='Responsable', compute='_compute_responsable_venta', store='True')

stock_quant()

class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'

    # FIELDS PARA STOCK.MOVE
    referencia = fields.Char(string='Referencia/Observaciones')
    responsable_id = fields.Many2one('res.users',string='Responsable')

    #Field para el total del movimiento
    total_movimiento =fields.Float(string='Total del movimiento', compute='_compute_total_movi', store='True')
    ids_movimientos = fields.Many2one('lafox.movimiento.de.grupo', string='Moviientos IDS')
    supplier_id = fields.Many2one('res.partner', string='Proveedor')

    # FUNCIONES PARA STOCK.MOVE
    # Función que  permite aprobar el movimiento y revisa si la cantidad de producto esta disponible en el stock
    @api.multi
    def button_approve_move(self):
        type_alb = self.env['stock.picking.type'].search([('code','=','internal')])
        product_move =self.env['stock.quant'].search([('location_id','=',self.location_id.id),('product_id','=',self.product_id.id)])
        product_move_qty=0
        for qty_pruduct in product_move:
            product_move_qty = product_move_qty + qty_pruduct.qty

        # Si no encuentra producto warning de que no hay producto
        if len(product_move) < 1:
            raise osv.except_osv(("No es posible realizar esta transacción"), ('EL Producto %s,que quiere transferir no se encuentra disponible en el almacén de origen'% self.product_id.name))
        # Si hay producto pero es menor, lanza alerte de faltante producto
        elif product_move_qty < self.product_uom_qty:
            raise osv.except_osv(("No es posible realizar esta transacción"),('EL Producto %s que quiere transferir no cuenta con la cantidad necesaria. La cantidad que dese enviar: %s, La cantidad en Stock: %s en %s'% (self.product_id.name,self.product_uom_qty,product_move_qty,self.location_id.complete_name)))
        # Si hay prodcuto suficiente deja continuar
        else:
           self.write({'state':'confirmed','picking_type_id':type_alb[0].id})


    #Funcion que permite calcular el total del movimiento realizado

    @api.multi
    @api.depends('product_uom_qty')
    def _compute_total_movi(self):
        for qty in self:
            qty.total_movimiento= qty.product_uom_qty * qty.product_id.list_price


stock_move()

#Class product_product inherit
class product_product(models.Model):
    _name='product.product'
    _inherit='product.product'
    _rec_name ='clave_prod'

    
    @api.multi
    def write(self, values):
        group_admin= self.env['res.groups'].search([('name', 'in', ("Administrador","Sistemas","Dirección","Coordinación General"))])

        print 'self._context',self._context
        admins = []
        for group_u in group_admin:
            for user_1 in group_u.users:
                admins.append(user_1.id)
        if not self.env.user.id in admins and 'in_context' in self._context:
            raise osv.except_osv(('¡Error!'),('Este Perfil no tiene permisos para moodificar la ficha de los productos'))

        write_id = super(product_product, self).write(values)
        return write_id

    #Default para poner un producto en sin grupo en caso de no tener seleccionado uno
    @api.multi
    def _default_grupo_precios(self):
        precios = ''
        grupo_precios_id = self.env['lafox.grupo.de.precios'].search([('nomenclatura', '=', '-')])
        print grupo_precios_id
        if grupo_precios_id:
            precios = grupo_precios_id[0].id
        return precios

    #Funcion para reemplazar el search de un many2one y buscar por id o clave
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args =args or []
        recs = self.browse()
        if not recs:
            recs = self.search(['|',('cod_crudos', operator, name),('name', operator, name)] + args, limit=limit)
        return recs.name_get()


    # FIELDS PARA PRODUCT PRODUCT
    clave_prod=fields.Char(string='Nombre del producto',require=True,help='Teclea la clave del producto')
    ref_prod=fields.Char(string='Referencia',require=True,help='Teclea la referencia del producto')
    c_t=fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO,require=True,string='Tipo de Producto')
    moneda_prod=fields.Selection([('P', 'MXN-PESOS'),('D', 'DLLS-DOLARES')],string='Moneda',require=True)
    iva_prod=fields.Float(string='I.V.A',require=True,help='I.V.A')
    observacion_prod=fields.Text(string='Observaciones',help='Observaciones al producto')
    poveedor_prod=fields.Many2one('res.partner',string='Proveedor',help='Proveedor...', domain="[('supplier','=','True')]")
    blo_si_no =fields.Boolean(string='Bloquear', require=True)
    cantidad_minima=fields.Integer(string='Cant. Min.',require=True)
    grupo_precios_id=fields.Many2one('lafox.grupo.de.precios',string='Grupo de Precios')
    grupo_descuentos_id=fields.Many2one('lafox.escala.de.descuentos',string='Grupo de Descuentos')
    grupo_inventarios_id=fields.Many2one('lafox.grupo.de.inventarios',string='Grupo de Inventarios')
    seguimiento_id = fields.One2many('lafox.seguimiento.venta.producto','account_ids',string='Ventas Realizadas')
    revisar_ventas = fields.Boolean(string='Revisar Ventas realizadas')
    #porcentaje_vendido = fields.Float(string='Porcentaje de Venta %', compute='_compute_product_vendidos')
    porcentaje_vendido = fields.Float(string='Porcentaje de Venta %')
    mes_venta = fields.Selection(SELECTION_MES,string='Mes de Venta', require=True)
    state_product = fields.Selection(LAFOX_STATE_PRODUCT,string='Estatus de Venta', compute='_compute_estado_producto', store=True)
    producto_vendidos = fields.Float(string='Cantidad Vendida')
    producto_move = fields.Float(string='Cantidad de Productos al Mes')
    cantidad_vende = fields.Float(string='Cantidad a Vender')
    cantidad_vendidos = fields.Many2one('lafox.informacion.ventas', string='Cantidad Vendida')
    unidad_product =fields.Selection(LAFOX_UNIDAD_PRODUCTO,string='Unidad del producto')
    cod_crudos =fields.Char(string='Codigo EAN13')
    piezas_x_paquete =fields.Float(string='Piezas por paquete', default=1)
    seg_pro= fields.Many2one('lafox.seguimiento.producto', 'seguimiento', invisible=True)
    especial_product= fields.Many2one('lafox.especiales', string='Escala Precio Especial')
    precio_especial = fields.Float(string='Precio Especial')
    promedio_mensual = fields.Float(string='Promedio Mensual')
    clave_prod_especiales = fields.Char(string='Clave para Agrupación por Precio')

    # FIELD PARA CREACION DE UN NUEVO PRODUCTO
    # new_product = fields.Char(string='Nuevo producto')

    #Funcion para cambiar el state del producto
    @api.multi
    @api.depends('state_product')
    def _compute_estado_producto(self):
        for product_id in self:
            if int(product_id.producto_vendidos) <= int(product_id.cantidad_vendidos.malo) +5:
                product_id.state_product ='MALO'
            elif int(product_id.producto_vendidos) <= int(product_id.cantidad_vendidos.regular) +5:
                product_id.state_product ='REGULAR'
            elif int(product_id.producto_vendidos) <= int(product_id.cantidad_vendidos.bueno) +5:
                product_id.state_product ='BUENO'
            elif int(product_id.producto_vendidos) > int(product_id.cantidad_vendidos.bueno):
                product_id.state_product ='EXTRAORDINARIO'







    # Probando la nueva API
    # @api.multi
    #def pruebas_de_nueva_api(self):
    #
    #     cantidad_por_id=self.env['account.invoice'].search([])
    #
    #     for valores in cantidad_por_id:
    #         datos=valores.amount_total
    #         print datos
    # product_product_busqueda=self.search([])
    # for valores in product_product_busqueda:
    #     print self.env['res.partner'].search([('id','=',valores.id)]).name

    #Funcion para el envio de email cuando la cantidad sea minima de dicho producto con crontab de 1 days.
    def envio_mail_cantidad_minima_products(self, cr, uid, context=None):
        servidor_ids = self.pool.get('res.users').browse(cr, uid, uid)
        servidor_id=self.pool.get('ir.mail_server').search(cr,uid,[('smtp_user','=',"oocampo@bpmtech.com")])
        if len(servidor_id):
            servidor=servidor_id[0]
        else:
            raise osv.except_osv(('¡Error!'),('Sin servicio configurado de email.'))

        servidor=self.pool.get('ir.mail_server').browse(cr,uid,servidor)
        cantidad_product_product=self.pool.get('product.product').search(cr,uid,[('cantidad_minima','!=',0)])

        for id_producto in self.pool.get('product.product').browse(cr, uid,cantidad_product_product):
            var_stock=self.pool.get('stock.quant').search(cr,uid,[('product_id','=',id_producto.id)])
            var_stock_b=sum(self.pool.get('stock.quant').browse(cr,uid,var_stock).mapped('qty'))
            producto_info=id_producto.name_template

            print var_stock_b,id_producto.cantidad_minima

            if var_stock_b<id_producto.cantidad_minima:
                context={}
                context["receptor_email"]='lortega@bpmtech.com'
                context['correo_from']=servidor.smtp_user
                context['nombre_form']=servidor.smtp_user
                context['producto_info']=producto_info
                src_tstamp_str = tools.datetime.now().strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
                src_format = tools.misc.DEFAULT_SERVER_DATETIME_FORMAT
                dst_format = DEFAULT_SERVER_DATETIME_FORMAT #format you want to get time in.
                dst_tz_name = self.pool.get('res.users').browse(cr, uid, uid, context=context).tz or 'Mexico/General'
                _now = tools.misc.server_to_local_timestamp(src_tstamp_str, src_format, dst_format, dst_tz_name)
                context['fecha_cotizacion']=_now
                template = self.pool.get('ir.model.data').get_object(cr, SUPERUSER_ID, 'lafox', 'template_email_cantidad_minima_producto')
                self.pool['email.template'].send_mail(cr, uid, template.id, id_producto.id, force_send=True, context=context)

    #Funcion para permitir redireccionar la vista a otro modelo
    def _get_act_window_dict(self, cr, uid, name, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.xmlid_to_res_id(cr, uid, name, raise_if_not_found=True)
        result = act_obj.read(cr, uid, [result], context=context)[0]
        return result

    #Funcion permite visulizar del producto
    def action_open_quants(self, cr, uid, ids, context=None):
        products = self._get_products(cr, uid, ids, context=context)
        result = self._get_act_window_dict(cr, uid, 'stock.product_open_quants', context=context)
        result['domain'] = "[('product_id','in',[" + ','.join(map(str, products)) + "]),('location_id.name','!=','VIRTUAL LOCATIONS / VENTAS'),('location_id.name','!=','VIRTUAL LOCATIONS / DEVOLUCIONES'),('location_id.name','!=','VIRTUAL LOCATIONS / DEVOLUCIONES-FABRICA')]"
        result['context'] = "{'search_default_locationgroup': 1, 'search_default_internal_loc': 1}"
        return result

    #Funcion para retornar los productos
    def _get_products(self, cr, uid, ids, context=None):
        products = []
        for prodtmpl in self.browse(cr, uid, ids, context=None):
            products += [x.id for x in prodtmpl.product_variant_ids]
        return products

    # Cron que permite actualizar los registros de cada producto vendido
    @api.model
    def _cron_execute_ventas(self):
        # Se realiza un busqueda para todas las ventas menores o iguales a hoy con el status pagado
        for search_id_ventas in self.env['account.invoice'].search([('fecha_venta','<=',fields.Date.today()),('state','=','paid')]):
            for product in search_id_ventas.invoice_line:
                # Por cada Venta se obtienen los productos vendidos
                search_product = self.env['lafox.seguimiento.venta.producto'].search([('id_invoice_line','=',product.id)])
                line=[]
                res={}
                res['value']={}
                # Si no se han registrado, se asignan a los registros de cada producto
                if not search_product:
                    dic_lista = {}
                    dic_lista['fecha_venta'] = search_id_ventas.fecha_venta
                    dic_lista['cantidad'] = product.quantity
                    dic_lista['costo'] = product.price_subtotal
                    dic_lista['cliente_venta'] = search_id_ventas.partner_id.id
                    dic_lista['venta_realizada'] = search_id_ventas.nomenclatura
                    dic_lista['id_invoice_line'] = product.id
                    dic_lista['account_ids'] = product.product_id.id

                    self.env['lafox.seguimiento.venta.producto'].sudo().create(dic_lista)
        return True



product_product()

#Class para llenar product.product->grupo_invetario
class lafox_grupo_de_inventarios(models.Model):
    _name='lafox.grupo.de.inventarios'
    _rec_name = "nomenclatura"

    # FIELDS PARA lafox_grupo_de_inventarios
    nombre=fields.Char(string='Grupo de inventario',require=True)
    nomenclatura=fields.Char(string='Nomenclatura',required=True)

lafox_grupo_de_inventarios()

class account_invoice(models.Model):
    _name = 'account.invoice'
    _rec_name = "nomenclatura"
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

    # Funcion que permite llenar el almacen para ventas segun sea el usuario de ventas
    @api.multi
    @api.depends('user_id')
    def _compute_tipo_almacen(self):
        email = self.user_id.login
        employee_id =  self.env['hr.employee'].search([('work_email','=',email)])
        print "employee_id",employee_id
        if employee_id:
            self.stock_venta = employee_id[0].almacenes_id
            print self.stock_venta

            if employee_id[0].almacenes_id.complete_name == 'Physical Locations / WH / LOCAL PRODUCTOS TERMINADO':
                self.tipo_producto = '1'
            elif employee_id[0].almacenes_id.complete_name == 'Physical Locations / WH / LOCAL PRODUCTOS ACCESORIOS':
                self.tipo_producto = '0'
            else:
                return False


    #FUNCION PARA OBTENER EL PRECIO DEL DOLAR ANTERIOR
    @api.model
    def _default_price_dls(self):
        price = 0.0
        prices_id = self.env['lafox.change.monetary'].search([('id', '=', 1)])
        if prices_id:
            price = prices_id.price_dolar
        return price


    @api.one
    @api.depends('invoice_line.price_subtotal', 'tax_line.amount', 'devolucion_id.amount','devolver')
    def _compute_amount(self):

        self.amount_untaxed = sum(line.price_subtotal for line in self.invoice_line)
        # self.total_dev_imp = sum(line.amount for line in self.tax_line)
        self.amount_tax = sum(line.amount for line in self.tax_line)

        if self.devolver == False:
            self.total_dev = 0.0
            self.total_dev_imp = 0.0
            self.precio_temporada = 0.0
            # self.amount_total = self.amount_untaxed + self.amount_tax
        else:
            # POR EL MOMENTO ESTOS IMPUESTOS ESTARAN EN $0
            self.total_dev = sum(line.amount for line in self.devolucion_id)
            self.total_dev_imp = 0.0
            # self.total_dev_imp = float(self.total_dev *0.16)
        
        # self.amount_total = self.amount_untaxed + self.amount_tax - self.total_dev - self.total_dev_imp 
        self.amount_total = self.amount_untaxed + self.amount_tax + self.total_dev - self.precio_temporada

        # self.amount_total = self.amount_untaxed + self.amount_tax - self.total_dev - self.total_dev_imp - self.precio_temporada

    #Funcion para buscar si dentro de cierta fecha se tiene promocion especial
    @api.multi
    @api.depends('stock_venta', 'fecha_venta', 'des_temporadaa', 'invoice_line', 'des_temporada')
    def _compute_fecha_espe(self):
        for account in self:

            varios = self.env['lafox.precio.temporada'].search([('date_temporada','<=',account.fecha_venta), ('dete_temp_fin','>=',account.fecha_venta)])

            for record in varios:
                almacen_tem = record.mapped('des_alamacen')
                for name_new in almacen_tem:
                    if account.fecha_venta >= record.date_temporada and account.fecha_venta <= record.dete_temp_fin and account.stock_venta.id == name_new.id:
                        account.des_temporadaa = record.name
                        if account.stock_venta in almacen_tem:
                            account.precio_temporada = (float(account.amount_total)*float(record.precio_tem/100))
            account.amount_total = account.amount_untaxed + account.amount_tax + account.total_dev - account.total_dev_imp - account.precio_temporada
            

    @api.model
    def _default_fecha(self):
        res = fields.datetime.now()
        return res

    @api.model
    def _default_fecha_6(self):
        res = fields.datetime.now() - timedelta(hours=6)
        return res

    @api.multi
    @api.depends('user_id')
    def _domain_almacen_usr(self):

        domain = [('location_id','=',11),('usage','=','internal')]

        group_admin= self.env['res.groups'].search([('name', 'in', ("Coordinación General","Sistemas","Dirección"))])

        admins = []
        for group_u in group_admin:
            for user_1 in group_u.users:
                admins.append(user_1.id)
        
        if not self.env.user.id in admins:
            email = self.env.user.login
            print email
            employee_id =  self.env['hr.employee'].search([('work_email','=',email)])
            print employee_id
            almacen = employee_id[0].almacenes_id.complete_name

            domain = [('location_id','=',11),('usage','=','internal'),('complete_name','=',almacen)]

        return  domain

    # COMPUTE para el saldo a credito
    @api.one
    @api.depends('amount_total','write_date', 'saldo_credito','saldo_abonado')
    def _saldo_credito_venta(self):
        for invoice in self:

            invoice.saldo_credito = float(invoice.amount_total) - float(invoice.saldo_abonado)

    @api.multi
    def unlink(self):
        group_admin= self.env['res.groups'].search([('name', 'in', ("Ventas","Ventas Esp", "Caja y Tesorería","Credito y Cobranza"))])
        for groups_id in group_admin:
            if groups_id in self.env.user.groups_id and self.state_ac != 'draft':
                raise osv.except_osv(("¡Acceso no Autorizado!"),('Este usuario no se encuentra autorizado para eliminar notas (Solo Borradores).'))

        return super(account_invoice, self).unlink()

    # COMPUTE PARA OBTENER LA FECHA SIN HORA
    @api.one
    @api.depends('fecha_venta')
    def _compute_fecha_sinhora(self):
        for d in self:
            dayT = datetime.strptime(d.fecha_venta, '%Y-%m-%d %H:%M:%S')
            day =  dayT - timedelta(hours=6)
            self.fecha_venta_6=day.date()
        return True

    #FIELDS PARA ACCOUNT.INVOICE
    nomenclatura = fields.Char(string='Código Nomenclatura')
    fecha_venta = fields.Datetime(string='Fecha Origen', default=_default_fecha)
    fecha_venta_6 = fields.Date(string='Fecha de Venta', compute='_compute_fecha_sinhora', store='Tr')
    tipo_producto = fields.Selection(LAFOX_SELECT_PRODUCTO, string='Tipo de Producto', store='True')
    # tipo_producto = fields.Selection(LAFOX_SELECT_PRODUCTO, string='Tipo de Producto', compute='_compute_tipo_almacen', store='True')
    validador=fields.Boolean(string='Pedido con Envio',default='False')
    stock_venta = fields.Many2one('stock.location', string='Tipo de Almacen', compute='_compute_tipo_almacen',store='True', domain = _domain_almacen_usr)
    # stock_venta = fields.Many2one('stock.location', string='Tipo de Almacen', compute='_compute_tipo_almacen',store='True')
    devolver = fields.Boolean(string='Devolución de Productos')
    devolucion_id = fields.One2many('lafox.devolucion.account','account_id', string='Devoluciones')
    total_dev = fields.Float(string='Devoluciones', compute='_compute_amount', store='True', default='0.0')
    price_before_dlls = fields.Float(string='Precio dolar', default = _default_price_dls)
    tiquet_pdf = fields.Char(string='Tiquet')
    check_credito = fields.Boolean(string='Venta a Credito')
    check_pagare = fields.Boolean(string='Anexar Pagare')
    total_dev_imp = fields.Float(string='Impuestos Devoluciones -', compute='_compute_amount', store='True', default='0.0', digits=dp.get_precision('Account'))

    #FIELD PARA COSTO SIN IVA
    cos_no_iva =fields.Float(string="Costo sin iva")
    esca_cliente = fields.Char(string='Escala de descuento', compute='_compute_escala_des', store=True)
    check_esp = fields.Boolean(string='Precio Especial', default=False)
    check_visible = fields.Boolean(string='Activar PE')

    #FIELD PARA PRECIO ESPECIAL POR TEMPORADA
    precio_temporada = fields.Float(string='Descuento Temporada', compute='_compute_fecha_espe', store='True', readonly=True)

    #CHECK PARA PRECIO TEMPORADA
    des_temporada = fields.Many2one('lafox.precio.temporada', string='Precio de temporada', readonly=True, invisible= True)
    des_temporadaa = fields.Char(string='Descuento especial', compute='_compute_fecha_espe', store='True', readonly=True)

    #FIELD PARA TIPO DE PRODUCTO: ACCESORIO O TERMINADO
    tip_product = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO, string='Base de Cliente')

    # FIELD PARA SALDO A CREDITO
    saldo_credito = fields.Float(string='Saldo a credito', compute='_saldo_credito_venta', store=True)
    saldo_abonado = fields.Float(string='Saldo abonado', default=0.0)

    
    @api.multi
    def change_price_esp(self, esp,invoice_line, context):
        for id_line in self.env['account.invoice.line'].search([('invoice_id','=',self.id)]):
            price_ES =  float(id_line.product_id.precio_especial)/float(id_line.product_id.piezas_x_paquete)
            if self.partner_id.moneda_valores != 'D':
                pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]
                price_ES = float(price_ES) * float(pesos.price_dolar)
            id_line.sudo().write({'price_unit':price_ES})

    @api.multi
    @api.depends('partner_id')
    def _compute_escala_des(self):
        descu = str(self.partner_id.escala_precios.escala) + " " + str(self.partner_id.escala_precios.descuentos)
        if descu == 'False False':
            descu = ' '
        self.esca_cliente = descu


    @api.multi
    def _self_create_new_id(self,folio,dt):
        print folio
        today = str(date.today())+' 00:00:00'
        # res = fields.datetime.now() - timedelta(hours=6)
        res =datetime.strptime(dt, '%Y-%m-%d')
        folio = folio + 1
        nom_v = "VEN-"+str(res.strftime("%d"))+"-"+str(res.strftime("%b"))+"-"+str(res.strftime("%Y"))+"-" +str(folio).zfill(4)
        return nom_v

    # Se modifica el create para poder crear un Codigo irrepetible por cotización
    @api.model
    def create(self, vals):
        today = str(date.today())+' 00:00:00'
        # res = fields.datetime.now() - timedelta(hours=6)
        res =datetime.strptime(vals['date_due'], '%Y-%m-%d')
        folio_existente = True 
        stock_v = vals['stock_venta']

        last_folio =self.env['account.invoice'].sudo().search([('create_date','>=',today),('stock_venta','=',stock_v)])
        folio = (len(last_folio)+1)

        while folio_existente:
            # last_folio =self.env['account.invoice'].search([('fecha_venta','>',today),('stock_venta','=',stock_v)])
            nom_v = "VEN-"+str(res.strftime("%d"))+"-"+str(res.strftime("%b"))+"-"+str(res.strftime("%Y"))+"-" +str(folio).zfill(4)
            folio_duplicado = self.env['account.invoice'].sudo().search([('nomenclatura','=',nom_v),('stock_venta','=',stock_v)])
            if not folio_duplicado:
                vals['nomenclatura'] = nom_v
                break
            else:
                nom_v = self._self_create_new_id(folio,vals['date_due'])
                folio_duplicado = self.env['account.invoice'].sudo().search([('nomenclatura','=',nom_v),('stock_venta','=',stock_v)])
                if not folio_duplicado:
                    vals['nomenclatura'] = nom_v
                    break
                else:
                    nom_v = self._self_create_new_id(folio,vals['date_due'])

        
        # print vals
        vals['name'] = vals['nomenclatura'] 
        _logger.info('VALS ACCOUNT INVOICE: %s', (vals))
        rec = super(account_invoice, self).create(vals)               
        return rec


    # FUNICON PARA LA CONFIRMACION DE LOS MOVIMIENTOS
    def _create_and_confirm_move(self, cr, uid, ids, vals_stok_move,context=None):
        print vals_stok_move
        ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
        self.pool.get('stock.move').action_done(cr, uid, ide, context=context)

    @api.multi
    def action_paid_venta(self):
        corte_z = self.env['lafox.valida.estatus.boton'].search([('fecha', '=', date.today()),('almacen_id','=',self.stock_venta.id)])
        if corte_z:
            raise osv.except_osv(("No se puede Realizar Operación!"),("Se ha Efectuado el Corte Z del día. No es posible realizar más ventas el día de hoy "))
            return False
            
        passed = 0
        self.button_reset_taxes()
        # Revisamos si hay devoluciones y si estas son mayor al 30%
        if self.devolver == True:
            if(float(self.amount_total*0.30) < float(self.total_dev)):
                raise osv.except_osv(("No se puede Realizar Operación!"),("El monto de la devolución es mayor al 30% del Total de la nota, favor de verificar "))

        if self.check_credito == True:
            if (float(self.partner_id.saldo_pendiente) + float(self.amount_total) >float(self.partner_id.limite_credito)):
                raise osv.except_osv(("No se puede Realizar Operación!"),("El monto de la venta a credito es mayor al disponible para el cliente, favor de verificar "))
            else:
                self.partner_id.sudo().write({'saldo_pendiente': float(self.partner_id.saldo_pendiente) + float(self.amount_total)})

        # Obtnemo las localizaciones de destino y de origen
        search_id_loc = self.env['stock.location'].search([('complete_name','ilike',self.stock_venta.complete_name)])
        search_id_loc_venta = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / VENTAS')])
        search_id_loc_dev = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / DEVOLUCIONES')])
        search_id_loc_dev_mal = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / DEVOLUCIONES MAL ESTADO')])
        # Por cada producto se revisa que haya suficiente en el stock
        for producto in self.invoice_line:
            sum_qty = sum(self.env['stock.quant'].search([('location_id','=',self.stock_venta.id),('product_id', '=',producto.product_id.id)]).mapped('qty'))
            # Si algun producto no es suficiente se manda warning
            if producto.quantity > sum_qty:
                raise osv.except_osv(("No es posible realizar esta operación"), ('EL Producto %s no tiene disponible la cantidad mencionada.\n Cantidad a vender: %s Cantidad en stock: %s'%(producto.product_id.name,producto.quantity,sum_qty)))
            # De lo conrario se guarda u estatus
            else:
                passed = 1
        # Si cambia el status passed se crean los movimientos para descontar del almacen a un almacen de ventas
        if passed == 1:
            for sell_product in self.invoice_line:
                vals_stok_move= {
                            'location_dest_id': search_id_loc_venta[0].id,
                            'location_id': search_id_loc[0].id,
                            'name': str('FV:VENTA: '+ sell_product.product_id.name),
                            'company_id': 1, #por el momento definido
                            'invoice_state': "none",
                            'partially_available': False,
                            'procure_method': "make_to_stock",
                            'product_id': int(sell_product.product_id.id),
                            'product_uom': int(sell_product.product_id.uom_id.id),
                            #'product_qty': float(tupple_taller.cantidad),
                            'product_uom_qty': float(sell_product.quantity),
                            'propagate': True,

                            }
                # print vals_stok_moves
                self._create_and_confirm_move(vals_stok_move)

            for dev_product in self.devolucion_id:
                if dev_product.estado_mer == False:
                    vals_stok_move= {
                                'location_dest_id': search_id_loc[0].id,
                                'location_id': search_id_loc_dev[0].id,
                                'name': str('FV:DEVOLUCION: '+ dev_product.product_id.name),
                                'company_id': 1, #por el momento definido
                                'invoice_state': "none",
                                'partially_available': False,
                                'procure_method': "make_to_stock",
                                'product_id': int(dev_product.product_id.id),
                                'product_uom': int(dev_product.product_id.uom_id.id),
                                #'product_qty': float(tupple_taller.cantidad),
                                'product_uom_qty': float(dev_product.piezas_qty),
                                'propagate': True,

                                }
                    # print vals_stok_moves
                    self._create_and_confirm_move(vals_stok_move)
                else:
                    vals_stok_move= {
                                'location_dest_id': search_id_loc[0].id,
                                'location_id': search_id_loc_dev_mal[0].id,
                                'name': str('FV:DEVOLUCIONMAL: '+ dev_product.product_id.name),
                                'company_id': 1, #por el momento definido
                                'invoice_state': "none",
                                'partially_available': False,
                                'procure_method': "make_to_stock",
                                'product_id': int(dev_product.product_id.id),
                                'product_uom': int(dev_product.product_id.uom_id.id),
                                #'product_qty': float(tupple_taller.cantidad),
                                'product_uom_qty': float(dev_product.piezas_qty),
                                'propagate': True,

                                }
                    print 'Esta en mal estado'
                    self._create_and_confirm_move(vals_stok_move)

        # Una vez realizado la venta se cambia el estatus a pagado
        self.write({'state_ac':'open','state':'open'})

        #TO-DO-validation
        if self.validador==True:
            dic_list={
            'estatus':'P',
            'grupo_ventas_facturacion':self.nomenclatura,
            }
            get_name=self.env['lafox.seguimiento.pedido'].sudo().create(dic_list)

        return True

    @api.multi
    def button_action_cancel_draft(self):
        if self.state == 'paid' or self.state=='open':
            search_id_loc = self.env['stock.location'].search([('complete_name','ilike',self.stock_venta.complete_name)])
            search_id_loc_venta = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / VENTAS')])
            if self.state == 'paid':
                amount_total_n  = self.amount_total * (-1)
            else:
                amount_total_n = 0.0
            for conceptos in  self.invoice_line:
                vals_stok_move= {
                            'location_dest_id': search_id_loc[0].id,
                            'location_id': search_id_loc_venta[0].id,
                            'name': str('FV:VENTA: '+ conceptos.product_id.name),
                            'company_id': 1, #por el momento definido
                            'invoice_state': "none",
                            'partially_available': False,
                            'procure_method': "make_to_stock",
                            'product_id': int(conceptos.product_id.id),
                            'product_uom': int(conceptos.product_id.uom_id.id),
                            #'product_qty': float(tupple_taller.cantidad),
                            'product_uom_qty': float(conceptos.quantity),
                            'propagate': True,

                        }
                        
                self._create_and_confirm_move(vals_stok_move)

            self.sudo().write({'state': 'cancel','amount_total':amount_total_n})
            self.delete_workflow()
            self.create_workflow()

            if self.state == 'open' and self.check_credito == True:
                saldo_pen = self.partner_id.saldo_pendiente - self.amount_total
                self.partner_id.write({'saldo_pendiente':saldo_pen})


        return True

    # @api.multi
    # @api.depends('check_temporada')
    # def _compute_temporada(self):
    #     if self.check_temporada == True:

        

    @api.multi
    def button_print_pdf2(self): 
        today=date.today()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sourceHtml = open(os.path.join(base_dir, 'lafox/prueba.html')).read()
        outputFilename = "/opt/lafox/odoo/lafox_addons/lafox/static/src/PDF/test"+str(today)+".pdf"
        valor = convertHtmlToPdf(sourceHtml, outputFilename,self.id)
        print "*************************************************"
        print valor
        self.tiquet_pdf = "http://192.168.1.100:8069/lafox/static/src/PDF/test2018-12-04.pdf"
        webbrowser.open_new_tab("http://192.168.1.100:8069/lafox/static/src/PDF/test2018-12-04.pdf")






account_invoice()

class account_invoice_line(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'


    @api.multi
    def _cantidad_piezas(self, cantidad_producto,product_id,price_unit,partner_id,check_visible,price_unit_false,context):
        product = self.env['product.product'].browse(product_id)
        part = self.env['res.partner'].browse(partner_id)
        pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]

        if part.moneda_valores != 'D' and product.moneda_prod !='P':
            price_unit_des= float(product.list_price) * float(pesos.price_dolar)
        
        else:
            price_unit_des= float(product.list_price)
        
        if product.c_t == '0':
            price_unit_des = float(price_unit_des) * 2

        if check_visible != True:
            res = {}
            res['value'] = {}           

            res['value']['quantity']= float(product.piezas_x_paquete) * float(cantidad_producto)
            res['value']['price_unit_des']= price_unit_des
            res['value']['price_unit_false']= (float(product.piezas_x_paquete)* float(price_unit))
        else:
            res = {}
            res['value'] = {}
            res['value']['price_unit']= float(price_unit_false) / float(product.piezas_x_paquete)
            res['value']['quantity'] = float(product.piezas_x_paquete) * float(cantidad_producto)

        return res

    @api.multi
    def _onchage_priceunit(self,product_id,price_unit_false,check_visible,cantidad_producto,context):
        if check_visible == True:
            res = {}
            res['value'] = {}

            # res['value']['quantity']= 1
            res['value']['price_unit']= price_unit_false
            if cantidad_producto > 0:
                product = self.env['product.product'].browse(product_id)
                res['value']['price_unit']= float(price_unit_false) / float(product.piezas_x_paquete)
            return res

    @api.multi
    @api.depends('price_unit','quantity')
    def _compute_price_monto(self):
        for r in self:
            r.monto_pago = float(r.quantity) * float(r.price_unit)
    
    # Compute para evitar modificacion en Precio Unitario en algunos Users
    @api.multi
    @api.depends('price_unit','price_unit_false')
    def _compute_price_unit(self):
        for r in self:
            r.price_unit_lst = float(r.price_unit_false)
    
    #FIELDS PARA account_invoice_line
    image_product = fields.Binary(string='Imagen')
    descuento_producto = fields.Char(string='Descuento')
    price_unit_des = fields.Float(string='Precio Lista', digits=dp.get_precision('Product Price'))
    price_unit_false = fields.Float(string='Precio Unitario', digits=dp.get_precision('Product Price'))
    cantidad_producto = fields.Float(string='Piezas')
    # monto_pago = fields.Float(string='Monto')
    cliente_account = fields.Char(string='Cliente')
    monto_pago = fields.Float(string='Monto', compute='_compute_price_monto', store='True', digits=dp.get_precision('Product Price'))
    # CAMPO INVISIBLES SOLO PARA VENDEDORES
    price_unit_lst = fields.Float(string='Precio Unitario', compute='_compute_price_unit', store='True', digits=dp.get_precision('Product Price'))
    descripcion_invoice = fields.Char(string='Descripcion')
    check_visible = fields.Boolean(string='Modificar Precio',default=False)

    # CREACION DE UN NUEVO PRODUCT ONCHANGE PARA EL TIPO DE VENTA EN LA FOX
    @api.multi
    def product_id_change_lf(self,producto_id, uom_id, qty=0, name='', type='out_invoice',partner_id=False, fposition_id=False, price_unit=False, currency_id=False,company_id=None, check_esp=False, context=False):
        if not partner_id:
            raise except_orm(_('No Partner Defined!'), _("You must first select a partner!"))
        values = {}
        part = self.env['res.partner'].browse(partner_id)
        pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]

        product = self.env['product.product'].browse(producto_id)
        fpos = self.env['account.fiscal.position'].browse(fposition_id)

        if float(product.piezas_x_paquete) <= 0 and producto_id != False:
            raise osv.except_osv(('Error en Operación'), ('Este producto no tiene Número de piezas por paquete, favor de modificar la ficha del producto'))
        values['name'] = product.partner_ref
        if type in ('out_invoice', 'out_refund'):
            account = product.property_account_income or product.categ_id.property_account_income_categ
        else:
            account = product.property_account_expense or product.categ_id.property_account_expense_categ
        account = fpos.map_account(account)
        if account:
            values['account_id'] = account.id

        if producto_id:
            price_unit_des = float(product.lst_price)
            price_unit = float(product.lst_price)/float(product.piezas_x_paquete)

            valor_descuento = float(product.lst_price) - (float(product.lst_price)*float(product.grupo_precios_id.descuento/100))            

            if len(part.escala_precios) > 0:
                price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete)) * float(part.escala_precios.factor)
            else:
                price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete))

            print "price_unit", price_unit


            if product.grupo_precios_id.nomenclatura == 'NT' or product.grupo_precios_id.nomenclatura == 'N' or product.grupo_precios_id.nomenclatura == 'U':
                price_unit = (float(product.lst_price)/float(product.piezas_x_paquete))


            if product.grupo_precios_id.nomenclatura != 'E' or product.grupo_precios_id.nomenclatura != 'NT' or product.grupo_precios_id.nomenclatura != 'N' or product.grupo_precios_id.nomenclatura != 'U':
                if product.grupo_precios_id.afectacion == False:
                    price_unit = (float(product.lst_price) - (float(product.lst_price)*float(product.grupo_precios_id.descuento/100))) / float(product.piezas_x_paquete)
                else:
                    price_unit = (float(product.lst_price) - (float(product.lst_price)*float(product.grupo_precios_id.descuento/100)))
                    if len(part.escala_precios) > 0:
                        price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete)) * float(part.escala_precios.factor)
                    else:
                        price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete))

            if product.grupo_precios_id.nomenclatura == 'E':
                fact = self.env['lafox.grupo.de.precios.esp'].search([('descuentos','=', part.escala_precios.descuentos)])
                if not fact:
                    raise osv.except_osv(('Error en Operación'), ('Este Cliente no tiene asignado un valor para Escala de Descuentos '))
                price_unit = (float(product.lst_price)*float(fact[0].factor))
                price_unit_des = (float(product.lst_price)/product.piezas_x_paquete)

            if len(product.especial_product) > 0:
                var1 = ""
                if not part.escala_precios_esp:
                        raise osv.except_osv(('Error en Operación'), ('Este Cliente no tiene asignado el precio para articulos CF, favor de revisar la ficha del Cliente'))
                for espec in part.escala_precios_esp:
                    if var1 == "":
                        var1 =  str(espec.name.id) 
                    if espec.name.id != False:
                        var1 = var1 + "," + str(espec.name.id) 
                    ids = var1.split(',')
                fact = self.env['lafox.grupo.de.precios.esp'].search([('id', 'in', (ids)), ('tipo_escala3', '=', product.especial_product.id)])
                if not fact:
                    raise osv.except_osv(('Error en Operación'), ('Este Cliente no tiene asignado el precio para este articulo CF, favor de revisar la ficha del Cliente'))
                especial2 = fact[0].factor * float(float(product.lst_price))
                price_unit = especial2
                
            # if product.c_t == '0':
            #     price_unit_des = float(price_unit_des) * float(part.escala_precios.factor)
            #     # price_unit = float(price_unit) * 2

            if check_esp == True and product.precio_especial != 0:
                price_unit_des = float(product.precio_especial)
                price_unit = float(product.precio_especial)/float(product.piezas_x_paquete)

            if part.moneda_valores != 'D' and product.moneda_prod !='P':
                price_unit_des= price_unit_des * float(pesos.price_dolar)
                price_unit= price_unit * float(pesos.price_dolar)
            
            # DECLARAMOS LOS VALUES A MOSTRAR
            values['descripcion_invoice'] = product.clave_prod
            values['quantity'] = product.piezas_x_paquete
            values['invoice_line_tax_id'] =False

            values['price_unit_des'] = price_unit_des
            values['price_unit_false'] = price_unit
            values['price_unit'] = price_unit

        return {'value': values}


account_invoice_line()


class lafox_inventario_producto(models.Model):
    _name = 'lafox.inventario.producto'

    @api.multi
    def _default_usr_id(self):
        return self.env.user.id

    # FIELDS PARA lafox_inventario_producto
    tipo_producto = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO,string='Selecciona un Área')
    producto = fields.Many2one('product.product', string='Producto')
    descripcion = fields.Char(string='Descripción')
    piezas = fields.Char(string='Piezas')
    cantidad = fields.Float(string='Cantidad')
    responsable = fields.Many2one('res.users',string='Responsable', default= _default_usr_id)
    product_id = fields.One2many('lafox.inventario.producto','product_ids', string='Productos ID')
    product_ids = fields.Many2one('lafox.inventario.producto', string='Productos ID')
    supplier_id = fields.Many2one('res.partner', string='Proveedor')
    referencia = fields.Char(string='Referencia/Observaciones')

    # FUNCIONES PARA lafox_inventario_producto
    # Funcion para carga de inventario
    def button_asignar_inventario(self, cr, uid, ids, context=None):
        # Se obtine los datos de la vista acutal
        tabla_crm_lead = self.pool.get('lafox.inventario.producto').browse(cr, uid, ids[0], context=context)
        # Obtenemos los dos stock entre los que se hará el movimiento, de abastecimiento virtual --> stock WH
        #search_id_loc = self.pool.get('stock.location').search(cr, uid, [('complete_name','ilike','Ubicaciones físicas / WH / Existencias')], context=context)
        search_id_loc = self.pool.get('stock.location').search(cr, uid, ['|',('name','=','Stock'),('complete_name','ilike','Physical Locations / WH / EXISTENCIAS')], context=context)
        search_id_loc_abas = self.pool.get('stock.location').search(cr, uid, [('complete_name','ilike','Virtual Locations / Procurements')], context=context)

        # Por cada producto se realiza el movimiento correspondiente
        for move in  tabla_crm_lead.product_id:
            vals_stok_move= {
                            'location_dest_id': 12, #12, ## por el  momento ira definido
                            # 'location_dest_id': search_id_loc[0], #12, ## por el  momento ira definido7
                            'location_id': search_id_loc_abas[0], #6, ## por el  momento ira definido
                            'name': str('FV:INV:ABAST: '+  move.producto.name),
                            'company_id': 1, #por el momento definido
                            'invoice_state': "none",
                            'partially_available': False,
                            'procure_method': "make_to_stock",
                            'product_id': int(move.producto.id),
                            'product_uom': int(move.producto.uom_id.id),
                            # 'product_qty': float(move.cantidad),
                            'product_uom_qty': float(move.cantidad) * float(move.piezas),
                            'propagate': True,
                            'responsable_id':move.responsable.id,
                            'supplier_id':tabla_crm_lead.supplier_id.id,
                            'referencia':tabla_crm_lead.referencia,
                        }
            ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
            self.pool.get('stock.move').action_done(cr, uid, ide, context=context)
        return True

    #FUNCION para obtener la descripcion y las piezas del producto

    def _onchange_domain_producto(self, cr, uid, ids, tipo_producto, context):
        res = {}
        if 'tipo_producto' in context:
            valor =  context['tipo_producto']
            res['domain'] ={}
            res['domain']['producto'] = [('c_t','=',valor)]
            print tipo_producto
            if tipo_producto !='1':
                if tipo_producto != '0':
                    atributos = self.pool.get('product.product').browse(cr, uid, tipo_producto, context=context)
                    res['value']={
                        'descripcion' : atributos.clave_prod,
                        'piezas' : atributos.piezas_x_paquete
                    }
        return res



    



lafox_inventario_producto()

# #Class para llenar product.product->grupo_precio
# class lafox_escala_de_precios(models.Model):
#     _name='lafox.grupo.de.precios'
#     nombre=fields.Char(string='Grupo de precios',require=True)
#     nomenclatura=fields.Char(string='Nomenclatura',required=True)
#     descuento=fields.Integer(string='Descuento aplicado',require=True)


#Class res.partner para clientes LAFOX
class res_partner(models.Model):
    _name='res.partner'
    _inherit='res.partner'

    #Campos para los Valores del Cliente
    clave_cliente=fields.Char(string='Clave del cliente',require=True)
    lada_cliente=fields.Char(string='Lada', require=True,size=3)
    # WhatsApp=fields.Char(string='WhatsApp', require=True,size=10)
    vendedor=fields.Many2one('lafox.clientes.vendedor',string='Vendedor',require=True)
    medio_contacto=fields.Selection(LAFOX_MEDIO_CONTACTO,string='Medio de contacto',require=True)
    referencia=fields.Char(string='Referencia',require=True)
    observaciones=fields.Text(string='Observaciones',require=True)

    #Campos para los Valores del Cliente
    rfc_cliente=fields.Char(string="R.F.C",size=13,require=True)
    metodo_pago=fields.Selection(METODO_PAGO_SELECTION,sting='Metodo de pago')
    fisica_moral=fields.Selection(LAFOX_SELECT_TIPO_CLIENTE,require=True,string='Fisica o Moral')
    moneda_valores=fields.Selection([('P', 'MXN-PESOS'),('D', 'DLLS-DOLARES')],string='Moneda',require=True)
    limite_credito=fields.Float(string='Limite de Credito',require=True)
    dias_credito=fields.Char(string='Dias de Credito',require=True,size=2)
    escala_precios=fields.Many2one('lafox.escala.de.descuentos',string='Escala de Descuentos',require=True)

    #Campos para los Valores del bloque Informativo del Cliente
    metodo_pago_readonly=fields.Selection(METODO_PAGO_SELECTION,string='Metodo de pago',readonly=True)
    saldo_pendiente=fields.Float(string='Saldo Pendiente',store=True)
    promedio_compra_mensual=fields.Float(string='Compra mensual',readonly=True,)
    mayor_compra_mensual=fields.Float(string='Compra mayor',readonly=True)
    ultima_compra_mensual=fields.Float(string='Ultima compra',readonly=True)
    puntualidad_de_pago=fields.Selection(LAFOX_PUNTUALIDAD_PAGO_CLIENTE,string='Puntualidad de pago',require=True)
    cantidad_compra = fields.Float(string='Cantidad Comprada en el mes')
    producto_pref = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO ,string="Preferencia de producto")
    escala_precios_esp =fields.One2many('lafox.precios.cf', 'precio_esp', string='Escala Precio Especial',require=True)

    #Campo para  el state del cliente
    state_cliente=fields.Selection(LAFOX_PUNTUALIDAD_PAGO_CLIENTE, string="Estado del cliente", compute='_compute_estado_cliente', store=False)
    proveedor1 =fields.Char(string="Sufijo del proveedor")
    num_exterior =fields.Char(string="Numero Exterior")
    num_interior = fields.Char(string="Numero Interior")


    # FUNCIONES PARA RES_PARTNER

    # Función que permmite verificar que el RFC para facturar sea el correcto
    @api.multi
    def validate_rfc(self):
        if self.rfc_cliente == "XEXX010101000" or self.rfc_cliente == "XAXX010101000":
            return True
        else:
            try:
                retorno = validate( self.rfc_cliente, validate_check_digits=True)
                return True
            except:
                raise osv.except_osv(("¡Error!"),('El RFC no es Valido, Favor de verificar'))

    # [TODO] REVISAR ESTO PARA QUE SIRVE
    def _menor_lista_1(self, cr, uid, ids, lista,context=None):
        mayor = lista[0]['amount']
        # print mayor de lista
        if valor > mayor:
            mayor = valor
        return mayor

    # Cron que permite actualizar los registros de cada producto vendido
    @api.model
    def _cron_execute_ventas_por_cliente(self):
        today=datetime.now()
        dateMonthStart="%s-%s-01" % (today.year, today.month)
        dateMonthEnd="%s-%s-%s" % (today.year, today.month, calendar.monthrange(today.year-1, today.month)[1])
        line=[]
        # Se crea una busqueda por todas las ventas pagadas y realizadas en el transcurso del mes actual
        for cliente_id in self.env['res.partner'].search([]):
            for account in self.env['account.invoice'].search([('state','=','paid'),('create_date','>',dateMonthStart),('create_date','<',dateMonthEnd),('partner_id','=',cliente_id.id)]):
                dic_line = {}
                dic_line['name']=cliente_id.name
                dic_line['name_id']=cliente_id.id
                dic_line['id_acount']=account.id
                dic_line['amount']=account.amount_total
                line.append(dic_line)

        # Si existe un diccionario y no es nulo se crea un nuevo diccionario y se agrupan por el valor de id_producto
        if line != []:
            list1 = []
            for key, items in itertools.groupby(line, operator.itemgetter('name')):
                list1.append(list(items))

            # Para cada agrupación se hace la suma de sus cantidades vendias y se ajusta a que porcentaje y estatus corresponde
            for ventas in list1:
                print ventas
                # venta_m = self._menor_lista_1(ventas)
                # partner_id = self.env['res.partner'].search([('id','=',venta_m['name_id'])])
                # partner_id.sudo().write({'mayor_compra_mensual':venta_m['amount']})
                # print ventas

    #Se crea una condicion para que no se cree duplicidad de los datos en clientes y en proveedores
    @api.model
    def create(self, values):
        record=super(res_partner,self).create(values)
        if 'in_context' in self._context:
            record['supplier'] = True
        return record

        #Funcion que permite ver el estate del cliente

    @api.multi
    @api.depends('state_cliente')
    def _compute_estado_cliente(self):
        for id_cliente in self:
            if int(id_cliente.promedio_compra_mensual) <= 5000:
                id_cliente.state_cliente = 'MALO'
            elif int(id_cliente.promedio_compra_mensual) <= 15000:
                id_cliente.state_cliente = 'REGULAR'
            elif int(id_cliente.promedio_compra_mensual) <= 30000:
                id_cliente.state_cliente = 'BUENO'
            elif int(id_cliente.promedio_compra_mensual) >= 31000:
                id_cliente.state_cliente = 'EXTRAORDINARIO'


    #Funcion para reemplazar el search de un many2one y buscar por id o clave
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args =args or []
        recs = self.browse()
        if not recs:
            recs = self.search(['|',('clave_cliente', operator, name),('name', operator, name)] + args, limit=limit)
        return recs.name_get()


res_partner()

class ir_attachment(osv.osv):
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'

    # field para ir_Attachment

    select_db = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO,string='Seleccionar Base de Datos')
    # select_vf = fields.Selection(LA_FOX_BLOQUEAR, string='Bloquear')

    def asignar_products(self, cr, uid, ids, context=None):
        # Declaramos el diccionario para la creación de un partner y obtenemos el archivo que se subio
        vals={}
        attachment_dic = self.pool.get('ir.attachment').read(cr, uid, ids, ['name', 'store_fname', 'datas_fname'], context=context)
        filename = attachment_dic[0]['store_fname']
        datas_fname = attachment_dic[0]['datas_fname']
        # data_dn = attachment_dic[0]['select_db']
        file_name, file_extension = os.path.splitext(datas_fname)
        att_ids = self.pool.get('ir.attachment').browse(cr, uid, ids)
        print att_ids.select_db

        # vf_ids = self.pool.get('product.product').browse(cr, uid, ids)
        # print att_ids.select_vf


        archivo_cargado = ODOO_HOME + '.local/share/Odoo/filestore/' + cr.dbname + '/' + filename
        # Consusmimos el script para el parseo del excel, obteniendo los valores
        datos_partner = cargar_MA(archivo_cargado)        
        # Por cada fila del xls creamos un registro con los valores que corresponden a la vista
        for dato in datos_partner:

            # Funcion para insertar el grupo de inventarios
            gpo_inven =self.pool.get('lafox.grupo.de.inventarios').search(cr,uid,[('nomenclatura', '=', dato['GPO_INVENTARIO'])])
            gpo_inventa = self.pool.get('lafox.grupo.de.inventarios').browse(cr,uid,gpo_inven,context=context)
            if gpo_inventa:
                gpo_in = gpo_inventa[0].id
            else:
                vals_gpo_in={
                'nomenclatura' : dato['GPO_INVENTARIO'],
                'nome' : dato['GPO_INVENTARIO'],
                }
                new_id = self.pool.get('lafox.grupo.de.inventarios').create(cr,uid, vals_gpo_in, context=context)
                gpo_in = new_id



            # Funcion para insertar el proveedor en el producto
            proveedor_prod = self.pool.get('res.partner').search(cr,uid,[('proveedor1', '=', dato['PROVEEDOR'])],context=context)
            proveedor_produ = self.pool.get('res.partner').browse(cr,uid,proveedor_prod,context=context)

            # Obtener el grupo de producto 
            gpp_ids = self.pool.get('lafox.grupo.de.precios').search(cr,uid,[('nomenclatura','=',dato['GPO_PRECIO'])])
            gpp_id = self.pool.get('lafox.grupo.de.precios').browse(cr,uid,gpp_ids,context=context)
            if gpp_id:
                gpo_p = gpp_id[0].id
            else:
                vals_gpo={
                'nomenclatura' : dato['GPO_PRECIO'],
                'nom' : dato['GPO_PRECIO'],
                }
                new_id = self.pool.get('lafox.grupo.de.precios').create(cr,uid, vals_gpo, context=context)
                gpo_p = new_id
        

            if len(proveedor_produ) > 0:
                vals={}
                vals['poveedor_prod'] = proveedor_produ[0].id
            else:
                vals['poveedor_prod'] = False


            vals['clave_prod'] = dato['DESCRIPCION']
            vals['cod_crudos'] = dato['CODE_BARRAS']
            vals['description'] = dato['DESCRIPCION']
            vals['piezas_x_paquete'] = dato['PIEZAS']
            vals['unidad_product'] = dato['UNIDDAD']
            vals['imagen_producto'] = dato['IMAGEN']
            vals['grupo_precios_id'] = gpo_p
            vals['ref_prod'] = dato['REFERENCIA']
            vals['grupo_inventarios_id'] = gpo_in
            vals['moneda_prod'] = dato['MONEDA']
            vals['iva_prod'] = dato['IVA']
            vals['list_price'] = dato['PRECIO_BASE']
            vals['observacion_prod'] = dato['OBSERVACION']
            vals['blo_si_no'] = dato['BLOQUEAR']
            vals['name'] = dato['CLAVE']
            
            #vals['ean13'] = dato['CODE_BARRAS']
            
            
            
            
            
            
            vals['c_t'] = att_ids.select_db
            
            #Creamos un nuevo registro en product.product con los valores del diccionario si no se encuentran registros
            product_search = self.pool.get('product.product').search(cr,uid,[('clave_prod', '=', dato['CLAVE'])],context=context)
            if not product_search:
                new_id = self.pool.get('product.product').create(cr,uid, vals, context=context)
            # return new_id

    def asignar_partner(self, cr, uid, ids, context=None):
        # Declaramos el diccionario para la creación de un partner y obtenemos el archivo que se subio
        vals={}
        attachment_dic = self.pool.get('ir.attachment').read(cr, uid, ids, ['name', 'store_fname', 'datas_fname'], context=context)
        filename = attachment_dic[0]['store_fname']
        datas_fname = attachment_dic[0]['datas_fname']
        file_name, file_extension = os.path.splitext(datas_fname)
        att_ids = self.pool.get('ir.attachment').browse(cr, uid, ids)
        print att_ids.select_db

        archivo_cargado = ODOO_HOME + '.local/share/Odoo/filestore/' + cr.dbname + '/' + filename
        # Consusmimos el script para el parseo del excel, obteniendo los valores
        datos_partner = cargar_PT(archivo_cargado)
        # Por cada fila del xls creamos un registro con los valores que corresponden a la vista
        pais = ''
        print 'print despues de pais'
        for dato in datos_partner:

            if dato['PAIS'] == 'GUA':
                pais = 'GT'
            elif dato['PAIS'] == 'CBA':
                pais = 'CU'
            elif dato['PAIS'] == 'PAN':
                pais = 'PA'
            elif dato['PAIS'] == 'USA':
                pais = 'US'
            elif dato['PAIS'] == 'SAL':
                pais = 'SV'
            elif dato['PAIS'] == 'CHI':
                pais = 'CL'
            elif dato['PAIS'] == 'CAN':
                pais = 'CA'
            elif dato['PAIS'] == 'VEN':
                pais = 'VE'
            elif dato['PAIS'] == 'MEX':
                pais = 'MX'
            print 'print despues de if y elif'
            # Obtener el país del cliente
            pais_ids = self.pool.get('res.country').search(cr,uid,[('code','=',pais)])
            pais_id = self.pool.get('res.country').browse(cr,uid,pais_ids,context=context)

            print pais
            print dato['PAIS']
            print pais_ids

            if pais_id:
                pais_p = pais_id[0].id
            # else:
            #     vals_pais = {
            #     'name' : dato['PAIS'],
            #     'code' : dato['PAIS'],
            #     # 'country_id' : edo_id[0].id,
            #     }

            # if not pais_ids:
            # new_id = self.pool.get('res.country').create(cr,uid, vals_pais, context=context)
            # pais_p = new_id

            # Obtener el estado del cliente
            
            edo_ids = self.pool.get('res.country.state').search(cr,uid,[('code','=',dato['ESTADO'])])
            edo_id = self.pool.get('res.country.state').browse(cr,uid,edo_ids,context=context)
            # pais_search = self.pool.get('ir.attachment').search(cr,uid,[('pais_id','=',edo_id.country_id)])
            
            if edo_id:
                edo_p = edo_id[0].id
            else:
                vals_edo = {
                'name' : dato['ESTADO'],
                'code' : dato['ESTADO'],
                'country_id' : pais_p,  
                }
                # print pais_search
                if not edo_id.id:
                    new_id = self.pool.get('res.country.state').create(cr,uid, vals_edo, context=context)
                    edo_p = new_id


            


            # Obtener el grupo de cliente
            # gpp_ids = self.pool.get('lafox.grupo.de.precios').search(cr,uid,[('nomenclatura','=',dato['ESCALA_PRECIOS'])])
            # gpp_id = self.pool.get('lafox.grupo.de.precios').browse(cr,uid,gpp_ids,context=context)
            # if gpp_id:
            #     gpo_p = gpp_id[0].id
            # else:
            #     vals_gpo={
            #     'nomenclatura' : dato['ESCALA_PRECIOS'],
            #     'nom' : dato['ESCALA_PRECIOS'],
            #     }
            #     new_id = self.pool.get('lafox.grupo.de.precios').create(cr,uid, vals_gpo, context=context)
            #     gpo_p = new_id


                #Obtener el vendendor del clientes
            ven_ids = self.pool.get('lafox.clientes.vendedor').search(cr,uid,[('name','=',dato['VENDEDOR'])])
            ven_id = self.pool.get('lafox.clientes.vendedor').browse(cr,uid,ven_ids,context=context)
            if ven_id:
                ven_p = ven_id[0].id
            else:
                vals_ven={
                'name' : dato['VENDEDOR'],
                'nam' : dato['VENDEDOR'],
                }
                new_id = self.pool.get('lafox.clientes.vendedor').create(cr,uid, vals_ven, context=context)
                ven_p = new_id

            #Obtener la escala de descuentos
            gpp_ids = self.pool.get('lafox.escala.de.descuentos').search(cr,uid,[('escala','=',(dato['ESCALA_PRECIOS'])), ('tipo_escala', '=', att_ids.select_db)])
            gpp_id = self.pool.get('lafox.escala.de.descuentos').browse(cr,uid,gpp_ids,context=context)

            print gpp_ids
            
            if gpp_id:
                gpo_p = gpp_id[0].id
            else:
                vals_gpo={
                'escala' : (dato['ESCALA_PRECIOS']),
                'tipo_escala' : att_ids.select_db,
                }
                new_id = self.pool.get('lafox.escala.de.descuentos').create(cr,uid, vals_gpo, context=context)
                gpo_p = new_id

            # des_ids = self.pool.get('lafox.escala.de.descuentos').search(cr,uid,[('escala','=',dato['VENDEDOR'])])
            # des_id = self.pool.get('lafox.escala.de.descuentos').browse(cr,uid,ven_ids,context=context)


            vals['producto_pref'] = att_ids.select_db
            vals['clave_cliente'] = dato['CLAVE']
            vals['name'] = dato['NOMBRE']
            vals['street'] = dato['DIRECCION']
            vals['rfc_cliente'] = dato['EXTERIOR']
            vals['rfc_cliente'] = dato['INTERIOR']
            vals['street2'] = dato['COLONIA']
            vals['city'] = dato['CIUDAD_DELEG']
            vals['zip'] = dato['ZIP']
            vals['state_id'] = edo_p
            vals['country_id'] = pais_p
            vals['lada_cliente'] = dato['LADA']
            vals['phone'] = dato['TELEFONO']
            vals['mobile'] = dato['MOBILE']
            vals['email'] = dato['EMAIL']
            vals['vendedor'] = ven_p
            vals['medio_contacto'] = dato['MEDIO_CONTACTO']
            vals['referencia'] = dato['REFERENCIA']
            vals['observaciones'] = dato['OBSERVACION']
            vals['rfc_cliente'] = dato['RFC']
            vals['metodo_pago_readonly'] = dato['METODO_PAGO']
            vals['fisica_moral'] = dato['FISICA_MORAL']
            vals['moneda_valores'] = dato['MONEDA']
            vals['limite_credito'] = dato['LIMITE_CREDITO']
            vals['dias_credito'] = dato['DIAS_CREDITO']
            vals['escala_precios'] = gpo_p
            vals['saldo_pendiente'] = dato['SALDO_PENDIENTE']
            vals['promedio_compra_mensual'] = dato['PROMEDIO_COMPRA_M']
            vals['mayor_compra_mensual'] = dato['COMPRA_MAYOR']
            vals['ultima_compra_mensual'] = dato['ULT_COMPRA']
            vals['puntualidad_de_pago'] = dato['PUNTUALIDAD_PAGO']
            # vals['rfc_cliente'] = dato['TELEFONO3']
            
            # Creamos un nuevo registro en product.product con los valores del diccionario
            print vals
            # state_search = self.pool.get('res.partner').search(cr,uid,[('state_id', '=', dato['ESTADO'] )],context=context)
            # if not state_search:
                # state_id = False
            partner_search = self.pool.get('res.partner').search(cr,uid,[('clave_cliente', '=', dato['CLAVE']),('producto_pref', '=', att_ids.select_db)],context=context)
            if not partner_search:
                new_id = self.pool.get('res.partner').create(cr,uid, vals, context=context)

        # return new_id
ir_attachment()

class res_company(models.Model):
    _name = 'res.company'
    _inherit = 'res.company'

res_company()

class seguimiento_pedido(models.Model):
    _name='lafox.seguimiento.pedido'

    pedido=fields.Char(string='Pedido',require=True,size=13,help='Introduce el numero del pedido a Enviar')
    estatus=fields.Selection(LAFOX_SELECT_ESTATUS_PEDIDO,require=True,string='Estatus del Pedido')
    contacto_seguimiento=fields.Char(string='Contacto de seguimiento')
    fecha_envio= fields.Datetime(string='Fecha y Hora de envio')
    fecha_entrega= fields.Datetime(string='Fecha y Hora de entrega')
    grupo_ventas_facturacion=fields.Char(string='Ventas y Facturacion',require=True)
    descripcion=fields.Text(string='Observaciones y notas...')
    ventas_ids = fields.Many2one('account.invoice', string='Venta')

seguimiento_pedido()

class lafox_seguimiento_venta_producto(models.Model):
    _name='lafox.seguimiento.venta.producto'
    # Fields para modelo lafox_seguimiento_venta_producto
    fecha_venta = fields.Datetime(string='Fecha de Venta')
    cantidad = fields.Float(string='Cantidad')
    costo = fields.Float(string='Costo-Venta')
    cliente_venta = fields.Many2one('res.partner', string='Cliente')
    account_ids = fields.Many2one('product.product', string='account Id')
    venta_realizada = fields.Char(string='Venta')
    id_invoice_line = fields.Integer(string='In invoice')

lafox_seguimiento_venta_producto()

class res_users(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    #FIELDS PARA RES USERS

    almacenes_id = fields.Many2one('stock.location', string='Almacen')

res_users()
class hr_employee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    # FIELDS PARA MODEL hr_employee
    departamento_user = fields.Many2one('res.groups', string='Departamento')
    almacenes_id = fields.Many2one('stock.location', string='Almacen')
    action_id = fields.Many2one('ir.actions.actions', string='Acción Inicial')

    #Fields para Datos del empleado
    country = fields.Char(string='Nacionalidad', default=lambda self: self._get_default_country(),)
    id_biometrico = fields.Char(string='ID Biometrico')
    oficina_fab = fields.Many2one('lafox.regla.asistencia.oficina', string='Lugar de trabajo')
    password_account = fields.Char('Contraseña para Precios Especiales')



    # # Modificcación de Create para poder crear usuarios sin necesidad de hacer los dos pasos
    @api.model
    def create(self, vals):
        employee_id = self.env['stock.location'].search([('id','=',int(vals['almacenes_id']))])
        if employee_id:
            almacen_ids = employee_id[0].id
        else:
            almacen_ids = False
        vals_users = {
            'groups_id': [
                [6, False, [int(vals['departamento_user'])]]
            ],
            'name': vals['name'],
            'mobile': vals.get('tel_celular', False),
            'image': vals.get('image_medium', False),
            'phone': vals['work_phone'],
            'login': vals.get('work_email', False),
            'email': vals['work_email'],
            'almacenes_id': almacen_ids,
            'action_id': vals['action_id'],
        }

        self.env['res.users'].sudo().create(vals_users)
        rec = super(hr_employee, self).create(vals)
    #     # ...
        return rec
    #Regresa como valor predeterminado Mexicana
    @api.model
    def _get_default_country(self):

        return "Méxicana"

hr_employee()

class hr_asistencia_employee(models.Model):
    _name = 'hr.asistencia.employee'

    # FIELDS PARA MODEL hr_asistencia_employee
    name = fields.Many2one('hr.employee',string='Empleado', required=True, index=True)
    hora_inicio = fields.Datetime(string='Fecha y hora Asistencia', required=True, index=True )
    hora_display = fields.Datetime(string='Fecha y hora Asistencia', required=True, index=True)
    hora_display_fin = fields.Datetime(string='Fecha y hora Asistencia', required=True, index=True)
    estatus = fields.Selection(LAFOX_SELECT_STATE_CLIENTE ,string='Estatus Asistencia', readonly=True)

    # Función que obtiene el status para cada registro segun la hora para cada registro del biometrico hacia el sistema
    @api.multi
    def _create_status(self,hora_display,employee_id):

        tz=pytz.timezone('America/Mexico_City')
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        UTC_DATE_BIO = datetime.strptime(str(hora_display),DATETIME_FORMAT)
        UTC_DATE_BIO = pytz.utc.localize(dt.datetime.strptime(str(UTC_DATE_BIO),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))
        # UTC_DATE_BIO2 = pytz.utc.localize(dt.datetime.strptime(str(UTC_DATE_BIO1[:20]),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))s

        entrada = str(fields.date.today()) + " " +  employee_id.oficina_fab.hora_entrada
        entrada = datetime.strptime(entrada,DATETIME_FORMAT)
        entrada = pytz.utc.localize(dt.datetime.strptime(str(entrada),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))

        r_suave = str(fields.date.today()) + " " + employee_id.oficina_fab.retardo_suave
        r_suave = datetime.strptime(r_suave,DATETIME_FORMAT)
        r_suave = pytz.utc.localize(dt.datetime.strptime(str(r_suave),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))

        r_duro = str(fields.date.today()) + " " + employee_id.oficina_fab.retardo_duro
        r_duro = datetime.strptime(r_duro,DATETIME_FORMAT)
        r_duro = pytz.utc.localize(dt.datetime.strptime(str(r_duro),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))

        desayuno = str(fields.date.today()) + " " + employee_id.oficina_fab.desayuno
        if employee_id.oficina_fab.desayuno == 'N/A':
            desayuno = str(fields.date.today()) + " " + '10:00:00'
        desayuno = datetime.strptime(desayuno,DATETIME_FORMAT)
        desayuno = pytz.utc.localize(dt.datetime.strptime(str(desayuno),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))

        desayuno_r = str(fields.date.today()) + " " + employee_id.oficina_fab.desayuno_retardo
        if employee_id.oficina_fab.desayuno_retardo =='N/A':
            desayuno_r = str(fields.date.today()) + " " + '10:20:00'
        desayuno_r = datetime.strptime(desayuno_r,DATETIME_FORMAT)
        desayuno_r = pytz.utc.localize(dt.datetime.strptime(str(desayuno_r),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))

        comida = str(fields.date.today())+ " " + employee_id.oficina_fab.comida
        if employee_id.oficina_fab.comida == 'N/A':
            comida = str(fields.date.today()) + " " + '14:00:00'
        comida = datetime.strptime(comida,DATETIME_FORMAT)
        comida = pytz.utc.localize(dt.datetime.strptime(str(comida),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))

        comida_r = str(fields.date.today()) + " " + employee_id.oficina_fab.comida_retardo
        if employee_id.oficina_fab.comida_retardo =='N/A':
            comida_r = str(fields.date.today()) + " " + '14:50:00'
        comida_r = datetime.strptime(comida_r,DATETIME_FORMAT)
        comida_r = pytz.utc.localize(dt.datetime.strptime(str(comida_r),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT'))

        salida = str(fields.date.today()) + " " + employee_id.oficina_fab.salida
        salida = datetime.strptime(salida,DATETIME_FORMAT)
        salida = pytz.utc.localize(dt.datetime.strptime(str(salida),DATETIME_FORMAT)).astimezone(pytz.timezone('UCT')) 


        if UTC_DATE_BIO <=entrada:
            return "0"

        elif UTC_DATE_BIO > entrada and UTC_DATE_BIO>=r_suave and UTC_DATE_BIO<r_duro and UTC_DATE_BIO<desayuno:
            return "1"

        elif UTC_DATE_BIO > entrada and UTC_DATE_BIO>r_suave and UTC_DATE_BIO>r_duro and UTC_DATE_BIO<=desayuno:
            return "2"

        elif UTC_DATE_BIO > entrada and UTC_DATE_BIO>r_suave and UTC_DATE_BIO>r_duro and UTC_DATE_BIO>desayuno and UTC_DATE_BIO<=desayuno_r and (employee_id.oficina_fab.lugar_trabajo == 'Fabrica' ):
            return "3"
        
        elif UTC_DATE_BIO > entrada and UTC_DATE_BIO>r_suave and UTC_DATE_BIO>r_duro and UTC_DATE_BIO>desayuno and UTC_DATE_BIO>desayuno_r and UTC_DATE_BIO<=comida and (employee_id.oficina_fab.lugar_trabajo == 'Fabrica' ):
            return "4"

        elif UTC_DATE_BIO > entrada and UTC_DATE_BIO>r_suave and UTC_DATE_BIO>r_duro and UTC_DATE_BIO>desayuno and UTC_DATE_BIO>desayuno_r and UTC_DATE_BIO>comida and UTC_DATE_BIO<=comida_r and (employee_id.oficina_fab.lugar_trabajo == 'Fabrica' ):
            return "5"

        elif UTC_DATE_BIO > entrada and UTC_DATE_BIO>r_suave and UTC_DATE_BIO>r_duro and UTC_DATE_BIO>desayuno and UTC_DATE_BIO>desayuno_r and UTC_DATE_BIO>comida and UTC_DATE_BIO>comida_r and UTC_DATE_BIO<=salida and (employee_id.oficina_fab.lugar_trabajo == 'Fabrica' ):
            return "6"

        elif UTC_DATE_BIO>salida:
            return "7"

        else:
            return "8"

    # Función que permite responder el .py para el consumo del ZKT Biometrico
    # [TODO] A espera de revisión de que registros se deberan tomar
    @api.multi
    def value_assistence(self,asistencias):
        print asistencias
        # Obtenemos las zonas horarias para el pintado correcto en Odoo y para la hora incial correspondiente a la CDMX
        UTC_DATE = datetime.utcnow()
        tz=pytz.timezone('America/Mexico_City')
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        STC_DATE  = pytz.utc.localize(UTC_DATE,DATETIME_FORMAT).astimezone(tz)
        UTC_DATE = datetime.strptime(str(UTC_DATE)[0:19],DATETIME_FORMAT)
        STC_DATE = datetime.strptime(str(STC_DATE)[0:19],DATETIME_FORMAT)
        UTC_DATE_TIME =UTC_DATE - STC_DATE
        TZ_TIMEDELTA= (UTC_DATE_TIME.seconds/3600)

        # Si el .py trae registros se obtienen las fechas,nombres y estatus para cada registro.
        for asistencia_usr in asistencias:
            someday = datetime.strptime(str(asistencia_usr[2])[0:8], '%Y%m%d')
            fecha_inicio =  datetime.strptime(str(asistencia_usr[2]), '%Y%m%dT%H:%M:%S')
            display  = fecha_inicio
            display_  = fecha_inicio + timedelta(hours=TZ_TIMEDELTA)
            display_fin  = display_ + timedelta(minutes=20)

            if someday.date()>= date.today():
                # Se busca el id del biometrico con el campo otherid dentro de los empleados de Lafox   
                employee_id = self.env['hr.employee'].search([('id_biometrico','=',asistencia_usr[0])])
                variable_estatus = self._create_status(display, employee_id[0])
                if len(employee_id)>0:
                    values = {}
                    values['name'] = asistencia_usr[0]
                    values['hora_inicio'] = fecha_inicio
                    values['estatus'] = str(variable_estatus)
                    values['hora_display'] = display_
                    values['hora_display_fin'] = display_fin
                    # Se crea el registro en odoo por cada registro del ZKT
                    self.env['hr.asistencia.employee'].sudo().create(values)
        return True

        # Obtnemos el id de la cotización a usar

hr_asistencia_employee()

class lafox_corteparcial_venta(models.Model):
    _name = 'lafox.corteparcial.venta'
    _auto = False

    # FIELDS PARA MODEL lafox_cortez_ventas
    # code_venta = fields.Many2one('account.invoice',string='Venta')
    nomenclatura_venta = fields.Char(string='Folio Venta')
    cliente_venta = fields.Many2one('res.partner', string='Cliente')
    fecha_venta = fields.Datetime(string='Fecha Venta')
    responsable_venta = fields.Many2one('res.users', string='Responsable')
    total_venta = fields.Float(string='Total Venta')
    estatus_venta = fields.Selection(ACCOUNT_STATE, string='Estatus')

    _order = 'fecha_venta desc'

    # FUNCIÓN QUE PERMITE OBTENER TODAS LAS VENTAS DEL DIA
    def init(self, cr):
        fecha_inicio = date.today()
        fecha_fin = date.today() + timedelta(days=1)
        today=datetime.now()
        dateMonthStart="%s-%s-01" % (today.year, today.month)
        dateMonthEnd="%s-%s-%s" % (today.year, today.month, calendar.monthrange(today.year-1, today.month)[1])

        tools.drop_view_if_exists(cr, 'lafox_corteparcial_venta')
        cr.execute("""
            create or replace view lafox_corteparcial_venta as (
                select
                    min(id) as id,
                    nomenclatura as nomenclatura_venta,
                    partner_id as cliente_venta,
                    fecha_venta as fecha_venta,
                    user_id as responsable_venta,
                    amount_total as total_venta,
                    state as estatus_venta
                from
                    account_invoice
                WHERE
                fecha_venta >= current_date  and fecha_venta <current_date +1
                GROUP BY
                    nomenclatura,fecha_venta,user_id,partner_id,amount_total,state

            )
        """)

lafox_corteparcial_venta()

    # fecha_inicial = fields.Datetime(string='Fecha Inicio')
    # fecha_final = fields.Datetime(string='Fecha fin')
    # tipo_venta = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO, string='Vendedor de:')

    # venta_total = fields.Float(string='Corte al día')

    # corteventas_ids = fields.Many2one('lafox.cortez.ventas',string='IDS Corte Z')
    # corteventas_id = fields.One2many('lafox.cortez.ventas','corteventas_ids',string='ID Corte Z')

class lafox_clientes_vendedor(models.Model):
    _name='lafox.clientes.vendedor'

    nombres=fields.Char(string='Nombre(s)',require=True)
    apellidos=fields.Char(string='Apellido(s)',require=True)
    movil=fields.Char(string='Movil',require=True,size=10)
    telefono=fields.Char(string='Telefono',size=10)
    area=fields.Char(string='Area/Zona',require=True)
    descripcion=fields.Text(string='Descrip./Obs.',size=50)
    name = fields.Char(string='Nomenclatura')

lafox_clientes_vendedor()

class lafox_change_monetary(models.Model):
    _name='lafox.change.monetary'

    # Compute para sacar el tipo de moneda en pesos siempre
    @api.model
    def _default_curreny(self):
        currency_id = self.env['res.currency'].search([('name', '=', "MXN")])
        return currency_id[0]

    # Compute para sacar el costo la fecha anteriror
    @api.model
    def _default_date_before(self):
        prices_id = self.env['lafox.change.monetary'].search([('id', '=', 1)])
        if prices_id:
            fecha = prices_id.fecha_cambio
            return fecha

    # Compute para sacar el costo del dolar anteriror
    @api.model
    def _default_price_before(self):
        price = 0.0
        prices_id = self.env['lafox.change.monetary'].search([('id', '=', 1)])
        if prices_id:
            price = prices_id.price_dolar
        return price

    @api.model
    def _default_percent_before(self):
        porcentaje=0.0
        porcentaje_id=self.env['lafox.change.monetary'].search([('id','=',1)])
        if porcentaje_id:
            porcentaje=porcentaje_id.porcentaje_cambio
        else:
            porcentaje = False
        return porcentaje

    #Campos  lafox_change_monetary
    price_dolar = fields.Float(string='Pesos',require=True)
    porcentaje_cambio=fields.Float(string='Porcentaje de descuento nuevo',require=True)
    precio_actual_dolar = fields.Float(string='Dolares', compute='compute_tipo_dolar', store='True')
    #----------------------------------------------------------------------------------
    porcentaje_cambio_before=fields.Float(string='Porcentaje anterior', default=_default_percent_before)
    #-------------------------------------------------------------------------------------------------------
    price_before = fields.Float(string='Costo anterior', default=_default_price_before)
    currency_id = fields.Many2one('res.currency',string='Tipo de moneda', default=_default_curreny)
    fecha_cambio = fields.Datetime(string='Fecha y Hora del último cambio', default=_default_date_before)


     #Compute para sacar el precio del dolar automaticamente
    @api.multi
    @api.depends('price_dolar')
    def compute_tipo_dolar(self):
        # client = Client('http://www.banxico.org.mx:80/DgieWSWeb/DgieWS?WSDL')
        # xml_tree = ET.fromstring(client.service.tiposDeCambioBanxico().encode('Latin-1'))
        # res = xml_tree.find('.//*[@IDSERIE="SF60653"]/*')
        # data = res.attrib
        # self.precio_actual_dolar = data['OBS_VALUE']
        resp = requests.get('http://api.cambio.today/v1/quotes/USD/MXN/json?quantity=1&key=2344|pAVwn9ASPPZJVWhOe2jFG9DGFc1_2g~*')
        dls = json.loads(resp.content)
        self.precio_actual_dolar = dls["result"]['value']

    # Funcion que permite sobreescribir el mismo regitro y elimina los registros basura
    @api.multi
    def button_change_money(self):
        # Se busca el primer registro y se asigna el valor del dolar
        prices_id = self.env['lafox.change.monetary'].search([('id', '=', 1)])
        fecha = fields.datetime.now()
        prices_id.write({'price_dolar':self.price_dolar,'fecha_cambio':fecha,'porcentaje_cambio':self.porcentaje_cambio})
        self.fecha_cambio = fields.datetime.now()
        # Los registros sobrantes existentes son eliminados
        for price_delete in self.env['lafox.change.monetary'].search([('id', '>', 1)]):
            self.env['lafox.change.monetary'].search([('id','=', price_delete.id)]).unlink()



lafox_change_monetary()



class lafox_realizar_pago(models.Model):
    _name='lafox.realizar.pago'

    # Función que nos permite obtner el monto de venta
    @api.multi
    @api.depends('monto_cambio')
    def _compute_monto_total(self):
        class_obj = self.env['account.invoice'].browse(self._context.get('active_id'))
        self.monto_total =  class_obj.amount_total

    # Funcion para obtener el total de cambio a devolver
    @api.multi
    def _on_change_monto_cambio(self,monto_total,monto_pagado):
        dic = {}
        cambio = monto_pagado - monto_total
        dic['value']={
            'monto_cambio': cambio
            }
        return dic

    # Funcioón para cambiar el status para realizar el pago
    @api.multi
    def action_paid_venta_money(self):
        class_obj = self.env['account.invoice'].browse(self._context.get('active_id'))
        cambio = (self.monto_pagado - self.monto_total)
        print self.monto_pagado
        print "----------"
        print self.monto_total
        if self.monto_pagado < self.monto_total:    
            raise osv.except_osv(('No es posible realizar el pago'), ('La cantidad Pagada es menor al monto Total'))
        else:
            class_obj.sudo().write({'state':'paid'})
            class_obj.sudo().write({'state_ac':'paid'})

    # Compute para sacar el tipo de moneda en pesos siempre
    @api.model
    def _default_curreny(self):
        currency_id = self.env['res.currency'].search([('name', '=', "MXN")])
        return currency_id[0]

    # Campos para la_fox_realizar_pago
    monto_total = fields.Float(string='Monto Total', compute='_compute_monto_total', store=True)
    monto_pagado = fields.Float(string='Cantidad Pagada')
    monto_cambio = fields.Float(string='Cambio')
    currency_id = fields.Many2one('res.currency',string='Tipo de moneda', default=_default_curreny)

lafox_realizar_pago()

#Inicia la clase para generar el reporte de ventas dependiendo de las fechas y el cliente...
class lafox_reporte_de_venta(models.Model):
    _name='lafox.reporte.de.venta'

    registro_One2many=fields.One2many('lafox.reporte.de.venta','registro_Many2one',string='Registros')
    registro_Many2one=fields.Many2one('lafox.reporte.de.venta',string='Registros')

    fecha_inicio=fields.Date(string='Fecha de inicio',require=True)
    fecha_final=fields.Date(string='Fecha de fin',require=True)
    seleccion_cliente=fields.Many2one('res.partner',string='Selecciona al cliente')
    seleccion_vendedor=fields.Many2one('res.users',string='Selecciona Vendedor')
    seleccion_producto=fields.Selection(LAFOX_SELECT_PRODUCTO,string='Selecciona tipo de producto')
    seleccion_pro=fields.Many2one('product.product',string='Reporte por producto')
    seleccion_tipo = fields.Selection(LAFOX_TIP_VENTA,string='Tipo de Venta')

    nomenclatura_venta_rv=fields.Char(string='Folio Venta')
    cliente_venta_rv=fields.Many2one('res.partner', string='Cliente')
    fecha_venta_rv=fields.Datetime(string='Fecha Venta')
    estatus_venta_rv=fields.Selection(ACCOUNT_STATE, string='Estatus')
    prod_name_rv=fields.Char(string='Producto')
    total_venta_rv=fields.Float(string='Total')
    #FIELD PARA FILTRO POR DESCUENTOS
    filtro_descuentos = fields.Many2one('lafox.escala.de.descuentos', 'Seleccione Descuento')
    #FIELD PARA EL CONTEO DE FORMULARIO
    serials_qty = fields.Integer(string='Total Piezas', readonly=True)
    serials_pac = fields.Integer(string='Total Paquetes', readonly=True)

    #FIELD PARA EL CONTEO DEl TOTAL DE VENTAS
    ventas_qty = fields.Float(string='Total $', readonly=True, digits=dp.get_precision('Product Price'))

    # FUNCION PARA DEVOLVER EN DOMAIN CON DIFERENTES FILTROS
    def _get_domain_report(self, dom, filtro, value):

        tupla = (filtro,"=",value)
        dom.append(tupla)

        return dom

    # FUNCION PARA E LLENADO DE LOS REPORTES
    @api.multi
    def _llenado_reporte_venta(self,fecha_inicio,fecha_final,seleccion_cliente,seleccion_vendedor,seleccion_producto,filtro_descuentos,seleccion_tipo,seleccion_pro,context):
        lines=[]
        dicct={}
        
        if (fecha_inicio and fecha_final and seleccion_pro == False):
            domain =  [('fecha_venta_6','>=',fecha_inicio),('fecha_venta_6','<=',fecha_final),('state','!=','cancel')]
            
            if seleccion_cliente:
                domain= self._get_domain_report(domain, "partner_id", seleccion_cliente)

            if seleccion_vendedor:
                domain= self._get_domain_report(domain, "create_uid", seleccion_vendedor)

            if seleccion_producto:
                domain= self._get_domain_report(domain, "tipo_producto", seleccion_producto)

            if seleccion_tipo:
                if seleccion_tipo == "0":
                    typeAcc = False
                else:
                    typeAcc = True
                domain= self._get_domain_report(domain, "check_credito", typeAcc)

            if filtro_descuentos:
                desc_id = self.env['lafox.escala.de.descuentos'].browse(filtro_descuentos)
                des = desc_id.escala + " " + desc_id.descuentos
                domain= self._get_domain_report(domain, "esca_cliente", des)

            t_ven = 0 
            p_ven = 0 
            am_ven = 0 
            for reg in self.env['account.invoice'].search(domain):
                for reg_line in self.env['account.invoice.line'].search([('invoice_id','=',reg.id)]):
                    t_ven = t_ven + reg_line.quantity
                    p_ven = p_ven + reg_line.cantidad_producto

                total_v = reg.amount_total
                if reg.partner_id.moneda_valores == 'D':
                    pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]
                    total_v = total_v * pesos.price_dolar

                if reg.tipo_producto == '0':
                    tipo_producto = 'ACCESORIOS'
                else:
                    tipo_producto = 'TERMINADO'
                dic_line = {}
                dic_line['nomenclatura_venta_rv'] = reg.nomenclatura
                dic_line['cliente_venta_rv'] = reg.partner_id
                dic_line['fecha_venta_rv'] = reg.fecha_venta
                dic_line['estatus_venta_rv'] = reg.state
                dic_line['prod_name_rv']= tipo_producto
                dic_line['total_venta_rv'] = total_v
                dic_line['seleccion_pro'] = False
                lines.append(dic_line)
                # t_ven = t_ven + 1
                am_ven = am_ven + total_v

            dicct['value']={'registro_One2many':lines, 'serials_qty':t_ven,'serials_pac':p_ven, 'ventas_qty': am_ven}

        elif (fecha_inicio and fecha_final and seleccion_pro != False):
            t_ven = 0 
            p_ven = 0 
            am_ven = 0
            for reg in self.env['account.invoice'].search([('fecha_venta_6','>=',fecha_inicio),('fecha_venta_6','<=',fecha_final)]):
                for prod in self.env['account.invoice.line'].search([('invoice_id','=',reg.id),('product_id','=',seleccion_pro)]):
                    print prod
                    t_ven = t_ven + prod.quantity
                    p_ven = p_ven + prod.cantidad_producto
                    if reg.tipo_producto == '0':
                        tipo_producto = 'ACCESORIOS'
                    else:
                        tipo_producto = 'TERMINADO'
                    dic_line = {}
                    dic_line['nomenclatura_venta_rv'] = reg.nomenclatura
                    dic_line['cliente_venta_rv'] = reg.partner_id
                    dic_line['fecha_venta_rv'] = reg.fecha_venta
                    dic_line['estatus_venta_rv'] = reg.state
                    dic_line['prod_name_rv']= tipo_producto
                    dic_line['total_venta_rv'] = reg.amount_total
                    dic_line['seleccion_pro'] = prod.product_id
                    lines.append(dic_line)
                    # t_ven = t_ven + 1
                    am_ven = am_ven + reg.amount_total

                dicct['value']={'registro_One2many':lines, 'serials_qty':t_ven,'serials_pac':p_ven, 'ventas_qty': am_ven}
                # dicct['value']={'registro_One2many':lines, 'serials_qty':t_ven, 'ventas_qty': am_ven}

        return dicct

class lafox_corte_z(models.Model):
    _name='lafox.corte.z'

    @api.multi
    @api.depends('registros_z_O')
    def _compute_get_total(self):
        for data in self:
            data.total_corte_z = sum(line.total_venta_z for line in data.registros_z_O)

    @api.multi
    def _default_almacen_corte(self):
        email =  self.env.user.login
        employee_id =  self.env['hr.employee'].search([('work_email','=',email)])
        if employee_id:
            return employee_id[0].almacenes_id.id

    registros_z_O=fields.One2many('lafox.registros.cortez', 'registros_z_M', string='Ventas')
    fecha_corte_z=fields.Date(string='Fecha de Corte Z',readonly=True, default=date.today())
    total_corte=fields.Float(string='TOTAL')
    total_corte_z=fields.Float(string='TOTAL', compute='_compute_get_total', store='True')
    almacen_id = fields.Many2one('stock.location', string='Ubicacion', default=_default_almacen_corte )
    can_view = fields.Boolean(string='Se puede ver', default='True')

    @api.onchange('fecha_corte_z','almacen_id')
    def _llenado_corte_Z(self):
        if self.almacen_id:
            corte_z = self.env['lafox.valida.estatus.boton'].search([('fecha', '=', date.today()),('almacen_id','=',self.almacen_id.id)])
            if corte_z:
                raise osv.except_osv(('No es posible realizar el CORTE-Z'), ('Ya ha sido realizado el corte Z con la fecha del día de hoy'))

            else:
                self.can_view = False

            today_today=date.today()
            today_tomorrow=today_today+timedelta(days=1)
            lines=[]
            total = 0
            for fill_args in self.env['account.invoice'].search([('fecha_venta_6','=',str(today_today)),('state','!=','draft'),('stock_venta','=',self.almacen_id.id)]):
                dic_line = {}
                dic_line['nomenclatura_venta_z'] = fill_args.nomenclatura
                dic_line['cliente_venta_z'] = fill_args.partner_id
                dic_line['fecha_venta_z'] = fill_args.fecha_venta
                dic_line['responsable_venta_z'] = fill_args.user_id
                dic_line['total_venta_z'] =fill_args.amount_total
                dic_line['estatus_venta_z'] =fill_args.state
                dic_line['registros_z_M'] = self.id
                lines.append(dic_line)
                total = total + fill_args.amount_total
            self.registros_z_O=lines
            self.total_corte = total

    @api.multi
    def button_corte_z(self):
        today_today=date.today()
        today_tomorrow=today_today+timedelta(days=1)

        for ventas_pagadas in self.env['account.invoice'].search([('fecha_venta_6','=',str(today_today)),('stock_venta','=',self.almacen_id.id)]):
            if ventas_pagadas.state!='draft':
                # estatus_venta_z_boton=self.env['lafox.valida.estatus.boton'].search([])
                vals_valida = {'estatus':True, 'fecha': today_today, 'almacen_id':self.almacen_id.id}
                self.env['lafox.valida.estatus.boton'].sudo().create(vals_valida)
                # estatus_venta_z_boton[0].sudo().create()

                #Si estan las ordenes 'paid' el estatus se le cambia la bandera a True mientras tanto estara en False cuando te permita generar ventas
                dic_line = {}
                dic_line['nomenclatura_venta_z'] = ventas_pagadas.nomenclatura
                dic_line['cliente_venta_z'] = ventas_pagadas.partner_id.id
                dic_line['fecha_venta_z'] = ventas_pagadas.fecha_venta
                dic_line['responsable_venta_z'] = ventas_pagadas.user_id.id
                dic_line['total_venta_z'] =ventas_pagadas.amount_total
                dic_line['estatus_venta_z'] =ventas_pagadas.state
                dic_line['registros_z_M'] = self.id
                self.env['lafox.registros.cortez'].sudo().create(dic_line)
            else:
                raise osv.except_osv(('No es posible realizar el CORTE-Z'), ('Aún hay facturas con estado BORRADOR(draft) ; es neceario cerrar las ventas'))

lafox_corte_z()

class lafox_registros_cortez(models.Model):
    _name="lafox.registros.cortez"

    registros_z_M=fields.Many2one('lafox.corte.z',string='Registros')
    nomenclatura_venta_z=fields.Char(string='Folio Venta')
    cliente_venta_z=fields.Many2one('res.partner', string='Cliente')
    fecha_venta_z=fields.Datetime(string='Fecha Venta')
    responsable_venta_z=fields.Many2one('res.users', string='Responsable')
    total_venta_z=fields.Float(string='Total Venta')
    estatus_venta_z=fields.Selection(ACCOUNT_STATE, string='Estatus')

lafox_registros_cortez()

class lafox_valida_estatus_boton(models.Model):
    _name='lafox.valida.estatus.boton'

    estatus=fields.Boolean(string='Estatus',default=True)
    fecha=fields.Date(string='Fecha')
    almacen_id = fields.Many2one('stock.location', string='Ubicacion')

    @api.model
    def _can_view_corte_z(self):
        estado=self.search([])
        fecha_ahora=date.today()
        estado[0].sudo().write({'estatus':False,'fecha':fecha_ahora})

lafox_valida_estatus_boton()

class lafox_escala_de_descuentos(models.Model):
    _name='lafox.escala.de.descuentos'
    _rec_name = "escala"
    
    escala=fields.Char(string='Escala')
    descuentos=fields.Char(string='Descuento')
    factor=fields.Float(string='Factor',digits=dp.get_precision('Product UoS'))
    tipo_escala = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO, string='Tipo de Escala')

lafox_escala_de_descuentos()

class lafox_control_horarios(models.Model):
    _name='lafox.control.horarios'
    
    name=fields.Char(string='Tipo de Horario')
    hr_entrada = fields.Char(string='Hora de Entrada')
    hr_salida = fields.Char(string='Hora de Salida')
    hr_retardo_suave = fields.Char(string='Hora Retardo Suave')
    hr_retardo_duro = fields.Char(string='Hora Retardo Duro')
    hr_desayuno = fields.Char(string='Hora del Desayuno')
    hr_desayuno_retardo = fields.Char(string='Retardo Fuerte Desayuno')
    hr_comida = fields.Char(string='Hora de la Comida')
    hr_comida_retardo = fields.Char(string='Retardo Fuerte Comida')


lafox_control_horarios()
#Inicia la clase para el registro de asistencia

class lafox_regla_asistencia_oficina(models.Model):
    _name='lafox.regla.asistencia.oficina'
    _rec_name = 'lugar_trabajo'

    #Inicia horario de entrada de la fabrica

    lugar_trabajo=fields.Selection(LAFOX_HR_ASISTECIA, string='Lugar de trabajo')
    hora_entrada=fields.Char(string='Hora Entrada', size=256)
    retardo_suave=fields.Char(string='Retardo Suave', size=256)
    retardo_duro=fields.Char(string='Retardo Duro', size=256)
    desayuno=fields.Char(string='Desayuno', size=256)
    desayuno_retardo=fields.Char(string='Retardo Fuerte del Desayuno', size=256)
    comida=fields.Char(string='Comida', size=256)
    comida_retardo=fields.Char(string='Retardo Fuerte de la Comida', size=256)
    salida=fields.Char(string='Salida', size=256)
    

lafox_regla_asistencia_oficina()

class lafox_informacion_ventas(models.Model):
    _name ='lafox.informacion.ventas'

    #Inicia tabla con la informacion de ventas
    name=fields.Char(string='Clave')
    extraordi=fields.Char(string='Extraordinario')
    bueno=fields.Char(string='Bueno')
    regular=fields.Char(string='Regular')
    malo=fields.Char(string='Malo')


lafox_informacion_ventas()

#Inicia la clase para la fabricacion de los porductos

class lafox_fabrica_producto(models.Model):
    _name ='lafox.fabrica.producto'
    _rec_name ='name_producto'


    #FUNCION para poner por default 1 en el campo num_porciones

    @api.model
    def _default_prociones(self):
        num_porciones = '1'
        return  num_porciones[0]


    # Funcion para poner automaticamente el precio del dolar

    @api.multi
    def _default_dls_cambio(self):
        price1 = 0.0
        prices = self.env['lafox.change.monetary'].search([('id', '=', 1)])
        if prices:
            price1 = prices.price_dolar
        return price1



    #fields para registrar el producto
    
    imagen_producto=fields.Binary(string='Imagen')
    name_producto=fields.Many2one('product.product', string='Nombre del producto', required=False, domain="[('c_t','=','1')]")
    fecha_material=fields.Date(string='Fecha')
    clave_produc =fields.Char(string='Modelo Clave')
    folio=fields.Char(string='Modelo', required=False)
    num_porciones=fields.Char(string='Numero de porciones', default=_default_prociones, readonly=True)
    costo_total=fields.Float(string='Costo total', invisible= False, digits=dp.get_precision('digi'))
    comentarios=fields.Text(string='Comentarios')
    costo_total_dlss=fields.Float(string='Precio final')


    mano_obra = fields.Float(string='Mano de obra MXN')
    tipo_cambio = fields.Float(string='Tipo de cambio US', readonly=False, default=_default_dls_cambio)
    factor = fields.Float(string='Factor')
    cambio = fields.Float(string='Mano de obra USD')
    sobrante = fields.Float(string='Sobrante')

    seguimiento_product=fields.One2many('lafox.seguimiento.producto', 'seguimiento', 'Informacion')

    soli_autorizacion = fields.Boolean(string='Solicitar autorizacion')
    autorizar =fields.Boolean(string='Autorizar')

    dls =fields.Many2one('lafox.change.monetary', string='Cambio')

    
    #Botones para pedir autorizacion y tambien para autorizarlos

    state_pedido = fields.Selection(LAFOX_SOLICITUD_PRODUCTO, string='Estatus', default="BORRADOR")


    @api.multi
    def button_solicitar_pedido (self):
        if self.soli_autorizacion == True:
            self.state_pedido = 'EN PROCESO'

    @api.multi
    def button_aprovar_pedido(self):
        if self.autorizar == True:
            self.state_pedido = 'APROBADO'

    @api.multi
    def button_cancelar_pedido(self):
        if self.autorizar == False:
            self.state_pedido ='CANCELADO'



    #FUNCION para calcular mano de obra / tipo de cambio
    @api.onchange('mano_obra', 'tipo_cambio')
    def _onchange_segui_product(self):
        if self.mano_obra and self.tipo_cambio > 0:
            self.cambio = float(self.mano_obra) / float(self.tipo_cambio)

    #FUNCION para sacar el costo total
    @api.onchange('seguimiento_product', 'cambio')
    def _compute_segui_product(self):
        if self.cambio > 0:
            self.costo_total = sum(cos.costo2 for cos in self.seguimiento_product) + float(self.cambio)


    #FUNCION para obtener el costo total en Dolares
    @api.onchange('costo_total', 'factor', 'seguimiento_product', 'tipo_cambio', 'mano_obra')
    def _onchange_dlss(self):
        self.costo_total_dlss = float(self.costo_total) * float(self.factor)




lafox_fabrica_producto()


class lafox_seguimiento_producto(models.Model):
    _name='lafox.seguimiento.producto'

    #Fields para el seguimiento del producto
    seguimiento=fields.Many2one('lafox.cotizacion', string='Clave')
    id_segui_pro=fields.Char(string='ID')
    pro=fields.Many2one('lafox.cotizacion', string='Producto')
    cantidad=fields.Float(string='Cantidad', required=True)
    cantidad_paquete=fields.Float(string='Piezas por paquete')
    costo_unidad=fields.Float(string='Costo por unidad', digits=dp.get_precision('digi'))
    costo2=fields.Float(string='Resultado', digits=dp.get_precision('digi'))
    pvf =fields.Char(string='PVF')
    ref =fields.Char(string='Referencia')
    
    accesorios = fields.Char(string='Accesorios')
    descrip_pro = fields.Char(string='Descripcion')
    equivalencia = fields.Char(string='Equivalencia')
    unidad2 = fields.Char(string='Unidad')
    sobrante = fields.Char(string='Sobrante')
    pieza_num = fields.Float(string='Piezas', digits=dp.get_precision('digi'))
    sobrante_pro = fields.Float(string='Sobrante')
    lafox_less=fields.Many2one('lafox.less.product', string='Less', invisible=True)

    cantione=fields.One2many('product.product', 'seg_pro', 'cantione', invisible=True )





    #Funcion para calcular el costo 2.0 

    @api.onchange('unidad2')
    def _onchange_cost_dos(self):
        for calcula2 in self:
            if calcula2.unidad2 == 'MT':
                calcula2.equivalencia = '100'
            elif calcula2.unidad2 == 'HILO':
                calcula2.equivalencia = calcula2.cantidad_paquete
            elif calcula2.unidad2 == 'PZ':
                calcula2.equivalencia = 'DIRECTO'
            elif calcula2.unidad2 == 'GR':
                calcula2.equivalencia = 'DIRECTO'


    #Funcion que permite calcular el total del costo

    @api.onchange('cantidad', 'costo_unidad','unidad', 'unidad2', 'equivalencia')
    def _onchange_cost_uno(self):
        for calcula in self:
            if calcula.unidad2 == 'MT':
                calcula.costo2 = float(calcula.costo_unidad) /100 * float(calcula.cantidad)
            elif calcula.unidad2 == 'HILO':
                calcula.costo2 = float(calcula.costo_unidad) / float(calcula.cantidad_paquete) * float(calcula.cantidad)
            elif calcula.unidad2 == 'PZ':
                calcula.costo2 = float(calcula.cantidad) * float(calcula.costo_unidad)
            elif calcula.unidad2 == 'GR':
                calcula.costo2 = float(calcula.cantidad) * float(calcula.costo_unidad)


    #FUNCION para obtener automaticamente el precio de un producto al seleccionarlo

    @api.onchange('pro')
    def _onchange_costo(self):
        for pr in self.pro:
            self.costo_unidad = pr.costo_coti
            self.pvf = pr.pvf_coti
            self.descrip_pro = pr.descripcion_coti
            self.ref = pr.referencia_coti
            self.unidad2 = pr.unidad
            self.cantidad_paquete = pr.piezas_pa

    #FUNCION para calcular el sobrante de cada producto
    @api.onchange('cantidad')
    def _onchange_sobrante(self):
        for sobra in self:
            self.sobrante_pro = float(sobra.cantidad_paquete) - float(sobra.cantidad)






lafox_seguimiento_producto()




class lafox_less_product(models.Model):
    _name='lafox.less.product'


    #Funcion para poner por default los FIELDS almace_origen


    @api.model
    def _default_almacen(self):
        almacen_origen = self.env['stock.location'].search([('name', '=', "LOCAL PRODUCTOS ACCESORIOS")])
        return almacen_origen[0]

    #Funcion para poner por default los FIELDS almacen_destino

    @api.model
    def _default_almacen_destino(self):
        almacen_destino = self.env['stock.location'].search([('name', '=', "LOCAL PRODUCTOS TERMINADO")])
        return almacen_destino[0]

    
    

    #fields lafox less product
    id_less_product= fields.Char(string='MODELO CLAVE')
    name_less_product= fields.Many2one('lafox.fabrica.producto','Nombre', domain="[('state_pedido', '=', 'APROBADO')]")
    cantidad_less= fields.Float(string='Cantidad', digits=dp.get_precision('digi'))
    unidad_less= fields.Char(string='Unidad')
    costo_total_less = fields.Float(string='Costo total', compute='_compute_less_product', store=True)
    costo_unidad_less = fields.Float(string='Costo/Unidad', digits=dp.get_precision('digi'))
    imagen_less_product= fields.Binary(string='Imagen')
    almacen_origen= fields.Many2one('stock.location', string='Almacen de origen', default=_default_almacen)
    almacen_destino= fields.Many2one('stock.location', string='Almacen de destino', default=_default_almacen_destino)

    lafox_less_product=fields.One2many('lafox.seguimiento.producto', 'lafox_less', 'Informacion')

    # related = fields.Char(related='seguimiento_product.seguimiento.pro', relation='lafox.fabrica.producto', string='Related')


    #FUNCION para mostrar solo los productos que ya esten aprovados

    # @api.multi
    # @api.depends('name_less_product')
    # def _compute_pro_aprovados(self):
    #     name_less_product = self.env['lafox.fabrica.producto'].search([('state_pedido', '=' 'APROBADO')])
    #     return name_less_product[0]


    #FUNCION para llenar los campos

    @api.onchange('name_less_product', 'cantidad_less')
    def _onchage_less(self):
        lines=[]

        for pro_less in self.env['lafox.seguimiento.producto'].search([('seguimiento', '=', self.name_less_product.id)]):
            if self.name_less_product and 'in_context' not in self._context:
                self.lafox_less_product= 0

                for data in pro_less:

                    dic_line={}
                    dic_line['id_segui_pro'] = data.id_segui_pro
                    dic_line['pro'] = data.pro
                    dic_line['accesorios'] = data.accesorios
                    dic_line['descrip_pro'] = data.descrip_pro
                    dic_line['cantidad'] = data.cantidad
                    dic_line['cantidad_paquete'] = data.cantidad_paquete
                    dic_line['equivalencia'] = data.equivalencia
                    dic_line['unidad2'] = data.unidad2
                    dic_line['sobrante_pro'] = data.sobrante_pro
                    dic_line['costo_unidad'] = data.costo_unidad
                    dic_line['costo2'] = data.costo2
                    lines.append(dic_line)

                    self.lafox_less_product=lines





    #FUNCION para agregar la cantidad de producto y piezas por paquete segun la catidad a utilizar

    @api.onchange('cantidad_less')
    def less_cantidad(self):
        for canti in self.lafox_less_product:
            canti.cantidad= float(self.cantidad_less) * float(canti.cantidad)
            # if canti.sobrante.pro < 0:
            #     canti.cantidad_paquete = float(self.cantidad_less) * float(canti.cantidad_paquete)


    #FUNCION para calcular el precio total dependiendo la cantidad de producto

    @api.onchange('cantidad_less')
    def less_tot(self):
        for tot in self.lafox_less_product:
            tot.costo2= float(tot.cantidad) * float(tot.costo_unidad)
            tot.sobrante_pro = float(tot.cantidad_paquete) - float(tot.cantidad)

        #FUNCION para sacar el costo total

    @api.multi
    @api.depends('lafox_less_product')
    def _compute_less_product(self):
        for cost in self.name_less_product:
            self.costo_total_less= float(cost.costo_total_dlss) * float(self.cantidad_less)




    # # FUNICON PARA LA CONFIRMACION DE LOS MOVIMIENTOS
    def _confirmar_movimiento(self, cr, uid, ids, vals_stok_move,context=None):
        print vals_stok_move
        ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
        self.pool.get('stock.move').action_done(cr, uid, ide, context=context)




    #Funcion para restar del inventario los productos utilizados

    @api.multi
    def boton_less(self):
        passed = 0

        # Obtenemos las localizaciones de destino y de origen
        search_id_loc = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / CRUDOS')])
        search_id_loc_pro = self.env['stock.location'].search([('complete_name','ilike',self.almacen_origen.complete_name)])

        # Por cada producto se revisa que haya suficiente en el stock
        for producto in self.lafox_less_product:
            sum_qty = sum(self.env['stock.quant'].search([('location_id','=',self.almacen_origen.id),('product_id', '=',producto.pro.id)]).mapped('qty'))
            # Si algun producto no es suficiente se manda warning
            if producto.lafox_less.cantidad_less > sum_qty:
                raise osv.except_osv(("No es posible realizar esta operación"), ('EL Producto %s no tiene disponible la cantidad mencionada.\n Cantidad a vender: %s Cantidad en stock: %s'%(producto.pro.name,producto.lafox_less.cantidad_less,sum_qty)))
            # De lo conrario se guarda su estatus
            else:
                passed = 1
        # Si cambia el status passed se crean los movimientos para descontar del almacen 
        if passed == 1:
            
            for sell_product in self.lafox_less_product:

                vals_stok_move= {
                    'location_dest_id': search_id_loc[0].id,
                    'location_id': search_id_loc_pro[0].id,
                    'name': str('FV:hh: '+ sell_product.pro.name),
                    'company_id': 1, #por el momento definido
                    'invoice_state': "none",
                    'partially_available': False,
                    'procure_method': "make_to_stock",
                    'product_id': int(sell_product.pro.id),
                    'product_uom': int(sell_product.pro.uom_id.id),
                    #'product_qty': float(tupple_taller.cantidad),
                    'product_uom_qty': float(sell_product.cantidad),
                    'propagate': True,

                    }
                    
                self._confirmar_movimiento(vals_stok_move)

        # Se obtinen los datos de la vista actual
        tabla_crm_lead = self.env['lafox.less.product'].search([('name_less_product','=',self.almacen_destino.complete_name)])

        # #Se obtienen las localizaciones de destino y origen
        search_p = self.env['stock.location'].search([('complete_name','ilike',self.almacen_destino.complete_name)])
        search_id_loc_abas = self.env['stock.location'].search([('complete_name','ilike','Virtual Locations / Procurements')])


        vals_stok_move ={
            'location_dest_id': search_p[0].id,
            'location_id': search_id_loc_abas[0].id,
            'name': str('FV:TERMINADO: '+ self.name_less_product.name_producto.name),
            'company_id': 1, #por el momento definido
            'invoice_state': "none",
            'partially_available': False,
            'procure_method': "make_to_stock",
            'product_id': int(self.name_less_product.name_producto.id),
            'product_uom': int(self.name_less_product.name_producto.uom_id.id),
            #'product_qty': float(tupple_taller.cantidad),
            'product_uom_qty': float(self.cantidad_less),
            'propagate': True,

                }

        self._confirmar_movimiento(vals_stok_move)



lafox_less_product()



class lafox_cotizacion(models.Model):
    _name = 'lafox.cotizacion'
    _rec_name ='modelo'
    

    name= fields.Char(string='Nombre')
    modelo = fields.Char(string='Modelo')
    referencia_coti = fields.Char(string='Referencia')
    piezas_pa =  fields.Char(string='Piezas por paquete')
    costo_coti =fields.Char(string='Costo')
    pvf_coti =fields.Char(string='PVF')
    descripcion_coti = fields.Char(string='Descripcion')
    observaciones_coti = fields.Char(string='Observaciones')
    unidad = fields.Char(string='Unidad')





lafox_cotizacion()

class lafox_carga_coti(models.Model):
    _name= 'lafox.carga.coti'
    _inherit = 'ir.attachment'

    name = fields.Char(string='Nombre del documento')
    type= fields.Char(string='Tipo')


    def asignar_cotizacion(self, cr, uid, ids, context=None):

        # Declaramos la funcion para que borre la base de datos que estaba antes en el sistema
       
        cr.execute("delete from lafox_cotizacion")




        # Declaramos el diccionario para la creación de un partner y obtenemos el archivo que se subio
        vals={}
        attachment_dic = self.pool.get('lafox.carga.coti').read(cr, uid, ids, ['name', 'store_fname', 'datas_fname'], context=context)
        filename = attachment_dic[0]['store_fname']
        datas_fname = attachment_dic[0]['datas_fname']
        file_name, file_extension = os.path.splitext(datas_fname)

        archivo_cargado = ODOO_HOME + '.local/share/Odoo/filestore/' + cr.dbname + '/' + filename
        # Consusmimos el script para el parseo del excel, obteniendo los valores
        datos_coti = cargar_CO(archivo_cargado)
        # Por cada fila del xls creamos un registro con los valores que corresponden a la vista
        for dato in datos_coti:

            vals['modelo'] = dato['MODELO']
            vals['descripcion_coti'] = dato['DESCRIPCION']
            vals['referencia_coti'] = dato['REFERENCIA']
            vals['piezas_pa'] = dato['PIEZAS_PA']
            vals['costo_coti'] = dato['COSTO']
            vals['pvf_coti'] = dato['PVF']
            vals['unidad'] = dato['UNI']

            new_id = self.pool.get('lafox.cotizacion').create(cr,uid, vals, context=context)


lafox_carga_coti()

class lafox_grupo_de_precios(models.Model):
    _name='lafox.grupo.de.precios'
    _rec_name = 'nomenclatura'

    # Fields para lafox_grupo_de_precios
    name = fields.Char(string='Nombre')
    nomenclatura = fields.Char(string='Nomenclatura')
    descuento = fields.Float(string='% Descuento')
    description = fields.Char(string='Descripción')
    afectacion = fields.Boolean(string='Aplica Afectación')

lafox_grupo_de_precios()

class lafox_movimiento_de_grupo(models.Model):
    _name ='lafox.movimiento.de.grupo'

    @api.multi
    def _default_type_albaran_id(self):
        type_alb = self.env['stock.picking.type'].search([('code','=','internal')])
        tp = type_alb[0].id
        return tp

    @api.multi
    def _default_usr_id(self):
        return self.env.user.id

    @api.multi
    @api.depends('product_ids',)
    def _compute_total_mov(self):
        print sum(prod.precio_mov for prod in self.product_ids)
        self.total_movimiento = sum(prod.precio_mov for prod in self.product_ids) 
        # return 1

    @api.multi
    def _default_origen_id(self):
        if 'in_abastecimiento' in self._context:
            search_id_loc_abas = self.env['stock.location'].search([('complete_name','like','Virtual Locations / Procurements')])
            return search_id_loc_abas[0]
        else:
            return False

    @api.multi
    def _default_destino_id(self):
        if 'in_abastecimiento' in self._context:
            search_id_loc = self.env['stock.location'].search(['|',('complete_name','like','Physical Locations / WH / EXISTENCIAS'),('complete_name','like','Ubicaciones físicas / WH / EXISTENCIAS')])

            return search_id_loc[0]
        else:
            return False

    # @api.multi
    # def _default_folio(self):
    #     folio_existente = True

    #     while folio_existente:
    #         folio = self.env['ir.sequence'].next_by_code('lafox.movimiento.de.grupo.folio')
            # res = datetime.strptime(dt, '%Y-%m-%d')
        #     res = fields.datetime.now() - timedelta(hours=6)
        #     print res

        #     new_folio = "MOV-"+str(res.strftime("%d"))+"-"+str(res.strftime("%b"))+"-"+str(res.strftime("%Y"))+"-" +str(folio).zfill(6)
        #     folio_duplicado =self.env['lafox.movimiento.de.grupo'].search([('nomenclatura','=',str(new_folio))])

        #     if not folio_duplicado:
        #         break

        # return new_folio.upper()    

    # Default para obtenr la fecha correcta
    @api.model
    def _default_fecha_6(self):
        res = fields.datetime.now()
        return res

    # create para folio consecutivo
    @api.model
    def create(self, vals):
        folio = self.env['ir.sequence'].next_by_code('lafox.movimiento.de.grupo.folio')

        res = fields.datetime.now() - timedelta(hours=6)

        if 'in_abastecimiento' in self._context:

            new_folio = "MOV-"+str(res.strftime("%d"))+"-"+str(res.strftime("%b"))+"-"+str(res.strftime("%Y"))+"-" +str(folio).zfill(6)
            #folio_duplicado =self.env['lafox.movimiento.de.grupo'].search([('nomenclatura','=',str(new_folio))])

            vals['nomenclatura'] = new_folio
        else:
            new_folio2 = "MOV-"+str(res.strftime("%d"))+"-"+str(res.strftime("%b"))+"-"+str(res.strftime("%Y"))+"-" +str(folio).zfill(6)
            #folio_duplicado =self.env['lafox.movimiento.de.grupo'].search([('nomenclatura','=',str(new_folio2))])

            vals['nomenclatura'] = new_folio2

        return super(lafox_movimiento_de_grupo, self).create(vals)

    #Fields para lafox_movimiento_de_grupo
    nomenclatura = fields.Char(string = 'Folio')
    product_id = fields.Many2one('product.product', string='Producto')
    product_uom_qty = fields.Float(string='Cantidad')
    product_uom = fields.Many2one('product.uom', string='Unidad')
    picking_type_id = fields.Many2one('stock.picking.type', string='Tipo de Albarán', default=_default_type_albaran_id)
    date_expected = fields.Datetime(string='Fecha Prevista')
    location_id = fields.Many2one('stock.location', string='Ubicación de Origen', default=_default_origen_id)
    location_dest_id = fields.Many2one('stock.location', string='Ubicación de Destino', default=_default_destino_id)
    create_date = fields.Datetime(string='Fecha de Creación')
    responsable_id = fields.Many2one('res.users',string='Responsable', default=_default_usr_id)
    total_movimiento =fields.Float(string='Total del movimiento', compute="_compute_total_mov", store='True')
    product_ids = fields.One2many('lafox.productos.para.movimiento','movimiento_id',string='Productos IDS')
    state = fields.Selection(LA_FOX_SELECT_MOV,string='Estado', default='draft')
    referencia = fields.Char(string='Referencia/Observaciones')
    supplier_id = fields.Many2one('res.partner', string='Proveedor')
    fecha = fields.Datetime('Fecha Movimiento', default=_default_fecha_6 )


    # FUNCIONES PARA LAFOX.MOVIMIETO.DE.GRUPO
    # Función que  permite aprobar el movimiento y revisa si la cantidad de producto esta disponible en el stock
    @api.multi
    def button_approve_move2(self):
        for producto in self.product_ids:
            product_move =self.env['stock.quant'].search([('location_id','=',self.location_id.id),('product_id','=',producto.product_id.id)])
            product_move_qty=0
            for qty_pruduct in product_move:
                product_move_qty = product_move_qty + qty_pruduct.qty

            # Si no encuentra producto warning de que no hay producto
            if len(product_move) < 1 and  self.location_id.id != 6:
                raise osv.except_osv(("No es posible realizar esta transacción"), ('EL Producto %s,que quiere transferir no se encuentra disponible en el almacén de origen'% producto.product_id.name))
            # Si hay producto pero es menor, lanza alerte de faltante producto
            elif product_move_qty < self.product_uom_qty and  self.location_id.id != 6:
                raise osv.except_osv(("No es posible realizar esta transacción"),('EL Producto %s que quiere transferir no cuenta con la cantidad necesaria. La cantidad que dese enviar: %s, La cantidad en Stock: %s'% (producto.product_id.name,producto.product_uom_qty,product_move_qty,)))
            # Si hay prodcuto suficiente deja continuar
            else:
                tm = self.total_movimiento = sum(prod.precio_mov for prod in self.product_ids) 
                self.write({'state':'draft', 'total_movimiento':tm})

        if not self.product_ids:
            raise osv.except_osv(("No es posible realizar esta transacción"),('No hay productos para Procesar'))

    # Función que  permite aprobar el movimiento y revisa si la cantidad de producto esta disponible en el stock
    @api.multi
    def button_approve_move3(self):
        for producto in self.product_ids:
            product_move =self.env['stock.quant'].search([('location_id','=',self.location_id.id),('product_id','=',producto.product_id.id)])
            product_move_qty=0
            for qty_pruduct in product_move:
                product_move_qty = product_move_qty + qty_pruduct.qty

            # Si no encuentra producto warning de que no hay producto
            if len(product_move) < 1 and  self.location_id.id != 6:
                raise osv.except_osv(("No es posible realizar esta transacción"), ('EL Producto %s,que quiere transferir no se encuentra disponible en el almacén de origen'% producto.product_id.name))
            # Si hay producto pero es menor, lanza alerte de faltante producto
            elif product_move_qty < self.product_uom_qty and  self.location_id.id != 6:
                raise osv.except_osv(("No es posible realizar esta transacción"),('EL Producto %s que quiere transferir no cuenta con la cantidad necesaria. La cantidad que dese enviar: %s, La cantidad en Stock: %s'% (producto.product_id.name,producto.product_uom_qty,product_move_qty,)))
            # Si hay prodcuto suficiente deja continuar
            else:
                tm = self.total_movimiento = sum(prod.precio_mov for prod in self.product_ids) 
                dic_lista = {}
                dic_lista['product_id'] = producto.product_id.id
                dic_lista['product_uom_qty'] = producto.product_uom_qty
                dic_lista['product_uom'] = producto.product_uom.id
                dic_lista['picking_type_id'] = self.picking_type_id.id
                dic_lista['date'] = datetime.now()
                dic_lista['location_id'] = self.location_id.id
                dic_lista['location_dest_id'] = self.location_dest_id.id
                dic_lista['create_date'] = datetime.now()
                dic_lista['name'] = producto.description
                dic_lista['ids_movimientos'] = self.id
                dic_lista['referencia'] = self.referencia
                self.env['stock.move'].sudo().create(dic_lista)
                self.write({'state':'confirmed', 'total_movimiento':tm})

        if not self.product_ids:
            raise osv.except_osv(("No es posible realizar esta transacción"),('No hay productos para Procesar'))


    def button_process_move(self, cr, uid, ids, vals_stok_move,context=None):

        movimientos_id = self.pool.get('stock.move').search(cr,uid,[('ids_movimientos','=',ids)])
        for movimiento in self.pool.get('stock.move').browse(cr, uid,movimientos_id):
            self.pool.get('stock.move').action_done(cr, uid, movimiento.id, context=context)
        
        vals_crm={}    
        vals_crm['state'] = 'aceptado'
        super(lafox_movimiento_de_grupo, self).write(cr,uid, ids, vals_crm, context=context)


lafox_movimiento_de_grupo()


class lafox_productos_para_movimiento(models.Model):
    _name = 'lafox.productos.para.movimiento'
    _rec_name = 'product_id'

    # @api.onchange('product_id','product_qty','product_uom_qty')
    # def _change_product_id(self):
    #     if self.product_id or self.product_uom_qty != 0:
    #         self.product_uom = self.product_id.uom_id
    #         self.description= 'FV:INT:MOVI: '+self.product_id.name
    #         self.precio_mov = float(self.product_id.lst_price) * float(product_uom_qty)
    #         self.product_uom_qty = float(self.product_id.piezas_x_paquete) * product_qty

    @api.multi
    def _change_product_id(self,product_id,product_qty,product_uom_qty):
        title = 'FV:INT:MOVI: '
        if 'in_abastecimiento' in self._context:
            title = 'FV:INV:ABAST: '
        res = {}
        res['value'] = {}
        if product_id or product_qty != 0:
            print "entro"
            product = self.env['product.product'].browse(product_id)
            res['value']['product_uom'] = product.uom_id
            res['value']['description']= title + product.name
            res['value']['descripcion_product'] = product.clave_prod
            res['value']['product_uom_qty'] = float(product.piezas_x_paquete) * product_qty
            res['value']['precio_mov'] = float(product.lst_price) * float(res['value']['product_uom_qty'])

        return res


    # fields para lafox_productos_para_movimiento
    product_id = fields.Many2one('product.product', string='Producto')
    product_uom_qty = fields.Float(string='Piezas')
    product_qty = fields.Float(string='Cantidad')
    product_uom = fields.Many2one('product.uom', string='Unidad')
    description = fields.Char(string='Descripción')
    movimiento_id =fields.Many2one('lafox.movimiento.de.grupo', string='Movimientos IDs')
    descripcion_product = fields.Char(string='Descripcion')
    precio_mov =fields.Float( string='Precio')

lafox_productos_para_movimiento()

class lafox_devolucion_account(models.Model):
    _name = 'lafox.devolucion.account'

    product_id = fields.Many2one('product.product', string='Producto')
    product_uom_qty = fields.Float(string='Cantidad')
    piezas_qty = fields.Float(string='Piezas')
    description = fields.Char(string='Descripción')
    precio_mov =fields.Float( string='Precio Lista')
    precio_lst =fields.Float( string='Precio Unitario')
    price_unit_false = fields.Float(string='Precio Unitario', digits=dp.get_precision('Product Price'))
    amount = fields.Float(string='Monto', compute='_compute_price_monto',store='True', digits=dp.get_precision('Product Price'))
    account_id = fields.Many2one('account.invoice',string='Account ID')
    uos_id = fields.Many2one('product.uom',string ='uom_id')
    invoice_line_tax_id = fields.Many2many('account.tax','account_dev_line_tax', 'invoice_line_id', 'tax_id', string='Impuestos', domain=[('parent_id', '=', False), '|', ('active', '=', False), ('active', '=', True)])
    check_visible = fields.Boolean(string='Modificar Precio')

    #FIELD PARA REGRESO DE MERCANCIA EN MAL ESTADO
    estado_mer = fields.Boolean(string='Mal estado')
    # Compute que obtiene el total del monto por registro
    @api.multi
    @api.depends('precio_lst','piezas_qty')
    def _compute_price_monto(self):
        for r in self:
            r.amount = float(r.piezas_qty) *float(r.precio_lst)*-1   
    
    # Onchange para modificar precio de lista en devoluciones
    @api.multi
    def _onchage_priceunit(self,product_id,price_unit_false,check_visible,cantidad_producto,context):
        if check_visible == True:
            res = {}
            res['value'] = {}

            # res['value']['quantity']= 1
            res['value']['precio_lst']= price_unit_false
            if cantidad_producto > 0:
                product = self.env['product.product'].browse(product_id)
                res['value']['precio_lst']= float(price_unit_false) / float(product.piezas_x_paquete)
            return res

    # Copiado del proceso para obtner los datos por producto para cadaregistro
    @api.multi
    def product_id_change(self,producto_id, uom_id, qty=0, name='', type='out_invoice',partner_id=False, fposition_id=False, price_unit=False, currency_id=False,company_id=None, check_esp=False, context=False):
        if not partner_id:
            raise except_orm(_('No Partner Defined!'), _("You must first select a partner!"))
        values = {}
        part = self.env['res.partner'].browse(partner_id)
        pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]

        product = self.env['product.product'].browse(producto_id)
        fpos = self.env['account.fiscal.position'].browse(fposition_id)

        if float(product.piezas_x_paquete) <= 0 and producto_id != False:
            raise osv.except_osv(('Error en Operación'), ('Este producto no tiene Número de piezas por paquete, favor de modificar la ficha del producto'))
        values['name'] = product.partner_ref
        if type in ('out_invoice', 'out_refund'):
            account = product.property_account_income or product.categ_id.property_account_income_categ
        else:
            account = product.property_account_expense or product.categ_id.property_account_expense_categ
        account = fpos.map_account(account)
        if account:
            values['account_id'] = account.id

        if producto_id:
            price_unit_des = float(product.lst_price)
            price_unit = float(product.lst_price)/float(product.piezas_x_paquete)

            valor_descuento = float(product.lst_price) - (float(product.lst_price)*float(product.grupo_precios_id.descuento/100))

            if len(part.escala_precios) > 0:
                price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete)) * float(part.escala_precios.factor)
            else:
                price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete))

            print "product.especial_product", product.especial_product

            if len(product.especial_product) > 0:
                var1 = ""
                if not part.escala_precios_esp:
                        raise osv.except_osv(('Error en Operación'), ('Este Cliente no tiene asignado el precio para articulos CF, favor de revisar la ficha del Cliente'))
                for espec in part.escala_precios_esp:
                    if var1 == "":
                        var1 =  str(espec.name.id) 
                    var1 = var1 + "," + str(espec.name.id) 
                    ids = var1.split(',')
                fact = self.env['lafox.grupo.de.precios.esp'].search([('id', 'in', (ids)), ('tipo_escala3', '=', product.especial_product.id)])
                especial2 = fact[0].factor * float(float(product.lst_price))
                price_unit = especial2


            if product.grupo_precios_id.nomenclatura == 'NT' or product.grupo_precios_id.nomenclatura == 'N' or product.grupo_precios_id.nomenclatura == 'U':
                price_unit = (float(product.lst_price)/float(product.piezas_x_paquete))


            if product.grupo_precios_id.nomenclatura != 'E' or product.grupo_precios_id.nomenclatura != 'NT' or product.grupo_precios_id.nomenclatura != 'N' or product.grupo_precios_id.nomenclatura != 'U':
                if product.grupo_precios_id.afectacion == False:
                    price_unit = (float(product.lst_price) - (float(product.lst_price)*float(product.grupo_precios_id.descuento/100))) / float(product.piezas_x_paquete)
                else:
                    price_unit = (float(product.lst_price) - (float(product.lst_price)*float(product.grupo_precios_id.descuento/100)))
                    if len(part.escala_precios) > 0:
                        price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete)) * float(part.escala_precios.factor)
                    else:
                        price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete))

            if product.grupo_precios_id.nomenclatura == 'E':
                fact = self.env['lafox.grupo.de.precios.esp'].search([('descuentos','=', part.escala_precios.descuentos)])
                if not fact:
                    raise osv.except_osv(('Error en Operación'), ('Este Cliente no tiene asignado un valor para Escala de Descuentos '))
                price_unit = (float(product.lst_price)*float(fact[0].factor))
                price_unit_des = (float(product.lst_price)/product.piezas_x_paquete)

            # if product.c_t == '0':
            #     price_unit_des = float(price_unit_des) * 2
                # price_unit = float(price_unit) * 2
            
            if check_esp == True and product.precio_especial != 0:
                price_unit_des = float(product.precio_especial)
                price_unit = float(product.precio_especial)/float(product.piezas_x_paquete)

            if part.moneda_valores != 'D' and product.moneda_prod !='P':
                price_unit_des= price_unit_des * float(pesos.price_dolar)
                price_unit= price_unit * float(pesos.price_dolar)
            # DECLARAMOS LOS VALUES A MOSTRAR
            values['description'] = product.clave_prod
            values['piezas_qty'] = product.piezas_x_paquete
            values['invoice_line_tax_id'] =False

            values['precio_mov'] = price_unit_des
            values['price_unit_false'] = price_unit
            values['precio_lst'] = price_unit

        return {'value': values}

    @api.multi
    def _onchange_cantidad(self, cantidad_producto,product_id,price_unit,partner_id,check_visible,price_unit_false,context):
        product = self.env['product.product'].browse(product_id)
        part = self.env['res.partner'].browse(partner_id)
        pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]

        if part.moneda_valores != 'D' and product.moneda_prod !='P':
            price_unit_des= float(product.list_price) * float(pesos.price_dolar)
        
        else:
            price_unit_des= float(product.list_price)
        
        if product.c_t == '0':
            price_unit_des = float(price_unit_des) * 2

        if check_visible != True:
            res = {}
            res['value'] = {}           

            res['value']['piezas_qty']= float(product.piezas_x_paquete) * float(cantidad_producto)
            res['value']['price_unit_des']= price_unit_des
            res['value']['price_unit_false']= (float(product.piezas_x_paquete)* float(price_unit))
        else:
            res = {}
            res['value'] = {}
            res['value']['precio_lst']= float(price_unit_false) / float(product.piezas_x_paquete)
            res['value']['piezas_qty'] = float(product.piezas_x_paquete) * float(cantidad_producto)

        return res
        
        return res


lafox_devolucion_account()


class lafox_devolucion_credito(models.Model):
    _name='lafox.devolucion.credito'

    # FUNCION PARA OBTENER AL EL TOTAL DEL MOVIMIENTO
    @api.multi
    @api.depends('cliente','devolucion_id')
    def _compute_total_movi(self):
        for data in self:
            data.total_movimientos = sum(line.amount for line in data.devolucion_id)


    # FIELDS PARA lafox_devolucion_credito
    state = fields.Selection(LA_FOX_SELECT_MOV,string='ESTADO', default='draft')
    cliente =  fields.Many2one('res.partner', string='Cliente')
    devolucion_id = fields.One2many('lafox.devolucion.productos','account_id', string='Devoluciones')
    total_movimientos = fields.Float(string='Total', compute='_compute_total_movi', store='True')
    maximo_dev = fields.Float(string='Cantidad Máxima-Devolucion', store='True', invisible= 'True')
    con_venta = fields.Boolean(string='¿Agregar devoluciones a Venta?')
    ventas_id = fields.Many2one('account.invoice', string='Venta', _rec_name='nomenclatura')

    # FUNICON PARA LA CONFIRMACION DE LOS MOVIMIENTOS
    def _create_and_confirm_move(self, cr, uid, ids, vals_stok_move,context=None):
        ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
        self.pool.get('stock.move').action_done(cr, uid, ide, context=context)
        
    @api.multi
    def button_aprove_devo(self):
        # devolver = self.maximo_dev
        for invoice in self.devolucion_id:
            if invoice.estado_mer == True:
                search_id_loc_dev = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / DEVOLUCIONES MAL ESTADO')])
            else:
                search_id_loc_dev = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / DEVOLUCIONES')])
            search_id_loc_abas = self.env['stock.location'].search([('complete_name','ilike','Virtual Locations / Procurements')])

            if self.con_venta == True:
                vals= {
                        'product_id':invoice.product_id.id,
                        'description':invoice.description,
                        'product_uom_qty':invoice.product_uom_qty,
                        'piezas_qty':invoice.piezas_qty,
                        'check_visible':invoice.check_visible,
                        'precio_mov':invoice.precio_mov,
                        'price_unit_false':invoice.price_unit_false,
                        'precio_lst':invoice.precio_lst,
                        'amount':float(invoice.amount)*-1,
                        'estado_mer':invoice.estado_mer,
                        'account_id':self.ventas_id.id,
                }
                self.env['lafox.devolucion.account'].sudo().create(vals)
                self.ventas_id.sudo().write({'devolver':True})
                self.ventas_id.button_reset_taxes()

            vals_move= {
                        'location_dest_id': search_id_loc_dev[0].id,
                        'location_id': search_id_loc_abas[0].id,
                        'name': str('FV:DEV: '+ invoice.product_id.name),
                        'company_id': 1, 
                        'invoice_state': "none",
                        'partially_available': False,
                        'procure_method': "make_to_stock",
                        'product_id': int(invoice.product_id.id),
                        'product_uom': int(invoice.product_id.uom_id.id),
                        'product_uom_qty': float(invoice.piezas_qty),
                        'propagate': True,

                        }
            self._create_and_confirm_move(vals_move)
        self.state = "confirmed"
        return True

lafox_devolucion_credito()


class lafox_devolucion_productos(models.Model):
    _name = 'lafox.devolucion.productos'

    @api.multi
    @api.depends('price_unit','quantity')
    def _compute_price_monto(self):
        for r in self:
            r.monto_pago = float(r.precio_lst) * float(r.price_unit)

     # Onchange para modificar precio de lista en devoluciones
    @api.multi
    def _onchage_priceunit(self,product_id,price_unit_false,check_visible,cantidad_producto,context):
        if check_visible == True:
            res = {}
            res['value'] = {}

            # res['value']['quantity']= 1
            res['value']['precio_lst']= price_unit_false
            if cantidad_producto > 0:
                product = self.env['product.product'].browse(product_id)
                res['value']['precio_lst']= float(price_unit_false) / float(product.piezas_x_paquete)
            return res

    @api.multi
    def _onchange_cantidad(self, cantidad_producto,product_id,price_unit,partner_id,check_visible,price_unit_false,context):
        product = self.env['product.product'].browse(product_id)
        part = self.env['res.partner'].browse(partner_id)
        pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]

        if part.moneda_valores != 'D' and product.moneda_prod !='P':
            price_unit_des= float(product.list_price) * float(pesos.price_dolar)
        
        else:
            price_unit_des= float(product.list_price)
        
        if product.c_t == '0':
            price_unit_des = float(price_unit_des) * 2

        if check_visible != True:
            res = {}
            res['value'] = {}           

            res['value']['piezas_qty']= float(product.piezas_x_paquete) * float(cantidad_producto)
            res['value']['price_unit_des']= price_unit_des
            res['value']['price_unit_false']= (float(product.piezas_x_paquete)* float(price_unit))
        else:
            res = {}
            res['value'] = {}
            res['value']['precio_lst']= float(price_unit_false) / float(product.piezas_x_paquete)
            res['value']['piezas_qty'] = float(product.piezas_x_paquete) * float(cantidad_producto)

        return res

    # Compute que obtiene el total del monto por registro
    @api.multi
    @api.depends('precio_lst','piezas_qty')
    def _compute_price_monto(self):
        for r in self:
            r.amount = float(r.piezas_qty) *float(r.precio_lst)

    product_id = fields.Many2one('product.product', string='Producto')
    product_uom_qty = fields.Float(string='Cantidad')
    piezas_qty = fields.Float(string='Piezas')
    description = fields.Char(string='Descripción')
    precio_mov =fields.Float( string='Precio Lista')
    precio_lst =fields.Float( string='Precio Unitario')
    price_unit_false = fields.Float(string='Precio Unitario', digits=dp.get_precision('Product Price'))
    amount = fields.Float(string='Monto', compute='_compute_price_monto', store='True', digits=dp.get_precision('Product Price'))
    account_id = fields.Many2one('lafox.devolucion.credito',string='Account ID')
    uos_id = fields.Many2one('product.uom',string ='uom_id')
    line_id =fields.Many2one('account.invoice.line', string='Lines')
    invoice_line_tax_id = fields.Many2many('account.tax','account_dev_line_tax', 'invoice_line_id', 'tax_id', string='Impuestos', domain=[('parent_id', '=', False), '|', ('active', '=', False), ('active', '=', True)])
    check_visible = fields.Boolean(string='Modificar Precio')
    estado_mer = fields.Boolean(string='Mal estado')
    venta_pro = fields.Char(string= 'Venta')

    # CREACION DE UN NUEVO PRODUCT ONCHANGE PARA EL TIPO DE VENTA EN LA FOX
    @api.multi
    def product_id_change_lf(self,producto_id, uom_id, qty=0, name='',partner_id=False, price_unit=False, context=False):
        if not partner_id:
            raise except_orm(_('No Partner Defined!'), _("You must first select a partner!"))
        values = {}
        part = self.env['res.partner'].browse(partner_id)
        pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]

        product = self.env['product.product'].browse(producto_id)

        if float(product.piezas_x_paquete) <= 0 and producto_id != False:
            raise osv.except_osv(('Error en Operación'), ('Este producto no tiene Número de piezas por paquete, favor de modificar la ficha del producto'))
        values['name'] = product.partner_ref

        if producto_id:
            price_unit_des = float(product.lst_price)
            price_unit = float(product.lst_price)/float(product.piezas_x_paquete)

            valor_descuento = float(product.lst_price) - (float(product.lst_price)*float(product.grupo_precios_id.descuento/100))            

            if len(part.escala_precios) > 0:
                price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete)) * float(part.escala_precios.factor)
            else:
                price_unit =  (float(valor_descuento)/float(product.piezas_x_paquete))

            print "price_unit", price_unit


            if product.grupo_precios_id.nomenclatura == 'NT' or product.grupo_precios_id.nomenclatura == 'N' or product.grupo_precios_id.nomenclatura == 'U':
                price_unit = (float(product.lst_price)/float(product.piezas_x_paquete))


            if product.grupo_precios_id.nomenclatura != 'E' or product.grupo_precios_id.nomenclatura != 'NT' or product.grupo_precios_id.nomenclatura != 'N' or product.grupo_precios_id.nomenclatura != 'U':
                if product.grupo_precios_id.afectacion == False:
                    price_unit = (float(product.lst_price) - (float(product.lst_price)*float(product.grupo_precios_id.descuento/100))) / float(product.piezas_x_paquete)

            print product.grupo_precios_id.nomenclatura
            print "product.grupo_precios_id.nomenclatura"
            
            if product.grupo_precios_id.nomenclatura == 'E':
                print "Entra"
                print product.grupo_precios_id.nomenclatura
                fact = self.env['lafox.grupo.de.precios.esp'].search([('descuentos','=', part.escala_precios.descuentos)])
                if not fact:
                    raise osv.except_osv(('Error en Operación'), ('Este Cliente no tiene asignado un valor para Escala de Descuentos '))
                price_unit = (float(product.lst_price)*float(fact[0].factor))
                price_unit_des = (float(product.lst_price)/product.piezas_x_paquete)
            

            if len(product.especial_product) > 0:
                var1 = ""
                if not part.escala_precios_esp:
                        raise osv.except_osv(('Error en Operación'), ('Este Cliente no tiene asignado el precio para articulos CF, favor de revisar la ficha del Cliente'))
                for espec in part.escala_precios_esp:
                    if var1 == "":
                        var1 =  str(espec.name.id) 
                    if espec.name.id != False:
                        var1 = var1 + "," + str(espec.name.id) 
                    ids = var1.split(',')
                fact = self.env['lafox.grupo.de.precios.esp'].search([('id', 'in', (ids)), ('tipo_escala3', '=', product.especial_product.id)])
                if not fact:
                    raise osv.except_osv(('Error en Operación'), ('Este Cliente no tiene asignado el precio para este articulo CF, favor de revisar la ficha del Cliente'))
                especial2 = fact[0].factor * float(float(product.lst_price))
                price_unit = especial2

            # if product.c_t == '0':
            #     price_unit_des = float(price_unit_des) * float(part.escala_precios.factor)
            #     # price_unit = float(price_unit) * 2

            # if check_esp == True and product.precio_especial != 0:
            #     price_unit_des = float(product.precio_especial)
            #     price_unit = float(product.precio_especial)/float(product.piezas_x_paquete)

            if part.moneda_valores != 'D' and product.moneda_prod !='P':
                price_unit_des= price_unit_des * float(pesos.price_dolar)
                price_unit= price_unit * float(pesos.price_dolar)
            
            # DECLARAMOS LOS VALUES A MOSTRAR
            values['description'] = product.clave_prod
            values['piezas_qty'] = product.piezas_x_paquete
            values['invoice_line_tax_id'] =False

            values['precio_mov'] = price_unit_des
            values['price_unit_false'] = price_unit
            values['precio_lst'] = price_unit

        return {'value': values}

lafox_devolucion_productos()

class lafox_grupo_de_precios_esp(models.Model):
    _name='lafox.grupo.de.precios.esp'
    _rec_name='escala'

    escala=fields.Char(string='Escala')
    descuentos=fields.Char(string='Descuento')
    factor=fields.Float(string='Factor',digits=dp.get_precision('Account'))
    # tipo_escala = fields.Char(string='Tipo de Escala')
    tipo_escala2 = fields.Many2one('lafox.precios.cf', string='Tipo de escala')
    tipo_escala3 = fields.Many2one('lafox.especiales', string='Tipo de escala')
    

lafox_grupo_de_precios_esp()

class lafox_precios_cf(models.Model):
    _name = 'lafox.precios.cf'

    name=fields.Many2one('lafox.grupo.de.precios.esp', string='Escala Precio Especial')
    escala=fields.Char(string='Escala')
    descuentos=fields.Char(string='Descuento')
    factor=fields.Float(string='Factor',digits=dp.get_precision('Account'))
    precio_esp = fields.Many2one('res.partner', string='escala_especial')

    @api.multi
    @api.onchange('name')
    def _onchange_precio_esp(self):
        for esp in self.name:
            self.factor = esp.factor


lafox_precios_cf()

class lafox_especiales(models.Model):
    _name = 'lafox.especiales'

    name= fields.Char(string='Escala Precio Especial')

lafox_especiales()

class lafox_precio_temporada(models.Model):
    _name = 'lafox.precio.temporada'

    name= fields.Char(string='Temporada')
    precio_tem = fields.Float(string='Precio de la temporada')
    des_temporada = fields.Char(string='Descripción')
    des_alamacen = fields.Many2many('stock.location','complete_name', string='Almacen con descuento')
    date_temporada = fields.Datetime(string='Fecha de inicio')
    dete_temp_fin =fields.Datetime(string='Fecha de termino')

lafox_precio_temporada()

class lafox_autorizacion_PE(models.Model):
    _name = 'lafox.autorizacion.pe'

    # FIELDS PARA lafox_autorizacion_PE
    user_id = fields.Many2one('hr.employee', string='Usuario')
    password = fields.Char('Contraseña')


    # FUNCION PARA ACTIVAR LOS PRECIOS ESP
    @api.multi
    def button_approve_precio_esp(self):
        print self.user_id
        print self.password

        user = self.env['hr.employee'].search([('id','=',self.user_id.id),('password_account','=',self.password)])
        if not user:
            raise osv.except_osv(("¡Error de Autenticación!"),('El usuario y/o Contraseña ingresado no son validos'))
        else:
            class_obj = self.env['account.invoice'].browse(self._context.get('active_id'))
            class_obj.sudo().write({'check_visible': True})
            pass

lafox_autorizacion_PE()


class lafox_new_product(models.Model):
    _name = 'lafox.new.product'


    # FIELDS PARA LA CREACION DE UN NUEVO PRODUCTO

    name= fields.Char(string='Nombre producto nuevo')
    new_clave = fields.Char(string='Clave del producto nuevo')
    piezas_tot = fields.Float(string='Total de piezas en almacen', compute= 'compute_total_piezas', store= True)
    pz_a_usar = fields.Float(string='Piezas para cambio')
    ubicacion = fields.Many2one('stock.location', string='Ubicacion')


    @api.multi
    @api.depends('ubicacion')
    def compute_total_piezas(self):
        class_obj = self.env['product.product'].browse(self._context.get('active_id'))
        print class_obj.name
        for producto in class_obj:
            sum_pro = sum(self.env['stock.quant'].search([('location_id', '=', self.ubicacion.id),('product_id', '=', producto.id)]).mapped('qty'))
            self.piezas_tot = float(sum_pro)
        print self.piezas_tot

    # FUNICON PARA LA CONFIRMACION DE LOS MOVIMIENTOS
    def _create_and_confirm_move(self, cr, uid, ids, vals_stok_move,context=None):
        print vals_stok_move
        ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
        self.pool.get('stock.move').action_done(cr, uid, ide, context=context)


    @api.multi
    def button_new_product(self):
        class_obj = self.env['product.product'].browse(self._context.get('active_id'))

        if self.pz_a_usar > self.piezas_tot:
            raise osv.except_osv(("No es posible crear este nuevo producto"),("El producto seleccionado, no tiene las piezas suficientes"))
        if not self.ubicacion:
            raise osv.except_osv(("No es posible realizar este movimiento"),("Por favor seleccione un almacen"))

        # Obtenemos los dos stock entre los que se hará el movimiento, de abastecimiento virtual --> stock WH
        #search_id_loc = self.pool.get('stock.location').search(cr, uid, [('complete_name','ilike','Ubicaciones físicas / WH / Existencias')], context=context)
        search_id_loc = self.env['stock.location'].search([('complete_name','ilike',self.ubicacion.complete_name)])
        search_id_loc_new = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / TRANS PRODUCT')])

        # search_loc_wh = self.env['stock.location'].search([('complete_name','ilike','Physical Locations / WH / Stock')])
        search_loc_wh = self.env['stock.location'].search(['|',('complete_name','like','Physical Locations / WH / EXISTENCIAS'),('complete_name','like','Ubicaciones físicas / WH / EXISTENCIAS')])
        search_id_loc_abas = self.env['stock.location'].search([('complete_name','ilike','Virtual Locations / Procurements')])
        # Por cada producto se realiza el movimiento correspondiente
        vals_stok_move= {
                        'location_dest_id': search_id_loc_new[0].id, #12, ## por el  momento ira definido
                        'location_id': search_id_loc[0].id, #6, ## por el  momento ira definido
                        'name': str('FV:TRANS:PRODUCT: '+ class_obj.name),
                        'company_id': 1, #por el momento definido
                        'invoice_state': "none",
                        'partially_available': False,
                        'procure_method': "make_to_stock",
                        'product_id': int(class_obj.id),
                        'product_uom': int(class_obj.uom_id.id),
                        # 'product_qty': float(move.cantidad),
                        'product_uom_qty': float(self.pz_a_usar),
                        'propagate': True,
                    }
        # ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
        self._create_and_confirm_move(vals_stok_move)

        vals={}

        vals['clave_prod'] = self.name
        vals['name'] = self.new_clave
        vals['piezas_x_paquete'] = class_obj.piezas_x_paquete
        vals['list_price'] = class_obj.list_price
        vals['grupo_precios_id'] = class_obj.grupo_precios_id.id
        vals['c_t'] = class_obj.c_t
        vals['moneda_prod'] = class_obj.moneda_prod
        vals['unidad_product'] = class_obj.unidad_product
        vals['cantidad_vendidos'] = class_obj.cantidad_vendidos.id


        product_buscar = self.env['product.product'].search([('clave_prod', '=', self.name)])
        if not product_buscar:
            # new_id = self.pool.get('product.product').create(cr,uid,vals, context=context)
            id_trans = self.env['product.product'].sudo().create(vals)


        vals_stok_move= {
                        'location_dest_id': search_loc_wh[0].id, #12, ## por el  momento ira definido
                        'location_id': search_id_loc_abas[0].id, #6, ## por el  momento ira definido
                        'name': str('FV:INV:ABAST: '+ class_obj.name),
                        'company_id': 1, #por el momento definido
                        'invoice_state': "none",
                        'partially_available': False,
                        'procure_method': "make_to_stock",
                        'product_id': int(id_trans),
                        'product_uom': int(class_obj.uom_id.id),
                        # 'product_qty': float(move.cantidad),
                        'product_uom_qty': float(self.pz_a_usar),
                        'propagate': True,
                    }
        # ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
        self._create_and_confirm_move(vals_stok_move)
        return True


lafox_new_product()


class lafox_eliminar_productos(models.Model):
    _name= 'lafox.eliminar.productos'
    _inherit = 'ir.attachment'

    name = fields.Char(string='Nombre del documento')
    type= fields.Char(string='Tipo')


    def asignar_delete(self, cr, uid, ids, context=None):



        # Declaramos el diccionario para la creación de un partner y obtenemos el archivo que se subio
        vals={}
        attachment_dic = self.pool.get('lafox.eliminar.productos').read(cr, uid, ids, ['name', 'store_fname', 'datas_fname'], context=context)
        filename = attachment_dic[0]['store_fname']
        datas_fname = attachment_dic[0]['datas_fname']
        file_name, file_extension = os.path.splitext(datas_fname)

        archivo_cargado = ODOO_HOME + '.local/share/Odoo/filestore/' + cr.dbname + '/' + filename
        # Consusmimos el script para el parseo del excel, obteniendo los valores
        datos_eliminar = cargar_delete(archivo_cargado)
        # Por cada fila del xls creamos un registro con los valores que corresponden a la vista
        for dato in datos_eliminar:
            pro = dato['NAME']
            print isinstance(dato['NAME'], float)
            if isinstance(dato['NAME'], float) == True:
                pro = int(dato['NAME'])

            registros = self.pool.get('product.product').search(cr,uid,[('name_template', '=', pro)])
            print  "-----------"
            print registros
            for reg in registros:
                print reg
                bus_move = self.pool.get('stock.move').search(cr,uid,[('product_id', '=', reg)])
                for move in bus_move:
                    vals ={
                       'product_uom_qty':0,
                    }
                    print move
                    self.pool.get('stock.move').write(cr,uid, move,vals)
                # delete_move = self.pool.get('stock.move').unlink(cr,uid, bus_move, context=context)

                bus_products = self.pool.get('stock.quant').search(cr,uid,[('product_id', '=', reg)])
                print "bus_products",bus_products
                for products_m in bus_products:
                    vals ={
                       'qty':0,
                    }
                    self.pool.get('stock.quant').write(cr,uid, products_m,vals)
                # delete_id = self.pool.get('stock.quant').unlink(cr,uid, bus_products, context=context)


lafox_eliminar_productos()

class lafox_abonos(models.Model):
    _name='lafox.abonos'

    @api.model
    def _default_date(self):
        res = fields.datetime.now()
        return res

    name= fields.Many2one('res.partner', string='cliente')
    monto_abono = fields.Float(string='Monto')
    # fecha_abono = fields.Datetime(string='Fecha', default=_default_date)
    # notas_abono = fields.Char(string='Comentarios')
    abonos_many = fields.One2many('lafox.notes.credito', 'abonos_ids', 'Informacion')


    @api.onchange('name')
    def _onchange_client_abono(self):
        lines= []
        for abonos_cliente in self.env['account.invoice'].search([('partner_id', '=', self.name.id)]):

            for pagos in abonos_cliente:
                if pagos.check_credito == True:

                    dic_line={}
                    dic_line['name'] = pagos.nomenclatura
                    dic_line['total_nota'] = pagos.amount_total
                    dic_line['total_adeudo'] = pagos.saldo_credito
                    dic_line['account_id'] = pagos.id
                    lines.append(dic_line)

            self.abonos_many=lines
                    
lafox_abonos()


class lafox_notes_credito(models.Model):
    _name = 'lafox.notes.credito'

    name = fields.Char(string='Nota')
    total_nota = fields.Float(string='Monto total')
    total_adeudo = fields.Float(string='Saldo pendiente')
    account_id = fields.Many2one('account.invoice', string='Venta ID')

    # Field para Many2one a lafox_abonos
    abonos_ids = fields.Many2one('lafox.abonos', string="abonos_ids")

lafox_notes_credito()


class lafox_resumen_abonos(models.Model):
    _name = 'lafox.resumen.abonos'


     # Función para realizar abono a una nota con pago a credito
    @api.multi
    def action_paid_venta_abono(self):
        class_obj = self.env['account.invoice'].browse(self._context.get('active_id'))
        abono = (self.monto_credito - self.name)
        if abono <= 0:
            abono = 0
            class_obj.sudo().write({'saldo_credito': abono,'state_ac': 'paid', 'state': 'paid'})

        sum_abonos = 0
        for abonos in self.env['lafox.resumen.abonos'].search([('invoice_id', '=', class_obj.id)]):
                sum_abonos = float(sum_abonos) + float(abonos.name)
        tot_abonos = sum_abonos + self.name

        class_obj.sudo().write({'saldo_credito': abono, 'saldo_abonado': tot_abonos})

        self.invoice_id = class_obj.id

    # Función que nos permite obtner el monto de credito en una venta

    @api.one
    @api.depends('date_abono','write_date')
    def _saldo_credito_venta(self):

        for invoice in self:
            sum_abonos =0

            class_obj = self.env['account.invoice'].browse(self._context.get('active_id'))
            for abonos in self.env['lafox.resumen.abonos'].search([('invoice_id', '=', class_obj.id)]):
                sum_abonos = float(sum_abonos) + float(abonos.name)

            invoice.monto_credito = float(class_obj.amount_total) - float(sum_abonos)

    @api.model
    def create(self,values):
        record = super(lafox_resumen_abonos, self).create(values)

        class_obj = self.env['account.invoice'].browse(self._context.get('active_id'))
        class_obj._saldo_credito_venta()
        return record




    # Funcion para obtener el total de cambio a devolver
    @api.multi
    def _on_change_monto_cambio(self,monto_credito,name):
        dic = {}
        cambio = name - monto_credito
        if (name == 0 or name == False) or monto_credito > name:
            cambio = 0
        # self.cambio_devuelto = cambio
        dic['value']={
            'cambio_devuelto': cambio
            }
        return dic


    @api.model
    def _default_date(self):
        res = fields.datetime.now()
        return res

    name = fields.Float(string='Abono')
    date_abono = fields.Datetime(string='Fecha abono', default=_default_date)
    monto_credito = fields.Float(string='Monto a credito', compute='_saldo_credito_venta', store= True)
    cambio_devuelto = fields.Float(string="Cambio")
    coment_abono = fields.Text(string='Comentarios')
    invoice_id = fields.Many2one('account.invoice', string='invoice id')

lafox_resumen_abonos()

class lafox_reporte_cliente(models.Model):

    _name= 'lafox.reporte.cliente'


    # FIELDS PARA lafox.reporte.cliente

    name= fields.Many2one('res.partner', string='Cliente')
    state_credito = fields.Selection(LAFOX_CREDITO, string='Venta')
    total_ventas = fields.Float(string='Total ventas')
    total_credito = fields.Float(string='Total credito')
    total_abonos = fields.Float(string='Total abonos')
    saldo_faltante = fields.Float(string='Saldo pendiente')

    registro_one2many = fields.One2many('lafox.reporte.cliente', 'registro_many2one', string='Registros')
    registro_many2one = fields.Many2one('lafox.reporte.cliente', string='Registros 2')


    #Fields para reporte
    folio_venta = fields.Char(string='Folio Venta')
    cliente_report = fields.Char(string='Cliente')
    fecha_venta_r = fields.Char(string='Fecha venta')
    estatus_r =fields.Selection(ACCOUNT_STATE,string='Estatus')
    producto_venta = fields.Char(string='Producto')
    clave_pro_report = fields.Char(string='Credito/Efectivo')
    total_report = fields.Float(string='Total')


    @api.multi
    def _llenado_reporte_venta(self,name,context):
        lines=[]
        dicct={}
        date= 0
        datas = 0
        credit = 0

        # REPORTE DE VENTAS CON FILTRO POR CLIENTE 
        for date_range in self.env['account.invoice'].search([('partner_id','=',name)]):
            dic_line = {}
            if date_range.tipo_producto == '0':
                ct = 'ACCESORIOS'
            else:
                ct = 'TERMINADO'


            total_v = date_range.amount_total

            if date_range.partner_id.moneda_valores == 'D':
                pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]
                total_v = total_v * pesos.price_dolar

            if date_range.state == 'cancel':
                    total_v  = 0

            if date_range.check_credito == True:
                c_ter = 'CREDITO'
                credit = credit + total_v
            else:
                c_ter = 'EFECTIVO'

            dic_line['folio_venta'] = date_range.nomenclatura
            dic_line['cliente_report'] = date_range.partner_id.name
            dic_line['fecha_venta_r'] = date_range.fecha_venta
            dic_line['estatus_r'] = date_range.state
            dic_line['producto_venta']=ct
            dic_line['clave_pro_report'] = c_ter
            dic_line['total_report'] = total_v
            lines.append(dic_line)
            date = date + 1
            datas = datas + total_v

        pendiente = 0
        tot_abonos = 0
        for date_range in self.env['account.invoice'].search([('partner_id','=',name), ('check_credito', '=', True)]):
            for abonoss in self.env['lafox.resumen.abonos'].search([('invoice_id', '=', date_range.id)]):

                dic_line = {}
                if date_range.tipo_producto == '0':
                    ct = 'ACCESORIOS'
                else:
                    ct = 'TERMINADO'

                if date_range.check_credito == True:
                    c_ter = 'CREDITO'
                else:
                    c_ter = 'EFECTIVO'

                total_v = abonoss.name

                if date_range.partner_id.moneda_valores == 'D':
                    pesos = self.env['lafox.change.monetary'].search([('id', '=', 1)])[0]
                    total_v = total_v * pesos.price_dolar

                if date_range.state == 'cancel':
                    total_v  = 0

                dic_line['folio_venta'] = date_range.nomenclatura
                dic_line['cliente_report'] = date_range.partner_id.name
                dic_line['fecha_venta_r'] = abonoss.date_abono
                dic_line['estatus_r'] = date_range.state
                dic_line['producto_venta']=False
                dic_line['clave_pro_report'] = 'ABONO'
                dic_line['total_report'] = total_v
                lines.append(dic_line)
                tot_abonos = tot_abonos + total_v

            pendiente = credit - tot_abonos
        dicct['value']={'registro_one2many':lines, 'total_ventas': datas, 'total_abonos': tot_abonos, 'total_credito': credit, 'saldo_faltante': pendiente}
        return dicct



lafox_reporte_cliente()