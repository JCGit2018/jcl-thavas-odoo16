# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import requests
from odoo.exceptions import UserError
import json


class Asap_Picking(models.Model):
    _inherit= "stock.picking"
    type_id = fields.Char()
    personal = fields.Char()
    special_inst = fields.Char(string='Instrucciones')
    vehicle_type = fields.Selection([('bike','Moto'),('car', 'Carro'),('van', 'Van'), ('pickup', 'Pickup'), ('truck', 'Camion')], string='Tipo Vehículo')
    dest_special_inst =  fields.Char(string='Instrucciones especiales en Destino')
    request_later =  fields.Selection([('0','Instantaneo'),('1', 'Programado')], string='Entrega Tardía')
    request_later_time = fields.Datetime(string='Tiempo de Entrega programado')
    asap_status = fields.Char()
    
    def asap_describe_status(self,status):
        result={
                0:"EN_PROGRESO	Orden en curso",
                1:"CANCELADA	Orden cancelada por el customer",
                2:"COMPLETED	Delivered",
                3:"PAYMENT_FAILED	Se entregó el pedido, pero no se pudo realizar el pago",
                4:"UNFULFILLED	Not delivered",
                5:"RETURNED	Pedido devuelto por el cliente",
                6:"CONFIRMED	Order confirmed by the merchant",
                7:"DISPATCHED	Orden recogida por el mensajero",
              100:"ARRIVED	Pedido recibido en destino",
              101:"ON_THE_WAY	El pedido está siendo entregado por el mensajero."
              }
        return result[status]
    
    def asap_check_status(self):
        self.asap_status = ''
        self.asap_status = self.asap_describe_status(self.env['delivery.carrier']._ultimo_estatus_orden(self.carrier_tracking_ref, self.carrier_id.id))
        
        
        
        
    def asap_check_log(self):
        self.env['delivery.carrier']._historico_status_orden(self.carrier_tracking_ref,self.carrier_id.id)