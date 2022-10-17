 #-*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError, ValidationError

'''
Modelo con las funciones para crear el log de eventos y asignar al CRON

'''  


class revisar(models.Model):
    _inherit = "facturas_electronicas.facturas_electronicas"
    
    def reenvio_masivo(self):
        modelo=self.env['facturas_electronicas.facturas_electronicas']
        registros=modelo.search([])
        numerrores = 0
        for record in registros:
            if (record.resultado == 'error' and record.mensaje != 'El documento está duplicado') or not record.resultado :
                try:
                  record.f_enviar()
                except: 
                   continue
            if record.resultado == 'error':
               numerrores += 1 
        self.env['facturas_electronicas.fe_log'].graba_log('Cron',  'Errores:' + ' ' + str(numerrores), 'Reenvios realizados',datetime.datetime.now())
                
class FE_log(models.Model):
    _name = 'facturas_electronicas.fe_log'
    _description = 'Logs de envio de facturas electrónicas'
    
    
    name = fields.Char(string='Documento',readonly = True)
    mensaje = fields.Char(string='Mensaje',readonly = True)
    estado = fields.Char(string='Estado del envio',readonly = True)
    fecha = fields.Datetime(string='Fecha' ,readonly = True)
    
    def graba_log(self, documento, mensaje, resultado, fecha):
        
        self.create({
            'name': documento,
            'mensaje': mensaje,            
            'estado': resultado if resultado else 'No enviado',
            'fecha': fecha
        })
        
        
