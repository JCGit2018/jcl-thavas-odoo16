# -*- coding: utf-8 -*-

import logging
import datetime

from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class CobroSuscripciones(models.Model):
    _inherit = "sale.subscription"
    
    def _cron_cobro_orden(self, execute = False):
        if not execute:
            print('Nada que Hacer')
            _logger.info('Nada que Hacer')
            return
        subscriptions = self.search([('stage_category', '=', 'progress')])
        current_date = datetime.date.today()
        for subscription in subscriptions:
            fecha = subscription.recurring_next_date or subscription.date_start
            if fecha <= current_date:
                print(subscription.id)
                print(subscription.recurring_next_date)
                print(fecha)
                subscription.genera_orden_pago()
                subscription.increment_period(renew=self.to_renew)
                subscription.set_open()
                self.env.cr.commit()
        print('Ejecucion Completa!!')  
        _logger.info('Ejecucion Completa!!')
        return

    def genera_orden_pago(self, discard_product_ids=False, new_lines_ids=False):
        self.ensure_one()
        payment_token =self.payment_token_id
        values = self._prepare_renewal_order_values(discard_product_ids, new_lines_ids)
        order = self.env['sale.order'].create(values[self.id])
        self.env.cr.commit()
        order.message_post(body=(_("This renewal order has been created from the subscription ") + " <a href=# data-oe-model=sale.subscription data-oe-id=%d>%s</a>" % (self.id, self.display_name)))
        order.order_line._compute_tax_id()
        
        #si hay token procesa el pago, sino aviso de cobro manual

        if payment_token:
            tx = self._do_payment_order(payment_token,order)
            if tx[0].renewal_allowed:
                order.state='sale'
                self.env.cr.commit()
            #tx.renewal_allowed true si esta aprobado
            #si el cobro falla avisar y no confirmar
            #si el pago queda confirmado confirmar la orden tx.renewal_allowed
        return
    
    
    def _do_payment_order(self, payment_token, document):
        tx_obj = self.env['payment.transaction']
        results = []

        for subscription in self:
            #reference = tx_obj._compute_reference(
            #    payment_token.acquirer_id.provider, prefix=subscription.code
            #)   # There is no sub_id field to rely on
            values = {
                'acquirer_id': payment_token.acquirer_id.id,
                'reference': document.name,
                'amount': document.amount_total,
                'currency_id': document.currency_id.id,
                'partner_id': subscription.partner_id.id,
                'token_id': payment_token.id,
                'operation': 'offline',
                #'invoice_ids': [(6, 0, [document.id])],#revisar este campo!!!!
                'callback_model_id': self.env['ir.model']._get_id(subscription._name),
                'callback_res_id': subscription.id,
                'callback_method': '_assign_token',
            }
            tx = tx_obj.create(values)
            tx._send_payment_request()
            self.env.cr.commit()
            results.append(tx)
        return results
        


