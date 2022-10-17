# -*- coding: utf-8 -*-
# from odoo import http


# class FacturasElectronicas(http.Controller):
#     @http.route('/facturas_electronicas/facturas_electronicas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/facturas_electronicas/facturas_electronicas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('facturas_electronicas.listing', {
#             'root': '/facturas_electronicas/facturas_electronicas',
#             'objects': http.request.env['facturas_electronicas.facturas_electronicas'].search([]),
#         })

#     @http.route('/facturas_electronicas/facturas_electronicas/objects/<model("facturas_electronicas.facturas_electronicas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('facturas_electronicas.object', {
#             'object': obj
#         })
