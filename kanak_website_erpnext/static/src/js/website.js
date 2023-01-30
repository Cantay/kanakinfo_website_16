odoo.define('kanak_website_erpnext.website', function(require) {
    "use strict";
    require('web.dom_ready');


    $('.erpnext-review .owl-carousel').owlCarousel({
        center: true,
        items: 1,
        loop: true,
        margin: 10,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 3
            },
            1000: {
                items: 3
            },
            1200: {
                items: 3
            }

        }
    });

    $(".erpnext-review .owl-carousel .owl-prev").html('');
    $(".erpnext-review .owl-carousel .owl-next").html('');


 

});