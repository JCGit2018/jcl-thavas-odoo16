# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    url_prod = fields.Text('URL produccion',company_dependent=True)
    url_test = fields.Text('URL pruebas',company_dependent=True )
    proveedor_PAC = fields.Selection([('ebi', 'EBI'),('factory','THE FACTORY HKA')], default= 'ebi' ,company_dependent=True)
    en_produccion = fields.Boolean(string='Ambiente Producción', default= False,company_dependent=True)
    datos_transporte_logistica = fields.Boolean(string='Enviar datos Transporte y Logística al PAC', default= False ,company_dependent=True)
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            url_prod = self.env['ir.config_parameter'].sudo().get_param('facturas_electronicas.url_prod'),
            url_test = self.env['ir.config_parameter'].sudo().get_param('facturas_electronicas.url_test'),
            proveedor_PAC = self.env['ir.config_parameter'].sudo().get_param('facturas_electronicas.proveedor_PAC'),
            en_produccion = self.env['ir.config_parameter'].sudo().get_param('facturas_electronicas.en_produccion'),
            datos_transporte_logistica = self.env['ir.config_parameter'].sudo().get_param('facturas_electronicas.datos_transporte_logistica'),           

        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        url_prod = self.url_prod or False
        url_test = self.url_test or False
        proveedor_PAC = self.proveedor_PAC or False
        en_produccion = self.en_produccion or False
        datos_transporte_logistica = self.datos_transporte_logistica or False


        param.set_param('facturas_electronicas.url_prod', url_prod)
        param.set_param('facturas_electronicas.url_test', url_test)
        param.set_param('facturas_electronicas.proveedor_PAC', proveedor_PAC)
        param.set_param('facturas_electronicas.en_produccion', en_produccion)
        param.set_param('facturas_electronicas.datos_transporte_logistica', datos_transporte_logistica)