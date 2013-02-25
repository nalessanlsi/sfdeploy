# -*- coding: utf-8 -*-
# config.py
#
# Copyright (c) 2012-2013 Henning Glatter-Götz
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# config.py - Collection of configuration tasks for fabric
#
# To include it in the fabfile.py add this near the top
#
# import sys
# import config

import os
from fabric.api import *
from fabric.colors import red, green

try:
    import yaml
except ImportError:
    if confirm(red('pyYaml module not installed. Install it now?', bold=True)):
        install_py_yaml()
        exit(0)
    else:
        exit(1)


def load_yaml(path):
    """
    Load a yaml file located at 'path' and return the content as a dictionary.
    If the yaml file does not exist an empty dictionary will be returned.
    """
    if os.path.exists(path):
        f = open(path)
        data = yaml.load(f)
        f.close()
        return data
    else:
        return {}


def load_yaml_config(path, env = ''):
    """
    Load an environment aware yaml configuration file into a dictionary.
    If a configuration depends on the target of the deployment it is possible
    to pass the name of the environment to this function (env). In such a case
    the yaml configuration file must look like this:

    all:
        key1: defaultValue1
        :
    prod:
        key1: prod_value1
        key2: prod_value2
        :
    dev:
        key1: dev_value1
        key2: dev_value2
        :

    'all' is the default that will be returned if no env value is passed.
    'prod' and 'dev' in the above example are the names of the environments
    present in this file.
    Calling the function with 'prod' as the value for env will return the key/
    value pairs from the 'all' section with the values from the 'prod' section
    overriding any that might have been loaded from the all section.
    """
    config = load_yaml(path)

    if config:
        if 'all' in config:
            all = config['all']
        else:
            return {}
        if env != '':
            if env in config:
                all.update(config[env])
                return all
            else:
                return {}

    return config


def load_settings(path):
    """
    Take given file path and return dictionary of any key=value pairs found.
    Copy and paste from fabric project's main.py.
    """
    if os.path.exists(path):
        comments = lambda s: s and not s.startswith("#")
        settings = filter(comments, open(path, 'r'))
        return dict((k.strip(), v.strip()) for k, _, v in
            [s.partition('=') for s in settings])
    # Handle nonexistent or empty settings file
    return {}


def install_py_yaml():
    """
    Install the pyYaml module
    """
    local('curl -O http://pyyaml.org/download/pyyaml/PyYAML-3.10.tar.gz && tar -xzf PyYAML-3.10.tar.gz && cd PyYAML-3.10 && python setup.py install && cd .. && rm -rf PyYAML-3.10.tar.gz PyYAML-3.10')

