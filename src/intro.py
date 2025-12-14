import asyncio
import pygame
from sys import exit
from pathlib import Path
from typing import List, Tuple, Union

__all__ = [
    "init",
    "start",
    "web_start",
    "settings",
    "add_image",
    "add_sound",
    "change_background",
]


class classproperty(property):
    def __get__(self, obj, objtype=None):
        return self.fget(objtype)


class PygameIntroRuntimeError(RuntimeError):
    pass


class Intro:
    @classmethod
    def init(cls) -> None:
        if not pygame.get_init():
            raise PygameIntroRuntimeError(
                "Pygame is not initialized. Call init() after pygame.init()."
            )
        cls._load_default_intro()
        cls._load_default_settings()

    @classmethod
    def settings(
        cls,
        duration: int,
        fade_in: int,
        fade_out: int,
        scale: float,
        progress_bar: bool,
        skippable: bool,
    ) -> None:
        if duration is not None:
            cls._duration = duration
        if fade_in is not None:
            cls._fade_in = fade_in
        if fade_out is not None:
            cls._fade_out = fade_out
        if scale is not None:
            cls._scale = scale
        if progress_bar is not None:
            cls._progress_enabled = progress_bar
        if skippable is not None:
            cls._skip_enabled = skippable

    @classproperty
    def surface(cls) -> pygame.Surface:
        surface = pygame.display.get_surface()
        if surface is None:
            raise PygameIntroRuntimeError(
                "No display surface set. Please call pygame.display.set_mode() before initializing intro."
            )
        return surface

    @classmethod
    def reset(cls) -> None:
        cls.init()

    @classmethod
    def set_images(cls, image_paths: Union[List[str], Tuple[str, ...]]) -> None:
        loaded_images = []
        for path in image_paths:
            img = cls.load_image(path)
            loaded_images.append(img)
        cls._images = loaded_images

    @classmethod
    def set_music(cls, path: str, volume: float = 0.7) -> None:
        if not isinstance(path, str):
            raise PygameIntroRuntimeError("path must be a string.")
        if not isinstance(volume, (float, int)) or not (0.0 <= volume <= 1.0):
            raise PygameIntroRuntimeError("volume must be a float between 0.0 and 1.0.")

        actual_path = cls.load_music(path)
        cls._music_path = actual_path
        cls._music_volume = float(volume)
        pygame.mixer.music.set_volume(cls._music_volume)

    @classmethod
    def set_background(
        cls, background: Union[pygame.Surface, Tuple[int, int, int], List[int], str]
    ) -> None:
        if not (
            isinstance(background, pygame.Surface)
            or isinstance(background, (tuple, list))
            or isinstance(background, str)
        ):
            raise PygameIntroRuntimeError(
                "background must be a pygame.Surface, an RGB tuple/list, or a color string."
            )
        cls._background = background

    @classmethod
    def run(cls) -> None:
        surface, clock = cls._prepare_run()
        start_time = pygame.time.get_ticks()
        base_font_size = 48

        while True:
            if cls._handle_exit():
                break

            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            progress = min(elapsed / cls._duration, 1.0)
            alpha = cls._fade_alpha(elapsed)
            scale = max(0.01, cls._scale)

            cls._run_frame(surface, elapsed, progress, alpha, scale, base_font_size)

            if elapsed >= cls._duration:
                break

            pygame.display.flip()
            clock.tick(60)

        cls._music_path and pygame.mixer.music.stop()
        cls.reset()

    @classmethod
    async def run_async(cls) -> None:
        surface, clock = cls._prepare_run()
        start_time = pygame.time.get_ticks()
        base_font_size = 48

        while True:
            if cls._handle_exit():
                break

            elapsed = (pygame.time.get_ticks() - start_time) / 1000
            progress = min(elapsed / cls._duration, 1.0)
            alpha = cls._fade_alpha(elapsed)
            scale = max(0.01, cls._scale)

            cls._run_frame(surface, elapsed, progress, alpha, scale, base_font_size)

            if elapsed >= cls._duration:
                break

            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)

        cls._music_path and pygame.mixer.music.stop()
        cls.reset()

    @classmethod
    def _prepare_run(cls):
        surface = cls.surface
        clock = pygame.time.Clock()
        if cls._music_path:
            try:
                pygame.mixer.music.load(cls._music_path)
                pygame.mixer.music.set_volume(cls._music_volume)
                pygame.mixer.music.play()
            except Exception as e:
                raise PygameIntroRuntimeError(f"Failed to load music: {e}")
        return surface, clock

    @classmethod
    def _handle_exit(cls):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if cls._skip_enabled and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
        return False

    @classmethod
    def _fade_alpha(cls, elapsed):
        alpha = 255
        if cls._fade_in and elapsed < cls._fade_in:
            alpha = int(255 * (elapsed / max(cls._fade_in, 0.01)))
        elif cls._fade_out and elapsed > (cls._duration - cls._fade_out):
            out_progress = (elapsed - (cls._duration - cls._fade_out)) / max(
                cls._fade_out, 0.01
            )
            alpha = int(255 * (1 - min(1.0, out_progress)))
        return max(0, min(255, alpha))

    @classmethod
    def _run_frame(cls, surface, elapsed, progress, alpha, scale, base_font_size):
        # Background
        if isinstance(cls._background, pygame.Surface):
            background = cls._background.copy()
            background.set_alpha(alpha)
            surface.blit(background, (0, 0))
        else:
            surface.fill(cls._background)
            if alpha < 255:
                fade_overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                fade_overlay.fill((0, 0, 0, 255 - alpha))
                surface.blit(fade_overlay, (0, 0))
        # Images
        if cls._images:
            index = int(progress * len(cls._images))
            index = min(index, len(cls._images) - 1)
            if len(cls._images) > 0:
                img = cls._images[index]
                w, h = img.get_size()
                new_w = max(1, int(w * scale))
                new_h = max(1, int(h * scale))
                new_img = pygame.transform.smoothscale(img, (new_w, new_h))
                new_img = new_img.copy()
                new_img.set_alpha(alpha)
                rect = new_img.get_rect(center=surface.get_rect().center)
                surface.blit(new_img, rect)
        # Progress bar
        if cls._progress_enabled:
            bar_width = int(surface.get_width() * 0.6 * scale)
            bar_height = int(10 * scale)
            bar_x = (surface.get_width() - bar_width) // 2
            bar_y = surface.get_height() - int(30 * scale)
            pygame.draw.rect(
                surface, (64, 64, 64), (bar_x, bar_y, bar_width, bar_height)
            )
            pygame.draw.rect(
                surface,
                (0, 200, 0),
                (bar_x, bar_y, int(bar_width * progress), bar_height),
            )
        # Skip prompt
        if cls._skip_enabled:
            skip_font = pygame.font.SysFont(None, int(base_font_size * scale))
            skip_text = skip_font.render("Press space to skip", True, (200, 200, 200))
            skip_text.set_alpha(alpha)
            skip_rect = skip_text.get_rect(
                bottomright=(surface.get_width() - 10, surface.get_height() - 10)
            )
            surface.blit(skip_text, skip_rect)

    @classmethod
    def _load_default_intro(cls) -> None:
        cls._images = []
        cls._music_path = None
        cls._music_volume = 0.7
        cls._background = (0, 0, 0)

    @classmethod
    def _load_default_settings(cls) -> None:
        cls._duration = 2
        cls._fade_in = 0.25
        cls._fade_out = 1
        cls._scale = 0.7
        cls._skip_enabled = True
        cls._progress_enabled = False

    @staticmethod
    def load_image(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            raise PygameIntroRuntimeError(f"Failed to load {path}\nError: {e}")

    @staticmethod
    def load_music(path):
        try:
            pygame.mixer.music.load(path)
            return path
        except Exception as e:
            raise PygameIntroRuntimeError(f"Failed to load {path}\nError: {e}")


intro = Intro


def init() -> None:
    intro.init()


def settings(*args, **kwargs) -> None:
    duration = kwargs.get("duration", None)
    fade_in = kwargs.get("fade_in", None)
    fade_out = kwargs.get("fade_out", None)
    scale = kwargs.get("scale", None)
    progress_bar = kwargs.get("progress_bar", None)
    skippable = kwargs.get("skippable", None)

    intro.settings(duration, fade_in, fade_out, scale, progress_bar, skippable)


def add_image(*image_paths: str) -> None:
    intro.set_images(image_paths)


def add_sound(path: str, volume: float = 0.7) -> None:
    intro.set_music(path, volume)


def change_background(
    background: Union[pygame.Surface, Tuple[int, int, int], List[int], str],
) -> None:
    intro.set_background(background)


def start():
    intro.run()


def web_start():
    return intro.run_async()
