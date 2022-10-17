 #-*- coding: utf-8 -*-
    
from odoo import models, fields, api
import datetime
from odoo.exceptions import UserError, ValidationError
import json
import zeep


class itemsFE(models.Model):
    _inherit = "sale.order.line"
    
    descripcion = fields.Char(string='descripcion') #buscar en producto
    codigo = fields.Char(string='codigo')
    unidadMedida = fields.Char(string='unidadMedida') #producto
    cantidad = fields.Char(string='cantidad')
    fechaFabricacion = fields.Date(string='fechaFabricacion') #producto
    fechaCaducidad = fields.Date(string='fechaCaducidad') #producto
    codigoCPBSAbrev = fields.Char(string='codigoCPBSAbrev') #producto
    codigoCPBS = fields.Char(string='codigoCPBS') #producto
    unidadMedidaCPBS = fields.Char(string='unidadMedidaCPBS') #producto
    infoItem = fields.Char(string='infoItem')
    precioUnitario = fields.Char(string='precioUnitario')  #price_unit
    precioUnitarioDescuento = fields.Char(string='precioUnitarioDescuento') #price unit -discount
    precioItem = fields.Char(string='precioItem')
    precioAcarreo = fields.Char(string='precioAcarreo')
    precioSeguro = fields.Char(string='precioSeguro')
    valorTotal = fields.Char(string='valorTotal') #price_total
    codigoGTIN = fields.Char(string='codigoGTIN')
    cantGTINCom = fields.Char(string='cantGTINCom')
    codigoGTINInv = fields.Char(string='codigoGTINInv')
    tasaITBMS = fields.Char(string='tasaITBMS')
    valorITBMS = fields.Char(string='valorITBMS')
    cantGTINComInv = fields.Char(string='cantGTINComInv')
    tasaISC = fields.Float(string='tasaISC', default = 0)
    tasOTI = fields.Char(string='tasOTI' , default = 0)
    valorTasa = fields.Char(string='valorTasa')


        
class productosFE(models.Model):
    _inherit = "product.template"
    
    descripcion = fields.Char(string='descripcion') #buscar en producto
    codigo = fields.Char(string='codigo')
    unidadMedida = fields.Char(string='unidadMedida') #producto
    cantidad = fields.Char(string='cantidad')
    fechaFabricacion = fields.Date(string='fechaFabricacion') #producto
    fechaCaducidad = fields.Date(string='fechaCaducidad') #producto
    codigoCPBSAbrev_aux = fields.Char(string='codigoCPBSAbrev_aux') #producto
    codigoCPBSAbrev = fields.Many2one('x_product.cpbs.segmento', 'CPBS Abrev')
    codigoCPBS_aux = fields.Char(string='codigoCPBS_aux') #producto
    codigoCPBS = fields.Many2one('x_product.cpbs.familia', 'CPBS')
    unidadMedidaCPBS = fields.Char(string='unidadMedidaCPBS') #producto
    infoItem = fields.Char(string='infoItem')
    precioUnitario = fields.Char(string='precioUnitario')  #price_unit
    precioUnitarioDescuento = fields.Char(string='precioUnitarioDescuento') #price unit -discount
    precioItem = fields.Char(string='precioItem')
    precioAcarreo = fields.Char(string='precioAcarreo')
    precioSeguro = fields.Char(string='precioSeguro')
    valorTotal = fields.Char(string='valorTotal') #price_total
    codigoGTIN = fields.Char(string='codigoGTIN')
    cantGTINCom = fields.Char(string='cantGTINCom')
    codigoGTINInv = fields.Char(string='codigoGTINInv')
    tasaITBMS = fields.Char(string='tasaITBMS')
    valorITBMS = fields.Char(string='valorITBMS')
    cantGTINComInv = fields.Char(string='cantGTINComInv')
    tasaISC = fields.Float(string='tasaISC', default = 0) #impuesto selctivo alñ consumo
    tasOTI = fields.Char(string='tasOTI' ,  default = '')
    valorTasa = fields.Float(string='valorTasa', default = 0)
    
    @api.onchange('codigoCPBSAbrev')
    def _onchange_codigoCPBSAbrev(self):
        self.codigoCPBS = ''
        self.codigoCPBSAbrev_aux = self.codigoCPBSAbrev.x_codigo 


        
    @api.onchange('codigoCPBS')    
    def _onchange_codigoCPBS(self):
        self.codigoCPBS_aux = self.codigoCPBS.x_codigo 
        
        
        
        
        
        
        
        
class vehiculo(models.Model):
    _inherit = "product.template"
    
    
    modalidadOperacionVenta = fields.Selection([('01', 'Venta a Representante'),
                                                ('02', 'Venta a consumidor final'),
                                                ('03', 'Venta a Gobierno'),
                                                ('04', 'Venta a Flota de vehiculos'),
                                                ('99', 'Otros') ], string='Tipo Modalidad Operación Ventas')    
    
    modalidadOperacionVentaNoDef = fields.Char(string='modalidadOperacionVentaNoDef' ,  default = '')
    chasis = fields.Char(string='Chasis')
    codigoColor = fields.Char(string='Codigo de Color')
    colorNombre = fields.Char(string='Color')
    potenciaMotor = fields.Char(string='Potencia del Motor')
    capacidadMotor = fields.Char(string='Capacidad del Motor')
    pesoNeto = fields.Char(string='Peso Neto')
    pesoBruto = fields.Char(string='Peso Bruto')
    tipoCombustible = fields.Selection([('01', 'Gasolina'),
                                                ('02', 'Diésel'),
                                                ('03', 'Etanol'),
                                                ('08', 'Eléctrico'),
                                                ('09', 'Gasolina/Eléctrico') ], string='Tipo de Combustible')    
    
    tipoCombustibleNoDef = fields.Char(string='Otro tipo de Combustible')
    numeroMotor = fields.Char(string='numeroMotor'),
    capacidadTraccion = fields.Char(string='capacidadTraccion')
    distanciaEjes = fields.Char(string='distanciaEjes')
    anoModelo = fields.Char(string='anoModelo')
    anoFabricacion = fields.Char(string='anoFabricacion')
    tipoPintura = fields.Selection([('1', 'Solida'),
                                                ('2', 'Metálica'),
                                                ('3', 'Perla'),
                                                ('4', 'Fosca'),
                                                ('9', 'Otra') ], string='Tipo de Pintura')
    tipoPinturaNodef = fields.Char(string='Otro Tipo de Pintura')
    tipoVehiculo = fields.Selection([('1', 'Motocicleta'),
                                                ('2', 'Bus'),
                                                ('3', 'Camión'),
                                                ('4', 'Sedán'),
                                                ('5', 'Camioneta'),
                                                ('6', 'Pickup') ], string='Tipo de Vehiculo')
    
    usoVehiculo = fields.Selection([('1', 'Comercial'),('2', 'Particular')], string='Uso del Vehiculo')
    
    condicionVehiculo = fields.Selection([('1', 'Acabado'),('2', 'Semi-acabado'),('3', 'inacabado')], string='Condicion del Vehiculo')
    capacidadPasajeros = fields.Integer(string='capacidadPasajeros')

    

     
    def dict_vehiculo(self, producto):
         
         vehiculo= dict(modalidadOperacionVenta = producto.modalidadOperacionVenta,
                   modalidadOperacionVentaNoDef = producto.modalidadOperacionVentaNoDef,
                   chasis = producto.chasis,
                   codigoColor = producto.codigoColor,
                   colorNombre =  producto.colorNombre,
                   potenciaMotor = producto.potenciaMotor,
                   capacidadMotor = producto.capacidadMotor,
                   pesoNeto = producto.pesoNeto,
                   pesoBruto = producto.pesoBruto,
                   tipoCombustible = producto.tipoCombustible,
                   tipoCombustibleNoDef = producto.tipoCombustibleNoDef,
                   numeroMotor = producto.numeroMotor,
                   capacidadTraccion = producto.capacidadTraccion,
                   distanciaEjes = producto.distanciaEjes,
                   anoModelo = producto.anoModelo,
                   anoFabricacion = producto.anoFabricacion,
                   tipoPintura = producto.tipoPintura,
                   tipoPinturaNodef = producto.tipoPinturaNodef,
                   tipoVehiculo = producto.tipoVehiculo,
                   usoVehiculo = producto.usoVehiculo,
                   condicionVehiculo = producto.condicionVehiculo,
                   capacidadPasajeros = producto.capacidadPasajeros)   

         return vehiculo
        
    

class medicina(models.Model):
    _inherit = "product.template"
    
    nroLote = fields.Char(string='Número de Lote')
    cantProductosLote = fields.Char(string='Cantidad productos en el Lote')
    
    def dict_medicina(self, producto):
            
         medicina = dict(nroLote = producto.nroLote , cantProductosLote = producto.cantProductosLote) 
         return medicina
     
    
class Lineas_factura(models.Model):
    _inherit = "account.move.line" 
    

    

    def busca_items_factura(self, documento):
        

        #detectar empresa en_uso par evitar error singleton
        empresa_en_uso =  self.env['res.company']._company_in_use()

        
        modeloFe = self.env['facturas_electronicas.facturas_electronicas'].search([('name','=', documento), ('company_id','=',empresa_en_uso.id)])
        
        
        modeloFe.totalPrecioNeto = 0
        modeloFe.nroItems = 0
        modeloFe.totalITBMS = 0
        modeloFe.totalTodosItems = 0
        modeloFe.totalDescuento = 0
        modeloFe.valorTotal = 0
        
        tipo_cliente = self.env['account.move'].sudo().search([('name','=', documento),('company_id.id','=',empresa_en_uso.id)]).partner_id.tipoClienteFE
        
        items = self.env['account.move'].sudo().search_read([('name','=', documento)],['invoice_line_ids'])
        result=[]
        invoice_line = items[0]['invoice_line_ids']
        for lines in invoice_line:
            linea_factura = self.env['account.move.line'].sudo().search([('id','=', lines)])
            linea_factura2  = self.env['account.move.line'].sudo().search_read([('id','=', lines)],['product_id'])

            if len(linea_factura.product_id)>0:
                producto = self.env['product.product'].sudo().search([('id','=', linea_factura2[0]['product_id'][0])])
            else:
                continue  
            if producto.code == 'DISC': #descuentoglobal
                modeloFe.totalDescuento = linea_factura.price_unit * -1 #(valor positivo del descuento)
                modeloFe.valorTotal = modeloFe.valorTotal - modeloFe.totalDescuento
                continue
            #producto = self.env['product.product'].sudo().search([('id','=', linea_factura2[0]['product_id'][0])])
            tipo_producto = producto.categ_id.name
            precioItem1 = linea_factura.quantity * (linea_factura.price_unit - (linea_factura.discount/100) * linea_factura.price_unit)
            precioDescuento = linea_factura.quantity * (linea_factura.discount/100) * linea_factura.price_unit
            valor_impuesto = linea_factura.price_total - linea_factura.price_subtotal
            valorTotal1 = precioItem1 + valor_impuesto 
            modeloFe.valorTotal= valorTotal1 + modeloFe.valorTotal
            salida = dict(descripcion= producto.name,
                          codigo = producto.default_code if producto.default_code else '' ,
                          #unidadMedida = producto.uom_name,
                          cantidad = "{0:.2f}".format(linea_factura.quantity), # ver con product_uom_qty 
                          #fechaFabricacion =  producto.fechaFabricacion if producto.fechaFabricacion else '',
                          #fechaCaducidad =  producto.fechaCaducidad if producto.fechaCaducidad else '',
                          precioUnitario = "{0:.2f}".format(linea_factura.price_unit),
                          precioUnitarioDescuento = "{0:.4f}".format((linea_factura.discount/100) * linea_factura.price_unit),
                          precioItem = "{0:.4f}".format(precioItem1),
                          valorTotal = "{0:.5f}".format(valorTotal1),
                          codigoGTIN = "0",
                          cantGTINCom= "0.00",
                          codigoGTINInv = "0",
                          valorITBMS =  "{0:.2f}".format(valor_impuesto),
                          cantGTINComInv = "0.00"
                          
                         )
            if tipo_cliente == '03':
               salida['codigoCPBSAbrev'] = producto.codigoCPBSAbrev_aux if producto.codigoCPBSAbrev_aux else ''
               salida['codigoCPBS'] = producto.codigoCPBS_aux if producto.codigoCPBS_aux else ''
               
               salida['unidadMedidaCPBS'] = 'und' 

            if len(linea_factura.tax_ids)==0: #si no tiene impuesto se pone como exento
               salida['tasaITBMS'] ='00'    
            else:
               salida['tasaITBMS'] =  linea_factura.tax_ids[0].clasificacion_DGI
           
            #no se contempla en version inicial
            '''
            if tipo_producto == 'Medicinas':
                salida['medicina'] = self.env['product.template'].dict_medicina(producto)
            elif tipo_producto == 'Vehiculos':
                salida['vehiculo'] = self.env['product.template'].dict_vehiculo(producto)
           '''             
            modeloFe.totalPrecioNeto = modeloFe.totalPrecioNeto + precioItem1
            modeloFe.nroItems = modeloFe.nroItems + 1 # lineas_factura
            #modeloFe.totalDescuento = modeloFe.totalDescuento + precioDescuento            
            modeloFe.totalITBMS = modeloFe.totalITBMS + valor_impuesto
            modeloFe.totalTodosItems = modeloFe.totalTodosItems + linea_factura.price_total
            result.append(salida)
            
            #para debug no usar en produccion
            #with open('/home/odoo/src/user/itemfact2.txt', 'w') as temp_file:
            #    temp_file.write("%s\n" % result)    
                
        return result
