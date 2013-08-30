import os
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from scss import Scss
from zope.annotation.interfaces import IAnnotations
from plone.app.layout.viewlets.common import ViewletBase

SCSS_FILES = [
    # "components/zug_variables.scss",
    "mixins.scss",
    "components/grid.scss",
    "components/base.scss",
    "components/icons.scss",
    "components/form.scss",
    "components/search.scss",
    "components/tabbedview.scss",
    "components/overlays.scss",
    "components/menues.scss",
    "components/messages.scss",
    "components/tables.scss",
    "components/responsive.scss",
    "components/overrides.scss",
    # "components/overrides_zug.scss",
    ]


class CustomStyles(ViewletBase):

    index = ViewPageTemplateFile('customstyles.pt')

    def update(self):
        css = Scss()
        self.base_path = os.path.split(__file__)[0]

        scss_input = ['@option compress:no;']
        # add variables
        scss_input.append(self.read_file('variables.scss'))

        # add overwritten variables
        scss_input.append(self.get_options())

        # add component files
        for scss_file in SCSS_FILES:
            scss_input.append(self.read_file(scss_file))

        # add overwritten component files
        # for now its not possible to add custom styles

        self.customstyles = css.compile('\n'.join(scss_input))

    def get_options(self):
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        options = IAnnotations(portal).get('customstyles', {})
        styles = []
        for key, value in options.items():
            styles.append('$%s: %s;' % (key.replace('css.',''),
                                        value))
        print '\n'.join(styles)
        return '\n'.join(styles)

    def read_file(self, file_path):
        handler = open(os.path.join(
                self.base_path,
                '../resources/sass/%s' % file_path), 'r')
        file_content = handler.read()
        handler.close()
        return file_content
