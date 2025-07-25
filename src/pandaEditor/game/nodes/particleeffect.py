import os

from direct.particles.ParticleEffect import ParticleEffect as DirectParticleEffect
from direct.showbase.PythonUtil import getBase as get_base
import panda3d.core as pc

from pandaEditor.game.nodes.attributes import PythonTagAttribute
from pandaEditor.game.nodes.constants import TAG_NODE_TYPE
from pandaEditor.game.nodes.nodepath import NodePath


class ParticleEffect(NodePath):

    type_ = DirectParticleEffect
    config_path = PythonTagAttribute(
        pc.Filename,
        read_only=True,
        required=True,
    )

    @classmethod
    def create(cls, *args, **kwargs):
        get_base().enable_particles()

        effect = DirectParticleEffect()
        effect.set_tag(TAG_NODE_TYPE, 'ParticleEffect')

        file_path = kwargs.get('config_path')
        if file_path is not None:
            # HAXXOR
            # Make relative to project somehow. We don't get this problem with
            # models because of panda's model search path.
            if not os.path.isabs(file_path):
                file_path = os.path.join(get_base().project.path, file_path)
            file_path = os.path.normpath(file_path)  # .replace('\\', '/')
            file_path = pc.Filename.from_os_specific(file_path)

            effect.load_config(file_path)
            effect.start()

        comp = super().create(data=effect)
        if file_path is not None:
            comp.config_path = file_path

        return comp
