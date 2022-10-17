odoo.define('payment_banesco.payment_form', require => {
    'use strict';

    
    const core = require('web.core');
    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');
    
    const _t = core._t;

    const paymentBanescoMixin = {

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Simulate a feedback from a payment provider and redirect the customer to the status page.
         *
         * @override method from payment.payment_form_mixin
         * @private
         * @param {string} provider - The provider of the acquirer
         * @param {number} acquirerId - The id of the acquirer handling the transaction
         * @param {object} processingValues - The processing values of the transaction
         * @return {Promise}
         */
        _processDirectPayment: function (provider, acquirerId, processingValues) {
            if (provider !== 'banesco') {
                return this._super(...arguments);
            }
            /*
            processingValues.numTarjeta = document.getElementById(`banesco_card_${acquirerId}`).value;
            processingValues.expiraMes = document.getElementById(`banesco_month_${acquirerId}`).value;
            processingValues.expiraAno = document.getElementById(`banesco_year_${acquirerId}`).value;
            processingValues.codigoTarjeta = document.getElementById(`banesco_code_${acquirerId}`).value;
            
            processingValues.nombreCliente =  document.getElementById(`banesco_name_${acquirerId}`).value;
            processingValues.codCliente='ClI001';
            processingValues.apellidoCliente = document.getElementById(`banesco_lastname_${acquirerId}`).value;
            processingValues.calle = document.getElementById(`banesco_street_${acquirerId}`).value;
            processingValues.ciudadCliente = document.getElementById(`banesco_city_${acquirerId}`).value;
            processingValues.estadoCliente =document.getElementById(`banesco_state_${acquirerId}`).value; //revisar para obtner el codigo
            processingValues.codPostalCliente = document.getElementById(`banesco_pcode_${acquirerId}`).value;
            processingValues.paisCliente = document.getElementById(`banesco_country_${acquirerId}`).value; //revisar para obtner el codigo
            processingValues.emailCliente = document.getElementById(`banesco_email_${acquirerId}`).value;
            processingValues.telCliente = "4158880000";
            */
            console.log(processingValues);
            /*
            return this._rpc({
                route: '/payment/banesco/payment',
                params: {
                    processingValues,
                },
            }).then(() => {
                window.location = '/payment/banesco/authenticate';
            });*/
            
           let parametros= JSON.stringify(processingValues);
           console.log(parametros);
            
           return window.location = `/payment/banesco/authenticate?response_content=${parametros}` ;
        },

        /**
         * Prepare the inline form of Test for direct payment.
         *
         * @override method from payment.payment_form_mixin
         * @private
         * @param {string} provider - The provider of the selected payment option's acquirer
         * @param {integer} paymentOptionId - The id of the selected payment option
         * @param {string} flow - The online payment flow of the selected payment option
         * @return {Promise}
         */
        _prepareInlineForm: function (provider, paymentOptionId, flow) {
            if (provider !== 'banesco') {
                return this._super(...arguments);
            } else if (flow === 'token') {
                return Promise.resolve();
            }
            this._setPaymentFlow('direct');
            return Promise.resolve()
        },
    };
    checkoutForm.include(paymentBanescoMixin);
    manageForm.include(paymentBanescoMixin);
});
