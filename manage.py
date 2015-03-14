#!/usr/bin/env python
import os
import sys
from TAPP.settings import DEPLOY_MODE

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TAPP.settings")

    from django.core.management import execute_from_command_line

    print("Running in %s\n"% DEPLOY_MODE)

    execute_from_command_line(sys.argv)
