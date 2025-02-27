# -*- coding: utf-8 -*-
"""
:copyright: Copyright 2020-2022 Sphinx Confluence Builder Contributors (AUTHORS)
:license: BSD-2-Clause (LICENSE)
"""

from sphinxcontrib.confluencebuilder.util import str2bool


# configures the default editor to publication
#
# The following configures the default editor to use for publication. The
# default value is "v1" (over the newer "v2"; Confluence default editor). This
# is a result of not all Sphinx capabilities are supported with the newer
# editor. Users can override the editor using configuration options -- but
# this selection is solely driven on maximizing capabilities provided by
# Sphinx over capabilities of Confluence.
DEFAULT_EDITOR = 'v1'


def apply_defaults(builder):
    """
    applies default values for select configurations

    This call will populate default values for various configuration options.
    This method is used in alternative to the default values provided in the
    `add_config_value` call, which allows this extension to apply defaults at
    a more controlled time.

    Args:
        builder: the builder which configuration defaults should be applied on
    """

    conf = builder.config
    config_manager = builder.app.config_manager_

    if conf.confluence_add_secnumbers is None:
        conf.confluence_add_secnumbers = True

    if conf.confluence_adv_ignore_nodes is None:
        conf.confluence_adv_ignore_nodes = []

    if conf.confluence_adv_restricted is None:
        conf.confluence_adv_restricted = []

    if conf.confluence_client_cert is not None:
        if not isinstance(conf.confluence_client_cert, tuple):
            conf.confluence_client_cert = (conf.confluence_client_cert, None)

    if conf.confluence_editor is None:
        conf.confluence_editor = DEFAULT_EDITOR

    if conf.confluence_file_suffix:
        if conf.confluence_file_suffix.endswith('.'):
            conf.confluence_file_suffix = '.conf'

    if conf.confluence_jira_servers is None:
        conf.confluence_jira_servers = {}

    if conf.confluence_latex_macro and \
            not isinstance(conf.confluence_latex_macro, dict):
        conf.confluence_latex_macro = {
            'block-macro': conf.confluence_latex_macro,
            'inline-macro': conf.confluence_latex_macro,
        }

    if conf.confluence_mentions is None:
        conf.confluence_mentions = {}

    if conf.confluence_page_hierarchy is None:
        conf.confluence_page_hierarchy = True

    if conf.confluence_publish_intersphinx is None:
        conf.confluence_publish_intersphinx = True

    if conf.confluence_remove_title is None:
        conf.confluence_remove_title = True

    if conf.confluence_secnumber_suffix is None:
        conf.confluence_secnumber_suffix = '. '

    if conf.confluence_sourcelink is None:
        conf.confluence_sourcelink = {}

    # ensure all boolean-based options are converted to boolean types
    for key in sorted(config_manager.options_bool):
        if getattr(conf, key) is not None:
            if not isinstance(getattr(conf, key), bool) and conf[key]:
                conf[key] = str2bool(conf[key])

    # ensure all integer-based options are converted to integer types
    for key in sorted(config_manager.options_int):
        if getattr(conf, key) is not None:
            if not isinstance(getattr(conf, key), int) and conf[key]:
                conf[key] = int(conf[key])

    # if the parent page is an integer value in a string type, cast it to an
    # integer; otherwise, assume it is a page name (string)
    if conf.confluence_parent_page:
        try:
            conf.confluence_parent_page = int(conf.confluence_parent_page)
        except ValueError:
            pass
