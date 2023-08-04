odoo.define('website_kanak.script', function(require) {
    "use strict";

    require('web.dom_ready');
    var core = require('web.core');
    var ajax = require('web.ajax');


    var showChar = 260; // How many characters are shown by default
    var ellipsestext = "";
    var moretext = "<i class='fa fa-caret-right' aria-hidden='true'></i><i class='fa fa-caret-right' aria-hidden='true'></i>";
    var lesstext = "<i class='fa fa-caret-left' aria-hidden='true'></i><i class='fa fa-caret-left' aria-hidden='true'></i>";


    $('.more').each(function() {
        var content = $(this).html();

        if (content.length > showChar) {

            var c = content.substr(0, showChar);
            var h = content.substr(showChar, content.length - showChar);

            var html = c + '<span class="moreellipses">' + ellipsestext + '</span><span class="morecontent"><span>' + h + '</span>&nbsp;&nbsp;<a href="" class="morelink">' + moretext + '</a></span>';

            $(this).html(html);
        }
    });

    $(".morelink").click(function() {
        if ($(this).hasClass("less")) {
            $(this).removeClass("less");
            $(this).html(moretext);
        } else {
            $(this).addClass("less");
            $(this).html(lesstext);
        }
        $(this).parent().prev().toggle();
        $(this).prev().toggle();
        return false;
    });

    $(".flip").click(function() {
        $(this).next(".fp-panel").slideToggle("fast");
    });


    $('.knk-faqs .implementation-heading1').click(function() {
        $(this).closest('.faq').find('div').toggleClass('d-none');
    });


    $('.theme-slider .owl-carousel').owlCarousel({
        center: false,
        items: 1,
        loop: true,
        margin: 10,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000,
        responsive: {
            600: {
                items: 1
            },
            1000: {
                items: 3
            },
            1200: {
                items: 4
            },
            1600: {
                items: 4
            }
        }
    });

    $(".theme-slider  .owl-carousel .owl-prev").html('');
    $(".theme-slider  .owl-carousel .owl-next").html('');


    $('#our-team-slider-sec003 .owl-carousel').owlCarousel({
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

    $("#our-team-slider-sec003 .owl-carousel .owl-prev").html('');
    $("#our-team-slider-sec003 .owl-carousel .owl-next").html('');

    $('.exp_solution .owl-carousel').owlCarousel({
        center: false,
        items: 1,
        loop: true,
        margin: 10,
        nav: true,
        responsive: {
            600: {
                items: 3
            },

        }
    });

    $(".exp_solution  .owl-carousel .owl-prev").html('');
    $(".exp_solution  .owl-carousel .owl-next").html('');


    $('.industries_we_serve .owl-carousel').owlCarousel({
        stagePadding: 30,
        center: true,
        items: 2,
        loop: true,
        margin: 20,
        dots: false,
        nav: false,
        autoplay: true,
        autoplayTimeout: 3000,
        autoplayHoverPause: false,
        responsive: {
            600: {
                items: 3
            },

        }
    });

    // $(".industries_we_serve .owl-carousel .owl-prev").html('');
    // $(".industries_we_serve .owl-carousel .owl-next").html('');


    $('.frappe-healthcare-slide .owl-carousel').owlCarousel({
        center: false,
        items: 3,
        loop: true,
        margin: 10,
        nav: true,
        slideBy:3,
        autoplay: false,
        autoplayTimeout: 5000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 3
            },
            1000: {
                items: 3
            }

        }
    });

    $(".frappe-healthcare-slide .owl-carousel .owl-prev").html('');
    $(".frappe-healthcare-slide .owl-carousel .owl-next").html('');

    $('.frappe-healthcare-slide-mob .owl-carousel').owlCarousel({
        center: false,
        items: 3,
        loop: true,
        margin: 10,
        nav: true,
        slideBy:3,
        autoplay: true,
        autoplayTimeout: 5000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 3
            },
            1000: {
                items: 3
            }

        }
    });

    $(".frappe-healthcare-slide-mob .owl-carousel .owl-prev").html('');
    $(".frappe-healthcare-slide-mob .owl-carousel .owl-next").html('');


    $('.why-frappe-health .owl-carousel').owlCarousel({
        center: false,
        items: 1,
        loop: true,
        margin: 5,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 4
            },
            1000: {
                items: 4
            }

        }
    });

    $(".why-frappe-health .owl-carousel .owl-prev").html('');
    $(".why-frappe-health .owl-carousel .owl-next").html('');



    $('.benefit-frappe-mob .owl-carousel').owlCarousel({
        center: false,
        items: 1,
        loop: true,
        margin: 5,
        nav: true,
        autoplay: true,
        autoplayTimeout: 3000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 4
            },
            1000: {
                items: 4
            }

        }
    });

    $(".benefit-frappe-mob .owl-carousel .owl-prev").html('');
    $(".benefit-frappe-mob .owl-carousel .owl-next").html('');

    $('.sec-lms-carousal .owl-carousel').owlCarousel({
        center: false,
        items: 3,
        loop: true,
        margin: 40,
        nav: true,
        autoplay: true,
        autoplayTimeout: 5000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            },
            1200: {
                items: 3
            },
            2560: {
                items: 3
            }

        }
    });

    $(".sec-lms-carousal .owl-carousel .owl-prev").html('');
    $(".sec-lms-carousal .owl-carousel .owl-next").html('');


    $('.lms-feature-mob .owl-carousel').owlCarousel({
        center: false,
        items: 3,
        loop: true,
        margin: 40,
        nav: true,
        autoplay: true,
        autoplayTimeout: 5000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            },
            1200: {
                items: 3
            }

        }
    });

    $(".lms-feature-mob .owl-carousel .owl-prev").html('');
    $(".lms-feature-mob .owl-carousel .owl-next").html('');

    $('.ring-slider-mob .owl-carousel').owlCarousel({
        center: false,
        items: 3,
        loop: true,
        margin: 10,
        nav: true,
        autoplay: true,
        autoplayTimeout: 5000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 2
            },
            1200: {
                items: 2
            },
        }
    });

    $(".ring-slider-mob .owl-carousel .owl-prev").html('');
    $(".ring-slider-mob .owl-carousel .owl-next").html('');

    $('.choose-lms-mob .owl-carousel').owlCarousel({
        center: false,
        items: 3,
        loop: true,
        margin: 10,
        nav: true,
        autoplay: true,
        autoplayTimeout: 5000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 2
            },
            1200: {
                items: 2
            },
        }
    });

    $(".choose-lms-mob .owl-carousel .owl-prev").html('');
    $(".choose-lms-mob .owl-carousel .owl-next").html('');

    $('.frappe-hr-feature-mob .owl-carousel').owlCarousel({
        center: false,
        items: 4,
        loop: true,
        margin: 10,
        nav: true,
        autoplay: true,
        dots:false,
        autoplayTimeout: 3000,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 2
            },
            1000: {
                items: 3
            },
            1200: {
                items: 4
            }

        }
    });

    $(".frappe-hr-feature-mob .owl-carousel .owl-prev").html('');
    $(".frappe-hr-feature-mob .owl-carousel .owl-next").html('');

    $('.choose-frappe-mob .owl-carousel').owlCarousel({
        center: false,
        items: 4,
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
                items: 2
            },
            1000: {
                items: 3
            },
            1200: {
                items: 4
            }

        }
    });

    $(".choose-frappe-mob .owl-carousel .owl-prev").html('');
    $(".choose-frappe-mob .owl-carousel .owl-next").html('');


    $('.geomark-mob .owl-carousel').owlCarousel({
        center: false,
        items: 3,
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
                items: 4
            }

        }
    });

    $(".geomark-mob .owl-carousel .owl-prev").html('');
    $(".geomark-mob .owl-carousel .owl-next").html('');


    $('.key-feature-box-mob .owl-carousel').owlCarousel({
        center: false,
        items: 3,
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
                items: 4
            }

        }
    });

    $(".key-feature-box-mob .owl-carousel .owl-prev").html('');
    $(".key-feature-box-mob .owl-carousel .owl-next").html('');


    $('.odoo_shoppe_slider .shoppe_slider.owl-carousel').owlCarousel({
        // center: true,
        // items: 1,
        loop: false,
        margin: 14,
        dots:false,
        nav: true,
        // autoplay: true,
        // autoplayTimeout: 3000,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 1
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            },
            4000: {
                items: 3
            }

        }
    });

    $(".odoo_shoppe_slider .shoppe_slider.owl-carousel .owl-prev").html('');
    $(".odoo_shoppe_slider .shoppe_slider.owl-carousel .owl-next").html('');


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



    if ($(".owl-item.active")[0]) {
        $($(".owl-item.active")[0]).find(".card").css({"height": "551px"})
    }
    if ($(".owl-item.active")[1]) {
        $($(".owl-item.active")[1]).find(".card").css({"height": "433px"})
    }
    if ($(".owl-item.active")[2]) {
        $($(".owl-item.active")[2]).find(".card").css({"height": "321px"})
    }

    var owl = $(".odoo_shoppe_slider .shoppe_slider.owl-carousel")
    owl.on('translate.owl.carousel', function (e) {
        var elm = e.relatedTarget._items[e.item.index][0];
        $(elm).find(".card").animate({
                height: '551px',
        }, 1000);
        $(elm).next().find(".card").animate({
                height: '433px',
        }, 1000);
        $(elm).next().next().find(".card").animate({
                height: '321px',
        }, 1000);
    });
    $('#main-symbol-all .owl-carousel').owlCarousel({
        loop:true,
        margin:10,
        nav:true,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:3
            },
            1000:{
                items:5
            }
        },
        navText : ['<i class="fa fa-angle-left" aria-hidden="true"></i>','<i class="fa fa-angle-right" aria-hidden="true"></i>'],
    });
    function initOwlCarousel() {
        $('#kanak_11_client_cust .owl-carousel').owlCarousel({
            loop:true,
            margin:20,
            nav:false,
            dots:false,
            autoplay: true,
            autoplayTimeout: 2000,
            responsive:{
                0:{
                    items:1
                }
            },
        });
    }

      // Function to destroy Owl Carousel on desktop devices
      function destroyOwlCarousel() {
        $('#kanak_11_client_cust .owl-carousel').trigger('destroy.owl.carousel');
      }

      // Check screen size and call appropriate functions
      function checkScreenSize() {
        if (window.innerWidth <= 768) {
          initOwlCarousel(); // Initialize Owl Carousel on mobile
        } else {
          destroyOwlCarousel(); // Destroy Owl Carousel on desktop
        }
      }
    checkScreenSize();
    $(window).resize(function() {
        checkScreenSize();
    });
    
});