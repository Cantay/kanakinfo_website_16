# Copyright © 2021 Garazd Creation (https://garazd.biz)
# Licensed under LGPL-3.0 or later (<https://www.gnu.org/licenses/lgpl-3.0.html>)

# flake8: noqa: E501

{
    'name': 'Google Analytics 4 Global Site Tag (gtag.js)',
    'version': '16.0.1.0.0',
    'category': 'Website',
    'author': 'Yurii Razumovskyi, Iryna Razumovska, <support@garazd.biz>',
    'website': 'https://garazd.biz/shop',
    'license': 'LGPL-3.0',
    'summary': 'Integrate Google Analytics 4 Global Site Tag (gtag.js) with your Odoo website, '
              'including Login and Sign Up events tracking.',
    'description': 'This module allows you to integrate Google Analytics 4 Global Site Tag (gtag.js) '
                  'into your Odoo website. It also tracks Login and Sign Up events.',
    'images': ['static/description/banner.png', 'static/description/icon.png'],
    'live_test_url': 'https://garazd.biz/r/CN9',
    'depends': [
        'website',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/website_templates.xml',
    ],
    'external_dependencies': {
    },
    'support': 'support@garazd.biz',
    'application': False,
    'installable': True,
    'auto_install': False,
}
