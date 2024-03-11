odoo.define('kanak_website_erpnext.erp_website', function(require) {
    "use strict";

    // Import the web dom ready module
    require('web.dom_ready');

    // Import the jQuery library
    const $ = require('jquery');

    // Check if the owlCarousel method is available
    if ($.fn.owlCarousel) {
        // Initialize the owlCarousel method on the selected elements
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
                    items: 1
                },
                1000: {
                    items: 3
                },
                1200: {
                    items: 3
                }
            }
        });
    } else {
        console.error('The owlCarousel method is not available');
    }

    // Leave the prev and next buttons empty
    // $(".erpnext-review .owl-carousel .owl-prev").html('');
    // $(".erpnext-review .owl-carousel .owl-next").html('');

});
