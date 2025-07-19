import panda3d.core as pm

from pandaEditor.game.nodes.lensnode import LensNode
from pandaEditor.game.nodes.componentmetaclass import ComponentMetaClass


class Camera(LensNode, metaclass=ComponentMetaClass):
    
    type_ = pm.Camera
