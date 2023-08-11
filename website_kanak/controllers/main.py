# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers import portal
from odoo.addons.website.controllers.form import WebsiteForm
import json
import werkzeug
from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment


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

    @http.route('/frappe-healthcare', auth="public", website=True)
    def frappe_healthcare(self, **kw):
        return http.request.render('website_kanak.frappe_healthcare_page', {})

    @http.route(['/frappe-lms'],type='http', auth="public", website=True)
    def frappe_lms(self, **post):
        return request.render('website_kanak.frappe_lms_page', {})

    @http.route(['/frappe-hrms'],
                type='http', auth="public", website=True)
    def frappe_hrms(self, **post):
        return request.render('website_kanak.frappe_hr_page', {})


    @http.route('/odoo-training', auth='public', website=True)
    def odoo_training(self, **kw):
        return http.request.render('website_kanak.odoo_training_form_view',{})

    
    @http.route('/netsuite-services' , auth="public", website=True)
    def netsuite_webpage(self, **kw):
        return http.request.render('website_kanak.tmp_netsuit_page',{})

    @http.route('/netsuite-support', auth='public', website=True)
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


    # @http.route(['/odoo-erp-services'], type='http', auth="public", website=True)
    # def odoo_developer(self, **post):
    #     return request.render("website_kanak.odoo_erp_services", {})

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

    @http.route(['/joomla-development-services'], type='http', auth="public", website=True)
    def busineess_bi_joomla(self, **post):
        return request.render("website_kanak.busineess_bi_joomla", {})

    @http.route(['/request-customization'],
                type='http', auth="public", website=True)
    def request_customization(self, **post):
        return request.render('website_kanak.request_customization', {})

    @http.route(['/kanak-Our-Services'],
                type='http', auth="public", website=True)
    def kanak_Our_Services(self, **post):
        return request.redirect('/our-services')

    @http.route(['/our-services'],
                type='http', auth="public", website=True)
    def Our_Services(self, **post):
        return request.render('website_kanak.kanak_Our_Services', {})

    @http.route(['/php-development-services'],
                type='http', auth="public", website=True)
    def service_web_php(self, **post):
        return request.render("website_kanak.service_web_php", {})

    @http.route(['/prestashop-development-services'],
                type='http', auth="public", website=True)
    def busineess_bi_presta(self, **post):
        return request.render("website_kanak.busineess_bi_presta", {})

    @http.route(['/seo-services'],
                type='http', auth="public", website=True)
    def service_digital_seo(self, **post):
        return request.render("website_kanak.service_digital_seo", {})

    @http.route(['/seo-smo-service-packages'],
                type='http', auth="public", website=True)
    def service_digital_seo_smo_value_packages(self, **post):
        return request.render("website_kanak.service_digital_seo-smo-value-packages", {})

    @http.route(['/smo-services'],
                type='http', auth="public", website=True)
    def service_digital_smo(self, **post):
        return request.render("website_kanak.service_digital_smo", {})

    @http.route(['/erp-solutions'],
                type='http', auth="public", website=True)
    def busineess_bi_erp_sol(self, **post):
        return request.render("website_kanak.busineess_bi_erp_sol", {})

    @http.route(['/terms-and-condition'],
                type='http', auth="public", website=True)
    def terms_condition(self, **post):
        return request.render('website_kanak.terms_and_condition', {})

    @http.route(['/linkbuilding-services'],
                type='http', auth="public", website=True)
    def service_digital_linkbuilding(self, **post):
        return request.render("website_kanak.service_digital_linkbuilding", {})

    @http.route(['/website-designing-services'],
                type='http', auth="public", website=True)
    def service_web_design(self, **post):
        return request.render("website_kanak.service_web_design", {})


class WebsiteForm(WebsiteForm):
    @http.route('/website_form/<string:model_name>', type='http', auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        if model_name == 'crm.lead':
            if 'g-recaptcha-response' in kwargs and request.website.is_captcha_valid(kwargs['g-recaptcha-response']):
                res = super(WebsiteForm, self).website_form(model_name, **kwargs)
                if kwargs.get('g-recaptcha-response', False):
                    kwargs.pop('g-recaptcha-response')
                if request.session.get('form_builder_id'):
                    crm_id = request.env['crm.lead'].sudo().browse(int(request.session.get('form_builder_id')))
                    crm_id.sudo().write({'odoo_version': kwargs.get('odoo_version', False),
                                         'subject_type': kwargs.get('subject_type', False),
                                         'skype_hangout': kwargs.get('skype_hangout', '')
                                         })
                    return res
                else:
                    return json.dumps(False)
            else:
                return json.dumps(False)
        if model_name != 'crm.lead':
            print("model_name---------", model_name, kwargs)
            res = super(WebsiteForm, self).website_form(model_name, **kwargs)
        return res



# class WebsiteHrRecruitmentInherit(WebsiteHrRecruitment):

#     @http.route()
#     def jobs(self, country=None, department=None, office_id=None, **kwargs):
#         res = super(WebsiteHrRecruitmentInherit, self).jobs(
#             country=country, department=department, office_id=office_id)
#         if kwargs.get('jobs'):
#             filter_job = res.qcontext.get('jobs').search(
#                 [("id", "=", int(kwargs.get('jobs')))])
#             res.qcontext['jobs'] = filter_job
#         return res

#     @http.route('/jobs/detail/<string:url>', type='http', auth="public", website=True)
#     def jobs_detail(self, url, **kwargs):
#         if url:
#             url = str('/jobs/detail/') + str(url)
#         job = request.env['hr.job'].search([('website_url', '=', url)], limit=1)
#         if not job:
#             raise werkzeug.exceptions.NotFound()
#         return request.render("website_hr_recruitment.detail", {
#             'job': job,
#             'main_object': job,
#         })

    # @http.route('/jobs/apply/<string:url>', type='http', auth="public", website=True)
    # def jobs_apply(self, url, **kwargs):
    #     error = {}
    #     default = {}
    #     job = request.env['hr.job'].search([('job_apply_website_url', '=', url)], limit=1)
    #     if not job:
    #         raise werkzeug.exceptions.NotFound()
    #     if 'website_hr_recruitment_error' in request.session:
    #         error = request.session.pop('website_hr_recruitment_error')
    #         default = request.session.pop('website_hr_recruitment_default')
    #     return request.render("website_hr_recruitment.apply", {
    #         'job': job,
    #         'error': error,
    #         'default': default,
    #     })
