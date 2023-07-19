# -*- coding: utf-8 -*-

import logging
import requests
import lxml.html
from odoo import fields, models, tools

_logger = logging.getLogger(__name__)


class GithubRepository(models.Model):
    _name = 'github.repository'
    _rec_name = 'github_url'

    sequence = fields.Integer(default=1)
    github_url = fields.Char(string='Branch Name', required=True)

    def action_branch_clone(self):
        url = "https://team.kanakinfosystems.com/api/get/%s/apps" % (self.github_url)
        headers = {
            'Authorization': 'Bearer 2fffeffc83024c6bbc0354751698be58cd3997e8'
        }
        response = requests.request("GET", url, headers=headers)
        product_product_obj = self.env['product.product'].sudo()
        res = response.json()
        for tech_name in res['data']:
            furl = "https://team.kanakinfosystems.com/api/apps/%s/%s/data" % (self.github_url, tech_name)
            product_id = self.env['product.product'].sudo().search([('technical_name', '=', tech_name), ('version', '=', self.github_url)], limit=1)
            payload = {'timestamp': ''}
            if product_id.app_timestamp:
                payload['timestamp'] = product_id.app_timestamp
            apps_response = requests.request("GET", furl, headers=headers, data=payload)
            module_info = apps_response.json()
            if module_info:
                module_version = product_product_obj.create_or_update_variants(module_info, self.github_url)
                description_rst_html = ''
                if module_info.get('documentation', False):
                    html = lxml.html.document_fromstring(module_info.get('documentation', False))
                    for element, attribute, link, pos in html.iterlinks():
                        if element.get('src') and not '//' in element.get('src') and not 'static/' in element.get('src'):
                            element.set('src', "//apps.odoocdn.com/apps/assets/%s/%s/%s" % (self.github_url, module_info['technical_name'], element.get('src')))
                    description_rst_html = tools.html_sanitize(lxml.html.tostring(html))
                else:
                    description_rst_html = module_info.get('description', '')
                banner_image = False
                theme_image = False
                if module_info.get('images', False):
                    banner_image = module_info.get('images')[0]
                if module_info.get('images', False) and len(module_info.get('images', False)) > 1:
                    theme_image = module_info.get('images')[1]
                module_version.write({
                    'repository_id': self.id,
                    'version': self.github_url,
                    'description_rst_html': description_rst_html,
                    'image_1920': module_info.get('icon', False),
                    'banner_image': banner_image,
                    'theme_image': theme_image,
                    'description_sale': module_info.get('summary', ''),
                    'license': module_info.get('license', '')
                })
