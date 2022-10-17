 #-*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError



class plazos(models.Model):
    _inherit = 'account.payment.term'
    
    tiempoPago = fields.Selection([('1', 'Inmediato'),('2', 'Plazo'),('3', 'Mixto')],string='Clasificación DGI', default='1', help='Clasificación del Plazo de pago de accuerdo a la DGI')

#descuentBonificacion =dict(descDescuento="descuentos", montoDescuento =20)


class totaliza(models.Model):
    _inherit = "facturas_electronicas.facturas_electronicas"
    
    def lista_descuentos_dict(self):
        pass
    

    def lista_plazo_dict(self, toma_fecha):
        result1=[]
        
        #detectar empresa en_uso par evitar error singleton
        empresa_en_uso =  self.env['res.company']._company_in_use()

        
        factura_objeto=self.env['account.move'].sudo().search([('name','=', self.name),('company_id.id','=',empresa_en_uso.id)])
        fecha_vencimiento_factura = factura_objeto.invoice_date_due
        total = self.valorTotal 
        if len(factura_objeto.user_id)>0:
            offset = factura_objeto.user_id.tz_offset
        else:
            offset = '-0500'

        lista_pagos=[]
        if toma_fecha:
            fecha_vencimiento = fecha_vencimiento_factura
            cuota = "{0:.2f}".format(total)
            salida=dict()
            salida['fechaVenceCuota'] = fecha_vencimiento.strftime("%Y-%m-%dT%H:%M:%S") + offset[0:3] + ':' + offset[3:5]
            salida['valorCuota'] = cuota
            result1.append(salida)
        else:
            plazos  = self.env['account.move'].sudo().search([('name','=',self.name),('company_id.id','=',empresa_en_uso.id)]).invoice_payment_term_id.line_ids
            pago_1 = 0
            for plazo in plazos:
                dias = plazo.days
                valor = plazo.value
                salida=dict()
                fecha_vencimiento = factura_objeto.create_date + timedelta(days=dias)
                if  valor == 'balance':
                    cuota = "{0:.2f}".format(total - pago_1)
                elif valor == 'percent':
                    cuota = "{0:.2f}".format(total * (plazo.value_amount/100))
                elif valor == 'fixed' :
                    cuota = "{0:.2f}".format(plazo.value_amount)
                pago_1 = float(cuota)
                salida['fechaVenceCuota'] = fecha_vencimiento.strftime("%Y-%m-%dT%H:%M:%S") + offset[0:3] + ':' + offset[3:5]
                salida['valorCuota'] = cuota
            #salida['infoPagoCuota'] = "Cuota pago" 
                result1.append(salida)
                pago = {"formaPagoFact": "02",
                        "descFormaPago": " ",
                        "valorCuotaPagada": cuota
                       }
                lista_pagos.append(pago)
        result=dict(
        pagoPlazo = result1
        )
        return (result,lista_pagos)
    
    
    def formaPago_dict(self):
        result=dict(
        formaPago=[
        {"formaPagoFact": "02",
        "descFormaPago": " ",
        "valorCuotaPagada": "{0:.2f}".format(self.valorTotal)
        }
        ]
        )
        return result

    def formaPago_Plazo_dict(self, lista_pagos):
        
        lista = []
        if len(lista_pagos) == 0:
           salida = {"formaPagoFact": "02",
        "descFormaPago": " ",
        "valorCuotaPagada": "{0:.2f}".format(self.valorTotal)
        }
        
           lista.append(salida) 
        else:
           lista = lista_pagos
        result=dict(
        formaPago=lista
        )
        return result
    
    
    
    def totales_dict(self):
        
        #detectar empresa en_uso par evitar error singleton
        empresa_en_uso =  self.env['res.company']._company_in_use()

        factura_objeto=self.env['account.move'].sudo().search([('name','=', self.name), ('company_id.id','=',empresa_en_uso.id)])
        
        tiempo_pago = factura_objeto.invoice_payment_term_id.tiempoPago
        fecha_vencimiento = factura_objeto.invoice_date_due
        fecha_factura = factura_objeto.invoice_date
        
        result=dict()
        
        result["totalPrecioNeto"] = "{0:.2f}".format(self.totalPrecioNeto)
        result["totalITBMS"] = "{0:.2f}".format(self.totalITBMS)
        result["totalMontoGravado"] =  "{0:.2f}".format(self.totalITBMS) #se asume ISC cero
        result["totalDescuento"] = "{0:.2f}".format(self.totalDescuento)
        #result["totalAcarreoCobrado"] = ""
        #result["valorSeguroCobrado"] = ""
        result["totalFactura"] = "{0:.2f}".format(self.valorTotal)
        result["totalValorRecibido"] = "{0:.2f}".format(self.valorTotal)
        result["vuelto"] = "0.00"
        result["nroItems"] = self.nroItems
        result["totalTodosItems"] = "{0:.2f}".format(self.totalTodosItems)
        result['listaFormaPago'] = self.formaPago_dict()
        if tiempo_pago:
            result["tiempoPago"] = tiempo_pago
            if tiempo_pago !='1' :
              result['listaPagoPlazo'] = self.lista_plazo_dict(False)[0]
        elif fecha_factura == fecha_vencimiento:
            result["tiempoPago"] = '1'
        elif fecha_factura < fecha_vencimiento:
            result["tiempoPago"] = '2'
            result['listaPagoPlazo'] = self.lista_plazo_dict(True)[0]
        result['listaFormaPago'] = self.formaPago_Plazo_dict(self.lista_plazo_dict(False)[1])    
        if self.totalDescuento: #emitir lista bonificaciones
           result['listaDescBonificacion'] ={'descuentoBonificacion':
                                              [{'descDescuento': 'Descuento',
                                                'montoDescuento' : "{0:.2f}".format(self.totalDescuento)
                                               }]
                                             }                                            
        #   result['']['descDescuento'] = 'Descuento'
        #   result['']['montoDescuento'] = "{0:.2f}".format(self.totalDescuento)
        return result

