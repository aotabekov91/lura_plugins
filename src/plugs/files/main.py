from qapp.app.plug import FileBrowser as Plug

class FileBrowser(Plug):

    def __init__(self, app): 

        super().__init__(app=app, 
                         position='left', 
                         listen_port=False,
                         mode_keys={'command':'f'})
