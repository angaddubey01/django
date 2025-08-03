class SyncToAsync:
    def __init__(self, func, *args, **kwargs):
        self.func = func

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class AsyncToSync(SyncToAsync):
    pass


def sync_to_async(func, *args, **kwargs):
    return func


def async_to_sync(func, *args, **kwargs):
    return func
