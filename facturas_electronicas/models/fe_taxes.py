 #-*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class fe_taxes(models.Model):
    _inherit = 'account.tax'
    
    clasificacion_DGI = fields.Selection([('00', 'ITBMS 0% (exento)'),('01', 'ITBMS 7%'),
                                    ('02', 'ITBMS 10%'),
                                    ('03', 'ITBMS 15%'),
                                    ('04', 'ISC'),
                                    ('05', 'OTI SUME 911'), #codigo 01 OTI
                                    ('06', 'OTI Tasa Portabilidad Numérica'), #codigo 02 OTI
                                    ('07', 'OTI Impuesto sobre seguro')] #codigo 03 OTI
                                         ,string='Clasificación DGI', default='01', help='Clasificación del impuesto de accuerdo a la DGI')
    
    #clasificacion_OTI = fields.Selection([('01', 'SUME 911'),
    #                                ('02', 'Tasa Portabilidad Numérica'),
    #                                ('03', 'Impuesto sobre seguro')], string='Clasificación  OTI', help='Clasificación  OTI (Oros tributos e impuestos)  de accuerdo a la DGI (si aplica el impuesto)', default='01')
    
    def codifica_impuestos(self,valor,tipo):
        codigo=''
        aplica_impuesto = False
        porcentaje = 0.00
        return (codigo, aplica_impuesto, porcentaje)
    
 