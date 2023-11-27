from gizmo.view.model import Model

class OutlineModel(Model):

    @classmethod
    def getSourceName(cls, source, **kwargs):
        return ('Outline', source)

    @classmethod
    def isCompatible(cls, source, **kwargs):
        return hasattr(source, 'hasOutline', False)
