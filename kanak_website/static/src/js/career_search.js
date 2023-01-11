odoo.define('kanak_website.career_search', function(require) {
    "use strict";
    require('web.dom_ready');
    var core = require('web.core');
    var ajax = require('web.ajax');

    $(document).ready(function() {

        //-------------Slider------------

        $(".slide_content").mouseover(function(ev) {
            $(".job_search").css("display", "block");
            $(".main_slide_container div").removeClass("slide_active");
            $(".main_slide_container div").removeClass("slide_second");
            $(this).addClass("slide_active");
        })

        $(".job_main").mouseover(function(ev) {
            $(".job_search").css("display", "block");
        })

        $(".job_main").mouseleave(function(ev) {
            $(".job_search").css("display", "none");
        })

        //-------------Auto selected IT & Development------------

        $('.list_of_department').find('option[value=3]').attr('selected','selected');
            var department_id = parseInt($('.list_of_department').val());
            ajax.jsonRpc("/jobs/search", 'call', { 'department_id': department_id }).then(function(data) {
                if (data) {
                    $('.preview_jobs').empty();
                    $('.preview_jobs').append(data.j_list);
                }
            });

        //-------------Dropdown_Department_list------------

        $('.list_of_department').on('change', function() {
            var department_id = parseInt($('.list_of_department').val());
            ajax.jsonRpc("/jobs/search", 'call', { 'department_id': department_id }).then(function(data) {
                if (data) {
                    $('.preview_jobs').empty();
                    $('.preview_jobs').append(data.j_list);
                }
            });
        });

        //-------------Owl Carousel_Mouse Slide------------

        var owl = $('.owl-carousel');
        owl.owlCarousel({
            smartSpeed: 300,
            loop: true,
            nav: false,
            margin: 10,
            slideBy: 1,
            stagePadding: 50,
            responsive: {
                0: {
                    items: 3,
                    // nav: false
                },
                // 300: {
                //     items: 1,
                //     nav: false
                // },
                // 600: {
                //     items: 3,
                //     nav: false
                // },
                // 960: {
                //     items: 3
                // },
                // 1200: {
                //     items: 3
                // }
            }
        });
        owl.on("mousewheel", "#team_member_slider .owl-stage", function(e) {
            //  if (e.originalEvent.wheelDelta > 0) {
            //     owl.trigger("next.owl");
            // } else {
            //     owl.trigger("prev.owl");
            // }
            if (e.originalEvent.wheelDelta > 0) {
                owl.trigger("next.owl",  [1000]);
            } else {
                owl.trigger("prev.owl",  [1000]);
            }
            e.preventDefault();
        });
    });

    //-------------Read More Button------------

    $(document).ready(function() {
        var readMoreBtn = $('.read_more_btn');
        var text = $('.text_hide');
        readMoreBtn.on("click", function(e) {
            text.toggleClass('show_more');
            if ($("#read_hide").hasClass('show_more')) {
                readMoreBtn.css("display", "none");
            } else {
                readMoreBtn.css("display", "block");
            }

        });

    });

    
    $(document).ready(function() {
        $('.slider_our_partners').hover(
            function() {
                $(".slide-track_our_partners").css("animation-play-state", "paused");
            },
            function() {
                $(".slide-track_our_partners").css("animation-play-state", "");
            });
    });



    $('.panel-title > a').click(function() {
            $(this).find('i').toggleClass('fa-plus fa-minus')
                .closest('panel').siblings('panel')
                .find('i')
                .removeClass('fa-minus').addClass('fa-plus');
        });


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