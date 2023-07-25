# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Website Kanak Infosystems',
    'category': 'Ecommerce',
    'summary': 'Kanak Infosystems website',
    'website': 'http://www.kanakinfosystems.com',
    'version': '1.1',
    'depends': [
        'base',
        'website',
        'mass_mailing',
        'website_hr_recruitment',
        'website_crm',
        'kanak_apps',
        'website_custome_blog_url',
        'kanak_github_connector'],
    'data': [
        'security/ir.model.access.csv',
        'data/menu.xml',
        'views/kanak_backend_view.xml',
        'views/kanak_homepage.xml',
        'views/footer.xml',

        'views/aboutus.xml',
        'views/privacy_policy.xml',
        'views/testimonial_page.xml',
        'views/our_team.xml',
        'views/engagement_model.xml',
        'views/careers.xml',
        
        'views/odoo_integration.xml',
        'views/odoo_development.xml',
        'views/odoo_Installation.xml',
        'views/odoo_Themes.xml',
        'views/odoo_Implementation.xml',
        'views/Hire_Odoo_Developer.xml',

        'views/odoo_Training.xml',
        'views/netsuite_template.xml',
        'views/netsuite_support_template.xml',
        
        'views/netsuite_consultant.xml',
        'views/netsuite_implementation_template.xml',
        'views/netsuite_licensing_template.xml',

        'views/ERP_Next.xml',
        'views/frappe_book_template.xml',
        'views/frappe_lms_template.xml',
        'views/frappe_hr_template.xml',
        'views/frappe_healthcare_template.xml',

        'views/IOS_Developer.xml',
        'views/Android_Mobile.xml',
        'views/geomarking_template.xml',
        'views/odoo_shoppe_template.xml',

        'views/contactus.xml',
        'views/contactus_thankyou.xml',

        'views/odoo_erp_services.xml',
        'views/template.xml',
        
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'website.assets_editor': [
            'website_kanak/static/src/js/website_kanak_crm_editor.js',
        ],
        'web.assets_frontend': [
            'website_kanak/static/lib/owlcarousel/assets/owl.carousel.min.css',
            'website_kanak/static/lib/owlcarousel/assets/owl.theme.default.min.css',
            'website_kanak/static/lib/owlcarousel/owl.carousel.min.js',
            'website_kanak/static/src/js/jquery.animateTyping.js',
            
            'website_kanak/static/src/scss/homepage.scss',
            'website_kanak/static/src/scss/privacy_policy.scss',
            'website_kanak/static/src/scss/about_us.scss',
            'website_kanak/static/src/scss/testimonial_page.scss',
            'website_kanak/static/src/scss/engagement.scss',
            'website_kanak/static/src/scss/our-team.scss',
            'website_kanak/static/src/scss/careers.scss',

            'website_kanak/static/src/scss/odoo-development.scss',
            'website_kanak/static/src/scss/odoo_integration.scss',
            'website_kanak/static/src/scss/odoo_Installation.scss',                 
            'website_kanak/static/src/scss/odoo_Themes.scss',
            'website_kanak/static/src/scss/odoo_Implementation.scss',
            'website_kanak/static/src/scss/odoo_Training.scss',
            'website_kanak/static/src/scss/Hire_Odoo_Developer.scss',

            'website_kanak/static/src/scss/ERP_Next.scss',
            'website_kanak/static/src/scss/frappe_books.scss',
            'website_kanak/static/src/scss/frappe_healthcare.scss',
            'website_kanak/static/src/scss/frappe_hr_template.scss',
            'website_kanak/static/src/scss/frappe_lms.scss',

            'website_kanak/static/src/scss/IOS_Developer.scss',
            'website_kanak/static/src/scss/Android_Mobile.scss',
            'website_kanak/static/src/scss/geomarking.scss',
            'website_kanak/static/src/scss/odoo_shoppe.scss',
            'website_kanak/static/src/scss/odoo_shoppe_animation.scss',
               
            'website_kanak/static/src/scss/netsuite_template.scss',
            'website_kanak/static/src/scss/netsuite_implementation.scss',
            'website_kanak/static/src/scss/netsuite_consultant.scss',
            'website_kanak/static/src/scss/netsuite_licensing.scss',
            'website_kanak/static/src/scss/netsuite_support.scss',  

            'website_kanak/static/src/scss/contactus.scss',
            'website_kanak/static/src/scss/odoo_website.scss',
            
            'website_kanak/static/src/js/script.js',
            'website_kanak/static/src/js/faq.js',
            'website_kanak/static/src/js/career_search.js',
            
        ],
        'web._assets_primary_variables':[
            ('after', 'website/static/src/scss/primary_variables.scss','website_kanak/static/src/scss/variable.scss')
        ],
    },
}