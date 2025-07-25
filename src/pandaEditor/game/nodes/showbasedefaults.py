from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.game.nodes.camera import Camera
from pandaEditor.game.nodes.modelnode import ModelNode
from pandaEditor.game.nodes.nodepath import NodePath
from pandaEditor.game.nodes.componentmetaclass import ComponentMetaClass


class Render(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(cls, data=get_base().render)

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):
        pass


class BaseCamera(ModelNode, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(cls, data=get_base().camera)


class BaseCam(Camera, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(cls, data=get_base().cam)


class Render2d(NodePath, metaclass=ComponentMetaClass):

    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(cls, data=get_base().render2d)

    @property
    def parent(self):
        return get_base().node_manager.wrap(get_base().scene)

    @parent.setter
    def parent(self, value):
        pass
    

class Aspect2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(cls, data=get_base().aspect2d)
    

class Pixel2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(cls, data=get_base().pixel2d)
    

class Camera2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(cls, data=get_base().camera2d)
    

class Cam2d(NodePath, metaclass=ComponentMetaClass):
    
    @classmethod
    def create(cls, *args, **kwargs):
        return super().create(cls, data=get_base().cam2d)
