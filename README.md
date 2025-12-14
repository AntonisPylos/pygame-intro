# pygame-intro

A minimal Python library to create intros for [`pygame community edition`](https://github.com/pygame-community/pygame-ce).

## Features

- Load and display custom images/frames
- Load and play custom sounds
- Progress bar and skippable intro options
- Customizable: duration, fade-in/fade-oud and scaling
- Async support for pygbag compatibility
- Set background (color or image/surface)

## Getting Started

Install:
```bash
pip install pygame_intro
```

Desktop Example:
```python
import pygame
import pygame_intro

pygame.init()
pygame_intro.init()

# Optional: customize intro settings
pygame_intro.settings(
    duration=2,
    fade_in=0.25,
    fade_out=1,
    scale=0.7,
    progress_bar=True,
    skippable=True,
)

# Optional: add image or images
pygame_intro.add_image("my_image.png", "my_image2.png", "my_image3.png")

# Optional: add sound
pygame_intro.add_sound("path/my_sound.mp3", volume=0.7)

# Optional: change background color
pygame_intro.change_background((30, 30, 30))

# Start the intro
pygame_intro.start()
```

Pygbag Example:
```python
# /// script
# dependencies = [
#   "pygame-intro",
# ]
# ///

import pygame_intro
import asyncio

# Make sure to implement any changes needed for pygbag
async def main():
	pygame_intro.init()
	pygame_intro.add_image("path/my_image.png")

    pygame_intro.settings(duration=2, fade_in=0.25, fade_out=1)
    
    await pygame_intro.web_start()

# Start the intro
asyncio.run(main())
```


## License

This project is licensed under the MIT License.  
See the [`LICENSE`](LICENSE.txt) file for the full license text.
