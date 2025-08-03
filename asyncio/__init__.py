from inspect import iscoroutine, iscoroutinefunction

__all__ = ["get_event_loop", "iscoroutine", "iscoroutinefunction"]


def get_event_loop():
    raise RuntimeError("asyncio event loop unavailable")
