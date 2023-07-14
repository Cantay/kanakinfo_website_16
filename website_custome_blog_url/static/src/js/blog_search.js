odoo.define('website_custome_blog_url.blog_search', function(require) {
    "use strict";

    require('web.dom_ready');
    var ajax = require('web.ajax');
    
    var $inputauto = $("form#blog_search.custom_blog_search input#search_blog");
    $('.website_blog').on("input", 'form#blog_search.custom_blog_search input#search_blog', function (event) {
        ajax.jsonRpc("/blogs/search", "call", {'values': event.currentTarget.value})
            .then(function (datas) {
                if(datas.blog_results != undefined){
                    $('.blog_result_main_cl').html(datas.blog_results);
                }else{
                    $('.blog_result_main_cl').html('');
                }
                
        });
    });

    $('.blog_add_comment').click(function () {
        $('.add-comment-box').css("display","block");
    });


    // var $inputauto = $("form#blog_post_comment");
    $('form#blog_post_comment .blog_comment_submit').click(function (event) {
        var comment = $('form#blog_post_comment textarea[name="description"]').val();
        var name = $('form#blog_post_comment input[name="partner_name"]').val();
        var email = $('form#blog_post_comment input[name="partner_email"]').val();
        var blog_id = $('form#blog_post_comment input[name="blog_post_id"]').val();
        ajax.jsonRpc("/blog_comment_form", "call", {
            'comment': comment,
            'name': name,
            'email': email,
            'blog_id': blog_id,
        }).then(function (datas) {
            if (datas === true) {
                $('.add-comment-box').css("display","none");
                $('#blog-comment').css("display","block");
            }
        });
    });


});

