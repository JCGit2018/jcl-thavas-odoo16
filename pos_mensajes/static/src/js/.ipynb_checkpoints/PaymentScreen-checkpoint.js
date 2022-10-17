odoo.define('pos_mensajes.POSValidateOverride', function(require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const POSValidateOverride = PaymentScreen =>
        class extends PaymentScreen {
            /**
             * @override
             */
            async validateOrder(isForceValidate) {
                //console.log('POSValidateOverride::validateOrder(): successfully overridden');
                if (await super._isOrderValid(isForceValidate)){
                 if (!this.currentOrder.is_to_invoice()){   
                 const { confirmed } = await this.showPopup('ConfirmPopup', {
                   title: 'Confirmación de Validación',
                   body: '¿Está seguro de validar sin generar factura?'
                 });
                 if (!confirmed) return;
                 await super.validateOrder(isForceValidate);
                 } 
                 else{
                     await super.validateOrder(isForceValidate);
                     }   
                }    
            }
        };
    Registries.Component.extend(PaymentScreen, POSValidateOverride);

    return PaymentScreen;
});