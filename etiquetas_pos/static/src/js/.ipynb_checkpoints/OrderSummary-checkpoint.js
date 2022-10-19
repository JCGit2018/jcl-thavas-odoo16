odoo.define('etiquetas_pos.OrderSummaryOverride', function(require) {
    'use strict';
    
    console.log("Custom JavaScript In POS");
    
    const OrderSummary = require('point_of_sale.OrderSummary');
    const Registries = require('point_of_sale.Registries');
    const { float_is_zero } = require('web.utils');
    
    const OrderSummaryOverride = OrderSummary =>
        class extends OrderSummary {
            /**
             * @override
             */
            getTotalWithoutTax() {
                return this.env.pos.format_currency(this.props.order.get_total_without_tax());
            }
        };
    
    OrderSummaryOverride.template = 'OrderSummary';
    
    Registries.Component.extend(OrderSummary, OrderSummaryOverride);

    return OrderSummary;



});