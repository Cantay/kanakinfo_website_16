# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

from odoo.addons.website_hr_recruitment.controllers.main import WebsiteHrRecruitment

import base64


class NetSuitForm(http.Controller):

    @http.route(['/netsuite'], type='http', auth="public", website=True)
    def netsuit_form(self, **post):
        return request.render("kanak_website.tmp_netsuit_form", {})

    @http.route(['/odooservice'], type='http', auth="public", methods=['POST'], website=True)
    def odoo_erp_service(self, **post):
        if 'g-recaptcha-response' in post and request.website.is_captcha_valid(post['g-recaptcha-response']):
            post.pop('g-recaptcha-response')
            tag = request.env['crm.lead.tag'].sudo()
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

    @http.route([
        '/netsuite-services-thankyou',
        '/netsuite-implementation-thankyou',
        '/netsuite-consultant-thankyou',
        '/netsuite-licensing-thankyou',
        '/netsuite-support-thankyou',
        '/thank-you'], type='http', csrf=False, auth="public", methods=['POST'], website=True)
    def netsuit_form_submit(self, **post):
        if 'g-recaptcha-response' in post and request.website.is_captcha_valid(post['g-recaptcha-response']):
            post.pop('g-recaptcha-response')
            tag = request.env['crm.lead.tag'].sudo()
            lead_tag = tag.search([('name', '=', 'NetSuite')], limit=1)
            if not lead_tag:
                lead_tag = tag.create({
                    'name': 'NetSuite'
                })
            crm = request.env['crm.lead']
            country_id = False
            if post.get('country'):
                country = request.env['res.country'].search([
                    ('name', '=', post.get('country'))])
                if country:
                    country_id = country.id
            email = crm.sudo().create({
                'name': post.get('name'),
                'email_from': post.get('email'),
                'phone': post.get('phone'),
                'partner_name': post.get('company'),
                'country_id': country_id,
                'description': post.get('question'),
                'type_of_business': post.get('type_of_bussiness'),
                'your_role': post.get('your_role'),
                'about_us': post.get('about_us'),
                'is_netsuite_lead': True,
                'tag_ids': [(4, lead_tag.id)],
            })
            template_id = request.env.ref('kanak_website.email_template_crm_lead')
            template_id.sudo().send_mail(email.id, force_send=True)
            return request.render("kanak_website.tmp_thank_you_form", {})

    # New Pages Develpoed
    @http.route(['/odoo-implementation'], type='http', auth="public", website=True)
    def odoo_implementation(self, **post):
        return request.render("kanak_website.tmp_odoo_implementation", {})

    @http.route(['/odoo-developer'], type='http', auth="public", website=True)
    def odoo_developer(self, **post):
        return request.render("kanak_website.tmp_odoo_developer", {})

    @http.route(['/odoo-erp-services'], type='http', auth="public", website=True)
    def odoo_developer(self, **post):
        return request.render("kanak_website.odoo_erp_services", {})

    @http.route(['/netsuite-services'], type='http', auth="public", website=True)
    def netsuit_page(self, **post):
        return request.render("kanak_website.tmp_netsuit_page", {})

    @http.route(['/netsuite-implementation'], type='http', auth="public", website=True)
    def netsuit_implementation_page(self, **post):
        return request.render("kanak_website.tmp_netsuit_implementation_page", {})

    @http.route(['/netsuite-consultant'], type='http', auth="public", website=True)
    def netsuit_consultant_page(self, **post):
        return request.render("kanak_website.tmp_netsuit_consultant_page", {})

    @http.route(['/netsuite-licensing'], type='http', auth="public", website=True)
    def netsuit_licensing_page(self, **post):
        return request.render("kanak_website.tmp_netsuit_licensing_page", {})

    @http.route(['/netsuite-support'], type='http', auth="public", website=True)
    def netsuit_support_page(self, **post):
        return request.render("kanak_website.tmp_netsuit_support_page", {})

    @http.route(['/netsuite-webinar'], type='http', auth="public", website=True)
    def webinar_ceo(self, **post):
        return request.render("kanak_website.webinar_ceo_page", {})

    @http.route(['/thank-you-for-register'], type='http', auth="public", website=True)
    def thank_you_for_register(self, **post):
        webinar = request.env['ceo.webinar']
        email = webinar.sudo().create({
            'company_name': post.get('company_name'),
            'person_name': post.get('person_name'),
            'email': post.get('email'),
            'title': post.get('title_name'),
            'contact_number': post.get('contact_number'),
            'secoand_webinar': True,
        })
        template_id = request.env.ref(
            'kanak_website.email_template_webinar_ceo')
        template_id.sudo().send_mail(email.id, force_send=True)
        register_template_id = request.env.ref(
            'kanak_website.email_template_register_webinar')
        register_template_id.sudo().send_mail(email.id, force_send=True)
        return request.render("kanak_website.webinar_register_page", {})

    @http.route(['/jobs/search'], type='json', auth="public", website=True)
    def job_search(self, **post):
        jobs_list = {}
        jobs = request.env['hr.job'].sudo().search(
            [('department_id', '=', post.get('department_id')),
             ('website_published', '=', True)])
        jobs_list['j_list'] = request.env["ir.ui.view"].render_template(
            "kanak_website.jobs_show_website", {'jobs': jobs})
        return jobs_list


class WebsiteHrRecruitmentInherit(WebsiteHrRecruitment):

    @http.route()
    def jobs(self, country=None, department=None, office_id=None, **kwargs):
        res = super(WebsiteHrRecruitmentInherit, self).jobs(
            country=country, department=department, office_id=office_id)
        if kwargs.get('jobs'):
            filter_job = res.qcontext.get('jobs').search(
                [("id", "=", int(kwargs.get('jobs')))])
            res.qcontext['jobs'] = filter_job
        return res

    @http.route('/jobs/detail/<string:url>', type='http', auth="public", website=True)
    def jobs_detail(self, url, **kwargs):
        job = request.env['hr.job'].search([('website_url', '=', url)], limit=1)
        return request.render("website_hr_recruitment.detail", {
            'job': job,
            'main_object': job,
        })

    @http.route('/jobs/apply/<string:url>', type='http', auth="public", website=True)
    def jobs_apply(self, url, **kwargs):
        error = {}
        default = {}
        job = request.env['hr.job'].search([('website_url', '=', url)], limit=1)
        if 'website_hr_recruitment_error' in request.session:
            error = request.session.pop('website_hr_recruitment_error')
            default = request.session.pop('website_hr_recruitment_default')
        return request.render("website_hr_recruitment.apply", {
            'job': job,
            'error': error,
            'default': default,
        })
