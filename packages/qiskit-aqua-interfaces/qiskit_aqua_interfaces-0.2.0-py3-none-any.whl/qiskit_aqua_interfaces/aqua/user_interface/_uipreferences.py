# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Qiskit Aqua user interface preferences."""

import os
import json


class UIPreferences:
    """ Aqua UI Preferences """
    _FILENAME = '.qiskit_aqua_ui'
    _VERSION = '1.0'

    def __init__(self):
        """Create UIPreferences object."""
        self._preferences = {
            'version': UIPreferences._VERSION
        }
        home = os.path.expanduser("~")
        self._filepath = os.path.join(home, UIPreferences._FILENAME)
        try:
            with open(self._filepath) as json_pref:
                self._preferences = json.load(json_pref)
        except Exception:  # pylint: disable=broad-except
            pass

    @property
    def filepath(self):
        """ get filepath """
        return self._filepath

    def save(self):
        """ save preferences """
        with open(self._filepath, 'w') as pref_output:
            json.dump(self._preferences, pref_output, sort_keys=True, indent=4)

    def get_version(self):
        """ get version """
        if 'version' in self._preferences:
            return self._preferences['version']

        return None

    def get_browser_geometry(self, default_value=None):
        """ get aqua browser geometry """
        if 'browser_geometry' in self._preferences:
            return self._preferences['browser_geometry']

        return default_value

    def set_browser_geometry(self, geometry):
        """ set aqua browser geometry """
        self._preferences['browser_geometry'] = geometry

    def get_geometry(self, default_value=None):
        """ get aqua geometry """
        if 'run_geometry' in self._preferences:
            return self._preferences['run_geometry']

        return default_value

    def set_geometry(self, geometry):
        """ set aqua geometry """
        self._preferences['run_geometry'] = geometry

    def get_openfile_initialdir(self):
        """ get open file initial folder """
        if 'openfile_initialdir' in self._preferences:
            if not os.path.isdir(self._preferences['openfile_initialdir']):
                self._preferences['openfile_initialdir'] = os.getcwd()

            return self._preferences['openfile_initialdir']

        return os.getcwd()

    def set_openfile_initialdir(self, initialdir):
        """ set open file initial folder """
        self._preferences['openfile_initialdir'] = initialdir

    def get_savefile_initialdir(self):
        """ get save file initial folder """
        if 'savefile_initialdir' in self._preferences:
            if not os.path.isdir(self._preferences['savefile_initialdir']):
                self._preferences['savefile_initialdir'] = os.getcwd()

            return self._preferences['savefile_initialdir']

        return os.getcwd()

    def set_savefile_initialdir(self, initialdir):
        """ set save file initial folder """
        self._preferences['savefile_initialdir'] = initialdir

    def get_populate_defaults(self, default_value=None):
        """ get populate defaults flag """
        if 'populate_defaults' in self._preferences:
            return self._preferences['populate_defaults']

        return default_value

    def set_populate_defaults(self, populate_defaults):
        """ set populate defaults flag """
        self._preferences['populate_defaults'] = populate_defaults

    def get_recent_files(self):
        """ get recent files list """
        files = []
        if 'recent_files' in self._preferences:
            for file in self._preferences['recent_files']:
                if os.path.isfile(file):
                    files.append(file)

            self._preferences['recent_files'] = files

        return files

    def add_recent_file(self, file):
        """ add a recent file """
        recent_files = self.get_recent_files()
        if file not in recent_files:
            recent_files.append(file)
            if len(recent_files) > 6:
                recent_files = recent_files[1:]
        self._preferences['recent_files'] = recent_files

    def clear_recent_files(self):
        """ clear recent files list """
        if 'recent_files' in self._preferences:
            del self._preferences['recent_files']

    def get_logging_config(self, default_value=None):
        """ get aqua logging """
        if 'logging_config' in self._preferences:
            return self._preferences['logging_config']

        return default_value

    def set_logging_config(self, logging_config):
        """ set aqua logging """
        self._preferences['logging_config'] = logging_config
