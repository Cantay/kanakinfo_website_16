odoo.define('kanak_website.career_search', function(require) {
    "use strict";

    require('web.dom_ready');
    var ajax = require('web.ajax');


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
    $("#hire-our-team-mob .owl-carousel .owl-next").html('');


    $('.list_of_department').on('change', function() {
        var department_id = parseInt($('.list_of_department').val());
        ajax.jsonRpc("/jobs/search", 'call', { 'department_id': department_id }).then(function(data) {
            if (data) {
                $('.preview_jobs').empty();
                $('.preview_jobs').append(data.j_list);
            }
        });
    });

    $('.list_of_department').trigger('change');
    

});