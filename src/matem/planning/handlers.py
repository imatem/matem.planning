# -*- coding: utf-8 -*-
from zope.component import adapter
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent

from matem.planning.content.plan import IPlan
import os
from plone import namedfile
# from plone.namedfile.field import NamedBlobFile

from plone import api
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite

PLAN_LATEX_TEMPLATE = r"""
    \documentclass[11pt, letterpaper]{article}
    \usepackage[utf8]{inputenc}
    \usepackage[spanish]{babel}
    \usepackage{graphics}
    \usepackage{graphicx}
    \usepackage{latexsym}
    \usepackage{amsmath}

    \usepackage{color}
    \usepackage{tikz}

    \makeatletter

    \hoffset = 0pt
    \oddsidemargin = 5pt
    \evensidemargin = 5pt
    \topmargin = -45pt
    \headheight = 12pt
    \headsep = 30pt
    \textheight = 623pt
    \textwidth = 475pt
    \marginparsep = 7pt
    \marginparwidth = 30pt
    \footskip = 36pt

    \newcommand*{\institution}[1]{\def\@institution{#1}}
    \newcommand*{\phone}[1]{\def\@phone{#1}}
    \newcommand*{\email}[1]{\def\@email{#1}}
    \newcommand*{\homepage}[1]{\def\@homepage{#1}}

    \newcommand*{\phonesymbol}{}
    \newcommand*{\emailsymbol}{}
    \newcommand*{\homepagesymbol}{}

    \newcommand*{\marvosymbol}[1]{{\fontfamily{mvs}\fontencoding{U}\fontseries{m}\fontshape{n}\selectfont\char#1}}
    \renewcommand*{\phonesymbol}{\marvosymbol{84}~}
    \renewcommand*{\emailsymbol}{\marvosymbol{66}~}
    \renewcommand*{\homepagesymbol}{{\Large\marvosymbol{205}}~}

    \newlength{\maketitlewidth}
    \renewcommand*{\maketitle}{
      \setlength{\maketitlewidth}{.9\textwidth}
      \hfil
      \parbox{\maketitlewidth}{
        \centering
           { \Large\bfseries\upshape\@author}
           {\Large\mdseries\upshape ~|~\@title}\\
           {\normalsize\mdseries\upshape\@institution \smallskip\\}
           
           {\phonesymbol\@phone\ \rmfamily\textbullet\ \emailsymbol\@email}
     }\\[4.5em]}

    \title{%s}
    \author{%s}
    \institution{%s}
    \phone{%s}
    \email{%s}
    \homepage{%s}
    \date{%s}

    \begin{document}
    \maketitle

    %s

    \end{document}

"""


@adapter(IPlan, IObjectCreatedEvent)
def handlerCreatedPlan(self, event):

    plant = self.plan_type
    userid = api.user.get_current().id
    # Be carefull with this
    # if userid == 'admin':
    #     userid = self.Login()

    if plant == 'plantext':

        plantext = self.text

        if plantext:

            tex_title = self.title
            tex_author = ""
            # tex_institution = "Instituto de Matemáticas, Universidad Nacional Autónoma de México".decode('utf-8')
            tex_institution = "IM - UNAM"
            tex_phone = ""
            tex_email = ""
            tex_homepage = ""
            tex_date = ""

            catalog = getToolByName(getSite(), 'portal_catalog')
            query = {
                'portal_type': 'FSDPerson',
                'id': userid
            }
            brains = catalog.searchResults(query)
            if brains:
                obj = brains[0].getObject()
                tex_author = obj.Title().decode('utf-8', 'ignore')
                tex_phone = getattr(obj, 'officePhone', '')
                tex_email = obj.getEmail()
                websites = obj.getWebsites()
                if websites:
                    tex_homepage = websites[0]
                # tex_date = "13 de Octubre de 2016"
            # title_plan = 'foo.tex'
            title_plan = "%s.tex" % (userid)
            mainTex = '% !TEX encoding = UTF-8 Unicode\n'
            mainTex += PLAN_LATEX_TEMPLATE % (
                tex_title,
                tex_author,
                tex_institution,
                tex_phone,
                tex_email,
                tex_homepage,
                tex_date,
                plantext,
            )
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

            pdfname = "%s.pdf" % (userid)
            new_file = open(pdfname, "rb")
            self.textfile = namedfile.NamedBlobFile(new_file.read(), filename=u"plan.pdf")
            try:
                logfile = "%s.log" % (userid)
                auxfile = "%s.aux" % (userid)
                os.remove(os.path.join(logfile))  # log file
                os.remove(os.path.join(auxfile))  # aux file
                os.remove(os.path.join(pdfname))  # pdf file
                os.remove(file_path)  # tex file
            except OSError:
                pass


@adapter(IPlan, IObjectModifiedEvent)
def handlerModifiedPlan(self, event):

    plant = self.plan_type
    userid = api.user.get_current().id
    # Be carefull with this
    if userid == 'admin':
        userid = self.Login()

    if plant == 'plantext':

        plantext = self.text

        if plantext:

            tex_title = self.title
            tex_author = ""
            tex_institution = "IM - UNAM"
            tex_phone = ""
            tex_email = ""
            tex_homepage = ""
            tex_date = ""

            catalog = getToolByName(getSite(), 'portal_catalog')
            query = {
                'portal_type': 'FSDPerson',
                'id': userid
            }
            brains = catalog.searchResults(query)
            if brains:
                obj = brains[0].getObject()
                tex_author = obj.Title().decode('utf-8', 'ignore')
                tex_phone = getattr(obj, 'officePhone', '')
                tex_email = obj.getEmail()
                websites = obj.getWebsites()
                if websites:
                    tex_homepage = websites[0]
            # title_plan = 'foo.tex'
            title_plan = "%s.tex" % (userid)
            mainTex = '% !TEX encoding = UTF-8 Unicode\n'
            mainTex += PLAN_LATEX_TEMPLATE % (
                tex_title,
                tex_author,
                tex_institution,
                tex_phone,
                tex_email,
                tex_homepage,
                tex_date,
                plantext,
            )

            # mainTex += PLAN_LATEX_TEMPLATE % (plantext,)
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

            pdfname = "%s.pdf" % (userid)
            new_file = open(pdfname, "rb")
            self.textfile = namedfile.NamedBlobFile(new_file.read(), filename=u"plan.pdf")
            try:
                logfile = "%s.log" % (userid)
                auxfile = "%s.aux" % (userid)
                os.remove(os.path.join(logfile))  # log file
                os.remove(os.path.join(auxfile))  # aux file
                os.remove(os.path.join(pdfname))  # pdf file
                os.remove(file_path)  # tex file
            except OSError:
                pass


