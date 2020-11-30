
class property:

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        val = self.func(instance)
        setattr(instance, self.func.__name__, val)
        return val


class classproperty(object):

    def __init__(self, func):
        self.func = func

    def __get__(self, owner_self, owner_cls):
        val = self.func(owner_cls)
        setattr(owner_cls, self.func.__name__, val)
        return val
