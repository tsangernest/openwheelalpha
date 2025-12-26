##################################################
# Receiving a lot of NoModuleFoundErrors when trying to import this
# decorator???? Look no further!
#
# This adds the path to sys.path, and remains LOCAL to that virtualenvironment
##################################################
#
# cd $(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
# echo /some/library/path > some-library.pth
##################################################

from time import perf_counter
from functools import wraps


def et(f):
    @wraps(f)
    def w(*args, **kwargs):
        ut = {
            "ns": (1e-6, 1e9),
            "us": (1e-3, 1e6),
            "ms": (1, 1e3),
            "s": (float("inf"), 1),
        }
        a = perf_counter()
        r = f(*args, **kwargs)
        dur = perf_counter() - a
        for u, (t, m) in ut.items():
            if dur < t:
                print(f"\n.:[{f.__name__}]:. .:[{dur*m:.4f}{u}]:.")
                break
        return r
    return w
