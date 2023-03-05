# -*- coding: utf-8 -*-
import time



class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def buildUrl(path):
        return path

    @staticmethod
    def buildStaticUrl(path):
        from application import app
        release_version = app.config.get('RELEASE_VERSION')
        ver = "%s" % (int(time.time())) if not release_version else release_version
        path = "/static" + path + "?ver=" + ver
        return UrlManager.buildUrl(path)

    @staticmethod
    def buildImageUrl(path):
        from application import app
        url = app.config['APP']['domain'] + app.config['UPLOAD']['prefix_url'] + path
        return url
