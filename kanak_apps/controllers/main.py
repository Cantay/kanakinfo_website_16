# -*- coding: utf-8 -*-

import os
import shutil

from odoo import http
from odoo.http import request
from werkzeug.exceptions import NotFound
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import UserError, AccessError, MissingError
from odoo.http import content_disposition
from odoo.addons.portal.controllers import portal
AVALABLE_VERSION = ['6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0']


class KanakApp(WebsiteSale):
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=False)
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        return request.redirect('/apps')

    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs):
        product_id = product._get_first_possible_variant_id()
        vproduct = request.env['product.product'].browse(product_id)
        if vproduct:
            if 'theme' in vproduct.technical_name:
                rurl = '/apps/themes/' + vproduct.version + '/' + vproduct.technical_name
                return request.redirect(rurl)
            else:
                rurl = '/apps/modules/' + vproduct.version + '/' + vproduct.technical_name
                return request.redirect(rurl)
        return request.redirect('/apps')

    @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=False)
    def old_product(self, product, category='', search='', **kwargs):
        product_id = product._get_first_possible_variant_id()
        vproduct = request.env['product.product'].browse(product_id)
        if vproduct:
            if 'theme' in vproduct.technical_name:
                rurl = '/apps/themes/' + vproduct.version + '/' + vproduct.technical_name
                return request.redirect(rurl)
            else:
                rurl = '/apps/modules/' + vproduct.version + '/' + vproduct.technical_name
                return request.redirect(rurl)
        return request.redirect('/apps')

    @http.route([
        '/apps',
        '/apps/<string:mtype>',
        '/apps/<string:mtype>/browse',
        '/apps/<string:mtype>/browse/page/<int:page>',
        '/apps/<string:mtype>/category/<string:category>',
        '/apps/<string:mtype>/category/<string:category>/browse',
        '/apps/<string:mtype>/category/<string:category>/browse/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=False)
    def kanakapps(self, mtype='', price='', series='', category='', search='', page=0, ppg=5, order='', **post):
        if not self.check_is_found_or_not(mtype, category):
            raise NotFound()
        if not mtype:
            mtype = 'modules'
        values = {
            'is_apps_header': True
        }
        values['categories'] = request.env['product.public.category'].search([])
        pricelist = request.website.get_current_pricelist()
        values['pricelist'] = pricelist
        combination = None
        vurl = '/apps'
        values['mtype'] = mtype
        is_top_chart_url = ''
        values['is_browser'] = request.httprequest.path
        values['is_browser_record'] = True
        values['category'] = category
        if '/browse' in request.httprequest.path:
            is_top_chart_url = request.httprequest.path.split('/browse')[0]
        else:
            is_top_chart_url = request.httprequest.path.split('/page')[0]
            if mtype not in is_top_chart_url:
                is_top_chart_url = is_top_chart_url + '/' + mtype + '/browse'
            else:
                is_top_chart_url = is_top_chart_url + '/browse'
        values['is_top_chart_url'] = is_top_chart_url
        if mtype:
            vurl = vurl + '/' + str(mtype)
            if category:
                vurl = vurl + '/category/' + category
            if '/browse' in request.httprequest.path:
                vurl = vurl + '/browse'
            if '/browse' not in request.httprequest.path:
                values['is_browser_record'] = False
                vurl = vurl + '/browse'
            vkeep = QueryURL(vurl, **{
                'series': series,
                'price': price,
                'search': search,
                'order': order
            })
            values['vkeep'] = vkeep
            values['order'] = order
            values['price'] = price
            values['series'] = series
            values['search'] = search
        if series in AVALABLE_VERSION:
            product_attribute_id = request.env['product.attribute'].sudo().search([('name', '=', 'Odoo Version')], limit=1)
            if product_attribute_id:
                attribut_value_id = request.env['product.attribute.value'].sudo().search([('attribute_id', '=', product_attribute_id.id), ('name', '=', series)])
                combination = request.env['product.template.attribute.value'].sudo().search([('attribute_id', '=', attribut_value_id.attribute_id.id), ('product_attribute_value_id', '=', attribut_value_id.id)])
        domain = self.search_domain_apps(mtype=mtype, price=price, series=series, search=search, category=category)
        products = request.env['product.template'].search(domain, order=self.get_order_by_products(order))
        if combination:
            product_tmp_ids = combination.mapped('product_tmpl_id').ids
            products = products.filtered(lambda x: x.id in product_tmp_ids)
        if not combination and series in AVALABLE_VERSION:
            products = request.env['product.template']
        values['products'] = products
        values['get_specific_combination'] = self.get_specific_combination
        values['search_count'] = len(products)
        values['combination'] = combination
        if '/browse' not in request.httprequest.path:
            values['top_sales_apps'] = products.sorted(lambda p: p.sudo().sales_count, reverse=True)[:4]
            values['news_apps'] = products.sorted(lambda p: p.create_date, reverse=True)[:4]
            values['most_downloads'] = products.sorted(lambda p: p.sudo().download_count, reverse=True)[:4]
            return request.render('kanak_apps.top_carts_tmpl', values)
        website = request.env['website'].get_current_website()
        if ppg:
            try:
                ppg = int(ppg)
                post['ppg'] = ppg
            except ValueError:
                ppg = False
        if not ppg:
            ppg = website.shop_ppg or 20
        url_args = {}
        if 'series' in values and values.get('series', ''):
            url_args['series'] = values.get('series', '')
        if 'order' in values and values.get('order', ''):
            url_args['order'] = values.get('order', '')
        if 'price' in values and values.get('price', ''):
            url_args['price'] = values.get('price', '')
        if 'search' in values and values.get('search', ''):
            url_args['search'] = values.get('search', '')
        pager = website.pager(url=is_top_chart_url + '/browse', total=values['search_count'], page=page, step=ppg, scope=7, url_args=url_args)
        offset = pager['offset']
        products = values['products'][offset:offset + ppg]
        values['products'] = products
        values['pager'] = pager
        return request.render('kanak_apps.apps_list', values)

    def check_is_found_or_not(self, mtype=None, category=None):
        if mtype and mtype not in ['modules', 'themes']:
            return False
        if category:
            categ_id = request.env['product.public.category'].search([('name', '=', category)], limit=1)
            if not categ_id:
                return False
        return True

    def get_specific_combination(self, combination, product_tmpl_id=None):
        return combination.filtered(lambda x: x.product_tmpl_id.id == product_tmpl_id)

    def search_domain_apps(self, mtype='', price='', series='', search='', category=''):
        domain = [('is_published', '=', True), ('sale_ok', '=', True)]
        if category:
            category_id = request.env['product.public.category'].search([('name', '=', category)], limit=1)
            domain = domain + [('public_categ_ids', 'child_of', category_id.id)]
        if price:
            if price == 'Free':
                domain = domain + [('list_price', '=', 0.0)]
            if price == 'Paid':
                domain = domain + [('list_price', '>', 0)]
        if search:
            domain = domain + ['|', ('name', 'like', search), ('technical_name', 'like', search)]
        if mtype != 'themes':
            domain = domain + [('technical_name', 'not like', 'theme')]
        if mtype == 'themes':
            domain = domain + [('technical_name', 'like', 'theme')]
        return domain

    def get_order_by_products(self, order=''):
        if not order:
            xorder = request.env['website'].get_current_website().shop_default_sort
            return 'is_published desc, %s, id desc' % xorder
        if order == 'Relevance':
            return 'sales_count desc'
        if order == 'Newest':
            return 'create_date desc'
        if order == 'Downloads':
            return 'download_count desc'
        if order == 'Name':
            return 'technical_name asc'
        if order == 'Ratings':
            return 'rating_avg desc'
        if order == 'Lowest+Price':
            return 'list_price asc'
        if order == 'Highest+Price':
            return 'list_price desc'

    @http.route(['/apps/<string:mtype>/<string:version>/<string:modulename>'], type='http', auth="public", website=True, sitemap=False)
    def AppsDetails(self, mtype='', version='', modulename='', **post):
        if not self.check_is_found_or_not(mtype) or (version and version not in AVALABLE_VERSION):
            raise NotFound()
        product = request.env['product.template'].search([('technical_name', '=', modulename)], limit=1)
        product_attribute_id = request.env['product.attribute'].sudo().search([('name', '=', 'Odoo Version')], limit=1)
        attribut_value_id = request.env['product.attribute.value'].sudo().search([('attribute_id', '=', product_attribute_id.id), ('name', '=', version)])
        combination = request.env['product.template.attribute.value'].sudo().search([('attribute_id', '=', attribut_value_id.attribute_id.id), ('product_attribute_value_id', '=', attribut_value_id.id), ('product_tmpl_id', '=', product.id)], limit=1)
        pricelist = request.website.get_current_pricelist()
        values = {
            'version': version,
            'mtype': mtype,
            'combination': combination,
            'product': product,
            'pricelist': pricelist
        }
        return request.render('kanak_apps.appdetails', values)

    @http.route('/download/app', type="http", auth="public", website=True)
    def DownloadAPPS(self, **post):
        product_id = request.env['product.product'].browse(int(post.get('product_id')))
        if product_id:
            if not product_id.list_price and product_id.product_template_attribute_value_ids and \
                product_id.product_template_attribute_value_ids[0].name == post.get('version', '') and \
                    product_id.technical_name == post.get('module_name', ''):
                modulename = post.get('module_name', '')
                version = post.get('version', '')
                get_param = request.env['ir.config_parameter'].sudo().get_param
                repo_path = get_param('github_repo_local_path')

                path = self.create_app_zip(repo_path, version, modulename)
                if os.path.exists(path + '.zip'):
                    product_tmp_id = product_id.product_tmpl_id
                    counter = product_id.product_tmpl_id.download_count + 1
                    product_tmp_id.sudo().write({
                        'download_count': counter
                    })
                    filename = "%s-%s.zip" % (modulename, version)
                    zippath = '%s.zip' % (path)

                    bytes_data = ''
                    with open(zippath, "rb") as f:
                        bytes_data = f.read()
                    os.remove(zippath)
                    return request.make_response(
                        bytes_data,
                        headers=[
                            ('Content-Type', 'application/zip'),
                            ('Content-Disposition', content_disposition(filename))
                        ])
        raise NotFound()

    def create_app_zip(self, repo_path, version, modulename):
        modulepath = "%s/%s/%s" % (repo_path, version, modulename)
        zip_path = modulepath + "-%s" % version

        if not os.path.exists(modulepath):
            raise UserError("No module available!")
        shutil.make_archive(zip_path, 'zip', modulepath)

        return zip_path


class CustomerPortal(portal.CustomerPortal):
    @http.route([
        '/download/apps/modules/<string:version>/<string:modulename>/<int:order_id>',
        '/download/apps/themes/<string:version>/<string:modulename>/<int:order_id>'], type='http', auth="public", website=True)
    def DownloadPaidVersion(self, order_id, version=None, modulename=None, access_token=None, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
            if order_sudo.state in ['sale', 'done']:
                product_id = None
                for line in order_sudo.order_line:
                    if line.product_id and line.product_id.version == version and line.product_id.technical_name == modulename:
                        product_id = line.product_id
                if not product_id:
                    return request.redirect('/apps')
                if product_id:
                    get_param = request.env['ir.config_parameter'].sudo().get_param
                    repo_path = get_param('github_repo_local_path')

                    path = self.skcreate_app_zip(repo_path, product_id.version, product_id.technical_name)
                    if os.path.exists(path + '.zip'):
                        filename = "%s-%s.zip" % (product_id.version, product_id.technical_name)
                        zippath = '%s.zip' % (path)

                        bytes_data = ''
                        with open(zippath, "rb") as f:
                            bytes_data = f.read()
                        os.remove(zippath)
                        return request.make_response(
                            bytes_data,
                            headers=[
                                ('Content-Type', 'application/zip'),
                                ('Content-Disposition', content_disposition(filename))
                            ])
        except (AccessError, MissingError):
            return request.redirect('/apps')

    def skcreate_app_zip(self, repo_path, version, modulename):
        modulepath = "%s/%s/%s" % (repo_path, version, modulename)
        zip_path = modulepath + "-%s" % version

        if not os.path.exists(modulepath):
            raise UserError("No module available!")
        shutil.make_archive(zip_path, 'zip', modulepath)

        return zip_path
