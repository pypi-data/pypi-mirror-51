# -*- coding: utf-8 -*-
# Copyright © 2019 Taylor C. Richberger
# This code is released under the license described in the LICENSE file

from .error import ExitError

class Commands:
    def bye(self):
        print('bye!')
        raise ExitError()

    exit = bye
