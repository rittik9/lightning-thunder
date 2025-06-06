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

import inspect
import os
import shutil
import sys
from importlib.util import module_from_spec, spec_from_file_location

from lightning_utilities.core.imports import package_available

_INSTALLED_NEW_THEME = package_available("lai_sphinx_theme")

if _INSTALLED_NEW_THEME:
    import lai_sphinx_theme
else:
    import pt_lightning_sphinx_theme
    import warnings

    warnings.warn(
        "You are using the old theme, please install the new theme 'lai_sphinx_theme';"
        " you can do this by running 'make get-sphinx-theme'."
    )


_PATH_HERE = os.path.abspath(os.path.dirname(__file__))
_PATH_ROOT = os.path.realpath(os.path.join(_PATH_HERE, "..", ".."))
sys.path.insert(0, os.path.abspath(_PATH_ROOT))

SPHINX_MOCK_REQUIREMENTS = int(os.environ.get("SPHINX_MOCK_REQUIREMENTS", True))

# alternative https://stackoverflow.com/a/67692/4521646
spec = spec_from_file_location("thunder/__about__.py", os.path.join(_PATH_ROOT, "thunder", "__about__.py"))
about = module_from_spec(spec)
spec.loader.exec_module(about)

# -- Project information -----------------------------------------------------

# this name shall match the project name in Github as it is used for linking to code
project = "lightning-thunder"
copyright = about.__copyright__
author = about.__author__

# The short X.Y version
version = about.__version__
# The full version, including alpha/beta/rc tags
release = about.__version__

# Options for the linkcode extension
# ----------------------------------
github_user = "Lightning-AI"
github_repo = project

linkcheck_ignore = [
    rf"https://github.com/Lightning-AI/lightning-thunder(/.*|\.git)",
    rf"https://github.com/Lightning-AI/.*/blob/.*#.*",  # github anchors are tricky
    rf"https://github.com/pytorch/.*/blob/.*#.*",  # github anchors are tricky
]

# -- Project documents -------------------------------------------------------


def _transform_changelog(path_in: str, path_out: str) -> None:
    with open(path_in) as fp:
        chlog_lines = fp.readlines()
    # enrich short subsub-titles to be unique
    chlog_ver = ""
    for i, ln in enumerate(chlog_lines):
        if ln.startswith("## "):
            chlog_ver = ln[2:].split("-")[0].strip()
        elif ln.startswith("### "):
            ln = ln.replace("###", f"### {chlog_ver} -")
            chlog_lines[i] = ln
    with open(path_out, "w") as fp:
        fp.writelines(chlog_lines)


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.

needs_sphinx = "5.3"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    # 'sphinxcontrib.mockautodoc',  # raises error: directive 'automodule' is already registered ...
    # 'sphinxcontrib.fulltoc',  # breaks pytorch-theme with unexpected kw argument 'titles_only'
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.linkcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
    "myst_parser",
    "nbsphinx",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
    "sphinx_paramlinks",
    "sphinx_togglebutton",
]
if _INSTALLED_NEW_THEME:
    extensions.append("lai_sphinx_theme.extensions.lightning")

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

myst_update_mathjax = False

# https://berkeley-stat159-f17.github.io/stat159-f17/lectures/14-sphinx..html#conf.py-(cont.)
# https://stackoverflow.com/questions/38526888/embed-ipython-notebook-in-sphinx-document
# I execute the notebooks manually in advance. If notebooks test the code,
# they should be run at build time.
nbsphinx_execute = "never"
nbsphinx_allow_errors = True
nbsphinx_requirejs_path = ""

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
# source_suffix = ['.rst', '.md', '.ipynb']
# source_suffix = {
#     ".rst": "restructuredtext",
#     ".txt": "markdown",
#     ".md": "markdown",
#     ".ipynb": "nbsphinx",
# }
source_parsers = {".rst": "restructuredtext", ".txt": "markdown", ".md": "markdown", ".ipynb": "nbsphinx"}

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "PULL_REQUEST_TEMPLATE.md",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "lai_sphinx_theme" if _INSTALLED_NEW_THEME else "pt_lightning_sphinx_theme"
html_theme_path = [
    lai_sphinx_theme.get_html_theme_path() if _INSTALLED_NEW_THEME else pt_lightning_sphinx_theme.get_html_theme_path()
]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.

html_theme_options = {
    "pytorch_project": about.__homepage__,
    "canonical_url": about.__homepage__,
    "collapse_navigation": False,
    "display_version": True,
    "logo_only": False,
}

html_favicon = "_static/images/icon.svg"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_templates", "_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = project + "-doc"

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',
    # Latex figure (float) alignment
    "figure_align": "htbp",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, project + ".tex", project + " Documentation", author, "manual"),
]

# MathJax configuration
mathjax3_config = {
    "tex": {"packages": {"[+]": ["ams", "newcommand", "configMacros"]}},
}

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, project, project + " Documentation", [author], 1)]

# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        project,
        project + " Documentation",
        author,
        project,
        about.__docs__,
        "Miscellaneous",
    ),
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
epub_exclude_files = ["search.html"]

# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "torch": ("https://pytorch.org/docs/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    # "optree": ("https://optree.readthedocs.io/en/latest/index.html", None),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


def setup(app):
    # this is for hiding doctest decoration,
    # see: http://z4r.github.io/python/2011/12/02/hides-the-prompts-and-output/
    app.add_js_file("copybutton.js")


# copy all notebooks to local folder
path_nbs = os.path.join(_PATH_HERE, "notebooks")
path_nbs_git = os.path.join(_PATH_ROOT, "notebooks")
if not os.path.isdir(path_nbs):
    os.mkdir(path_nbs)
for pathname, dirnames, filenames in os.walk(path_nbs_git):
    dest_pathname = pathname.replace(path_nbs_git, path_nbs)
    for path_ipynb in filenames:
        if path_ipynb.endswith(".ipynb"):
            os.makedirs(dest_pathname, exist_ok=True)
            shutil.copy(os.path.join(pathname, path_ipynb), os.path.join(dest_pathname, path_ipynb))


# Ignoring Third-party packages
# https://stackoverflow.com/questions/15889621/sphinx-how-to-exclude-imports-in-automodule
def _package_list_from_file(file):
    list_pkgs = []
    with open(file) as fp:
        lines = fp.readlines()
    for ln in lines:
        found = [ln.index(ch) for ch in list(",=<>#") if ch in ln]
        pkg = ln[: min(found)] if found else ln
        if pkg.rstrip():
            list_pkgs.append(pkg.rstrip())
    return list_pkgs


# define mapping from PyPI names to python imports
PACKAGE_MAPPING = {
    "PyYAML": "yaml",
}
MOCK_PACKAGES = []
if SPHINX_MOCK_REQUIREMENTS:
    # mock also base packages when we are on RTD since we don't install them there
    MOCK_PACKAGES += _package_list_from_file(os.path.join(_PATH_ROOT, "requirements", "base.txt"))
MOCK_PACKAGES = [PACKAGE_MAPPING.get(pkg, pkg) for pkg in MOCK_PACKAGES]

autodoc_mock_imports = MOCK_PACKAGES


# Resolve function
# This function is used to populate the (source) links in the API
def linkcode_resolve(domain, info):
    def find_source():
        # try to find the file and line number, based on code from numpy:
        # https://github.com/numpy/numpy/blob/master/doc/source/conf.py#L286
        obj = sys.modules[info["module"]]
        for part in info["fullname"].split("."):
            obj = getattr(obj, part)
        fname = inspect.getsourcefile(obj)
        # https://github.com/rtfd/readthedocs.org/issues/5735
        if any(s in fname for s in ("readthedocs", "rtfd", "checkouts")):
            # /home/docs/checkouts/readthedocs.org/user_builds/pytorch_lightning/checkouts/
            #  devel/pytorch_lightning/utilities/cls_experiment.py#L26-L176
            path_top = os.path.abspath(os.path.join("..", "..", ".."))
            fname = os.path.relpath(fname, start=path_top)
        else:
            # Local build, imitate master
            fname = "master/" + os.path.relpath(fname, start=os.path.abspath(".."))
        source, lineno = inspect.getsourcelines(obj)
        return fname, lineno, lineno + len(source) - 1

    if domain != "py" or not info["module"]:
        return None
    try:
        filename = "%s#L%d-L%d" % find_source()
    except Exception:
        filename = info["module"].replace(".", "/") + ".py"
    # import subprocess
    # tag = subprocess.Popen(['git', 'rev-parse', 'HEAD'], stdout=subprocess.PIPE,
    #                        universal_newlines=True).communicate()[0][:-1]
    branch = filename.split("/")[0]
    # do mapping from latest tags to master
    branch = {"latest": "main", "stable": "main"}.get(branch, branch)
    filename = "/".join([branch] + filename.split("/")[1:])
    return f"https://github.com/{github_user}/{github_repo}/blob/{filename}"


autosummary_generate = True
autodoc_typehints = "description"

autodoc_member_order = "groupwise"
autoclass_content = "both"
# the options are fixed and will be soon in release,
#  see https://github.com/sphinx-doc/sphinx/issues/5459
autodoc_default_options = {
    "members": None,
    "methods": None,
    # 'attributes': None,
    "special-members": "__call__",
    "exclude-members": "_abc_impl",
    "show-inheritance": True,
    "private-members": True,
    "noindex": True,
}

# Sphinx will add “permalinks” for each heading and description environment as paragraph signs that
#  become visible when the mouse hovers over them.
# This value determines the text for the permalink; it defaults to "¶". Set it to None or the empty
#  string to disable permalinks.
# https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_add_permalinks
# html_add_permalinks = "¶"

# True to prefix each section label with the name of the document it is in, followed by a colon.
#  For example, index:Introduction for a section called Introduction that appears in document index.rst.
#  Useful for avoiding ambiguity when the same section heading appears in different documents.
# http://www.sphinx-doc.org/en/master/usage/extensions/autosectionlabel.html
autosectionlabel_prefix_document = True

# only run doctests marked with a ".. doctest::" directive
doctest_test_doctest_blocks = ""
doctest_global_setup = """

import importlib
import os
import torch

"""
coverage_skip_undoc_in_source = True

import thunder  # noqa: E402 # making the docs build happy

# Avoid the Sphinx error when using `inspect.signature(Timer.adaptive_autorange)`
from torch.utils.benchmark import Timer
