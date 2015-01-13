#-*- coding: utf-8 -*-

from logpot.admin.base import AuthenticateView
from logpot.utils import ALLOWED_EXTENSIONS

from flask import flash, redirect
from flask.ext.admin import expose
from flask.ext.admin.contrib.fileadmin import FileAdmin
from flask.ext.admin.babel import gettext

import os
import os.path as op
from operator import itemgetter
from datetime import datetime


class EntryFileView(AuthenticateView, FileAdmin):

    def __init__(self, dirpath, **kwargs):
        super().__init__(dirpath, **kwargs)
    can_delete = False
    can_upload = False
    can_mkdir = False
    allowed_extensions = ALLOWED_EXTENSIONS

    # Fix bug
    @expose('/')
    @expose('/b/<path:path>')
    def index(self, path=None):
        """
            Index view method

            :param path:
                Optional directory path. If not provided, will use the base directory
        """
        # Get path and verify if it is valid
        base_path, directory, path = self._normalize_path(path)

        if not self.is_accessible_path(path):
            flash(gettext('Permission denied.'))
            return redirect(self._get_dir_url('.index'))

        # Get directory listing
        items = []

        # Parent directory
        if directory != base_path:
            parent_path = op.normpath(op.join(path, '..'))
            if parent_path == '.':
                parent_path = None

            items.append(('..', parent_path, True, 0, 0))

        for f in os.listdir(directory):
            fp = op.join(directory, f)
            rel_path = op.join(path, f)

            if self.is_accessible_path(rel_path):
                items.append((f, rel_path, op.isdir(fp), op.getsize(fp), op.getmtime(fp)))

        # Sort by name
        items.sort(key=itemgetter(0))

        # Sort by type
        items.sort(key=itemgetter(2), reverse=True)

        # Sort by modified date
        items.sort(
            key=lambda values: (
                values[0],
                values[1],
                values[2],
                values[3],
                datetime.fromtimestamp(values[4])
            ), reverse=True
        )

        # Generate breadcrumbs
        accumulator = []
        breadcrumbs = []
        for n in path.split(os.sep):
            accumulator.append(n)
            breadcrumbs.append((n, op.join(*accumulator)))

        # Actions
        actions, actions_confirmation = self.get_actions_list()

        return self.render(self.list_template,
                           dir_path=path,
                           breadcrumbs=breadcrumbs,
                           get_dir_url=self._get_dir_url,
                           get_file_url=self._get_file_url,
                           items=items,
                           actions=actions,
                           actions_confirmation=actions_confirmation)
