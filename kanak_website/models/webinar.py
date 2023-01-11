# -*- coding: utf-8 -*-

from odoo import fields, models


class Webinar(models.Model):
    _name = 'ceo.webinar'
    _rec_name = 'person_name'

    company_name = fields.Char(string="Company Name")
    person_name = fields.Char(string="Person Name")
    email = fields.Char(string="Email")
    title = fields.Char(string="Title")
    contact_number = fields.Char(string="Contact Number")
    secoand_webinar = fields.Boolean()
