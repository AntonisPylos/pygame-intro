# This is a practical test script for the pygame-intro library.
# It runs the intro to verify basic functionality and to check that it does not throw an error.

import sys, os
import pygame
import wave, struct, tempfile
from intro import init, settings, add_image, add_sound, change_background, start


def create_dummy_image(filename):
    path = os.path.join(tempfile.gettempdir(), filename)

    size = (128, 128)
    surface = pygame.Surface(size)
    surface.fill((200, 200, 255))
    pygame.draw.circle(
        surface,
        (255, 100, 100),
        (size[0] // 2, size[1] // 2),
        min(size) // 3,
    )
    pygame.image.save(surface, path)

    return path


def create_dummy_sound(filename):
    path = os.path.join(tempfile.gettempdir(), filename)

    duration = 0.2
    sample_rate = 44100
    frames = int(duration * sample_rate)
    silence = struct.pack("<h", 0)

    with wave.open(path, "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(silence * frames)

    return path


image = create_dummy_image("pygame.png")
os.environ["SDL_VIDEODRIVER"] = "dummy"

sound = create_dummy_sound("intro.wav")
os.environ["SDL_AUDIODRIVER"] = "dummy"


try:
    print("[1] Initializing Pygame...")
    pygame.init()

    print("[2] Creating hidden window...")
    pygame.display.set_mode((400, 300))

    print("[3] Initializing intro system...")
    init()

    print("[4] Applying intro settings...")
    settings(
        duration=1,
        fade_in=0.5,
        fade_out=0.5,
        scale=0.7,
        progress_bar=True,
        skippable=True,
    )

    print("[5] Changing intro image...")
    add_image(image)

    print("[6] Changing intro sound...")
    add_sound(sound, 1)

    print("[6] Changing background color...")
    change_background((60, 40, 80))

    print("[7] Starting intro sequence...")
    start()  # ~1 second

    print("[8] Quitting pygame...")
    pygame.quit()

    print("[PASS] Test complete. No errors detected.")
    sys.exit(0)

except Exception as e:
    print("[FAIL] Test failed with exception:")
    print(f"        {type(e).__name__}: {e}")
    sys.exit(1)
