u"""atendimento URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from __future__ import absolute_import
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView

import servicos.urls
import usuarios.urls

urlpatterns = [
    url(ur'^admin/', admin.site.urls),
    url(ur'^$', TemplateView.as_view(template_name=u'index.html'), name=u'home'),
    url(ur'', include(servicos.urls)),
    url(ur'', include(usuarios.urls)),
    url(ur'^captcha/', include(u'captcha.urls')),
]
