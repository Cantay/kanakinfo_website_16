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
from odoo.modules.module import MANIFEST_NAMES

_logger = logging.getLogger(__name__)
try:
    from git import Repo
except ImportError:
    _logger.debug("Cannot import 'git' python library.")


class GithubRepository(models.Model):
    _name = 'github.repository'
    _rec_name = 'github_url'

    sequence = fields.Integer(default=1)
    github_url = fields.Char(string='Github URL', required=True)

    def action_branch_clone(self):
        owner_match = re.search(r'github\.com:(.*)/', self.github_url)
        owner = owner_match.group(1)
        get_param = self.env['ir.config_parameter'].sudo().get_param
        token = get_param('git_token')
        branch_match = re.search(r'#(.*)', self.github_url)
        branch = branch_match.group(1)
        repo_match = re.search(r'github\.com:.*/(.*).git', self.github_url)
        repo = repo_match.group(1)
        repo_url = f'https://{token}@github.com/{owner}/{repo}.git'
        product_product_obj = self.env['product.product'].sudo()
        try:
            temp_dir = tempfile.mkdtemp(prefix=f"kanak_apps_{branch}_")
            repo = git.Repo.clone_from(repo_url, temp_dir, branch=branch)
            contents = os.listdir(temp_dir)
            for item in contents:
                item_path = os.path.join(temp_dir, item)  # Get the full path of the item
                if os.path.isdir(item_path) and not item.startswith('.'):
                    full_module_path = os.path.join(temp_dir, item)
                    module_info = {}
                    _ICON_PATH = [
                        'static/src/img/',
                        'static/description/',
                    ]
                    _INDEX_HTML_PATH = 'static/description/'
                    manifest_path = next((opj(full_module_path, name) for name in MANIFEST_NAMES if os.path.exists(opj(full_module_path, name))), None)
                    if manifest_path:
                        if os.path.isfile(manifest_path):
                            with open(manifest_path, 'rb') as f:
                                module_info.update(ast.literal_eval(f.read().decode()))
                        module_info['technical_name'] = item
                        module_version = product_product_obj.create_or_update_variants(module_info, branch)
                        theme_image_path = False
                        banner_path = False
                        icon_path = False
                        resize = False
                        product_image = False
                        theme_image = False
                        banner_image = False
                        license = False
                        if module_info.get('images', False):
                            full_current_icon_path = os.path.join(
                                full_module_path, module_info.get('images')[0])
                            if os.path.exists(full_current_icon_path):
                                banner_path = full_current_icon_path
                            if module_info.get('images', False) and len(module_info.get('images', False)) > 1:
                                full_current_theme_image_path = os.path.join(full_module_path, module_info.get('images', False)[1])
                                if os.path.exists(full_current_theme_image_path):
                                    theme_image_path = full_current_theme_image_path
                        for current_icon_path in _ICON_PATH:
                            full_current_icon_path = os.path.join(
                                full_module_path, current_icon_path, 'icon.png')
                            if os.path.exists(full_current_icon_path):
                                icon_path = full_current_icon_path
                                resize = True
                                break
                        if theme_image_path:
                            image_enc = False
                            try:
                                with open(theme_image_path, 'rb') as f:
                                    image = f.read()
                                image_enc = base64.b64encode(tools.image_process(image, output_format='gif'))
                            except Exception:
                                _logger.warning("Unable to read or resize %s", banner_path)
                            theme_image = image_enc
                        if banner_path:
                            image_enc = False
                            try:
                                with open(banner_path, 'rb') as f:
                                    image = f.read()
                                image_enc = base64.b64encode(tools.image_process(image, output_format='gif'))
                            except Exception:
                                _logger.warning("Unable to read or resize %s", banner_path)
                            banner_image = image_enc
                        if icon_path:
                            image_enc = False
                            try:
                                with open(icon_path, 'rb') as f:
                                    image = f.read()
                                if resize:
                                    image_enc = base64.b64encode(tools.image_process(image, output_format='png'))
                                else:
                                    image_enc = base64.b64encode(image)
                            except Exception:
                                _logger.warning("Unable to read or resize %s", icon_path)
                            product_image = image_enc
                        else:
                            # Set the default icon
                            try:
                                with open(os.path.join(
                                        os.path.dirname(__file__),
                                        '../data/kanak.png'), 'rb') as f:
                                    image = base64.b64encode(f.read())
                                    product_image = image
                            except Exception as e:
                                _logger.error(
                                    'Unable to read the icon image, error is %s', e)

                        index_path = False
                        description_rst_html = False
                        full_current_index_path = os.path.join(full_module_path, _INDEX_HTML_PATH, 'index.html')
                        license_path = os.path.join(full_module_path, 'LICENSE')
                        if os.path.exists(full_current_index_path):
                            index_path = full_current_index_path
                        if index_path:
                            with open(index_path, 'rb') as desc_file:
                                doc = desc_file.read()
                                html = lxml.html.document_fromstring(doc)
                                for element, attribute, link, pos in html.iterlinks():
                                    if element.get('src') and not '//' in element.get('src') and not 'static/' in element.get('src'):
                                        element.set('src', "//apps.odoocdn.com/apps/assets/%s/%s/%s" % (branch, module_info['technical_name'], element.get('src')))
                                description_rst_html = tools.html_sanitize(lxml.html.tostring(html))
                        else:
                            description_rst_html = module_info['description']

                        if os.path.exists(license_path):
                            with open(license_path, 'rb') as desc_file:
                                license = desc_file.read()
                        module_version.write({
                            'repository_id': self.id,
                            'version': branch,
                            'description_rst_html': description_rst_html,
                            'image_1920': product_image,
                            'banner_image': banner_image,
                            'theme_image': theme_image,
                            'description_sale': module_info.get('summary', ''),
                            'license': license or ''
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
