from plugin.app.plugin import FileBrowser as Plugin

class FileBrowser(Plugin):

    def __init__(self, app): 

        super().__init__(app, position='left', mode_keys={'command':'f'})
