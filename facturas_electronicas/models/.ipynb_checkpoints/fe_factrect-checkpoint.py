 #-*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError, ValidationError

'''
Modelo para manejar los datos de facturas rectificativas (notas de crédito) y generar la parte del diccionario requerida para el envio al PAC

'''  


class Factrec(models.Model):
    _inherit = "account.move"


    def doc_referenciados_dict(self, POS =False):
        result=[]
        documento=dict()
        if not POS:
            for factura in self.reversed_entry_id:
                if len(factura.user_id)>0:
                   offset = factura.user_id.tz_offset
                else:
                   offset = '-0500'
                documento["fechaEmisionDocFiscalReferenciado"] =  factura.create_date.strftime("%Y-%m-%dT%H:%M:%S") + offset[0:3] + ':' + offset[3:5]
                documento["cufeFEReferenciada"] = factura.cufe
                documento["nroFacturaPapel"] = '' #no se informa por ser factura electronica
                documento['nroFacturaImpFiscal'] = ''
                result.append(documento)
        else:
            my_pos=self.convierte_correl(self.invoice_origin)
            ncpos=self.env['pos.order'].search([('name','=', my_pos)])
               
            if ncpos.user_id:
                   offset = ncpos.user_id.tz_offset
            else:
                   offset = '-0500'
            documento["fechaEmisionDocFiscalReferenciado"] =  ncpos.create_date.strftime("%Y-%m-%dT%H:%M:%S") + offset[0:3] + ':' + offset[3:5]
            documento["cufeFEReferenciada"] = ncpos.account_move.cufe
            result.append(documento)
        return result

    
