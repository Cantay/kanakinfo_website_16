# -*- coding: utf-8 -*-

from odoo import fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    type_of_business = fields.Char(string="Type Of Business")
    about_us = fields.Char(string="How did you here about us?")
    your_role = fields.Char(string="Your Role")
    is_netsuite_lead = fields.Boolean()
