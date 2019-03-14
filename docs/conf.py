# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------
import eqllib
name = 'eqllib'
project = 'EQL Analytics Library'
copyright = '2018, Endgame'
author = 'Endgame'

# The short X.Y version
version = eqllib.__version__
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    # 'rst2pdf.pdfbuilder',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # 'style_external_links': True,
    'display_version': False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}
# html_sidebars = {
#     # "index": ["searchbox.html"],
#     "**": ["localtoc.html", "relations.html", "searchbox.html"],
# }
# singlehtml_sidebars = {"index": ["localtoc.html"]}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = name


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, '%s.tex' % name, project,
     'endgame', 'manual'),
]

# -- Options for pdf output ------------------------------
pdf_documents = [
    ('analytics', name, project, author),
]

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, project, project, [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, name, project,
     author, name, project,
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.

from docutils.core import Publisher
import docutils.utils.code_analyzer
import pygments.lexers


def process_programmatic_settings(self, settings_spec, settings_overrides, config_section):
    if self.settings is None:
        defaults = (settings_overrides or {}).copy()
        defaults.setdefault('traceback', True)
        defaults.setdefault('syntax_highlight', 'short')
        self.get_settings(settings_spec=settings_spec, config_section=config_section, **defaults)


Publisher.process_programmatic_settings = process_programmatic_settings


intersphinx_mapping = {'https://docs.python.org/': None}
from eql.ast import PipeCommand
from eql.functions import builtins
from pygments import token

# Write a custom lexer for EQL to integrate with Pygments and get syntax highlighting
from pygments.lexer import RegexLexer, bygroups, include
from sphinx.highlighting import lexers
import shutil


class EqlLexer(RegexLexer):
    name = 'eql'
    aliases = ['eql']
    filenames = ['.eql']

    _sign = r'[\-+]'
    _integer = r'\d+'
    _float = r'\d*\.\d+([Ee][-+]?\d+)?'
    _time_units = 's|sec\w+|m|min\w+|h|hour|hr|d|day'
    _name = r'[a-zA-Z][_a-zA-Z0-9]*'
    _pipe_names = set(PipeCommand.lookup.keys())

    tokens = {
        'whitespace': [
            (r'//(\n|[\w\W]*?[^\\]\n)', token.Comment.Single),
            (r'/[*][\w\W]*?[*]/', token.Comment.Multiline),
            (r'/[*][\w\W]*', token.Comment.Multiline),
            (r'\s+', token.Text),
        ],
        'root': [
            include('whitespace'),
            (r'(and|in|not|or)\b', token.Operator.Word),  # Keyword.Pseudo can also work
            (r'(join|sequence|until|where)\b', token.Keyword),
            (r'(const)(\s+)(%s)\b' % _name, bygroups(token.Keyword.Declaration, token.Whitespace, token.Name.Constant)),
            (r'(macro)(\s+)(%s)\b' % _name, bygroups(token.Keyword.Declaration, token.Whitespace, token.Name.Constant)),
            (r'(by|of|with)\b', token.Keyword.QueryModifier),
            (r'(true|false|null)\b', token.Name.Builtin),

            # built in pipes
            (r'(\|)(\s*)(%s)' % '|'.join(_pipe_names), bygroups(token.Operator, token.Whitespace, token.Name.Function.Magic)),

            # built in functions
            (r'(%s)(\s*\()' % '|'.join(builtins), bygroups(token.Name.Function, token.Text)),

            # all caps names
            (r'[A-Z][_A-Z0-9]+\b', token.Name.Other),
            (_name, token.Name),

            # time units
            (r'(%s|%s)[ \t]*(%s)\b' % (_float, _integer, _time_units), token.Literal.Date),

            (_sign + '?' + _float, token.Number.Float),
            (_sign + '?' + _integer, token.Number.Integer),

            (r'"(\\[btnfr"\'\\]|[^\r\n"\\])*"', token.String),
            (r"'(\\[btnfr'\"\\]|[^\r\n'\\])*'", token.String),
            (r'\?"(\\"|[^"])*"', token.String.Regex),
            (r"\?'(\\'|[^'])*'", token.String.Regex),
            (r'(==|=|!=|<|<=|>=|>)', token.Operator),
            (r'[()\[\],.]', token.Punctuation),
        ]
    }


eql_lexer = EqlLexer(startinline=True)
lexers['eql'] = eql_lexer
_get_lexer_by_name = pygments.lexers.get_lexer_by_name


def get_lexer_by_name(_alias, **options):
    if _alias == 'eql':
        return eql_lexer
    return _get_lexer_by_name(_alias, **options)


# Path this function to load EQL
docutils.utils.code_analyzer.get_lexer_by_name = get_lexer_by_name

# Dynamic Generation
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from eqllib.attack import build_attack, techniques, tactics, get_matrix

config = eqllib.Configuration.default_with_analytics()
html_context = {}

build_attack()
rst_context = {
    'analytics': config.analytics,
    'red_analytics': [r for r in config.analytics if 'atomicblue' in r.metadata.get('tags', [])],
    'non_red_analytics': [r for r in config.analytics if 'atomicblue' not in r.metadata.get('tags', [])],
    'tactics': tactics,
    'analytic_lookup': config.analytic_lookup,
    'techniques': techniques,
    'domains': config.domains,
    'sources': config.sources,
    # force default dict to serialize
    'coverage': {k: dict(v) for k, v in config.coverage.items()},
    'zip': zip
}


def rstjinja(app, docname, source):
    src = source[0]
    rendered = app.builder.templates.render_string(src, rst_context)
    source[0] = rendered


def setup(app):
    if os.path.exists("analytics"):
        shutil.rmtree("analytics")

    if os.path.exists("matrices"):
        shutil.rmtree("matrices")

    os.mkdir("analytics")
    os.mkdir("matrices")

    def create_analytics(app):
        # Dynamically create the .RST files for each analytic
        if getattr(app.builder, 'templates', None) is None:
            app.builder.create_template_bridge()
            app.builder.templates.init(app.builder)

        # .. include with ReST doesn't work with Jinja templates, so it needs to be expanded
        template = app.builder.templates.environment.get_template("links.rst")
        with open(os.path.join("links.rst"), "wb") as f:
            f.write(template.render(**rst_context).encode("utf8"))

        template = app.builder.templates.environment.get_template("analytic.rst")
        for analytic in config.analytics:
            with open(os.path.join("analytics", analytic.id + ".rst"), "wb") as f:
                rendered = template.render(analytic=analytic, **rst_context)
                f.write(rendered.encode("utf8"))

        # Generate ATT&CK matrices
        template = app.builder.templates.environment.get_template("matrix.rst")
        with open(os.path.join("matrices", "enterprise.rst"), "wb") as f:
            rendered = template.render(matrix_cells=get_matrix(), platform="Enterprise ATT&CK Matrix", **rst_context)
            f.write(rendered.encode("utf8"))

        with open(os.path.join("matrices", "windows.rst"), "wb") as f:
            rendered = template.render(matrix_cells=get_matrix("Windows"), os=True, platform="Windows", **rst_context)
            f.write(rendered.encode("utf8"))

        # Will add back when support exists
        with open(os.path.join("matrices", "linux.rst"), "wb") as f:
            rendered = template.render(matrix_cells=get_matrix("Linux"), os=True, platform="Linux", **rst_context)
            f.write(rendered.encode("utf8"))

        with open(os.path.join("matrices", "macos.rst"), "wb") as f:
            rendered = template.render(matrix_cells=get_matrix("macOS"), os=True, platform="macOS", **rst_context)
            f.write(rendered.encode("utf8"))

    app.add_stylesheet('atomicblue.css')
    app.connect("source-read", rstjinja)
    app.connect("builder-inited", create_analytics)
