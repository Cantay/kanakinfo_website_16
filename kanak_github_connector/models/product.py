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
    app_timestamp = fields.Char(string="Last Time")
    depends = fields.Char(string="Depends")

    @api.model
    def get_module_category(self, info):
        """Used to search the category of the module by the data given
        on the manifest.

        :param dict info: The parsed dictionary with the manifest data.
        :returns: recordset of the given category if exists.
        """
        category_obj = self.env['product.public.category']
        category = info.get('category', False)
        if category:
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
        return []

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

        _logger.info("===Technical Name====%s" % (info.get('technical_name')))
        default_currency = self.env.ref('base.EUR')
        if info.get('currency'):
            default_currency = self.env.ref("base.%s" % info.get('currency'))
        default_price = default_currency._convert(float(info.get('price', 0.00)), self.env.company.currency_id, self.env.company, fields.Date.context_today(self))
        values = {
            'name': info['name'],
            'technical_name': info['technical_name'],
            'website_published': True,
            'description': info.get('description', ''),
            'public_categ_ids': [(6, 0, self.get_module_category(info) or [])],
            'list_price': default_price,
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

    def price_compute(self, price_type, uom=None, currency=None, company=None, date=False):
        company = company or self.env.company
        date = date or fields.Date.context_today(self)

        self = self.with_company(company)
        if price_type == 'standard_price':
            # standard_price field can only be seen by users in base.group_user
            # Thus, in order to compute the sale price from the cost for users not in this group
            # We fetch the standard price as the superuser
            self = self.sudo()

        prices = dict.fromkeys(self.ids, 0.0)
        for product in self:
            price = product[price_type] or 0.0
            price_currency = product.currency_id
            if price_type == 'standard_price':
                price_currency = product.cost_currency_id

            if price_type == 'list_price':
                price += product.price_extra
                # we need to add the price from the attributes that do not generate variants
                # (see field product.attribute create_variant)
                if self._context.get('no_variant_attributes_price_extra'):
                    # we have a list of price_extra that comes from the attribute values, we need to sum all that
                    price += sum(self._context.get('no_variant_attributes_price_extra'))

            if uom:
                price = product.uom_id._compute_price(price, uom)
                if product.depends:
                    price += product.get_product_extra_price(uom)
            # Convert from current user company currency to asked one
            # This is right cause a field cannot be in more than one currency
            if currency:
                price = price_currency._convert(price, currency, company, date)

            prices[product.id] = price

        return prices

    @api.model
    def get_product_extra_price(self, uom):
        othermodule_price = 0.0
        for modulename in self.depends.split(','):
            module_obj = self.search([('technical_name', '=', modulename), ('version', '=', self.version)], limit=1)
            if module_obj and module_obj.exists():
                othermodule_price += module_obj.uom_id._compute_price(module_obj['list_price'], uom)
        return othermodule_price
