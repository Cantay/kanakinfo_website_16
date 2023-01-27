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
