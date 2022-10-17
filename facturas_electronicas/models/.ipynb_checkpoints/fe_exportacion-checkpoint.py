 #-*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

'''
Modelo para generar la parte del diccionario de las facturas de exportación requerida para el envio al PAC

'''  


class fe_exportacion(models.Model):
    _inherit = 'account.move'
    
    puertoEmbarque = fields.Char(string = 'Puerto de embarque', help = 'Puerto de embarque de la Mercancia, debe ser mayor a 5 caracteres')
    
    
    
    def dict_exportacion(self, valorfactura):
        result = dict()
        
        
        if self.invoice_incoterm_id :
            result['condicionesEntrega'] = self.invoice_incoterm_id.code
        
        result['monedaOperExportacion'] = self.currency_id.name
        
        if self.currency_id.name !='USD':
            result['tipoDeCambio'] = "{0:.4f}".format(self.currency_id.rate)
            result['montoMonedaExtranjera'] =  "{0:.4f}".format(self.currency_id.rate * valorfactura)
        
        if self.puertoEmbarque:
            result['puertoEmbarque'] = self.puertoEmbarque    
        
        
        return result
 