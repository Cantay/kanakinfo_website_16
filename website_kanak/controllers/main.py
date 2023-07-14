# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers import portal


class WebsiteKanak(http.Controller):

    @http.route(['/about-us'],
                type='http', auth="public", website=True)
    def about_us(self, **post):
        return request.render('website_kanak.kanak_aboutus', {})
    
    @http.route(['/privacy-policy'],
                type='http', auth="public", website=True)
    def privacy_policy(self, **post):
        return request.render('website_kanak.privacy_policy_page', {})
    
    @http.route(['/testimonial'], type='http', auth="public", website=True)
    def testimonial(self, **post):
        return request.render('website_kanak.testimonial_page', {})

    @http.route(['/engagement-models'], type='http', auth="public", website=True)
    def engagement_models(self, **post):
        return request.render('website_kanak.engagement_model_page', {})
    
    @http.route(['/odoo-integration-services'],
                type='http', auth="public", website=True)
    def busineess_odoo_openerp_int(self, **post):
        return request.render('website_kanak.busineess_odoo_openerp_int', {})

    @http.route('/odoo-development-services', type='http', auth="public", website=True)
    def busineess_odoo_openerp_dev(self, **post):
        return request.render('website_kanak.busineess_odoo_openerp_dev')

    @http.route(['/our-team'], type='http', auth="public", website=True)
    def our_team(self, **post):
        return request.render('website_kanak.our_team_page', {})

    @http.route(['/hire-odoo-developer'],
                type='http', auth="public", website=True)
    def busineess_odoo_openerp_developer(self, **post):
        return request.render('website_kanak.tmp_odoo_developer', {})

    @http.route(['/netsuite-implementation'], type='http', auth="public", website=True)
    def netsuit_implementation_page(self, **post):
        return request.render("website_kanak.tmp_netsuit_implementation_page", {})

    @http.route(['/netsuite-licensing'], type='http', auth="public", website=True)
    def netsuit_licensing_page(self, **post):
        return request.render("website_kanak.tmp_netsuit_licensing_page", {})


    @http.route(['/erpnext-services'],
                type='http', auth="public", website=True)
    def busineess_bi_erp_sol_next(self, **post):
        return request.render("website_kanak.busineess_bi_erp_sol_next", {})

    @http.route(['/frappe-books-accounting-system'],type='http', auth="public", website=True)
    def frappe_books(self, **post):
        return request.render('website_kanak.frappe_book_page', {})

    @http.route('/frappe_healthcare', auth="public", website=True)
    def frappe_healthcare(self, **kw):
        return http.request.render('website_kanak.frappe_healthcare_page', {})

    @http.route(['/frappe-lms'],type='http', auth="public", website=True)
    def frappe_lms(self, **post):
        return request.render('website_kanak.frappe_lms_page', {})

    @http.route(['/frappe-hrms'],
                type='http', auth="public", website=True)
    def frappe_hrms(self, **post):
        return request.render('website_kanak.frappe_hr_page', {})


    @http.route('/odoo_Training', auth='public', website=True)
    def odoo_training(self, **kw):
        return http.request.render('website_kanak.odoo_training_form_view',{})

    
    @http.route('/netsuite_webpage' , auth="public", website=True)
    def netsuite_webpage(self, **kw):
        return http.request.render('website_kanak.tmp_netsuit_page',{})

    @http.route('/netsuite_support', auth='public', website=True)
    def netsuite_support_webpage(self, **kw):
        return http.request.render('website_kanak.tmp_netsuit_support_page',{})
        

    @http.route(['/odoo-installation-services'],
                type='http', auth="public", website=True)
    def busineess_odoo_openerp_install(self, **post):
        return request.render('website_kanak.busineess_odoo_openerp_install', {})
    
    @http.route(['/odoo-themes'],
                type='http', auth="public", website=True)
    def busineess_odoo_openerp_theme(self, **post):
        return request.render('website_kanak.busineess_odoo_openerp_theme', {})
    
    @http.route(['/odoo-customization-implementation-services'],
                type='http', auth="public", website=True)
    def busineess_odoo_openerp_imp(self, **post):
        return request.render('website_kanak.tmp_odoo_Implementation', {})
    
    @http.route(['/ios-app-development-company'],
                type='http', auth="public", website=True)
    def busineess_bi_mobile_ioss(self, **post):
        return request.render("website_kanak.busineess_bi_mobile_ios", {})

    @http.route(['/android-app-development-company'],
                type='http', auth="public", website=True)
    def busineess_bi_mobile_android(self, **post):
        return request.render("website_kanak.busineess_bi_mobile_android", {})

    @http.route(['/geomarking-employee-attendance-app'],
                type='http', auth="public", website=True)
    def geomarking(self, **post):
        return request.render('website_kanak.geomarking_page', {})

    @http.route(['/odooshoppe'],
                type='http', auth="public", website=True)
    def odooshoppe(self, **post):
        return request.render('website_kanak.odoo_shoppe_page', {})
    
    @http.route(['/netsuite-consultant'], type='http', auth="public", website=True)
    def netsuit_consultant_page(self, **post):
        return request.render("website_kanak.tmp_netsuit_consultant_page", {})
    
    @http.route(['/frappe-hrms'],
                type='http', auth="public", website=True)
    def frappe_hrms(self, **post):
        return request.render('website_kanak.frappe_hr_page', {})


    @http.route(['/jobs/search'], type='json', auth="public", website=True)
    def job_search(self, **post):
        jobs_list = {}
        jobs = request.env['hr.job'].sudo().search(
            [('department_id', '=', post.get('department_id')),
             ('website_published', '=', True)])
        jobs_list['j_list'] = request.env["ir.ui.view"]._render_template(
            "website_kanak.jobs_show_website", {'jobs': jobs})
        return jobs_list


    @http.route(['/odoo-erp-services'], type='http', auth="public", website=True)
    def odoo_developer(self, **post):
        return request.render("website_kanak.odoo_erp_services", {})

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
            return request.render("website_kanak.tmp_thank_you_form", {})
        return request.redirect('/odoo-erp-services')
