 #-*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError, ValidationError
import json
import zeep
import pytz
    
'''
Modelo para manejar los datos del cliente y generar la parte del diccionario requerida para el envio al PAC

'''    
    
class cliente(models.Model):
    _inherit = "res.partner"
    
    
    tipoClienteFE = fields.Selection([('01', 'Contribuyente'),
                                      ('02', 'Consumidor Final'),
                                      ('03', 'Gobierno'),
                                      ('04', 'Extranjero')], string='Tipo Cliente' ,default='02' )
    digitoVerificadorRUC = fields.Char(string='Digito Verificador RUC')
    codigoUbicacion = fields.Char(string='Codigo de Ubicacion', default = '1-1-1' )
    provincia = fields.Char( default = "1")
    distrito = fields.Char( string = 'Dist', default = "1-1")
    #corregimiento = fields.Char(string='Corregimiento', default = "Bocas del Toro")
    tipoIdentificacion = fields.Selection([('01', 'Pasaporte'),
                                           ('02', 'Número Tributario'),
                                           ('99', 'Otro')], string='Tipo de Identificacion', default="")
    nroIdentificacionExtranjero = fields.Char(string='Nro Identificación Extranjero',default="")
    
    distrito_id = fields.Many2one('x_res.state.distrito', 'Distrito')

    corregimiento_id = fields.Many2one('x_res.state.corregimiento', 'Corregimiento')

    
    def busca_cliente(self, cliente):
        campos_cliente = ['tipoClienteFE',
                          'email',
                          'company_type', #indivdual = natural, compañia es juridica
                          'vat',
                          'digitoVerificadorRUC',
                          'phone',
                          'country_code',
                          'contact_address_complete',
                          "codigoUbicacion",
                          "tipoIdentificacion",
                          "nroIdentificacionExtranjero"]
        return self.env['res.partner'].sudo().search_read([('id','=',cliente)],campos_cliente)[0]
    


    
    def cliente_dict(self, cliente_actual,destino_operacion):
        cliente = self.env['res.partner'].sudo().search([('id','=',cliente_actual)])
        result = dict(tipoClienteFE =  cliente.tipoClienteFE,tipoContribuyente = 2 if cliente.company_type =='company' else 1 , numeroRUC =  cliente.vat)
        
        #se pone numero ruc en 123456 si nose coloca,sólo consumidor final
        if not cliente.vat:
            result['numeroRUC'] =  '123456'

        #se pone cliente si no se coloca nonbre al cliente 
        if cliente.display_name:
           result['razonSocial'] =  cliente.display_name
        else:    
           result['razonSocial'] =  'Cliente'
        
        #se coloca '02' consumidor final si no selecciona tipo de cliente
        if cliente.tipoClienteFE:
           result['tipoClienteFE'] =  cliente.tipoClienteFE
        else:
           result['tipoClienteFE'] =  '02' 
        
        #datos obligatorios para contribuyente
        if cliente.tipoClienteFE=='01' or cliente.tipoClienteFE=='03' :
           result['digitoVerificadorRUC'] = cliente.digitoVerificadorRUC
           #result['razonSocial'] =  cliente.display_name
           result['direccion'] =  cliente.contact_address_complete
           if cliente.codigoUbicacion:
               result['codigoUbicacion'] =  cliente.codigoUbicacion
           else:
               result['codigoUbicacion'] =  '1-1-1'
           if cliente.state_id.name:
               result['provincia'] = cliente.state_id.name
           else:
               result['provincia'] = 'Bocas Del Toro'
           if cliente.corregimiento_id.x_name:     
              result['distrito'] =  cliente.corregimiento_id.x_name
           else:
              result['distrito'] = 'BOCAS DEL TORO'
           if cliente.distrito_id.x_name:    
              result['corregimiento'] = cliente.distrito_id.x_name
           else:
              result['corregimiento'] = 'BOCAS DEL TORO (CABECERA)' 
            
        # clientes del extranjero   
        if cliente.tipoClienteFE == '04':
            #result['razonSocial'] =  cliente.display_name
            result['direccion'] =  cliente.contact_address_complete
            del result['tipoContribuyente'] # El campo tipoContribuyente no debe ser informado   
            del result['numeroRUC']
            if cliente.tipoIdentificacion:
                result['tipoIdentificacion'] = cliente.tipoIdentificacion.strip() 
            result['nroIdentificacionExtranjero'] = cliente.nroIdentificacionExtranjero if cliente.nroIdentificacionExtranjero else ''
            if cliente.tipoIdentificacion =='01':
               result['paisExtranjero']= cliente.country_id.name 
         
        if destino_operacion == '1':
           result['pais'] = "PA"
        else:
           result['pais'] = cliente.country_code #pais el codigo del pais del cliente
         
       # if cliente.phone and cliente.tipoClienteFE != '04' : #no se registra telefono para clientes extarnjeros mo regsitar si el formato es distinto al requerido (usar regex)
                
        #    telefono = cliente.phone[4 :]  if cliente.phone.startswith('+') else cliente.phone
        #    result['telefono1'] = telefono

        if cliente.email :
          result['correoElectronico1'] = cliente.email   

        #print(result)          
        return result

    
    @api.onchange('corregimiento_id')
    def _onchange_corregimiento_id(self):
        if self.corregimiento_id and self.distrito_id  and not  isinstance(self.corregimiento_id, bool)  :
          try:  
            self.codigoUbicacion = self.corregimiento_id.x_codigo
          except:  
            self.codigoUbicacion = '' 
                
    @api.onchange('distrito_id')
    def _onchange_distrito_id(self):
        self.distrito= self.distrito_id.x_codigo
        self.corregimiento_id = False


    @api.onchange('state_id')
    def _onchange_state_id(self):
        self.provincia= self.state_id.code
        self.codigoUbicacion = ''
        self.distrito_id = ''
        self.corregimiento_id = ''

    
class empresa(models.Model):
    _inherit = "res.company"
    
    codigoSucursalEmisor = fields.Char(string='Código Sucursal', help = 'Código Sucursal del emisor')
    tipoSucursal = fields.Selection([('1', 'Detal'), ('2', 'Mayor')], string='Tipo Sucursal', default = '1' )
    tokenEmpresa = fields.Char(string='Token Empresa', help = 'Token EBI')
    tokenPassword = fields.Char(string='Token Password', help = 'Token Password EBI')


    
    def datos_cia(self, id_cia):
         result = self.env['res.company'].sudo().search([('id','=', id_cia)])
         return result   
    
    
    def _company_in_use(self):

        #para saber la compañia en uso del usuario se cambia reuest por self cuando no es controlador
        cia_actual_id = self.env.context['allowed_company_ids']
        
        res = self.env['res.company'].sudo().search([('id','=', cia_actual_id[0])])
        
        return res
