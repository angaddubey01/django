class Local:
    def __init__(self, thread_critical=False):
        self._storage = {}

    def __getattr__(self, name):
        if name in self._storage:
            return self._storage[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == '_storage':
            super().__setattr__(name, value)
        else:
            self._storage[name] = value

    def __delattr__(self, name):
        if name in self._storage:
            del self._storage[name]
        else:
            raise AttributeError(name)
