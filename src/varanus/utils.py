""" Varanus utilities
"""
import time

COLUMNS, LINES = (80, 20)


def gmtime(ts: int = None) -> time.struct_time:
    if isinstance(ts, str):
        return ts

    if ts:
        ts = int(float(ts))
        if ts > 9999999999:  # a date > 20 Nov 2286 we assume is given in ms
            ts /= 1000       # ts == 10000000000 == 10000000 -> 26 Apr 1970

    return time.gmtime(ts)


def strftime(ts: int = None, format: str = '%a %d %b %Y %I:%M %p') -> str:
    # http://strftime.org/
    return time.strftime(format, gmtime(ts))


def out(o, title=''):
    # Debug
    print()
    print(chr(9635), title, type(o), repr(o))


def see(o, title='', call=False, full=False):
    """Debugging output of introspection of the values of the attributes
        of the given object.
    """
    def _val():
        try:
            return attr() if call and callable(attr) else attr
        except Exception:
            return attr

    def val():
        val = repr(_val())
        return val if full else val[:max(32, COLUMNS - 40)].replace('\n', ' ')

    def label():
        label = name + ('()' if callable(attr) else '')
        return label[:32]

    out(o, title)
    import inspect
    for name, attr in inspect.getmembers(o):
        print(f"  {chr(9671)} {label():32} {val()}\n"
              if not name.startswith('__') else '\r',
              end='')
