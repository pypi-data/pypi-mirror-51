# -*- coding: utf-8 -*-

from zhlite.zhlite import *

__author__ = "zhangbo"
__email__ = "deplives@deplives.com"

__license__ = "MIT"

__version__ = "1.5.2"
__date__ = "2019-08-19"
__release__ = "`User` 增加 `is_org` 字段区分机构号和个人号"


class Version(object):

    def __init__(self):
        self.info = {
            "version": __version__,
            "date": __date__,
            "release": __release__
        }

    def __str__(self):
        return " ".join([f"{k}: {v}" for k, v in self.info.items()])


version = Version()

__all__ = ["Auth", "User", "Question", "Answer"]
