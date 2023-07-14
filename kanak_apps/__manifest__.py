# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    "name": "Kanak Apps",
    "version": "16.0.0.0",
    "category": "website",
    "depends": ['sale', 'website_sale',],
    'license': 'OPL-1',
    'website': 'https://www.kanakinfosystems.com',
    'author': 'Kanak Infosystems LLP.',
    'summary': 'Kanak Apps',
    "description": "Kanak Apps",
    "data": [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/components.xml',
        'views/header_apps.xml',
        'views/template.xml',
        'views/AppsDetails.xml'
    ],
    "auto_install": False,
    'assets': {
        'web.assets_frontend': [
            'kanak_apps/static/src/js/**',
            'kanak_apps/static/src/scss/**'
        ],
    },
    "installable": True,
}
