import pygame
from piece import get_shape
from grid import create_grid, convert_shape_format, valid_space, clear_rows, check_lost
from ui import draw_text_middle, draw_grid, draw_next_shape, draw_window, screen_width, screen_height
from score_manager import ScoreManager  


play_width = 300  
play_height = 600 
block_size = 30
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height


score_manager = ScoreManager()


def main(name):
    pygame.init()
    pygame.font.init()
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')

    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_speed = 0.27

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, name)
        draw_next_shape(win, next_piece)
        pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False

    score_manager.save_score(name, score)


def main_menu():
    run = True
    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')

    while run:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Enter Your Name', 60, (255, 255, 255))
        pygame.display.update()
        name = get_name_input(win)
        if name:
            main(name)
            run = False
    pygame.display.quit()


def get_name_input(win):
    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 60)
    input_font = pygame.font.Font(pygame.font.get_default_font(), 40)  

    name = ""
    input_active = True

    while input_active:
        win.fill((0, 0, 0))
        draw_text_middle(win, 'Enter Your Name: ', 60, (255, 255, 255))
        input_label = input_font.render(name, 1, (255, 255, 255))  

        
        win.blit(input_label, (top_left_x + play_width / 2 - (input_label.get_width() / 2), screen_height / 2 + 70))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                input_active = False
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

    return name


def draw_window(surface, grid, score=0, name=""):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.Font(pygame.font.get_default_font(), 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    font = pygame.font.Font(pygame.font.get_default_font(), 30)
    label = font.render(f'Score: {score}', 1, (255, 255, 255))

    
    max_name_width = screen_width - top_left_x - play_width - 50 - 20  
    name_label = font.render(f'Player: {name}', 1, (255, 255, 255))
    if name_label.get_width() > max_name_width:
        trimmed_name = name
        while font.render(f'Player: {trimmed_name}...', 1, (255, 255, 255)).get_width() > max_name_width:
            trimmed_name = trimmed_name[:-1]
        name = trimmed_name + "..."
    name_label = font.render(f'Player: {name}', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height // 2

    surface.blit(label, (sx + 20, sy + 100))
    surface.blit(name_label, (sx + 20, sy + 60))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)

    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)


if __name__ == "__main__":
    main_menu()
