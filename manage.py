#!/usr/bin/env python
from __future__ import absolute_import
import os
import sys
import dotenv

if __name__ == u"__main__":
    dotenv.read_dotenv(u'.env')

    os.environ.setdefault(u"DJANGO_SETTINGS_MODULE", u"atendimento.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
