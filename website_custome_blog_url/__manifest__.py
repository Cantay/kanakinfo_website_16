# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<http://kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <http://kanakinfosystems.com/license>
#################################################################################
{
    'name': 'Website Custome Blog Url',
    'version': '1.1',
    'description': """
Website Custome Blog Url
========================
    """,
    'author': 'Kanak Infosystems LLP.',
    'website': 'http://www.kanakinfosystems.com',
    'category': 'Website',
    'depends': ['website_blog'],
    'data': [
        'security/ir.model.access.csv',
        'views/blog_comment_view.xml',
        'views/blog_post_templates.xml',
        'views/custome_blog_url_view.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'website_custome_blog_url/static/src/css/custom_blog_style.min.css',
            'website_custome_blog_url/static/src/js/blog_script.js',
            'website_custome_blog_url/static/src/js/blog_search.js',
        ]
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 0.0,
    'currency': 'EUR',
}
