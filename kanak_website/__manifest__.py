# -*- coding: utf-8 -*-
#################################################################################
# Author      : Kanak Infosystems LLP. (<https://www.kanakinfosystems.com/>)
# Copyright(c): 2012-Present Kanak Infosystems LLP.
# All Rights Reserved.
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.kanakinfosystems.com/license>
#################################################################################

{
    'name': "Kanak Website",
    'version': '1.0',
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'summary': '',
    'description': """
    """,
    'depends': ['base', 'website_sale', 'crm', 'website', 'website_hr_recruitment', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/careers.xml',
        'views/careers_added_models.xml',
        'views/template.xml',
        'views/netsuite_template.xml',
        'views/netsuite_implementation_template.xml',
        'views/netsuite_consultant_template.xml',
        'views/netsuite_licensing_template.xml',
        'views/netsuite_support_template.xml',
        'views/odoo_implementation.xml',
        'views/odoo_developer.xml',
        'views/odoo_erp_services.xml',
        'views/crm_lead.xml',
        'views/mail.xml',
        'views/webinar_ceo.xml',
        'views/webinar_ceo_template.xml',
    ],
    # 'qweb': ['static/src/xml/website_seo.xml'],
    'images': ['static/description/main_image.png'],
    'sequence': 1,
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 60,
    'currency': 'EUR',
}
