import pygame


class PygameIntroImportError(ImportError):
    pass


if not getattr(pygame, "IS_CE", False):
    raise PygameIntroImportError(
        "Pygame-Intro requires the Pygame Community Edition (pygame-ce). "
        "Please install it and ensure you are not using legacy pygame."
    )

from .intro import *
