 #-*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


  

class X_familia(models.Model):
     
    _name = 'x_product.cpbs.familia'
    _description = 'Familia Códigos CPBS'
 
    _rec_name='x_display_name' 

    x_codigo = fields.Char(string='Codigo')
    x_display_name = fields.Char(string='Nombre Familia')
    x_segmento_id = fields.Char('Codigo Segmento asociado')
    x_name =  fields.Char(string='Familia') 
  

class X_segmento(models.Model):
     
    _name = 'x_product.cpbs.segmento'
    _description = 'Segmentos Códigos CPBS'
 
    _rec_name='x_display_name'
    
    x_codigo = fields.Char(string='Codigo')
    x_display_name = fields.Char(string='Nombre Segmento')
    x_name =  fields.Char(string='Segmento') 
         