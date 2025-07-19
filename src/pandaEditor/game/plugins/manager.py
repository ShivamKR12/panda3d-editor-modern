from yapsy.PluginManager import PluginManager


class Manager(PluginManager):
    """
    Manager class extending yapsy.PluginManager to manage plugins.

    Methods:
        on_init(): Initialize all loaded plugins by calling their on_init method.
    """

    def on_init(self):
        """
        Initialize all loaded plugins by invoking their on_init method.

        Calls on_init on each plugin's plugin_object.
        """
        for plugin in self.getAllPlugins():
            plugin.plugin_object.on_init()
