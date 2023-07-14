# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug


class BlogPost(models.Model):
    _inherit = 'blog.post'

    url = fields.Char("URL", required=True)
    product_id = fields.Many2one('product.template', string='Product')
    banner = fields.Binary('Post Banner', help='1200px x 628px size for best view.')
    banner_medium = fields.Binary('Banner Medium', help='465px x 321px size for best view.')
    banner_thumbnail = fields.Binary(
        'Banner Thumbnail', help='228px x 158px size for best view.')
    custom_json_schema = fields.Boolean('Own JSON Schema')
    json_schema = fields.Text(
        'JSON Schema', help='If any customer schema then enter here.')

    _sql_constraints = [
        ('blog_url_uniq', 'unique (url)', 'The url must be unique per blog!'),
    ]

    def _compute_website_url(self):
        super(BlogPost, self)._compute_website_url()
        for blog_post in self:
            blog_post.website_url = "/blog/%s/post/%s" % (slug(blog_post.blog_id), blog_post.url)


class BlogBlog(models.Model):
    _inherit = 'blog.blog'

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name must be unique per blog!'),
    ]

    blog_url = fields.Char(string='URL')

    @api.onchange('name')
    def _onchange_blog_url(self):
        if self.name:
            self.blog_url = self.name.lower().replace(' ', '-')


class BlogPostComment(models.Model):
    _name = 'blog.post.comment'
    _description = 'Blog Comment online by public user'


    name = fields.Char('Name')
    partner_email = fields.Char("Email")
    comment_accept = fields.Boolean('Accept', default=False)
    comment_description = fields.Text("Description")
    blog_post_id = fields.Many2one('blog.post','Blog Id')




