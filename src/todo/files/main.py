from plug.qt.plugs import FileBrowser as Plug

class FileBrowser(Plug):

    def __init__(self, 
                 app, 
                 position='left',
                 **kwargs): 

        super().__init__(app=app, 
                         position=position, 
                         **kwargs,
                         )
