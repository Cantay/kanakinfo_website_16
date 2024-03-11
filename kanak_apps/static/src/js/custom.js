odoo.define('my_module.DownloadApps', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.MyDownloadApps = publicWidget.Widget.extend({
    selector: '.js_apps_download',
    template: 'MyModule.DownloadApps',
    events: {
        'click .submit-download': 'onSubmitDownload',
    },
    init: function(){
        this.formSubmitted = false;
        return this._super.apply(this, arguments);
    },
    start: function(){
        return this._super.apply(this, arguments);
    },
    onSubmitDownload: function(ev){
        if (this.formSubmitted) {
            return;
        }
        this.formSubmitted = true;
        this.$('.spinner').show();
        this.$('#download_apps_form').submit();
    }
});

return publicWidget.registry.MyDownloadApps;

});

<!-- MyModule.DownloadApps template -->
<template id="MyModule.DownloadApps" name="My Module Download Apps">
    <form id="download_apps_form" method="POST" action="/download_apps">
        <button class="btn btn-primary submit-download">Download Apps</button>
        <div class="spinner" style="display: none;">
            <i class="fa fa-spinner fa-spin"></i>
        </div>
    </form>
</template>
