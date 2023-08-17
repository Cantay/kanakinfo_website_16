# -*- coding: utf-8 -*-

import logging
import requests
import lxml.html
from odoo import fields, models, tools

_logger = logging.getLogger(__name__)


class GithubRepositoryLine(models.Model):
    _name = 'github.repository.line'

    github_repo = fields.Many2one('github.repository', ondelete='cascade')
    name = fields.Char()
    timestamp = fields.Char('Last Modification')


class GithubRepository(models.Model):
    _name = 'github.repository'
    _rec_name = 'github_url'

    sequence = fields.Integer(default=1)
    github_url = fields.Char(string='Branch Name', required=True)
    app_lines = fields.One2many('github.repository.line', 'github_repo')

    def sync_apps(self, appdata):
        product_product_obj = self.env['product.product'].sudo()
        product_id = self.env['product.product'].sudo().search([('technical_name', '=', appdata[0]), ('version', '=', self.github_url)], limit=1)
        furl = "https://team.kanakinfosystems.com/api/apps/%s/%s/data" % (self.github_url, appdata[0])
        headers = {
            'Authorization': 'Bearer 2fffeffc83024c6bbc0354751698be58cd3997e8'
        }
        payload = {'timestamp': ''}
        if product_id.app_timestamp:
            payload['timestamp'] = product_id.app_timestamp
        apps_response = requests.request("GET", furl, headers=headers, data=payload)
        module_info = apps_response.json()
        if module_info:
            module_version = product_product_obj.create_or_update_variants(module_info, self.github_url)
            description_rst_html = ''
            if module_info.get('documentation', False):
                try:
                    html = lxml.html.document_fromstring(module_info.get('documentation', False))
                    for element, attribute, link, pos in html.iterlinks():
                        if element.get('src') and '//' not in element.get('src') and 'static/' not in element.get('src'):
                            # /apps/assets/8.0/odoo_shoppe_backend_theme/v1_0_10.png
                            element.set('src', "https://team.kanakinfosystems.com/apps/assets/%s/%s/%s" % (self.github_url, module_info['technical_name'], element.get('src')))
                    description_rst_html = tools.html_sanitize(lxml.html.tostring(html))
                except Exception as e:
                    _logger.info("error:%s", e)
                    description_rst_html = module_info.get('description', '')
                    pass
            else:
                description_rst_html = module_info.get('description', '')
            banner_image = False
            theme_image = False
            if module_info.get('images', False):
                banner_image = module_info.get('images')[0]
            if module_info.get('images', False) and len(module_info.get('images', False)) > 1:
                theme_image = module_info.get('images')[1]
            default_currency = self.env.ref('base.EUR')
            if module_info.get('currency'):
                default_currency = self.env.ref("base.%s" % module_info.get('currency'))
            default_price = default_currency._convert(float(module_info.get('price', 0.00)), self.env.company.currency_id, self.env.company, fields.Date.context_today(self))
            module_version.write({
                'repository_id': self.id,
                'version': self.github_url,
                'description_rst_html': description_rst_html,
                'image_1920': module_info.get('icon', False),
                'banner_image': banner_image,
                'depends': ','.join(module_info.get('depends', '')),
                'theme_image': theme_image,
                'description_sale': module_info.get('summary', ''),
                'license': module_info.get('license', ''),
                'app_timestamp': module_info.get('timestamp', '')
            })
            module_version.product_template_attribute_value_ids.write({
                'price_extra': default_price - module_version.list_price
            })

    def get_apps(self):
        url = "https://team.kanakinfosystems.com/api/get/%s/apps" % (self.github_url)
        headers = {
            'Authorization': 'Bearer 2fffeffc83024c6bbc0354751698be58cd3997e8'
        }
        response = requests.request("GET", url, headers=headers)
        res = response.json()
        for appdata in res['data']:
            appline = self.env['github.repository.line'].search([('name', '=', appdata[0]), ('github_repo', '=', self.id)])
            if not appline:
                self.env['github.repository.line'].create({
                    'github_repo': self.id,
                    'name': appdata[0],
                    'timestamp': appdata[1]
                })
                self.sync_apps(appdata)
            else:
                if appline.timestamp != appdata[1]:
                    self.sync_apps(appdata)
                    appline.write({'timestamp': appdata[1]})
