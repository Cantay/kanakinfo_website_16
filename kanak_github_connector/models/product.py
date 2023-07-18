# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    technical_name = fields.Char(string='Technical Name')
    url = fields.Char()
    live_preview = fields.Char(string="Live Preview")


class ProductProduct(models.Model):
    _inherit = 'product.product'

    repository_id = fields.Many2one('github.repository', string='Repository')
    version = fields.Char(string='Version (Manifest)', readonly=True)
    description_rst_html = fields.Html(
        string='HTML the RST Description')
    banner_image = fields.Image(string="App Banner")
    theme_image = fields.Image(string="Theme Banner")
    license = fields.Text(string="License")
    _ICON_PATH = [
        'static/src/img/',
        'static/description/',
    ]
    _INDEX_HTML_PATH = 'static/description/'

    @api.model
    def get_module_category(self, info):
        """Used to search the category of the module by the data given
        on the manifest.

        :param dict info: The parsed dictionary with the manifest data.
        :returns: recordset of the given category if exists.
        """
        category_obj = self.env['product.public.category']
        category = info.get('category', False)
        categorys = category.split("/")
        category_ids = []
        if categorys:
            for categ in categorys:
                category_search = category_obj.search([('name', '=', categ)], limit=1)
                if not category_search:
                    category_search = category_obj.create({'name': categ})
                category_ids.append(category_search.id)
        else:
            category_search = category_obj.search([('name', '=', category)], limit=1)
            category_ids.append(category_search.id)
        return category_ids

    @api.model
    def create_or_update_variants(self, info, branch):
        ProductTemplate = self.env['product.template'].sudo()
        technical_name = info['technical_name']
        product_id = ProductTemplate.search([('technical_name', '=', technical_name)])
        if not product_id:
            product_id = ProductTemplate.create(self.product_on_manifest(info, branch))
        else:
            product_id.write(self.product_on_manifest(info, branch, product_id))
        attribut_value_id = False
        if branch:
            attribut_value_id = self.env['product.attribute.value'].sudo().search([('name', '=', branch)])
        rec_ids = self.env['product.template.attribute.value'].search([('attribute_id', '=', attribut_value_id.attribute_id.id), ('product_attribute_value_id', '=', attribut_value_id.id)])
        module_version = self.search([
            ('technical_name', '=', str(technical_name)),
            ('product_template_variant_value_ids', 'in', rec_ids.ids)], limit=1)
        return module_version

    @api.model
    def product_on_manifest(self, info, branch, product_id=False):
        product_attribute_id = self.env['product.attribute'].sudo().search([
            ('name', '=', 'Odoo Version')], limit=1)
        if not product_attribute_id:
            product_attribute_id = self.env['product.attribute'].sudo().create({
                'name': 'Odoo Version'
            })
        if branch:
            attribut_value_id = self.env['product.attribute.value'].sudo().search([
                ('name', '=', branch)])
            if not attribut_value_id:
                attribut_value_id = self.env['product.attribute.value'].sudo().create({
                    'name': branch,
                    'attribute_id': product_attribute_id.id
                })
        values = {
            'name': info['name'],
            'technical_name': info['technical_name'],
            'website_published': True,
            'description': info['description'],
            'public_categ_ids': [(6, 0, self.get_module_category(info) or [])],
            'list_price': info.get('price') or 0,
            'url': info['name'].lower().replace(' ', '-'),
            'live_preview': info.get('live_test_url', '') or '',
            'sale_ok': True,
            'attribute_line_ids': [(0, 0, {
                'attribute_id': product_attribute_id.id,
                'value_ids': [(4, attribut_value_id.id)],
            })]
        }
        if product_id:
            odoo_attribute_line = product_id.attribute_line_ids.filtered(lambda line: line.attribute_id == product_attribute_id)
            if odoo_attribute_line:
                values.update({'attribute_line_ids': [(1, odoo_attribute_line.id, {
                    'value_ids': [(4, attribut_value_id.id)]})
                ]})
        return values
