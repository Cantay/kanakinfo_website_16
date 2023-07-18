# -*- coding: utf-8 -*-

import ast
import logging
import os
import git
import tempfile
import base64
import shutil
import re
import lxml.html
from os.path import join as opj
from odoo import fields, models, tools

_logger = logging.getLogger(__name__)
try:
    from git import Repo
except ImportError:
    _logger.debug("Cannot import 'git' python library.")

MANIFEST_NAMES = ['__openerp__.py', '__manifest__.py']
_ICON_PATH = [
    'static/src/img/',
    'static/description/',
]
_INDEX_HTML_PATH = 'static/description/'


class GithubRepository(models.Model):
    _name = 'github.repository'
    _rec_name = 'github_url'

    sequence = fields.Integer(default=1)
    github_url = fields.Char(string='Github URL', required=True)

    def action_branch_clone(self):
        owner = re.search(r'github\.com:(.*)/', self.github_url).group(1)
        token = self.env['ir.config_parameter'].sudo().get_param('git_token')
        branch = re.search(r'#(.*)', self.github_url).group(1)
        repo = re.search(r'github\.com:.*/(.*).git', self.github_url).group(1)
        repo_url = f'https://{token}@github.com/{owner}/{repo}.git'
        product_product_obj = self.env['product.product'].sudo()
        
        try:
            temp_dir = tempfile.mkdtemp(prefix=f"kanak_apps_{branch}_")
            repo = git.Repo.clone_from(repo_url, temp_dir, branch=branch)
            contents = os.listdir(temp_dir)
            
            for item in contents:
                item_path = os.path.join(temp_dir, item)
                if os.path.isdir(item_path) and not item.startswith('.'):
                    module_info = {}
                    full_module_path = os.path.join(temp_dir, item)
                    manifest_path = next((opj(full_module_path, name) for name in MANIFEST_NAMES if os.path.exists(opj(full_module_path, name))), None)
                    
                    if manifest_path and os.path.isfile(manifest_path):
                        with open(manifest_path, 'rb') as f:
                            module_info.update(ast.literal_eval(f.read().decode()))
                    
                    module_info['technical_name'] = item
                    module_version = product_product_obj.create_or_update_variants(module_info, branch)
                    
                    for current_icon_path in _ICON_PATH:
                        full_current_icon_path = os.path.join(full_module_path, current_icon_path, 'icon.png')
                        if os.path.exists(full_current_icon_path):
                            icon_path = full_current_icon_path
                            resize = True
                            break
                    
                    index_path = os.path.join(full_module_path, _INDEX_HTML_PATH, 'index.html')
                    license_path = os.path.join(full_module_path, 'LICENSE')
                    banner_path = None
                    theme_image_path = None
                    license = ''
                    
                    if module_info.get('images'):
                        full_current_banner_path = os.path.join(full_module_path, module_info['images'][0])
                        _logger.info('banner_image_path==%s', full_current_banner_path)
                        if os.path.exists(full_current_banner_path):
                            banner_path = full_current_banner_path
                        
                        if len(module_info['images']) > 1:
                            full_current_theme_image_path = os.path.join(full_module_path, module_info['images'][1])
                            if os.path.exists(full_current_theme_image_path):
                                theme_image_path = full_current_theme_image_path
                    
                    if os.path.exists(license_path):
                        with open(license_path, 'rb') as desc_file:
                            license = desc_file.read()
                    
                    description_rst_html = ''
                    if os.path.exists(index_path):
                        with open(index_path, 'rb') as desc_file:
                            doc = desc_file.read()
                            html = lxml.html.document_fromstring(doc)
                            for element, attribute, link, pos in html.iterlinks():
                                if element.get('src') and not '//' in element.get('src') and not 'static/' in element.get('src'):
                                    element.set('src', "//apps.odoocdn.com/apps/assets/%s/%s/%s" % (branch, module_info['technical_name'], element.get('src')))
                            description_rst_html = tools.html_sanitize(lxml.html.tostring(html))
                    else:
                        description_rst_html = module_info.get('description', '')
                    
                    product_image = None
                    if icon_path:
                        try:
                            with open(icon_path, 'rb') as f:
                                image = f.read()
                            if resize:
                                image = base64.b64encode(tools.image_process(image, output_format='png'))
                            else:
                                image = base64.b64encode(image)
                            product_image = image
                        except Exception:
                            _logger.warning("Unable to read or resize %s", icon_path)
                    else:
                        try:
                            with open(os.path.join(os.path.dirname(__file__), '../data/kanak.png'), 'rb') as f:
                                image = base64.b64encode(f.read())
                                product_image = image
                        except Exception as e:
                            _logger.error('Unable to read the icon image, error is %s', e)
                    
                    banner_image = None
                    if banner_path:
                        try:
                            with open(banner_path, 'rb') as f:
                                image = f.read()
                            banner_image = base64.b64encode(tools.image_process(image, output_format='gif'))
                        except Exception:
                            _logger.warning("Unable to read or resize %s", banner_path)
                    
                    theme_image = None
                    if theme_image_path:
                        try:
                            with open(theme_image_path, 'rb') as f:
                                image = f.read()
                            theme_image = base64.b64encode(tools.image_process(image, output_format='gif'))
                        except Exception:
                            _logger.warning("Unable to read or resize %s", theme_image_path)
                    
                    module_version.write({
                        'repository_id': self.id,
                        'version': branch,
                        'description_rst_html': description_rst_html,
                        'image_1920': product_image,
                        'banner_image': banner_image,
                        'theme_image': theme_image,
                        'description_sale': module_info.get('summary', ''),
                        'license': license
                    })

            shutil.rmtree(temp_dir)
        except Exception as e:
            _logger.error(e)

    def listdir(self, dir):
        def clean(name):
            name = os.path.basename(name)
            if name[-4:] == '.zip':
                name = name[:-4]
            return name

        def is_really_module(name):
            for mname in MANIFEST_NAMES:
                if os.path.isfile(opj(dir, name, mname)):
                    return True

        return map(clean, filter(is_really_module, os.listdir(dir)))
