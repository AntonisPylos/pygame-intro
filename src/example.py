import pygame
import pygame_intro


def intro():
    pygame.display.set_caption("Intro Example")

    pygame_intro.settings(
        duration=1.5,
        fade_in=0.25,
        fade_out=1,
        scale=0.7,
        progress_bar=True,
        skippable=True,
    )

    # pygame_intro.add_image(image_path)
    # pygame_intro.add_sound(sound_path)
    pygame_intro.change_background((30, 30, 30))

    pygame_intro.start()


def game(screen):
    clock = pygame.time.Clock()
    ball_color = (250, 30, 80)
    ball_radius = 30
    x = screen.get_width() // 2
    y = screen.get_height() // 2
    speed = 1000
    direction = -1

    dt = 0

    y_min = ball_radius
    y_max = screen.get_height() - ball_radius

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        y += speed * direction * dt
        if y <= y_min:
            direction = 1

        if y >= y_max:
            direction = -1

        screen.fill((85, 37, 60))
        pygame.draw.circle(screen, ball_color, (x, int(y)), ball_radius)
        pygame.display.flip()
        dt = clock.tick(-1) / 1000
    pygame.quit()


def main():
    pygame.init()
    pygame_intro.init()
    screen = pygame.display.set_mode((1200, 800))
    intro()
    game(screen)


if __name__ == "__main__":
    main()
