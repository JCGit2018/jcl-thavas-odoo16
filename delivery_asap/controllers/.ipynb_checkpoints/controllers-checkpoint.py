# -*- coding: utf-8 -*-
# from odoo import http


# class DeliveryAsap(http.Controller):
#     @http.route('/delivery_asap/delivery_asap', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/delivery_asap/delivery_asap/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('delivery_asap.listing', {
#             'root': '/delivery_asap/delivery_asap',
#             'objects': http.request.env['delivery_asap.delivery_asap'].search([]),
#         })

#     @http.route('/delivery_asap/delivery_asap/objects/<model("delivery_asap.delivery_asap"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('delivery_asap.object', {
#             'object': obj
#         })
