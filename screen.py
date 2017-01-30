def show_array(screen, array, highlights):
    bar_size = (700 / len(array)) / 1.4
    space = 0.4 * bar_size

    x = space // 2
    for i, val in enumerate(array):
        y = round((500 * val) / len(array))

        # green bars for current bars. white for all others
        color = (0, 255, 0) if i in highlights else (255, 255, 255)

        pygame.draw.rect(screen, color, pygame.Rect(round(x), 501 - y, round(bar_size), y))
        x += bar_size + space

    pygame.display.update()

def draw_completed_array(screen, array):
    bar_size = (700 / len(array)) / 1.4
    space = 0.4 * bar_size

    # we have 500 ms for the whole array
    wait_time = 500 // len(array)

    # this is just because the switching looks ugly otherwise
    # because the last switched indexes are still green
    show_array(screen, array, ())

    x = space // 2
    for i, val in enumerate(array):
        y = round((500 * val) / len(array))

        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(round(x), 501 - y, round(bar_size), y))
        x += bar_size + space

        pygame.time.wait(wait_time)
        pygame.display.update()

