# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    download_count = fields.Integer(string="Download Count", default=0)
    app_sale_count = fields.Integer(string="Apps Sale Count", default=0)


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
                    line.product_id.product_tmpl_id.app_sale_count = line.product_id.product_tmpl_id.app_sale_count + 1

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
