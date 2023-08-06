from guillotina.schema import BytesLine
from zope.interface import Interface


class IDatabaseConfigurationFactory(Interface):
    """
    Factory to create database object
    """


class IConfigurationContext(Interface):
    """Configuration Context

    The configuration context manages information about the state of
    the configuration system, such as the package containing the
    configuration file. More importantly, it provides methods for
    importing objects and opening files relative to the package.
    """

    package = BytesLine(
        title="The current package name",
        description="""\
          This is the name of the package containing the configuration
          file being executed. If the configuration file was not
          included by package, then this is None.
          """,
        required=False,
    )

    def action(
        discriminator, callable, args=None, kw=None, order=0, includepath=None, info=None  # noqa: N805
    ):
        """Record a configuration action

        The job of most directives is to compute actions for later
        processing.  The action method is used to record those
        actions.  The discriminator is used to to find actions that
        conflict. Actions conflict if they have the same
        discriminator. The exception to this is the special case of
        the discriminator with the value None. An actions with a
        discriminator of None never conflicts with other actions. This
        is possible to add an order argument to crudely control the
        order of execution.  'info' is optional source line information,
        'includepath' is None (the default) or a tuple of include paths for
        this action.
        """
