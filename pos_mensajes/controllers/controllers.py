# -*- coding: utf-8 -*-
# from odoo import http


# class PosMensajes(http.Controller):
#     @http.route('/pos_mensajes/pos_mensajes', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_mensajes/pos_mensajes/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_mensajes.listing', {
#             'root': '/pos_mensajes/pos_mensajes',
#             'objects': http.request.env['pos_mensajes.pos_mensajes'].search([]),
#         })

#     @http.route('/pos_mensajes/pos_mensajes/objects/<model("pos_mensajes.pos_mensajes"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_mensajes.object', {
#             'object': obj
#         })
