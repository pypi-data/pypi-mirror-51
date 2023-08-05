import functools as ft
import math
import torch
from torch import nn
from torch import autograd
from torch.autograd import function as autograd_function

from . import backend

# noinspection PyUnresolvedReferences
from . import _impl

# noinspection PyUnreachableCode
if False:
    from typing import Any, Union


try:
    lru_cache = ft.partial(ft.lru_cache, maxsize=None)
except AttributeError:
    # Python 2
    # A poor man's lru_cache, sufficient for our needs below.
    # no maxsize argument for simplicity (hardcoded to None)
    class LruCache:
        def __init__(self, fn):
            self.memodict = {}
            self.fn = fn

        def __call__(self, *args):
            try:
                return self.memodict[args]
            except KeyError:
                out = self.fn(*args)
                self.memodict[args] = out
                return out

    def lru_cache():
        return LruCache


# noinspection PyProtectedMember
class _LogSignatureFunction(autograd.Function):
    @staticmethod
    def forward(ctx, path, depth, stream, basepoint, mode, lyndon_info):
        # lyndon_info isn't a documented parameter because it's only used internally in the package.
        # It must be either None or the result of a call to _impl._make_lyndon_info

        mode = backend.mode_convert(mode)
        return backend.forward(ctx, path, depth, stream, basepoint, _impl.logsignature_forward, (mode, lyndon_info))

    @staticmethod
    @autograd_function.once_differentiable  # Our backward function uses in-place operations for memory efficiency
    def backward(ctx, grad_result):
        return backend.backward(ctx, grad_result, _impl.logsignature_backward) + (None, None)


def logsignature(path, depth, stream=False, basepoint=False, mode="brackets"):
    # type: (torch.Tensor, int, bool, Union[bool, torch.Tensor], str) -> torch.Tensor
    """Applies the logsignature transform to a stream of data.

    The :attr:`modes` argument determines how the logsignature is represented.

    Note that if performing many logsignature calculations for the same depth and size of input, then you will
    see a performance boost by using :class:`signatory.LogSignature` over :class:`signatory.logsignature`.

    Arguments:
        path (:class:`torch.Tensor`): as :func:`signatory.signature`.

        depth (int): as :func:`signatory.signature`.

        stream (bool, optional): as :func:`signatory.signature`.

        basepoint (bool or :class:`torch.Tensor`, optional): as :func:`signatory.signature`.

        mode (str, optional): How the output should be presented. Valid values are :attr:`"expand"`, :attr:`"brackets"`,
            or :attr:`"words"`. Precisely what each of these options mean is described in the "Returns" section below.
            As a rule of thumb: use :attr:`"words"` for new projects (as it is the fastest), and use :attr:`"brackets"`
            for compatibility with other projects which do not provide equivalent functionality to :attr:`"words"`.
            (Such as `iisignature <https://github.com/bottler/iisignature>`__). The mode :attr:`"expand"` is mostly only
            interesting for mathematicians.

    Returns:
        A :class:`torch.Tensor`. If :attr:`mode == "expand"` then it will be of the same shape as the returned tensor
        from :func:`signatory.signature`. If :attr:`mode in ("brackets", "words")` then it will again be of the
        same shape, except that the channel dimension will instead be of size
        :attr:`signatory.logsignature_channels(C, depth)`, where :attr:`C` is the number of input channels, i.e.
        :attr:`path.size(2)`.
        (Thus the logsignature is much smaller than the signature, which is the whole point of using the logsignature
        over the signature in the first place.)

        We now go on to explain what the different values for :attr:`mode` mean. This discussion is in the "Returns"
        section a the value of :attr:`mode` essentially just determines how the output is represented; the
        mathematical meaning is the same in all cases.

        If :attr:`mode == "expand"` then the logsignature is presented as a member of the tensor algebra; the numbers
        returned correspond to the coefficients of all words in the tensor algebra.

        If :attr:`mode == "brackets"` then the logsignature is presented in terms of the coefficients of the Lyndon
        basis of the free Lie algebra.

        If :attr:`mode == "words"` then the logsignature is presented in terms of the coefficients of a particular
        basis of the free Lie algebra that is not a Hall basis. Every basis element is given as a sum of Lyndon
        brackets. When each bracket is expanded out and the sum computed, the sum will contains precisely one Lyndon
        word (and some collection of non-Lyndon words). Moreover
        every Lyndon word is represented uniquely in this way. We identify these basis elements with each corresponding
        Lyndon word. This is natural as the coefficients in this basis are found just by extracting the coefficients of
        all Lyndon words from the tensor algebra representation of the logsignature.

        In all cases, the ordering corresponds to the ordering on words given by first ordering the words by length,
        and then ordering each length class lexicographically.
    """
    # noinspection PyUnresolvedReferences
    return _LogSignatureFunction.apply(path, depth, stream, basepoint, mode, None)


class LogSignature(nn.Module):
    """Module wrapper around the :func:`signatory.logsignature` function.

    Calling this module on an input :attr:`path` with the same number of channels as the last input :attr:`path` it was
    called with will be faster than the corresponding :func:`signatory.logsignature` function, as this module caches the
    result of certain computations which depend only on this value. (For larger numbers of channels, this speedup will
    be substantial.)

    Arguments:
        depth (int): as :func:`signatory.logsignature`.

        stream (bool, optional): as :func:`signatory.logsignature`.

        basepoint (bool or :class:`torch.Tensor`, optional): as :func:`signatory.logsignature`.

        mode (str, optional): as :func:`signatory.logsignature`.

    Called with a single argument :attr:`path` of type :class:`torch.Tensor`.
    """

    def __init__(self, depth, stream=False, basepoint=False, mode="brackets", **kwargs):
        # type: (int, bool, Union[bool, torch.Tensor], str, **Any) -> None
        super(LogSignature, self).__init__(**kwargs)
        self.depth = depth
        self.stream = stream
        self.basepoint = basepoint
        self.mode = mode

    @staticmethod
    @lru_cache()  # This computation can be pretty slow! We definitely want to reuse it between instances
    def lyndon_info_cache(channels, depth, mode):
        mode = backend.mode_convert(mode)
        return _impl.make_lyndon_info(channels, depth, mode)

    def forward(self, path):
        # type: (torch.Tensor) -> torch.Tensor

        lyndon_info = self.lyndon_info_cache(path.size(-1), self.depth, self.mode)
        # don't call logsignature itself because that (deliberately) doesn't expose a lyndon_info argument.
        # noinspection PyProtectedMember, PyUnresolvedReferences
        return _LogSignatureFunction.apply(path, self.depth, self.stream, self.basepoint, self.mode, lyndon_info)

    def extra_repr(self):
        return ('depth={depth}, stream={stream}, basepoint={basepoint}, mode{mode}'
                .format(depth=self.depth, stream=self.stream, basepoint=str(self.basepoint)[:6], mode=self.mode))


def _get_prime_factors(x):
    if x == 1:
        return []
    prime_factors = []
    largest_i_so_far = 2
    while True:
        for i in range(largest_i_so_far, int(round(math.sqrt(x))) + 1):  # int needed for Py2 compatability
            if x % i == 0:
                largest_i_so_far = i
                break
        else:
            prime_factors.append(x)  # x is prime
            break
        x = x // i
        prime_factors.append(i)
    return prime_factors


def _mobius_function(x):
    prime_factors = _get_prime_factors(x)
    prev_elem = None
    for elem in prime_factors:
        if elem == prev_elem:
            return 0
        prev_elem = elem
    num_unique_factors = len(set(prime_factors))
    if num_unique_factors % 2 == 0:
        return 1
    else:
        return -1


def logsignature_channels(in_channels, depth):
    # type: (int, int) -> int
    """Computes the number of output channels from a logsignature call with :attr:`mode in ("words", "brackets")`.

    Arguments:
        in_channels (int): The number of channels in the input; that is, the dimension of the space that the input path
            resides in.

        depth (int): The depth of the signature that is being computed.

    Returns:
        An int specifying the number of channels in the logsignature of the path.
    """

    if in_channels < 1:
        raise ValueError("in_channels must be at least 1")

    if depth < 1:
        raise ValueError("depth must be at least 1")

    total = 0
    for d in range(1, depth + 1):
        subtotal = 0
        for d_divisor in range(1, d + 1):
            if d % d_divisor == 0:
                subtotal += _mobius_function(d // d_divisor) * in_channels ** d_divisor
        total += subtotal // d
    return total
