# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Kanak Website',
    'category': '',
    'summary': 'Kanak Website landing Page',
    'website': 'https://www.kanakinfosystems.com',
    'version': '16.0',
    'depends': ['website','mass_mailing','crm'],
    'data': [
        'views/odoo_erp_services.xml',
        'views/template.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_frontend': [
            'https://www.google.com/recaptcha/api.js',
            'kanak_website/static/lib/dist/owl.carousel.js',
            'kanak_website/static/lib/dist/owl.carousel.min.js',
            'kanak_website/static/lib/dist/assets/owl.carousel.css',
            'kanak_website/static/lib/dist/assets/owl.carousel.min.css',
            'kanak_website/static/src/css/odoo_website.css',
            'kanak_website/static/src/js/odoo_website.js',
        ],
    },
    'license': 'LGPL-3',
}
