"""Sphinx Material theme."""

import os
import re
import sys
import xml.etree.ElementTree as ET
from multiprocessing import Manager

import slugify
from bs4 import BeautifulSoup
from sphinx.util import logging, console

input_list = ['A', 'B', 'C', 'D', 'E', 'F']


__version__ = "0.1.0"


def setup(app):
    """Setup connects events to the sitemap builder"""
    app.connect('html-page-context', add_html_link)
    app.connect('build-finished', create_sitemap)
    app.connect('build-finished', reformat_pages)
    app.connect('build-finished', minify_css)
    manager = Manager()
    site_pages = manager.list()
    sitemap_links = manager.list()
    app.multiprocess_manager = manager
    app.sitemap_links = sitemap_links
    app.site_pages = site_pages
    return {'version': __version__,
            'parallel_read_safe': True,
            'parallel_write_safe': True}


def add_html_link(app, pagename, templatename, context, doctree):
    """As each page is built, collect page names for the sitemap"""
    base_url = app.config['html_theme_options'].get('base_url', '')
    if base_url:
        app.sitemap_links.append(base_url + pagename + '.html')
    minify = app.config['html_theme_options'].get('html_minify', False)
    prettify = app.config['html_theme_options'].get('html_prettify', False)
    if minify and prettify:
        raise ValueError('html_minify and html_prettify cannot both be True')
    if minify or prettify:
        app.site_pages.append(os.path.join(app.outdir, pagename + '.html'))


def create_sitemap(app, exception):
    """Generates the sitemap.xml from the collected HTML page links"""
    if (not app.config['html_theme_options'].get('base_url', '') or
            exception is not None or not app.sitemap_links):
        return

    filename = app.outdir + '/sitemap.xml'
    print('Generating sitemap for {0} pages in '
          '{1}'.format(len(app.sitemap_links),
                       console.colorize('blue', filename)))

    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    for link in app.sitemap_links:
        url = ET.SubElement(root, 'url')
        ET.SubElement(url, 'loc').text = link
    app.sitemap_links[:] = []

    ET.ElementTree(root).write(filename)


def reformat_pages(app, exception):
    if exception is not None or not app.site_pages:
        return
    minify = app.config['html_theme_options'].get('html_minify', False)
    last = -1
    npages = len(app.site_pages)
    transform = 'Minifying' if minify else 'Prettifying'
    print('{0} {1} files'.format(transform, npages))
    # TODO: Consider using parallel execution
    for i, page in enumerate(app.site_pages):
        if int(100 * (i / npages)) - last >= 1:
            last = int(100 * (i / npages))
            color_page = console.colorize('blue', page)
            msg = 'minifying files... [{0}%] {1}'.format(last, color_page)
            sys.stdout.write('\033[K' + msg + '\r')
        with open(page, 'r', encoding='utf-8') as content:
            if minify:
                from css_html_js_minify.html_minifier import html_minify
                html = html_minify(content.read())
            else:
                soup = BeautifulSoup(content.read(), features='lxml')
                html = soup.prettify()
        with open(page, 'w', encoding='utf-8') as content:
            content.write(html)
    app.site_pages[:] = []
    print()


def minify_css(app, exception):
    if (exception is not None or
            not app.config['html_theme_options'].get('css_minify', False)):
        app.multiprocess_manager.shutdown()
        return
    import glob
    from css_html_js_minify.css_minifier import css_minify
    css_files = glob.glob(os.path.join(app.outdir, '**', '*.css'),
                          recursive=True)
    print('Minifying {0} css files'.format(len(css_files)))
    for css_file in css_files:
        colorized = console.colorize('blue', css_file)
        msg = 'minifying css file {0}'.format(colorized)
        sys.stdout.write('\033[K' + msg + '\r')
        with open(css_file, 'r', encoding='utf-8') as content:
            css = css_minify(content.read())
        with open(css_file, 'w', encoding='utf-8') as content:
            content.write(css)
    print()
    app.multiprocess_manager.shutdown()


def html_theme_path():
    return [os.path.dirname(os.path.abspath(__file__))]


def toctree_format(toc_text):
    try:
        toc = BeautifulSoup(toc_text, features='html.parser')
        uls = toc.findChildren('ul', recursive=False)
        # Consolidate to a single ul if multiple at the root
        base = uls[0]
        for ul in uls[1:]:
            for child in ul.children:
                if isinstance(child, str):
                    continue
                base.append(child)
            ul.clear()
            ul.extract()

        for ul in toc.find_all('ul'):
            ul['class'] = 'md-nav__list'
            ul['data-md-scrollfix'] = None
        for li in toc.find_all('li'):
            li['class'] = 'md-nav__item'
        for a in toc.find_all('a'):
            a['class'] = 'md-nav__link'
        return str(toc)
    except Exception as exc:
        logger = logging.getLogger(__name__)
        logger.warning('Failed to process toctree_text\n' +
                       str(exc) + '\n' +
                       str(toc_text))
        return toc_text


def walk_contents(tags):
    out = []
    for tag in tags.contents:
        if hasattr(tag, 'contents'):
            out.append(walk_contents(tag))
        else:
            out.append(str(tag))
    return ''.join(out)


def toc_format(toc_text):
    try:
        toc = BeautifulSoup(toc_text, features='html.parser')
        for ul in toc.select('ul'):
            ul['class'] = 'md-nav__list'
        for li in toc.select('li'):
            li['class'] = 'md-nav__item'
        for a in toc.select('a'):
            a['class'] = 'md-nav__link'
            if a['href'] == '#' and a.contents:
                a['href'] = '#' + slugify.slugify(walk_contents(a))
        toc.ul['data-md-scrollfix'] = None
        return str(toc)
    except Exception as exc:
        logger = logging.getLogger(__name__)
        logger.warning('Failed to process toc_text\n' +
                       str(exc) + '\n' +
                       str(toc_text))
        return toc_text


def table_fix(body_text):
    try:
        body = BeautifulSoup(body_text, features='html.parser')
        for table in body.select('table'):
            classes = table.get('class', tuple())
            if 'highlighttable' in classes or 'longtable' in classes:
                continue
            del table['class']
        headers = body.find_all(re.compile('^h[1-6]$'))
        for i, header in enumerate(headers):
            for a in header.select('a'):
                if 'headerlink' in a.get('class', ''):
                    header['id'] = a['href'][1:]
        divs = body.find_all('div', {'class': 'section'})
        for div in divs:
            div.unwrap()

        return str(body)
    except Exception as exc:
        logger = logging.getLogger(__name__)
        logger.warning('Failed to process body_text\n' + str(exc))
        return body_text


def get_html_context():
    return {'toctree_format': toctree_format,
            'toc_format': toc_format,
            'table_fix': table_fix}

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
