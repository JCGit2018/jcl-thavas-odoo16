 #-*- coding: utf-8 -*-
    
from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError, ValidationError
import json


class Infoentrega(models.Model):
    _inherit = "stock.picking"
    
    
   
                                      
    telefonoEntregaAlt = fields.Char(string='Telefono Entrega Alternativo', help= 'Teléfono de contacto adicional, o alterno del local de la entrega. Formatos aceptables 999-9999 ó 9999-9999')

    
    def dict_entrega(self, documento,orden_venta):
        
        entrega=self.env["stock.picking"].search([('origin','=',orden_venta)])
                                          
        result = dict(tipoRucEntrega =  2 if entrega.partner_id.company_type == 'company' else 1,
                      numeroRucEntrega = entrega.partner_id.vat,
                      digitoVerifRucEntrega = entrega.partner_id.digitoVerificadorRUC,
                      #razonSocialEntrega = entrega.partner_id.commercial_company_name,
                      razonSocialEntrega = entrega.partner_id.name,
                      direccionEntrega = entrega.partner_id.contact_address_complete,
                      codigoUbicacionEntrega = entrega.partner_id.codigoUbicacion,
                      corregimientoEntrega =  entrega.partner_id.corregimiento_id.x_name,
                      distritoEntrega = entrega.partner_id.distrito_id.x_name,
                      provinciaEntrega = entrega.partner_id.provincia,
                      #telefonoEntrega =  entrega.partner_id.phone if entrega.partner_id.phone else '',
                      #telefonoEntregaAlt = entrega.telefonoEntregaAlt if entrega.telefonoEntregaAlt else '' 
        )
        
        if entrega.partner_id.phone:
                
            telefono = entrega.partner_id.phone[4 :]  if entrega.partner_id.phone.startswith('+') else entrega.partner_id.phone
            
            result['telefonoEntrega'] = telefono
            
        if entrega.telefonoEntregaAlt:
            
            result['telefonoEntregaAlt'] = entrega.telefonoEntregaAlt
            
        return result
                                   
                                   
                                   
    
class infoLgistica(models.Model):
     
     _inherit = "stock.picking"
                                   
      
     transportista = fields.Many2one(comodel_name ='res.partner', string ="Nombre o Razón social del transportista" ) 
     licVehiculoCarga =	fields.Char(string='Licencia del vehículo de carga',
                                    help= 'Licencia del vehículo de carga debe ser de 6 caracteres' )
                                   
                                            
     infoLogisticaEmisor = 	fields.Text(string='Información de interés con respeto a logística.',
                                        help= 'Información de interés del emisor con respeto a logística')	
     
        
     def dict_logistica(self,documento,orden_venta):
        
        entrega = self.env["stock.picking"].search([('origin','=',orden_venta)])
        
        lineas_entrega = self.env["stock.picking"].search_read([('origin','=',orden_venta)],['move_lines'])
        
        lineas_entrega = lineas_entrega[0]['move_lines']
        cantidad=0
        peso_total = 0
        unidadPesoTotal= 2 #kg ver para convertir en la unidad mayor 
        for line in lineas_entrega:
            item = self.env["stock.move"].search([('id','=', line)])
            cantidad = item.product_qty + cantidad
            peso_total = item.product_id.weight * item.product_qty + peso_total
            
        #validaciones
        '''
        if not entrega.transportista.name:
            #self.env['facturas_electronicas.fe_log'].graba_log(documento, 'Falta asignar transportista  en la nota de entrega', 'Error en validación', datetime.datetime.now())
            #raise ValidationError('Falta asignar transportista  en la nota de entrega')
            return True
        elif  not entrega.licVehiculoCarga: 
            raise ValidationError('Falta registrar la licencia del vehiculo de carga  en la nota de entrega')
        elif len(entrega.licVehiculoCarga) != 6:
            raise ValidationError('La longitud de la Licencia del vehiculo de carga debe ser de 6 caracteres')                       
            
        elif not entrega.transportista.company_type or not entrega.transportista.vat or  not entrega.transportista.digitoVerificadorRUC:
            raise ValidationError('Revise los datos del transportista en el modulo de contactos')
               
        result = dict(#nroVolumenes = int(cantidad) ,
                      #pesoCarga = "{0:.2f}".format(peso_total),
                      #unidadPesoTotal = unidadPesoTotal,
                      #licVehiculoCarga = entrega.licVehiculoCarga,
                      razonSocialTransportista = entrega.transportista.name,
                      tipoRucTransportista = 2 if entrega.transportista.company_type=='company' else 1,
                      rucTransportista = entrega.transportista.vat,
                      digitoVerifRucTransportista = entrega.transportista.digitoVerificadorRUC,
                      #infoLogisticaEmisor =  entrega.infoLogisticaEmisor if entrega.infoLogisticaEmisor else ''
        )
        ''' 
        result = dict()
        result['nroVolumenes'] = int(cantidad)
        result['pesoCarga'] = "{0:.2f}".format(peso_total)
        result['unidadPesoTotal'] = unidadPesoTotal
        if entrega.licVehiculoCarga:
            result['licVehiculoCarga'] = entrega.licVehiculoCarga
        result['razonSocialTransportista'] = entrega.transportista.name
        result['tipoRucTransportista'] = 2 if entrega.transportista.company_type=='company' else 1
        result['rucTransportista'] = entrega.transportista.vat
        result['digitoVerifRucTransportista'] = entrega.transportista.digitoVerificadorRUC
        result['infoLogisticaEmisor'] =  entrega.infoLogisticaEmisor if entrega.infoLogisticaEmisor else ''
        
        return result
                                 
     '''   
     @api.constrains('licVehiculoCarga') #validar en la funcion de envio
     def check_licencia(self):
            if len(self.licVehiculoCarga) != 6:
                raise ValidationError('La longitud de la Licencia del vehiculo de carga debe ser de 6 caracteres')
     '''           