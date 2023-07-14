# -*- coding: utf-8 -*-

import json
import werkzeug
import itertools
import pytz
import babel.dates
from collections import OrderedDict
from datetime import datetime
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website_blog.controllers.main import WebsiteBlog
from odoo import http, fields, _
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from dateutil.relativedelta import relativedelta
from odoo.fields import Datetime
import logging
_logger = logging.getLogger(__name__)


class WebsiteCustomeBlog(WebsiteBlog):

    def all_nav_list(self):
        dom = []
        if not request.env.user.has_group('website.group_website_designer'):
            dom += [('post_date', '<=', fields.Datetime.now())]
        groups = request.env['blog.post']._read_group_raw(
            dom,
            ['name', 'post_date'],
            groupby=["post_date"], orderby="post_date desc")
        for group in groups:
            (r, label) = group['post_date']
            start, end = r.split('/')
            group['post_date'] = label
            group['date_begin'] = start
            group['date_end'] = end

            locale = request.context.get('lang') or 'en_US'
            start = pytz.UTC.localize(fields.Datetime.from_string(start))
            tzinfo = pytz.timezone(request.context.get('tz', 'utc') or 'utc')

            group['month'] = babel.dates.format_datetime(start, format='MMMM', tzinfo=tzinfo, locale=locale)
            group['year'] = babel.dates.format_datetime(start, format='YYYY', tzinfo=tzinfo, locale=locale)

        return OrderedDict((year, [m for m in months]) for year, months in itertools.groupby(groups, lambda g: g['year']))

    @http.route([
        '/blog',
        '/blog/<int:blog_id>',
        '/blog/page/<int:page>',
        '/blog/<string:year>/<string:month>'
    ], type='http', auth="public", website=True)
    def blog(self, page=1, year=None, search='', month=None, blog_id='',**post):
        domain = []
        BlogPost = request.env['blog.post']
        total = BlogPost.search([], count=True)
        flag = False

        if blog_id:
            domain += [('id', '=', blog_id)]

        if year and month:
            flag = True
            mnth = datetime.strptime(month, '%B').month
            date_format = '{}-{}-01 00:00:00'.format(year, mnth)
            start_date = datetime.strptime(date_format, '%Y-%m-%d %H:%M:%S')
            next_month = start_date + relativedelta(months=1)
            end_date = next_month - relativedelta(days=1)

            date_begin = Datetime.to_string(start_date)
            date_end = Datetime.to_string(end_date)

        Blog = request.env['blog.blog']
        blogs = Blog.search([], limit=2)
        if len(blogs) == 1:
            return werkzeug.utils.redirect('/blog/%s' % slug(blogs[0]), code=302)

        if flag:
            domain += [("post_date", ">=", date_begin), ("post_date", "<=", date_end)]

        posts = BlogPost.search(domain, order="post_date desc")
        pager = request.website.pager(
            url='/blog',
            total=len(posts),
            page=page,
            step=self._blog_post_per_page,
        )
        blog_url = QueryURL('', ['blog', 'tag'], date_begin=date_begin if flag else '', date_end=date_end if flag else '')

        pager_begin = (page - 1) * self._blog_post_per_page
        pager_end = page * self._blog_post_per_page
        posts = posts[pager_begin:pager_end]

        return request.render("website_custome_blog_url.latest_blogs", {
            'posts': posts,
            'pager': pager,
            'all_nav_list': self.all_nav_list(),
            'blog_url': blog_url,
        })

    @http.route([
        '''/blog/<model("blog.blog", "[('website_id', 'in', (False, current_website_id))]"):blog>''',
        '''/blog/<model("blog.blog"):blog>/page/<int:page>''',
        '''/blog/<model("blog.blog"):blog>/tag/<string:tag>''',
        '''/blog/<model("blog.blog"):blog>/tag/<string:tag>/page/<int:page>''',
    ], type='http', auth="public", website=True)
    def cate_blog(self, blog=None, tag=None, page=1, **opt):
        if blog and tag and page > 1:
            return request.redirect('/blog/category/%s/tag/%s/page/%s' % (blog.blog_url, tag, page))
        elif blog and tag:
            return request.redirect('/blog/category/%s/tag/%s' % (blog.blog_url, tag))
        elif blog and page > 1:
            return request.redirect('/blog/category/%s/page/%s' % (blog.blog_url, page))
        elif blog:
            return request.redirect('/blog/category/%s' % blog.blog_url)

    @http.route([
        '/blog/category/<string:blog_url>',
        '/blog/category/<string:blog_url>/page/<int:page>',
        '/blog/category/<string:blog_url>/tag/<string:tag>',
        '/blog/category/<string:blog_url>/tag/<string:tag>/page/<int:page>',
    ], type='http', auth="public", website=True)
    def custom_blog(self, blog_url, blog=None, tag=None, page=1, **opt):

        date_begin, date_end, state = opt.get('date_begin'), opt.get('date_end'), opt.get('state')
        published_count, unpublished_count = 0, 0

        BlogPost = request.env['blog.post']

        Blog = request.env['blog.blog']
        blog = Blog.search([('blog_url', '=', blog_url)])
        blogs = Blog.search([('blog_url', '=', blog_url)], order="create_date asc")

        # build the domain for blog post to display
        domain = []
        # retrocompatibility to accept tag as slug
        active_tag_ids = tag and [int(unslug(t)[1]) for t in tag.split(',')] or []
        if active_tag_ids:
            domain += [('tag_ids', 'in', active_tag_ids)]
        if blog:
            domain += [('blog_id', '=', blog.id)]
        if date_begin and date_end:
            domain += [("post_date", ">=", date_begin), ("post_date", "<=", date_end)]

        if request.env.user.has_group('website.group_website_designer'):
            count_domain = domain + [("website_published", "=", True), ("post_date", "<=", fields.Datetime.now())]
            published_count = BlogPost.search_count(count_domain)
            unpublished_count = BlogPost.search_count(domain) - published_count

            if state == "published":
                domain += [("website_published", "=", True), ("post_date", "<=", fields.Datetime.now())]
            elif state == "unpublished":
                domain += ['|', ("website_published", "=", False), ("post_date", ">", fields.Datetime.now())]
        else:
            domain += [("post_date", "<=", fields.Datetime.now())]

        blog_url = QueryURL('', ['blog', 'tag'], blog=blog, tag=tag, date_begin=date_begin, date_end=date_end)

        blog_posts = BlogPost.search(domain, order="post_date desc")
        pager = request.website.pager(
            url=request.httprequest.path.partition('/page/')[0],
            total=len(blog_posts),
            page=page,
            step=self._blog_post_per_page,
            url_args=opt,
        )
        pager_begin = (page - 1) * self._blog_post_per_page
        pager_end = page * self._blog_post_per_page
        blog_posts = blog_posts[pager_begin:pager_end]
        all_tags = blog.all_tags()[blog.id]

        # function to create the string list of tag ids, and toggle a given one.
        # used in the 'Tags Cloud' template.
        def tags_list(tag_ids, current_tag):
            tag_ids = list(tag_ids) # required to avoid using the same list
            if current_tag in tag_ids:
                tag_ids.remove(current_tag)
            else:
                tag_ids.append(current_tag)
            tag_ids = request.env['blog.tag'].browse(tag_ids).exists()
            return ','.join(slug(tag) for tag in tag_ids)
        values = {
            'blog': blog,
            'blogs': blogs,
            'main_object': blog,
            'tags': all_tags,
            'state_info': {"state": state, "published": published_count, "unpublished": unpublished_count},
            'active_tag_ids': active_tag_ids,
            'tags_list': tags_list,
            'blog_posts': blog_posts,
            'posts': blog_posts,
            'blog_posts_cover_properties': [json.loads(b.cover_properties) for b in blog_posts],
            'pager': pager,
            'nav_list': self.nav_list(blog),
            'blog_url': blog_url,
            'date': date_begin,
        }
        response = request.render("website_custome_blog_url.latest_blogs", values)
        return response

    @http.route([
        '''/blog/<model("blog.blog"):blog>/post/<string:post_url>'''], type='http', auth="public", website=True)
    def blog_post(self, blog, post_url, tag_id=None, page=1, enable_editor=None, **post):
        return request.redirect("/blog/%s" % post_url)

    @http.route(['''/blog/<string:post_url>'''], type='http', auth="public", website=True)
    def custom_blog_post(self, blog=None, post_url=None, tag_id=None, page=1, enable_editor=None, **post):
        BlogPost = request.env['blog.post']
        # Redirect for old url to new url redirect
        if post_url == 'why-odoo-does-is-one-of-the-fastest-growing-business-solutions':
            return request.redirect(
                '/blog/why-odoo-is-one-of-the-fastest-growing-business-solutions')
        elif post_url == 'login-in-odoo-with-external-gareway-google-facebook':
            return request.redirect(
                '/blog/login-with-social-signon-in-odoo')
        elif post_url == 'search':
            return request.redirect('/blog')
        elif post_url == 'tomtomer-required':
            return request.redirect('/blog')

        blog_post = BlogPost.search([('url', '=', post_url)])
        date_begin, date_end = post.get('date_begin'), post.get('date_end')

        pager_url = "/blogpost/%s" % post_url

        pager = request.website.pager(
            url=pager_url,
            total=len(blog_post.website_message_ids),
            page=page,
            step=self._post_comment_per_page,
            scope=7
        )
        pager_begin = (page - 1) * self._post_comment_per_page
        pager_end = page * self._post_comment_per_page
        comments = blog_post.website_message_ids[pager_begin:pager_end]

        tag = None
        if tag_id:
            tag = request.env['blog.tag'].browse(int(tag_id))
        blog_url = QueryURL('', ['blog', 'tag'], blog=blog_post.blog_id, tag=tag, date_begin=date_begin, date_end=date_end)

        if not blog_post.url == post_url:
            # return request.redirect("/blog/%s/post/%s" % (slug(blog_post.blog_id), blog_post)
            return request.redirect("/blog")

        tags = request.env['blog.tag'].search([])

        # Find next Post
        all_post = BlogPost.search([('url', '=', post_url)])
        if not request.env.user.has_group('website.group_website_designer'):
            all_post = all_post.filtered(lambda r: r.post_date <= fields.Datetime.now())

        if blog_post not in all_post:
            return request.redirect("/blog/%s" % post_url)

        # should always return at least the current post
        all_post_ids = all_post.ids
        current_blog_post_index = all_post_ids.index(blog_post.id)
        nb_posts = len(all_post_ids)
        next_post_id = all_post_ids[(current_blog_post_index + 1) % nb_posts] if nb_posts > 1 else None
        next_post = next_post_id and BlogPost.browse(next_post_id) or False

        values = {
            'tags': tags,
            'tag': tag,
            'blog': blog_post.blog_id,
            'blog_post': blog_post,
            'blog_post_cover_properties': json.loads(blog_post.cover_properties),
            'main_object': blog_post,
            'nav_list': self.nav_list(blog_post.blog_id),
            'enable_editor': enable_editor,
            'next_post': next_post,
            'next_post_cover_properties': json.loads(next_post.cover_properties) if next_post else {},
            'date': date_begin,
            'blog_url': blog_url,
            'pager': pager,
            'comments': comments,
        }
        response = request.render("website_blog.blog_post_complete", values)

        request.session[request.session.sid] = request.session.get(request.session.sid, [])
        if not (blog_post.id in request.session[request.session.sid]):
            request.session[request.session.sid].append(blog_post.id)
            # Increase counter
            blog_post.sudo().write({
                'visits': blog_post.visits + 1,
            })
        return response

    def _blog_post_message(self, blog_post_id, message_content, **post):
        BlogPost = request.env['blog.post']
        # for now, only portal and user can post comment on blog post.
        if request.env.user.id == request.website.user_id.id:
            raise UserError(_('Public user cannot post comments on blog post.'))
        # get the partner of the current user
        partner_id = request.env.user.partner_id.id

        message = BlogPost.message_post(
            int(blog_post_id),
            body=message_content,
            message_type='comment',
            subtype='mt_comment',
            author_id=partner_id,
            path=post.get('path', False),
        )
        return message.id

    def _get_discussion_detail(self, ids, publish=False, **post):
        values = []
        for message in request.env['mail.message'].sudo().browse(ids):
            values.append({
                "id": message.id,
                "author_name": message.author_id.name,
                "author_image": message.author_id.image and \
                    (b"data:image/png;base64,%s" % message.author_id.image) or \
                    b'/website_blog/static/src/img/anonymous.png',
                "date": message.date,
                'body': html2plaintext(message.body),
                'website_published' : message.website_published,
                'publish' : publish,
            })
        return values


class WebsiteSearch(http.Controller):

    @http.route('/blogs/search', type="json", auth="public", website=True)
    def search_contents(self, **kw):
        search = kw.get('values')
        domain = []
        if search:
            for srch in search.split(" "):
                domain += [('name', 'ilike', srch)]
        domain.append(('website_published', '=', True))
        product_as_category = request.env['blog.post'].sudo().search(domain, limit=50)
        values = {}
        values['blog_results'] = request.env['ir.ui.view']._render_template("website_custome_blog_url.search_blog_results", {
            'blogs_posts': product_as_category if search != '' else []
        })
        return values

    @http.route('/blog_comment_form', type="json", auth="public", website=True, methods=['POST'], csrf=False)
    def blog_comment(self, **kw):
        blog_comment = request.env['blog.post.comment'].sudo()
        blog_comment.create({
            'name': kw.get('name'),
            'partner_email': kw.get('email'),
            'comment_description': kw.get('comment'),
            'blog_post_id': int(kw.get('blog_id')),
        })
        return True
