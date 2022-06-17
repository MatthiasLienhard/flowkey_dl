try:
    from importlib.metadata import distribution
except ModuleNotFoundError:
    from importlib_metadata import distribution  # py3.7
__version__ = distribution('flowkey-dl').version
from .flowkey_dl import flowkey_dl, find_measure, parse_nums, arange_image
from .flowkey_dl import load_image, strip_url, make_url, save_png, save_pdf
__all__ = ['flowkey_dl', 'find_measure', 'parse_nums', 'arange_image',
           'load_image', 'strip_url', 'make_url', 'save_png']
