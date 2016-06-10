from __future__ import absolute_import
import os

import yaml
from django import template
from django.core.urlresolvers import reverse

from sapl.settings import BASE_DIR
from io import open

register = template.Library()
TEMPLATES_DIR = BASE_DIR.child(u"templates")


@register.inclusion_tag(u'menus/subnav.html', takes_context=True)
def subnav(context, path=None):
    u"""Renders a subnavigation for views of a certain object.

    If not provided, path defaults to <app_name>/subnav.yaml
    """
    # TODO: 118n !!!!!!!!!!!!!!
    # How to internationalize yaml files????
    menu = None
    root_pk = context.get(u'root_pk', None)
    if not root_pk:
        obj = context.get(u'object', None)
        if obj:
            root_pk = obj.pk
    if root_pk:
        request = context[u'request']
        app = request.resolver_match.app_name
        # Esse IF elimina o bug do subnav em Tabelas Auxiliares
        # e também em proposições
        if request.path.find(app) == -1:
            return
        default_path = u'%s/subnav.yaml' % app
        path = os.path.join(TEMPLATES_DIR, path or default_path)
        if os.path.exists(path):
            menu = yaml.load(open(path, u'r'))
            resolve_urls_inplace(menu, root_pk, app)
    return {u'menu': menu}


def resolve_urls_inplace(menu, pk, app):
    if isinstance(menu, list):
        for item in menu:
            resolve_urls_inplace(item, pk, app)
    else:
        if u'url' in menu:
            menu[u'url'] = reverse(u'%s:%s' % (app, menu[u'url']),
                                  kwargs={u'pk': pk})
        if u'children' in menu:
            resolve_urls_inplace(menu[u'children'], pk, app)
