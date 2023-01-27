# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class kanakWebsite(http.Controller):

	@http.route(['/odoo-erp-services'], type='http', auth="public", website=True)
	def odoo_developer(self, **post):
		return request.render("kanak_website.odoo_erp_services", {})

	@http.route(['/odooservice-thankyou'], type='http', auth="public", methods=['POST'], website=True)
	def odoo_erp_service(self, **post):
		if 'g-recaptcha-response' in post and request.website.is_captcha_valid(post['g-recaptcha-response']):
			post.pop('g-recaptcha-response')
			tag = request.env['crm.tag'].sudo()
			lead_tag = tag.search([('name', '=', 'Odoolandingpage')], limit=1)
			if not lead_tag:
				lead_tag = tag.create({
					'name': 'Odoolandingpage'
					})
			crm = request.env['crm.lead']
			values = {
				'name': 'Odoo landing page Lead',
				'contact_name':post.get('name'),
				'phone': post.get('mobile'),
				'email_from': post.get('email'),
				'description': post.get('question'),
				'tag_ids': [(4, lead_tag.id)],
			}
			crm.sudo().create(values)
			return request.render("kanak_website.tmp_thank_you_form", {})
		return request.redirect('/odoo-erp-services')


	