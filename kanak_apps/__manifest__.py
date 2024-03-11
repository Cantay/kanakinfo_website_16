# -*- coding: utf-8 -*-
# Powered by Kanak Infosystems LLP.
# © 2020 Kanak Infosystems LLP. (<https://www.kanakinfosystems.com>).

{
    'name': "Kanak Apps",
    'version': "16.0.0.0",
    'category': "website",
    'description': "Kanak Apps",
    'summary': 'Kanak Apps',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'license': 'OPL-1',
    'depends': ['sale', 'website_sale', 'kanak_github_connector'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'views/components.xml',
        'views/header_apps.xml',
        'views/template.xml',
        'views/AppsDetails.xml',
        'views/portal.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'kanak_apps/static/src/js/**',
            'kanak_apps/static/src/scss/**'
        ],
    },
    'auto_install': False,
    'installable': True,
}
