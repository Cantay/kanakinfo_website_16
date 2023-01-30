# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class KanakErpNextWebsite(http.Controller):

	@http.route(['/erpnext-services'], type='http', auth="public", website=True)
	def erp_next_page(self, **post):
		return request.render("kanak_website_erpnext.erpnext_services", {})


	@http.route(['/erpnext-service-thankyou'], type='http', auth="public", methods=['POST'], website=True)
	def erpnext_service(self, **post):
		if 'g-recaptcha-response' in post and request.website.is_captcha_valid(post['g-recaptcha-response']):
			post.pop('g-recaptcha-response')
			tag = request.env['crm.tag'].sudo()
			lead_tag = tag.search([('name', '=', 'ErpNextlandingpage')], limit=1)
			if not lead_tag:
				lead_tag = tag.create({
					'name': 'ErpNextlandingpage'
					})
			crm = request.env['crm.lead']
			values = {
				'name': 'ErpNext landing page Lead',
				'contact_name':post.get('name'),
				'phone': post.get('mobile'),
				'email_from': post.get('email'),
				'description': post.get('question'),
				'tag_ids': [(4, lead_tag.id)],
			}
			crm.sudo().create(values)
			return request.render("kanak_website_erpnext.tmp_thank_you_form", {})
		return request.redirect('/erpnext-services')



	