odoo.define('kanak_website.career_search', function(require) {
    "use strict";
    require('web.dom_ready');


    $('.review-box .owl-carousel').owlCarousel({
        center: false,
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
                items: 1
            },
            1200: {
                items: 1
            }

        }
    });

    $(".review-box .owl-carousel .owl-prev").html('');
    $(".review-box .owl-carousel .owl-next").html('');

});