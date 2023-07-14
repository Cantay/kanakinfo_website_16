odoo.define('kanak_github_connector.github_connector', function (require) {
'use strict';

require('website_sale.website_sale');
var publicWidget = require('web.public.widget');
var core = require('web.core');
var _t = core._t;

publicWidget.registry.WebsiteSale.include({
    onChangeVariant: function (ev) {
        var variant_id = $("input[name='product_id']").val();
        $('#details div[itemprop="description"]').addClass('hidden');
        var $doc_exist = $('div[itemprop="description"][product_id='+ variant_id + ']');
       if ($doc_exist.length > 0) {
            $doc_exist.removeClass('hidden');
       } else {
            $('#details div[itemprop="description"]:first').removeClass('hidden');
       }
        return this._super.apply(this, arguments);
    }
});
});
