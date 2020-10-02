# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 alzp.
#
# testInvenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""JS/CSS Webpack bundles for theme."""

from __future__ import absolute_import, print_function

from flask_webpackext import WebpackBundle

theme = WebpackBundle(
    __name__,
    'assets',
    entry={
        'testinvenio-theme': './scss/testinvenio/theme.scss',
        'testinvenio-preview': './js/testinvenio/previewer.js',
    },
    dependencies={
        # add any additional npm dependencies here...
    }
)
