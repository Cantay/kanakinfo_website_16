# -*- coding: utf-8 -*-
{
    'name': 'Github Connector',
    'summary': 'Synchronize information from Github repositories',
    'version': '12.0',
    'category': 'Connector',
    'author': 'Kanak Infosystems LLP.',
    'website': 'http://www.kanakinfosystems.com',
    'depends': [
        'base',
        'web',
        'website_sale'
    ],
    'data': [
            'security/ir.model.access.csv',
            'views/github_repository_views.xml',
            'views/res_config_settings_views.xml',
            'views/menus.xml',
            'views/product_details_template.xml',
            ],
    'installable': True,
    'assets': {
        'web.assets_frontend': [
            'kanak_github_connector/static/src/js/github_connector.js',
        ]
    }
}
