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

class res_company(models.Model):
    _name = 'res.company'
    _inherit="res.company"

    # FIELDS PARA FACTURACION
    logo_emisor = fields.Char(string='Logo')
    usr_proveedor = fields.Char(string='Usuario de Rfacil', help='Usuario de Rfacil para poder facturar con esta Razón Social')
    psw_proveedor = fields.Char(string='Password de Rfacil', help='Contraseña de Rfacil para poder facturar con esta Razón Social')
    rfc = fields.Char(string='RFC', index=True)
    fiscal_name = fields.Char(string='Nombre Fiscal',help='Nombre Fiscal', size=64, required=True, index=True)
    cer = fields.Binary(string='Certificate File', filters='*.cer,*.certificate,*.cert', required=True, help='This file .cer is proportionate by the SAT')
    key = fields.Binary(string='Certificate Key File', filters='*.key', required=True, help='This file .key is proportionate by the SAT')
    jpassword = fields.Char(string='Certificate Password', size=64, invisible=False, required=True, help='This password is proportionate by the SAT')

res_company()