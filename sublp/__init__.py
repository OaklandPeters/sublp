"""
@todo: Remove project_directory as argument in OpenProjectFromName methods, other than __init__
@todo: Make project_directory mandatory into OpenProjectFromName.__init__
@todo: Add __call__ to cases - should open sublime appropriately
@todo: Change importation to proper relative imports (requires changing test_sublp.py first)
"""
__all__ = [
    "Sublp"
]

from .sublp import Sublp
