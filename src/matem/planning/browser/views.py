# -*- coding: utf-8 -*-
from matem.planning import _
from plone.dexterity.browser.view import DefaultView
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from AccessControl import getSecurityManager
from AccessControl.User import UnrestrictedUser
from Products.CMFCore.utils import getToolByName
from AccessControl.SecurityManagement import newSecurityManager
from Products.statusmessages.interfaces import IStatusMessage


class PlanView(DefaultView):
    """The default view for plans."""

    def hasfile(self):
        if self.context.plan_type == 'plantext':
            if self.context.textfile:
                return True
            return False
        else:
            if self.context.file:
                return True
            return False

    def getFile(self):
        if self.context.plan_type == 'plantext':
            return self.context.textfile

        return self.context.file

    def candownload(self):
        current_state = api.content.get_state(self.context)
        if current_state == 'sended':
            return True
        return False
    
    def viewButtonSendAgain(self):
        # self.context.workflow_history

        plan_content = self.context

        if 'sended' == api.content.get_state(obj=plan_content):
            return False
        
        year_plan = int(plan_content.id)
        year_report = year_plan - 1
        noappoved = []
        try:
            reports_path = '/acerca-de/estructura-interna/secretaria-academica/informes/investigadores/'+ str(year_report)
            with api.env.adopt_user(username='admin'):
                annual = api.content.get(reports_path)
                noappoved = eval(annual.noapprovedplanparticipants)
        except Exception:
            noappoved = []
        
        usercurrent = api.user.get_current()
        userid = usercurrent.id
        roles = api.user.get_roles(username=userid, obj=plan_content)
        modifyplan = api.user.has_permission('matem.planning: Modify Plan', username=userid, obj=plan_content)
        if userid in noappoved or ('Manager' in roles):
            if 'Owner' in roles and modifyplan:
                return True

        return False


class SendPlanAgainView(BrowserView):

    template = ViewPageTemplateFile('templates/send_plan_again.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request


    def __call__(self):
        import pdb; pdb.set_trace()
        
        if self.request.form:
            if self.request.form.get('again', ''):
                plan_content = self.context
                year_plan = plan_content.id
                plans_path = '/acerca-de/estructura-interna/secretaria-academica/informes/planes/' + year_plan
                with api.env.adopt_user(username='admin'):
                    plan_folder = api.content.get(plans_path)
                # crear una copia en plan_folder
                # moverlo a los enviados
                portal = getToolByName(self.context, 'portal_url').getPortalObject()
                
                sm = getSecurityManager()
                try:
                    tmp_user = UnrestrictedUser(sm.getUser().getId(), '', ['Manager'], '')
                    tmp_user = tmp_user.__of__(portal.acl_users)
                    newSecurityManager(None, tmp_user)

                    wft = api.portal.get_tool('portal_workflow')
                    wft.doActionFor(plan_content, 'submit_send')
                    id = self.context.Login()

                    plan_folder.manage_clone(plan_content, id)
                    newplanfile = plan_folder[id]
                    newplanfile.setTitle('Plan de trabajo de %s para el %s' % (self.context.getResearcherName(), year_plan))
                    newplanfile.reindexObject()

                    wft.doActionFor(newplanfile, 'submit_send')

                    # very important la fixed structure
                    parentobj = plan_content.aq_parent
                    cvfolderparent = parentobj.aq_parent
                    cvfolderparent['enviados']['planes'].manage_pasteObjects(parentobj.manage_cutObjects([plan_content.id]))

                    self.fixOwnerRole(newplanfile, 'admin', recursive=False)
                except Exception:
                    IStatusMessage(self.request).addStatusMessage(_(u"Error: no se pudo hacer el reenvio"), "error")
                    context_state = self.context.aq_parent.restrictedTraverse("@@plone_context_state")
                    # url = context_state.view_url() + "/" + "reportsended"
                    url = context_state.view_url()
                    self.request.response.redirect(url)
                    return ''
                    

            context_state = self.context.aq_parent.restrictedTraverse("@@plone_context_state")
            IStatusMessage(self.request).addStatusMessage(_(u"Su reenvio de plan ha sido recibido por la Secretaría Académica"), "info")
            # url = context_state.view_url() + "/" + "send_plan_again"
            url = context_state.view_url()
            self.request.response.redirect(url)
            return ''

        return self.template()

    def fixOwnerRole(self, obj, user_id, recursive=True):
        owners = obj.users_with_local_role("Owner")
        obj.manage_delLocalRoles(owners)
        obj.manage_setLocalRoles(user_id, ('Owner', ))

        if recursive:
            for item in obj.objectValues():
                self.fixOwnerRole(item, user_id, recursive=True)