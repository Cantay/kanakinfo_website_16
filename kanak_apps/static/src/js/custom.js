odoo.define('kanak_apps.custom', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.DownloadApps = publicWidget.Widget.extend({
    selector: '.js_apps_download',
    events: {
        'click': 'DownloadAPPS'
    },
    init: function(){
        return this._super.apply(this, arguments);
    },
    start: function(){
        return this._super.apply(this, arguments);
    },
    DownloadAPPS: function(ev){
        $("#download_apps_form").submit();
    }
});

});