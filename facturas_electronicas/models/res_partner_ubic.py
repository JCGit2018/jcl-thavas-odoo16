 #-*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


  

class X_distrito(models.Model):
     
    _name = 'x_res.state.distrito'
    _description = 'Distritos Panama'
 
    _rec_name='x_name' 

    x_codigo = fields.Char(string='Codigo Compuesto Provincia-Distrito')
    x_provincia_id = fields.Char('Código Provincia')
    x_display_name = fields.Char(string='Nombre Distrito')
    x_name =  fields.Char(string='Distrito') 
  

class X_corregimiento(models.Model):
     
    _name = 'x_res.state.corregimiento'
    _description = 'Corregimientos Panama'
 
    _rec_name='x_name'
    
    x_codigo = fields.Char(string='Codigo Compuesto Provincia-Distrito-Corregimiento')
    x_distrito_id = fields.Char('Distrito asociado')
    x_display_name = fields.Char(string='Nombre Corregimiento')
    x_name =  fields.Char(string='Corregimiento') 
         