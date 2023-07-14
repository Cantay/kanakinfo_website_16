# -*- coding: utf-8 -*-
import logging
import os
import base64
import lxml.html
import errno
import shutil
from odoo import api, fields, models, modules, tools, _

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
    def manifest_2_odoo(self, info, repository_branch, product_id=False):
        product_attribute_id = self.env['product.attribute'].sudo().search([
            ('name', '=', 'Odoo Version')], limit=1)
        if not product_attribute_id:
            product_attribute_id = self.env['product.attribute'].sudo().create({
                'name': 'Odoo Version'
            })
        if repository_branch:
            branch = repository_branch.github_url.split('#')[1]
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
                                'value_ids': [(4, attribut_value_id.id)],
                                })]
                               })
            # values.update({'product_tmpl_id': product_id.id})

        return values

    @api.model
    def create_or_update_from_manifest(self, info, repository_branch, full_module_path):
        ProductTemplate = self.env['product.template'].sudo()
        branch = repository_branch.github_url.split('#')[1]
        technical_name = info['technical_name']
        product_id = ProductTemplate.search([('technical_name', '=', technical_name)])
        if not product_id:
            product_id = ProductTemplate.create(self.manifest_2_odoo(info, repository_branch))
        else:
            product_id.write(self.manifest_2_odoo(info, repository_branch, product_id))
        attribut_value_id = False
        if repository_branch:
            attribut_value_id = self.env['product.attribute.value'].sudo().search([('name', '=', branch)])
        rec_ids = self.env['product.template.attribute.value'].search([('attribute_id', '=', attribut_value_id.attribute_id.id), ('product_attribute_value_id', '=', attribut_value_id.id)])
        module_version = self.search([
            ('technical_name', '=', str(technical_name)),
            ('product_template_variant_value_ids', 'in', rec_ids.ids)], limit=1)

        theme_image_path = False
        banner_path = False
        icon_path = False
        resize = False
        product_image = False
        theme_image = False
        banner_image = False
        license = False
        if info.get('images'):
            full_current_icon_path = os.path.join(
                full_module_path, info.get('images')[0])
            if os.path.exists(full_current_icon_path):
                banner_path = full_current_icon_path
            if info.get('images') and len(info.get('images')) > 1:
                full_current_theme_image_path = os.path.join(
                full_module_path, info.get('images')[1])
                if os.path.exists(full_current_theme_image_path):
                    theme_image_path = full_current_theme_image_path
        for current_icon_path in self._ICON_PATH:
            full_current_icon_path = os.path.join(
                full_module_path, current_icon_path, 'icon.png')
            if os.path.exists(full_current_icon_path):
                icon_path = full_current_icon_path
                resize = True
                break
        if theme_image_path:
            image_enc = False
            try:
                with open(theme_image_path, 'rb') as f:
                    image = f.read()
                image_enc = base64.b64encode(tools.image_process(image, output_format='gif'))
            except Exception:
                _logger.warning("Unable to read or resize %s", banner_path)
            theme_image = image_enc
        if banner_path:
            image_enc = False
            try:
                with open(banner_path, 'rb') as f:
                    image = f.read()
                image_enc = base64.b64encode(tools.image_process(image, output_format='gif'))
            except Exception:
                _logger.warning("Unable to read or resize %s", banner_path)
            banner_image = image_enc
        if icon_path:
            image_enc = False
            try:
                with open(icon_path, 'rb') as f:
                    image = f.read()
                if resize:
                    image_enc = base64.b64encode(tools.image_process(image, output_format='png'))
                else:
                    image_enc = base64.b64encode(image)
            except Exception:
                _logger.warning("Unable to read or resize %s", icon_path)
            product_image = image_enc
        else:
            # Set the default icon
            try:
                with open(os.path.join(
                        os.path.dirname(__file__),
                        '../data/kanak.png'), 'rb') as f:
                    image = base64.b64encode(f.read())
                    product_image = image
            except Exception as e:
                _logger.error(
                    'Unable to read the icon image, error is %s', e)

        index_path = False
        description_rst_html = False
        full_current_index_path = os.path.join(full_module_path, self._INDEX_HTML_PATH, 'index.html')
        license_path = os.path.join(full_module_path, 'LICENSE')
        if os.path.exists(full_current_index_path):
            index_path = full_current_index_path

        def copytree(src, dst, symlinks=False, ignore=None):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            for item in os.listdir(src):
                s = os.path.join(src, item)
                d = os.path.join(dst, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, symlinks, ignore)
                else:
                    shutil.copy2(s, d)

        dest_path = modules.get_module_resource('kanak_github_connector') + '/static/apps/'
        if repository_branch:
            dest_path = dest_path + str(branch) + '/' + str(technical_name) + '/'

        copytree(full_module_path + '/static/description/', dest_path)
        if index_path:
            with open(index_path, 'rb') as desc_file:
                doc = desc_file.read()
                html = lxml.html.document_fromstring(doc)
                for element, attribute, link, pos in html.iterlinks():
                    if element.get('src') and not '//' in element.get('src') and not 'static/' in element.get('src'):
                        element.set('src', "/kanak_github_connector/static/apps/%s/%s/%s" % (branch, info['technical_name'], element.get('src')))
                description_rst_html = tools.html_sanitize(lxml.html.tostring(html))
        else:
            description_rst_html = info['description']

        if os.path.exists(license_path):
            with open(license_path, 'rb') as desc_file:
                license = desc_file.read()
        module_version.write({
            'repository_id': repository_branch.id,
            'version': branch,
            'description_rst_html': description_rst_html,
            'image_1920': product_image,
            'banner_image': banner_image,
            'theme_image': theme_image,
            'description_sale': info.get('summary', ''),
            'license': license or ''
        })
