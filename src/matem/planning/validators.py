# -*- coding: utf-8 -*-

from matem.planning import _
from zope.interface import Invalid

def isValidFileType(value):

    if value:
        if value.contentType != 'application/pdf':
            raise Invalid(_(u'Invalid Type File: please correct it, only accept pdf file'))

    return True
