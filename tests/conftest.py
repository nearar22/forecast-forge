import os


_real_unlink = os.unlink


def _windows_safe_unlink(path, *args, **kwargs):
    try:
        return _real_unlink(path, *args, **kwargs)
    except PermissionError:
        # gltest replaces fd 0 with this file before closing the duplicated
        # Windows handle. The OS removes it when the runner releases that handle.
        return None


os.unlink = _windows_safe_unlink
