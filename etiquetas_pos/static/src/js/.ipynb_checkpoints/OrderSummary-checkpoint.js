odoo.define('etiquetas_pos.OrderSummaryOverride', function(require) {
    'use strict';
    
    console.log("Custom JavaScript In POS");
    
    const OrderSummary = require('point_of_sale.OrderSummary');
    const Registries = require('point_of_sale.Registries');
    
    const OrderSummaryOverride = OrderSummary =>
        class extends OrderSummary {
            /**
             * @override
             */
            get order() {
               return this.env.pos.get_order()
            }
 
            get subtotal() {
               return this.env.pos.format_currency(this.order ? this.order.get_total_without_tax() : 0);
            }
        };
    
    OrderSummaryOverride.template = 'OrderSummary';
    
    Registries.Component.extend(OrderSummary, OrderSummaryOverride);

    return OrderSummary;



});