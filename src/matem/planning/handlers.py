# -*- coding: utf-8 -*-
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from matem.planning.content.plan import IPlan
import os
from plone import namedfile
# from plone.namedfile.field import NamedBlobFile

PLAN_LATEX_TEMPLATE = r"""
    \documentclass[11pt, letterpaper]{article}
    \usepackage[utf8]{inputenc}
    \usepackage[spanish]{babel}
    \usepackage{graphics}
    \usepackage{graphicx}
    \usepackage{latexsym}
    \usepackage{amsmath}

    \begin{document}

    %s

    \end{document}

"""


@adapter(IPlan, IObjectCreatedEvent)
def handlerCreatedPlan(self, event):

    plant = self.plan_type

    if plant == 'plantext':

        plantext = self.text

        if plantext:

            title_plan = 'foo.tex'
            mainTex = '% !TEX encoding = UTF-8 Unicode\n'
            mainTex += PLAN_LATEX_TEMPLATE % (plantext,)
            try:
                # fileTex = unicode(mainTex, "utf-8", errors="ignore")
                fileTex = mainTex.encode('utf-8', 'ignore')

                file_path = os.path.join(title_plan)
                file_os = open(file_path, 'wb')
                file_os.write(fileTex)
                file_os.close()

                pdf_file = os.system("pdflatex -interaction=nonstopmode %s"% (file_path))

            except:
                pass

            new_file = open('foo.pdf', "rb")
            self.file = namedfile.NamedBlobFile(new_file.read(), filename=u"plan.pdf")


@adapter(IPlan, IObjectModifiedEvent)
def handlerModifiedPlan(self, event):

    plant = self.plan_type

    if plant == 'plantext':

        plantext = self.text

        if plantext:

            title_plan = 'foo.tex'
            mainTex = '% !TEX encoding = UTF-8 Unicode\n'
            mainTex += PLAN_LATEX_TEMPLATE % (plantext,)
            try:
                # fileTex = unicode(mainTex, "utf-8", errors="ignore")
                fileTex = mainTex.encode('utf-8', 'ignore')

                file_path = os.path.join(title_plan)
                file_os = open(file_path, 'wb')
                file_os.write(fileTex)
                file_os.close()

                pdf_file = os.system("pdflatex -interaction=nonstopmode %s"% (file_path))

            except:
                pass

            new_file = open('foo.pdf', "rb")
            self.file = namedfile.NamedBlobFile(new_file.read(), filename=u"plan.pdf")
