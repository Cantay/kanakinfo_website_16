odoo.define('my_module_name.career_search', function(require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var $ = core.$;

    var QWeb = core.qweb;

    var CareerSearch = core.Class.extend({
        init: function() {
            this._super();
            onMounted(this.initCarousels.bind(this));
            this.initDepartmentSelect();
        },

        initCarousels: function() {
            $('#kanak_11_0_1_002 .owl-carousel').owlCarousel({
                center: false,
                items: 1,
                loop: true,
                margin: 10,
                nav: true,
                dots:false,
                autoplay: true,
                autoplayTimeout: 3000,
                responsive: {
                    600: {
                        items: 3
                    },
                }
            });

            $("#kanak_11_0_1_002 .owl-carousel .owl-prev").html('');
            $("#kanak_11_0_1_002 .owl-carousel .owl-next").html('');

            $('#hire-our-team-mob .owl-carousel').owlCarousel({
                center: false,
                items: 1,
                loop: true,
                margin: 10,
                nav: true,
                autoplay: true,
                autoplayTimeout: 3000,
                responsive: {
                    600: {
                        items: 3
                    },
                }
            });

            $("#hire-our-team-mob .owl-carousel .owl-prev").html('');
            $("#hire-our-team-mob .owl-carousel .
