import pytest
import pip
import subprocess
import sys
import json
from mock import patch, Mock
from pip._vendor.pkg_resources import Distribution
from pipsy import *

class TestPackaging:
    mock_installed = [Distribution(project_name='pipsy-test', version='0.1')]
    mock_pkg_json = json.dumps({ "info": { "version": "0.1", "name": "pipsy-test" }, "releases": { "0.3": [{ }], "0.2": [{ }], "0.1": [{ }] } }).encode('utf-8')

    @patch('pip.get_installed_distributions')
    def test_pip_installed(self, pip_mock):
        pip_mock.return_value = self.mock_installed
        packages = pip.get_installed_distributions()
        assert len(packages) == 1

    @patch('urllib.request.urlopen')
    def test_get_pkg_info(self, info_mock):
        req_mock = Mock()
        req_mock.readall.return_value = self.mock_pkg_json
        info_mock.return_value = req_mock

        pkg = get_pkg_info(self.mock_installed[0])
        versions = get_versions(pkg)
        assert len(versions) == 3

    @patch('urllib.request.urlopen')
    def test_get_version_range(self, info_mock):
        req_mock = Mock()
        req_mock.readall.return_value = self.mock_pkg_json
        info_mock.return_value = req_mock

        pkg = get_pkg_info(self.mock_installed[0])
        version_range = get_version_range(pkg, '0.1')
        assert len(version_range) == 2

    @patch('urllib.request.urlopen')
    def test_get_latest_version(self, info_mock):
        req_mock = Mock()
        req_mock.readall.return_value = self.mock_pkg_json
        info_mock.return_value = req_mock

        pkg = get_pkg_info(self.mock_installed[0])
        latest_version = get_latest_version(pkg)
        assert str(latest_version) == '0.3'
