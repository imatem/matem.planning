# -*- coding: utf-8 -*-
# from matem.planning import _
from Products.Five.browser import BrowserView
from Products.ATContentTypes.content.base import ATCTMixin


class AlbumPdfView(BrowserView):

    def albums(self):

        items = self.context.items()

        albums = {
            'thumbs': [],
            'files': []
        }

        for item in items:
            obj = item[1]
            if obj.portal_type == 'plan':
                if obj.thumbpdf:
                    albums['thumbs'].append(obj)
                else:
                    albums['files'].append(obj)

        return albums









