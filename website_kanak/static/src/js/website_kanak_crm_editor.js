odoo.define('website_kanak.form', function (require) {
'use strict';

// Import required modules
var core = require('web.core');
var FormBuilderRegistry = require('web.form_builder_registry');

// Translation function
var _t = core._t;

// Add the form to the form builder registry
FormBuilderRegistry.add('create_lead', {
    // Define the fields for the form
    formFields: [{
        type: 'char',
        required: true,
        name: 'contact_name',
        fillWith: 'name',
        string: 'Your Name',
    }, {
        type: 'tel',
        name: 'phone',
        fillWith: 'phone',
        string: 'Phone Number',
    }, {
        type: 'email',
        required: true,
        fillWith: 'email',
        name: 'email_from',
        string: 'Your Email',
    }, {
        type: 'char',
        required: true,
        fillWith: 'commercial_company_name',
        name: 'partner_name',
        string: 'Your Company',
    }, {
        type: 'char',
        required: true,
        fillWith: 'commercial_company_name',
        name: 'name',
        string: 'Subject',
    }, {
        type: 'text',
        required: true,
        name: 'description',
        string: 'Your Question',
    }, {
        type: 'selection',
        custom: true,
        name: 'subject_type',
        string: 'Category',
    }],
    // Define the fields for the model
    fields: [{
        name: 'team_id',
        type: 'many2one',
        relation: 'crm.team',
        domain: [['use_opportunities', '=', true]],
        string: _t('Sales Team'),
        title: _t('Assign leads/opportunities to a sales team.'),
    }, {
        name: 'user_id',
        type: 'many2one',
        relation: 'res.users',
        domain: [['share', '=', false]],
        string: _t('Salesperson'),
        title: _t('Assign leads/opportunities to a salesperson.'),
    }
