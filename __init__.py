# Add context menu entries for opening Windows Explorer.
#
# Copyright 2026 Michael Beckh (mbeckh)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from functools import partial
import os
import subprocess
from typing import cast, override

from PyQt6 import QtGui, QtWidgets

from picard.const.sys import IS_WIN
from picard.plugin3.api import (
    BaseAction,
    PluginApi,
    t_,
)
from picard.util import iter_files_from_objects

from . import monkey

from picard.ui.filebrowser import FileBrowser
from picard.ui.util import context_menu_global_pos


def _open_explorer(self: FileBrowser) -> None:
    """Open explorer in path, select file if action started from a file."""
    indexes = self.selectedIndexes()
    if indexes:
        model = cast(QtGui.QFileSystemModel, self.model())
        path = model.filePath(indexes[0])
        path = os.path.normpath(path)

        if model.isDir(indexes[0]):
            os.startfile(path, 'explore')
        else:
            subprocess.Popen(f'explorer /select,"{path}"')


#
# Patch FileBrowser which has no extension point.
#

_open_explorer_action: QtGui.QAction | None = None


@monkey.patch(FileBrowser, FileBrowser.contextMenuEvent)
def _extended_FileBrowser_contextMenuEvent(wrapped, self: FileBrowser, event):
    """Patch FileBrowser to add context menu to leftmost panel which has no extension point."""
    global _open_explorer_action

    if not _enabled:
        wrapped(self, event)
        return

    menu = QtWidgets.QMenu(self)
    menu.addAction(self.load_selected_files_action)
    menu.addSeparator()
    menu.addAction(self.move_files_here_action)
    menu.addAction(self.toggle_hidden_action)
    menu.addAction(self.set_as_starting_directory_action)

    indexes = self.selectedIndexes()
    if indexes:
        if not _open_explorer_action:
            _open_explorer_action = QtGui.QAction(_api.tr('ui.action.title', "Open &Explorer..."), self)
            _open_explorer_action.triggered.connect(partial(_open_explorer, self))
            self.addAction(_open_explorer_action)

        menu.addSeparator()
        menu.addAction(_open_explorer_action)

    menu.exec(context_menu_global_pos(self, event))
    event.accept()


class ExplorerAction(BaseAction):
    """Custom action for plugin extension point."""

    TITLE = t_('ui.action.title', "Open &Explorer...")

    @override
    def callback(self, objs):
        for file in iter_files_from_objects(objs):
            # open path for first file in case of multi-select
            path = os.path.normpath(file.filename)
            subprocess.Popen(f'explorer /select,"{path}"')
            return


def enable(api: PluginApi):
    """Enable plugin (Windows only)."""
    global _api, _enabled

    _api = api

    if IS_WIN:
        # cannot enable on other platforms
        _enabled = True
        api.register_file_action(ExplorerAction)


def disable():
    """Disable plugin."""
    global _api, _enabled, _open_explorer_action

    _enabled = False
    _open_explorer_action = None

    monkey.unpatch_module(__name__)

    del _api
