# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

import requests
import json


class website(models.Model):
    _inherit = 'website'

    recaptcha_site_key = fields.Char('reCAPTCHA Site Key', default='6LchkgATAAAAAAdTJ_RCvTRL7_TTcN3Zm_YXB39s')
    recaptcha_private_key = fields.Char('reCAPTCHA Private Key', default='6LchkgATAAAAADbGqMvbRxHbTnTEkavjw1gSwCng')

    def is_captcha_valid(self, response):
        for website in self:
            get_res = {'secret': website.recaptcha_private_key,
                       'response': response}
            try:
                response = requests.get('https://www.google.com/recaptcha/api/siteverify', params=get_res)
            except Exception:
                raise ValidationError(_('Invalid Data!.'))
            res_con = response.json()
            if res_con.get('success'):
                return True
        return False


    def get_our_recent_work(self):
        works = self.env['our.recent.work'].sudo().search([])
        return works


    def latest_blog_posts(self):
        latest_posts = self.env['blog.post'].sudo().search([('website_published', '=', True)], limit=6, order="post_date desc")
        return latest_posts

    def update_shop_menu_sequence(self):
        shop_record = self.env.ref('website_sale.menu_shop')
        if shop_record:
            shop_record.sequence = 3000
        blog_record = self.env.ref('website_blog.menu_blog')
        if blog_record:
            blog_record.sequence = 4000
        menus = self.env['website.menu'].search([('name', '=', ['Shop','Blog'])])
        if menus:
            for m in menus:
                if m.name == 'Shop':
                    m.sequence = 3000
                if m.name == 'Blog':
                    m.sequence = 4000




class OurRecentWork(models.Model):
    _name = 'our.recent.work'
    _description = 'Kanak Recent Projects'
    _order = 'sequence'

    name = fields.Char('Name')
    image = fields.Binary('Banner Image', help="Banner image size must be 450px x 300x.")
    link = fields.Char('Link')
    date = fields.Date('Date')
    description = fields.Char('Description')
    sequence = fields.Integer('Sequence', default=10)


class Lead(models.Model):
    _inherit = "crm.lead"

    subject_type = fields.Selection(
        [('web_designing', 'Web Designing'), ('odoo_developer', 'Odoo Developer'),
         ('back-end_developer', 'Back-end Developer'), ('mobile_apps', 'Mobile Apps'),
         ('wordpress_deve', 'Wordpress'), ('magento_deve', 'Magento'),
         ('Shopify_q', 'Shopify'), ('designing_job', 'Designing Job'),
         ('any_other', 'Others'), ('moodle', 'Moodle'),
         ('oracle_netsuite', 'Oracle Netsuite')],
         string='Type Your Subject')

    odoo_version = fields.Selection([('v11', 'v11'), ('v10', 'v10'), ('v9', 'v9'), ('v8', 'v8'), ('v7', 'v7')], string='Odoo Version')
    skype_hangout = fields.Char(string="Skype / Hangout")
