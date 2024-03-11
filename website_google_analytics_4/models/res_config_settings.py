# Copyright © 2021 Garazd Creation (<https://garazd.biz>)
# @author: Yurii Razumovskyi (<support@garazd.biz>)
# @author: Iryna Razumovska (<support@garazd.biz>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.html).

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ga4_debug_mode = fields.Boolean(
        related='website_id.ga4_debug_mode',
        readonly=False,
    )

    google_analytics_4_key = fields.Char(
        string='Google Analytics 4 Key',
    )

    @api.depends('google_analytics_4_key')
    def _compute_has_google_analytics_4(self):
        for record in self:
            record.has_google_analytics_4 = bool(record.google_analytics_4_key)

    has_google_analytics_4 = fields.Boolean(
        string='Google Analytics 4',
        compute='_compute_has_google_analytics_4',
        store=True,
    )

    def _inverse_has_google_analytics_4(self):
        for record in self:
            if not record.has_google_analytics_4:
                record.google_analytics_4_key = False

    def set_has_google_analytics_4(self):
        for record in self:
            if record.has_google_analytics_4:
                record.google_analytics_4_key = record.google_analytics_4_key or ''
            else:
                record.google_analytics_4_key = False
        return True
