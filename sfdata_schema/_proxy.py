import operator
import sys


class _Proxy:
    __slots__ = ("__wrapped__",)

    def __init__(self):
        __wrapped__ = None

    @property
    def __name__(self):
        return self.__wrapped__.__name__

    @__name__.setter
    def __name__(self, value):
        self.__wrapped__.__name__ = value

    @property
    def __class__(self):
        return self.__wrapped__.__class__

    @__class__.setter
    def __class__(self, value):
        self.__wrapped__.__class__ = value

    def __dir__(self):
        return dir(self.__wrapped__)

    def __str__(self):
        return str(self.__wrapped__)

    def __bytes__(self):
        return bytes(self.__wrapped__)

    def __repr__(self):
        return "<{} at 0x{:x} for {} at 0x{:x}>".format(
            type(self).__name__,
            id(self),
            type(self.__wrapped__).__name__,
            id(self.__wrapped__),
        )

    def __reversed__(self):
        return reversed(self.__wrapped__)

    def __round__(self):
        return round(self.__wrapped__)

    if sys.hexversion >= 0x03070000:

        def __mro_entries__(self, bases):
            return (self.__wrapped__,)

    def __lt__(self, other):
        return self.__wrapped__ < other

    def __le__(self, other):
        return self.__wrapped__ <= other

    def __eq__(self, other):
        return self.__wrapped__ == other

    def __ne__(self, other):
        return self.__wrapped__ != other

    def __gt__(self, other):
        return self.__wrapped__ > other

    def __ge__(self, other):
        return self.__wrapped__ >= other

    def __hash__(self):
        return hash(self.__wrapped__)

    def __nonzero__(self):
        return bool(self.__wrapped__)

    def __bool__(self):
        return bool(self.__wrapped__)

    def __setattr__(self, name, value):
        if name.startswith("_self_"):
            object.__setattr__(self, name, value)

        elif name == "__wrapped__":
            object.__setattr__(self, name, value)
            try:
                object.__delattr__(self, "__qualname__")
            except AttributeError:
                pass
            try:
                object.__setattr__(self, "__qualname__", value.__qualname__)
            except AttributeError:
                pass
            try:
                object.__delattr__(self, "__annotations__")
            except AttributeError:
                pass
            try:
                object.__setattr__(self, "__annotations__", value.__annotations__)
            except AttributeError:
                pass

        elif name == "__qualname__":
            setattr(self.__wrapped__, name, value)
            object.__setattr__(self, name, value)

        elif name == "__annotations__":
            setattr(self.__wrapped__, name, value)
            object.__setattr__(self, name, value)

        elif hasattr(type(self), name):
            object.__setattr__(self, name, value)

        else:
            setattr(self.__wrapped__, name, value)

    def __getattr__(self, name):
        # If we are being to lookup '__wrapped__' then the
        # '__init__()' method cannot have been called.

        if name == "__wrapped__":
            raise ValueError("wrapper has not been initialised")

        return getattr(self.__wrapped__, name)

    def __delattr__(self, name):
        if name.startswith("_self_"):
            object.__delattr__(self, name)

        elif name == "__wrapped__":
            raise TypeError("__wrapped__ must be an object")

        elif name == "__qualname__":
            object.__delattr__(self, name)
            delattr(self.__wrapped__, name)

        elif hasattr(type(self), name):
            object.__delattr__(self, name)

        else:
            delattr(self.__wrapped__, name)

    def __add__(self, other):
        return self.__wrapped__ + other

    def __sub__(self, other):
        return self.__wrapped__ - other

    def __mul__(self, other):
        return self.__wrapped__ * other

    def __div__(self, other):
        return operator.div(self.__wrapped__, other)

    def __truediv__(self, other):
        return operator.truediv(self.__wrapped__, other)

    def __floordiv__(self, other):
        return self.__wrapped__ // other

    def __mod__(self, other):
        return self.__wrapped__ % other

    def __divmod__(self, other):
        return divmod(self.__wrapped__, other)

    def __pow__(self, other, *args):
        return pow(self.__wrapped__, other, *args)

    def __lshift__(self, other):
        return self.__wrapped__ << other

    def __rshift__(self, other):
        return self.__wrapped__ >> other

    def __and__(self, other):
        return self.__wrapped__ & other

    def __xor__(self, other):
        return self.__wrapped__ ^ other

    def __or__(self, other):
        return self.__wrapped__ | other

    def __radd__(self, other):
        return other + self.__wrapped__

    def __rsub__(self, other):
        return other - self.__wrapped__

    def __rmul__(self, other):
        return other * self.__wrapped__

    def __rdiv__(self, other):
        return operator.div(other, self.__wrapped__)

    def __rtruediv__(self, other):
        return operator.truediv(other, self.__wrapped__)

    def __rfloordiv__(self, other):
        return other // self.__wrapped__

    def __rmod__(self, other):
        return other % self.__wrapped__

    def __rdivmod__(self, other):
        return divmod(other, self.__wrapped__)

    def __rpow__(self, other, *args):
        return pow(other, self.__wrapped__, *args)

    def __rlshift__(self, other):
        return other << self.__wrapped__

    def __rrshift__(self, other):
        return other >> self.__wrapped__

    def __rand__(self, other):
        return other & self.__wrapped__

    def __rxor__(self, other):
        return other ^ self.__wrapped__

    def __ror__(self, other):
        return other | self.__wrapped__

    def __iadd__(self, other):
        self.__wrapped__ += other
        return self

    def __isub__(self, other):
        self.__wrapped__ -= other
        return self

    def __imul__(self, other):
        self.__wrapped__ *= other
        return self

    def __idiv__(self, other):
        self.__wrapped__ = operator.idiv(self.__wrapped__, other)
        return self

    def __itruediv__(self, other):
        self.__wrapped__ = operator.itruediv(self.__wrapped__, other)
        return self

    def __ifloordiv__(self, other):
        self.__wrapped__ //= other
        return self

    def __imod__(self, other):
        self.__wrapped__ %= other
        return self

    def __ipow__(self, other):
        self.__wrapped__ **= other
        return self

    def __ilshift__(self, other):
        self.__wrapped__ <<= other
        return self

    def __irshift__(self, other):
        self.__wrapped__ >>= other
        return self

    def __iand__(self, other):
        self.__wrapped__ &= other
        return self

    def __ixor__(self, other):
        self.__wrapped__ ^= other
        return self

    def __ior__(self, other):
        self.__wrapped__ |= other
        return self

    def __neg__(self):
        return -self.__wrapped__

    def __pos__(self):
        return +self.__wrapped__

    def __abs__(self):
        return abs(self.__wrapped__)

    def __invert__(self):
        return ~self.__wrapped__

    def __int__(self):
        return int(self.__wrapped__)

    def __long__(self):
        return long(self.__wrapped__)

    def __float__(self):
        return float(self.__wrapped__)

    def __complex__(self):
        return complex(self.__wrapped__)

    def __oct__(self):
        return oct(self.__wrapped__)

    def __hex__(self):
        return hex(self.__wrapped__)

    def __index__(self):
        return operator.index(self.__wrapped__)

    def __len__(self):
        return len(self.__wrapped__)

    def __contains__(self, value):
        return value in self.__wrapped__

    def __getitem__(self, key):
        return self.__wrapped__[key]

    def __setitem__(self, key, value):
        self.__wrapped__[key] = value

    def __delitem__(self, key):
        del self.__wrapped__[key]

    def __getslice__(self, i, j):
        return self.__wrapped__[i:j]

    def __setslice__(self, i, j, value):
        self.__wrapped__[i:j] = value

    def __delslice__(self, i, j):
        del self.__wrapped__[i:j]

    def __enter__(self):
        return self.__wrapped__.__enter__()

    def __exit__(self, *args, **kwargs):
        return self.__wrapped__.__exit__(*args, **kwargs)

    def __iter__(self):
        return iter(self.__wrapped__)


class Proxy(_Proxy):
    __slots__ = ["__initialised__", "__proxies__"]

    def __init__(self):
        super().__init__()
        self.__initialised__ = False
        self.__wrapped__ = None
        self.__proxies__ = {}

    def __getattr__(self, item):
        if self.__initialised__:
            return getattr(self.__wrapped__, item)
        if not item in self.__proxies__:
            self.__proxies__[item] = Proxy()
        return self.__proxies__[item]

    def __init_proxy__(self, value):
        self.__wrapped__ = value
        self.__initialised__ = True
        for key, proxy in self.__proxies__.items():
            proxy.__init_proxy__(getattr(value, key, None))

    @classmethod
    def init_proxy(cls, proxy, value):
        if isinstance(proxy, dict):
            for item in proxy.values():
                Proxy.init_proxy(item, value)
        elif isinstance(proxy, list):
            for item in proxy:
                Proxy.init_proxy(item, value)
        elif isinstance(proxy, Proxy):
            proxy.__init_proxy__(value)
