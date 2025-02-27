# -*- coding: utf-8 -*-
"""
:copyright: Copyright 2021-2022 Sphinx Confluence Builder Contributors (AUTHORS)
:license: BSD-2-Clause (LICENSE)
"""

from docutils import nodes
from os import path
from sphinx import addnodes
from sphinxcontrib.confluencebuilder.compat import docutils_findall as findall
from sphinxcontrib.confluencebuilder.nodes import confluence_expand
from sphinxcontrib.confluencebuilder.util import first
import itertools


# ##############################################################################
# disable import/except warnings for third-party modules
# pylint: disable=E

# load sphinx_toolbox extension if available to handle node pre-processing
try:
    from sphinx_toolbox.assets import AssetNode as sphinx_toolbox_AssetNode
    sphinx_toolbox_assets = True
except:  # noqa: E722
    sphinx_toolbox_assets = False

try:
    from sphinx_toolbox.collapse import CollapseNode as sphinx_toolbox_CollapseNode
    sphinx_toolbox_collapse = True
except:  # noqa: E722
    sphinx_toolbox_collapse = False

try:
    from sphinx_toolbox.github.issues import IssueNode as sphinx_toolbox_IssueNode
    from sphinx_toolbox.github.issues import IssueNodeWithName as sphinx_toolbox_IssueNodeWithName
    sphinx_toolbox_github_issues = True
except:  # noqa: E722
    sphinx_toolbox_github_issues = False

try:
    from sphinx_toolbox.github.repos_and_users import GitHubObjectLinkNode as sphinx_toolbox_GitHubObjectLinkNode
    sphinx_toolbox_github_repos_and_users = True
except:  # noqa: E722
    sphinx_toolbox_github_repos_and_users = False

# re-enable pylint warnings from above
# pylint: enable=E
# ##############################################################################


def replace_sphinx_toolbox_nodes(builder, doctree):
    """
    replace sphinx_toolbox nodes with compatible node types

    Various sphinx_toolbox nodes are pre-processed and replaced with compatible
    node types for a given doctree.

    Args:
        builder: the builder
        doctree: the doctree to replace nodes on
    """

    # allow users to disabled third-party implemented extension changes
    restricted = builder.config.confluence_adv_restricted
    if 'ext-sphinx_toolbox' in restricted:
        return

    if sphinx_toolbox_assets:
        for node in findall(doctree, sphinx_toolbox_AssetNode):
            # mock a docname based off the configured sphinx_toolbox's asset
            # directory; which the processing of a download_reference will
            # strip and use the asset directory has the container folder to find
            # the file in
            mock_docname = path.join(builder.config.assets_dir, 'mock')
            new_node = addnodes.download_reference(
                node.astext(),
                node.astext(),
                refdoc=mock_docname,
                refexplicit=True,
                reftarget=node['refuri'],
            )
            node.replace_self(new_node)

    if sphinx_toolbox_collapse:
        for node in findall(doctree, sphinx_toolbox_CollapseNode):
            new_node = confluence_expand(node.rawsource, title=node.label,
                *node.children, **node.attributes)
            node.replace_self(new_node)

    if sphinx_toolbox_github_issues:
        # note: using while loop since replacing issue nodes has observed to
        #  cause an exception while docutils is processing a doctree
        while True:
            node = first(itertools.chain(
                findall(doctree, sphinx_toolbox_IssueNode),
                findall(doctree, sphinx_toolbox_IssueNodeWithName)))
            if not node:
                break

            if isinstance(node, sphinx_toolbox_IssueNodeWithName):
                title = '{}#{}'.format(node.repo_name, node.issue_number)
            else:
                title = '#{}'.format(node.issue_number)

            new_node = nodes.reference(title, title, refuri=node.issue_url)
            node.replace_self(new_node)

    if sphinx_toolbox_github_repos_and_users:
        for node in findall(doctree, sphinx_toolbox_GitHubObjectLinkNode):
            new_node = nodes.reference(node.name, node.name, refuri=node.url)
            node.replace_self(new_node)
