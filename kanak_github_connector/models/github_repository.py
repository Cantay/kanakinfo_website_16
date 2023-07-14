# -*- coding: utf-8 -*-

import ast
import logging
import os
from os.path import join as opj
from odoo import _, api, exceptions, fields, models, modules
from odoo.modules.module import MANIFEST_NAMES
from datetime import datetime
from subprocess import check_output
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
    is_clone = fields.Boolean()
    last_analyze_date = fields.Datetime(string='Last Sync', readonly=True, store=True)
    size = fields.Char(readonly=True, store=True)
    local_path = fields.Char(string='Local Path', compute='_compute_local_path')

    @api.depends('github_url')
    def _compute_local_path(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        source_path = get_param('github_repo_local_path')
        if not source_path:
            raise exceptions.Warning(_(
                "github_repo_local_path should be defined in your "
                " configuration file"))
        for repo in self:
            if repo.github_url:
                branch = self.github_url.split('#')[1]
                repo.local_path = os.path.join(source_path, branch)

    def action_branch_clone(self):
        url = self.github_url.split('#')[0]
        branch = self.github_url.split('#')[1]
        if not os.path.exists(self.local_path):
            _logger.info(
                "Cloning new branch into %s ..." % self.local_path)
            # Cloning the self
            try:
                os.makedirs(self.local_path)
            except Exception:
                raise exceptions.Warning(_(
                    "Error when trying to create the folder %s\n"
                    " Please check Odoo Access Rights.") % (
                        self.local_path))

            os.system("git clone -b %s --depth 1 %s %s" % (branch, url, self.local_path))
            self.write({
                'is_clone': True
            })

    def action_git_pull(self):
        branch = self.github_url.split('#')[1]
        try:
            res = check_output(
                ['git', 'pull', 'origin', branch],
                cwd=self.local_path)
            res = res.decode("utf-8")
        except Exception:
            # Trying to clean the local folder
            _logger.warning(_(
                "Error when updating the branch %s in the local folder"
                " %s.\n Deleting the local folder and trying"
                " again."), branch, self.local_path)
            command = "rm -rf %s" % self.local_path
            os.system(command)
            self.action_branch_clone()

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

    def _get_analyzable_files(self):
        res = []
        for root, dirs, files in os.walk(self.local_path):
            if '/.git' not in root:
                for fic in files:
                    if fic != '.gitignore':
                        res.append(os.path.join(root, fic))
        return res

    def _analyze_module_name(self, path, module_name):
        ProductProduct = self.env['product.product'].sudo()
        try:
            full_module_path = os.path.join(path, module_name)
            module_info = {}
            manifest_path = next((opj(full_module_path, name) for name in MANIFEST_NAMES if os.path.exists(opj(full_module_path, name))), None)
            if manifest_path:
                if os.path.isfile(manifest_path):
                    with open(manifest_path, 'rb') as f:
                        module_info.update(ast.literal_eval(f.read().decode()))

            # Create module version, if the module is installable
            # in the serie
            if module_info.get('installable', False):
                module_info['technical_name'] = module_name
                ProductProduct.create_or_update_from_manifest(module_info, self, full_module_path)
        except Exception as e:
            _logger.error('Cannot process module with name %s, error '
                          'is: %s', module_name, e)

    def _sync(self):
        self.ensure_one()
        # Change log level to avoid warning, when parsing odoo manifests
        self.action_git_pull()
        logger1 = logging.getLogger('odoo.modules.module')
        logger2 = logging.getLogger('odoo.addons.base.module.module')
        currentLevel1 = logger1.level
        currentLevel2 = logger2.level
        logger1.setLevel(logging.ERROR)
        logger2.setLevel(logging.ERROR)

        # add github_repo_local_path in module path list
        source_path = self.env['ir.config_parameter'].get_param('github_repo_local_path')

        try:
            paths = [self.local_path]

            # Scan each path, if exists
            for path in paths:
                if not os.path.exists(path):
                    _logger.warning(
                        "Unable to analyse %s. Source code not found.", path
                    )
                else:
                    # Analyze folders and create module versions
                    _logger.info("Analyzing repository %s ...", path)
                    for module_name in self.listdir(path):
                        self._analyze_module_name(path, module_name)
        finally:
            # Reset Original level for module logger
            logger1.setLevel(currentLevel1)
            logger2.setLevel(currentLevel2)

        path = self.local_path
        # Compute Files Sizes
        size = 0
        for file_path in self._get_analyzable_files():
            try:
                size += os.path.getsize(file_path)
            except Exception:
                _logger.warning(
                    "Warning : unable to eval the size of '%s'.", file_path)

        try:
            Repo(path)
        except Exception:
            # If it's not a correct repository, we flag the branch
            # to be downloaded again
            return {'size': 0}

        return {'size': "%.2f" % ((float(size) / 1024.00) / 1024.00) + " MB"}

    def action_branch_sync(self):
        path = self.local_path
        if not os.path.exists(path):
            _logger.warning("Warning Folder %s not found: Analysis skipped.", path)
        else:
            _logger.info("Analyzing Source Code in %s ...", path)
            # try:
            vals = self._sync()
            vals.update({
                'last_analyze_date': datetime.today(),
            })
            self.write(vals)
            # except Exception as e:
            #     _logger.warning('Cannot analyze branch so skipping it, error is: %s' % e)
