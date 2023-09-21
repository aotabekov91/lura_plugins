from plug.plugs.parser import Parser as Base

class Parser(Base):

    def setup(self):

        super().setup()
        self.setParser()

    def setParser(self):

        super().setParser()
        self.parser.add_argument(
                'file', nargs='?', default=None, type=str)
        self.parser.add_argument(
                '-p', '--page', default=0, type=int)
        self.parser.add_argument(
                '-x', '--xaxis', default=0., type=float)
        self.parser.add_argument(
                '-y', '--yaxis', default=0., type=float)
