# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.addons.http_routing.models.ir_http import slugify


class VacantLocation(models.Model):
	_name = 'vacant.location'

	name = fields.Char(string="Vacancy Location")


class JobSkillsRequired(models.Model):
	_name = 'job.skills.require'

	name = fields.Char(string="Job Skills")


class Job(models.Model):
	_inherit = 'hr.job'

	vacant_location = fields.Many2many('vacant.location', string="Vacancy Location")
	job_skill = fields.Many2many('job.skills.require', string="Job Skills")
	exp_required = fields.Char(string="Experiance")
	job_summary = fields.Text(string="Summary")
	website_url = fields.Char(compute="_compute_website_url", store=True)
	job_apply_website_url = fields.Char(compute="_compute_website_url", store=True)
	job_image = fields.Binary(string="Job Image")

	_sql_constraints = [
		('website_url_unique', 'unique (website_url)', 'Every job must be Unique!')
	]

	@api.depends('name')
	def _compute_website_url(self):
		super(Job, self)._compute_website_url()
		for job in self:
			job.website_url = '/jobs/detail/' + str(slugify(job.name or '').strip().strip('-'))
			job.job_apply_website_url = str(slugify(job.name or '').strip().strip('-'))
