odoo.define('website_kanak.script', function($) {
    "use strict";

    const showChar = 260; // How many characters are shown by default
    const ellipsestext = "";
    const moretext = "<i class='fa fa-caret-right' aria-hidden='true'></i><i class='fa fa-caret-right' aria-hidden='true'></i>";
    const lesstext = "<i class='fa fa-caret-left' aria-hidden='true'></i><i class='fa fa-caret-left' aria-hidden='true'></i>";

    $(document).ready(function() {
        $('.more').each(function() {
            const content = $(this).html();

            if (content.length > showChar) {
                const c = content.substr(0, showChar);
                const h = content.substr(showChar, content.length - showChar);

                const html = `${c} <span class="moreellipses">${ellipsestext}</span><span class="morecontent"><span>${h}</span>&nbsp;&nbsp;<a href="" class="morelink">${moretext}</a></span>`;

                $(this).html(html);
            }
        });

        $(document).on('click', '.morelink', function(e) {
            e.preventDefault();

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

        $(document).on('click', '.flip', function() {
            $(this).next(".fp-panel").slideToggle("fast");
        });

        $('.knk-faqs .implementation-heading1').click(function() {
            $(this).closest('.faq').find('div').toggleClass('d-none');
        });
    });

    function initOwlCarousel() {
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
        // $(".industries_we_serve .owl-carousel .
