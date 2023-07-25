# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    download_count = fields.Integer(string="Download Count", default=0)
    odoo_apps_sale_count = fields.Integer(string="Odoo Apps Sale Count", default=0)
    kanak_apps_sale_count = fields.Integer(string="Kanak Apps Sale Count", default=0)
    app_sale_count = fields.Integer(string="Apps Sale Count", default=0, compute="compute_app_sale_count", store=True)

    @api.depends('odoo_apps_sale_count', 'kanak_apps_sale_count')
    def compute_app_sale_count(self):
        for rec in self:
            rec.app_sale_count = rec.kanak_apps_sale_count + rec.odoo_apps_sale_count

    def action_odoo_apps_count(self):
        for product_tmpl in self:
            version = ''
            if product_tmpl.product_variant_ids:
                versions = product_tmpl.product_variant_ids.mapped('version')
                if versions:
                    version = versions[0]
            if version:
                app_url = "https://apps.odoo.com/apps/modules/%s/%s" % (version, product_tmpl.technical_name)
                content_page = requests.get(app_url)
                if content_page.status_code == 200:
                    soup = BeautifulSoup(content_page.text, 'html.parser')
                    purchase_count = soup.find("span", attrs={"title": 'Purchases'})
                    if purchase_count:
                        product_tmpl.odoo_apps_sale_count = purchase_count.text.strip() or 0
                    download_count = soup.find("span", attrs={"title": 'Downloads'})
                    if download_count:
                        product_tmpl.download_count = download_count.text.strip() or 0


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.depends_context('lang')
    @api.depends('product_tmpl_id.website_url', 'product_template_attribute_value_ids')
    def _compute_product_website_url(self):
        for product in self:
            if product.technical_name and 'theme' in product.technical_name:
                if product.product_template_attribute_value_ids:
                    product.website_url = "/apps/themes/%s/%s" % (product.product_template_attribute_value_ids[0].name, product.technical_name)
            else:
                if product.product_template_attribute_value_ids and product.technical_name:
                    product.website_url = "/apps/modules/%s/%s" % (product.product_template_attribute_value_ids[0].name, product.technical_name)
                else:
                    attributes = ','.join(str(x) for x in product.product_template_attribute_value_ids.ids)
                    product.website_url = "%s#attr=%s" % (product.product_tmpl_id.website_url, attributes)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _action_confirm(self):
        super(SaleOrder, self)._action_confirm()
        for order in self:
            for line in order.order_line:
                if line.product_id and line.product_id.product_tmpl_id:
                    line.product_id.product_tmpl_id.kanak_apps_sale_count = line.product_id.product_tmpl_id.kanak_apps_sale_count + 1

    def get_download_module_links(self):
        self.ensure_one()
        links = []
        for line in self.order_line:
            if line.product_id.version and line.product_id.technical_name:
                if 'theme' in line.product_id.technical_name:
                    link = '%s/download/apps/themes/%s/%s/%s?access_token=%s' % (self.get_base_url(), line.product_id.version, line.product_id.technical_name, self.id, self.access_token)
                    links.append(link)
                else:
                    link = '%s/download/apps/modules/%s/%s/%s?access_token=%s' % (self.get_base_url(), line.product_id.version, line.product_id.technical_name, self.id, self.access_token)
                    links.append(link)
        return links


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _is_not_sellable_line(self):
        return self.product_id and self.product_id.product_tmpl_id and \
            self.product_id.product_tmpl_id.technical_name or super()._is_not_sellable_line()
