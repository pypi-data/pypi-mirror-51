from sprockets.mixins import metrics

project = 'sprockets.mixins.metrics'
copyright = 'AWeber Communications, Inc.'
version = metrics.__version__
release = '.'.join(str(v) for v in metrics.version_info[0:2])

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

master_doc = 'index'
html_style = 'custom.css'
html_static_path = ['_static']
html_sidebars = {
    '**': ['about.html', 'navigation.html'],
}
html_theme_options = {
    'github_user': 'sprockets',
    'github_repo': 'sprockets.mixins.metrics',
    'description': 'Application metrics tracker',
    'github_banner': True,
    'travis_button': True,
    'codecov_button': True,
}

intersphinx_mapping = {
    'python': ('http://docs.python.org/3/', None),
    'tornado': ('http://tornadoweb.org/en/latest/', None),
}
