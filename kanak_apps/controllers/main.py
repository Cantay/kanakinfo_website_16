# -*- coding: utf-8 -*-
import logging
import os
import shutil
import json
import requests
from typing import Any, Dict, List, Optional, Tuple
from odoo import http
from odoo.exceptions import UserError, AccessError, MissingError
from odoo.http import content_disposition, request, serialize_exception, route
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers import portal
from odoo.tools.config import get_ir_config_parameter

AVALABLE_VERSION = [
    '6.0', '7.0', '8.0', '9.0', '10.0', '11.0', '12.0', '13.0', '14.0', '15.0', '16.0', '17.0', '18.0', '19.0'
]
_logger = logging.getLogger(__name__)


class KanakApp(WebsiteSale):
    @http.route([
        '/shop',
        '/shop/page/<int:page>',
        '/shop/category/<model("product.public.category"):category>',
        '/shop/category/<model("product.public.category"):category>/page/<int:page>',
    ], type='http', auth="public", website=True, sitemap=False)
    def shop(self, page: int = 0, category=None, search: str = '', min_price: float = 0.0, max_price: float = 0.0,
             ppg: bool = False, **post: Any) -> http.Response:
        return request.redirect('/apps')

    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs) -> http.Response:
        product_id = product._get_first_possible_variant_id()
        vproduct = request.env['product.product'].browse(product_id)
        if vproduct:
            if 'theme' in vproduct.technical_name:
                rurl = f'/apps/themes/{vproduct.version}/{vproduct.technical_name}'
                return request.redirect(rurl)
            else:
                rurl = f'/apps/modules/{vproduct.version}/{vproduct.technical_name}'
                return request.redirect(rurl)
        return request.redirect('/apps')

    @http.route(['/shop/product/<string:product>'], type='http', auth="public", website=True, sitemap=True)
    def old_url_product(self, product, category='', search='', **kwargs) -> http.Response:
        product = request.env['product.template'].search([]).filtered(lambda x: x.old_url_product == product)[:1]
        if not product.exists():
            return request.redirect('/apps')
        product_id = product._get_first_possible_variant_id()
        vproduct = request.env['product.product'].browse(product_id)
        if vproduct:
            if 'theme' in vproduct.technical_name:
                rurl = f'/apps/themes/{vproduct.version}/{vproduct.technical_name}'
                return request.redirect(rurl)
            else:
                rurl = f'/apps/modules/{vproduct.version}/{vproduct.technical_name}'
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
    def kanakapps(self, mtype: str = '', price: str = '', series: str = '', category: str = '',
                  search: str = '', page: int = 0, ppg: int = 20, order: str = '', **post: Any) -> http.Response:
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
        is_top_
