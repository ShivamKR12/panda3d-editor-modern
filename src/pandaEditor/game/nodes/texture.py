import panda3d.core as pc
from direct.showbase.PythonUtil import getBase as get_base

from pandaEditor.game.nodes.attributes import Attribute
from pandaEditor.game.nodes.nongraphobject import NonGraphObject


class Texture(NonGraphObject):

    type_ = pc.Texture
    fullpath = Attribute(
        pc.Filename,
        pc.Texture.get_fullpath,
        required=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        fullpath = kwargs.pop('fullpath', None)
        panda_fullpath = pc.Filename.from_os_specific(fullpath)
        texture = get_base().loader.load_texture(panda_fullpath)
        return super().create(data=texture)
