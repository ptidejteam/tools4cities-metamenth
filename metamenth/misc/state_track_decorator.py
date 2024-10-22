import sys
from metamenth.datatypes.observable_message import ObservableMessage


class StateTrackDecorator:
    """
    This decorator class wraps around methods that need their state
    to be logged whenever changed occur
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return lambda *args, **kwargs: self(instance, *args, **kwargs)

    def __call__(self, instance, *args, **kwargs):
        """

        :param instance: the instance of the class whose state needs to be logged
        :param args: arguments of method modifying instance state
        :param kwargs: key value argument of method modifying instance state
        :return:
        """
        try:
            if getattr(instance, 'track_state'):
                variable_name = self.func.__name__

                index = variable_name.find('_')
                # for methods such as add_room, add_open_space, remove "remove" and "add"
                if variable_name[:3] == 'add' or variable_name[:6] == 'remove':
                    variable_name = variable_name[index+1:]

                # check if after removing add and remove prefix, the resulting output is a class instance
                # variable. If not add s to the resulting variable
                if not hasattr(instance, variable_name) and variable_name[-1] != 's':
                    variable_name = variable_name + 's'

                instance.notify_observers(ObservableMessage(
                    instance.__class__.__name__,
                    instance.UID, {variable_name: getattr(instance, '_' + variable_name)}))
        except AttributeError as err:
            print(err, file=sys.stderr)
        return self.func(instance, *args, **kwargs)
