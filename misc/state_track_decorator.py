import sys
from datatypes.observable_message import ObservableMessage
from enumerations import BuildingEntity


class LogMethodCall:
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
        :param args:
        :param kwargs:
        :return:
        """
        print(args)
        try:
            if getattr(instance, 'track_state'):
                instance.notify_observers(ObservableMessage(
                    instance.__class__.__name__,
                    instance.UID, {self.func.__name__: getattr(instance, self.func.__name__)}))
        except AttributeError as err:
            print(err, file=sys.stderr)
        return self.func(instance, *args, **kwargs)
