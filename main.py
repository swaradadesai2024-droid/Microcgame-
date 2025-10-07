import pygame
import random
import sys
from questions import questions  # Your questions module

# -------------------- INIT --------------------
pygame.init()
pygame.font.init()
pygame.mixer.init()

# -------------------- CONSTANTS --------------------
WIDTH, HEIGHT = 1000, 600
GRID_SIZE = 3
BLOCK_SIZE = 150
MARGIN = 50
RIGHT_MARGIN = 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Microeconomics Input Market Game")

# Colors
BG_COLOR = (50, 50, 50)           # Dark grey game background
INTRO_BG = (29, 26, 57)           # #1D1A39 for intro screen
PLAYER_COLOR = (255, 100, 100)
CORRECT_COLOR = (7, 102, 83)      # Green
WRONG_COLOR = (134, 17, 46)       # Red
BUTTON_COLOR = (42, 69, 230)      # Blue for answer bubbles
BUTTON_HOVER = (70, 100, 250)
QUIT_COLOR = (134, 17, 46)
STAT_BG = (69, 25, 82)            # Stats bubble
STAT_TEXT = (232, 188, 137)       # Stats text
QA_BG = (0, 70, 140, 120)         # Transparent blue background for question+answers
TEXT_COLOR = (255, 255, 255)
NAME_BG = (50, 20, 100)
NAME_BORDER = (255, 255, 255)

# Tiles
TILE_COLORS = [(50, 200, 50), (0, 100, 0)]

# Fonts
TITLE_FONT = pygame.font.SysFont("timesnewroman", 36, bold=True)
STAT_FONT = pygame.font.SysFont("timesnewroman", 18, bold=True)
QA_FONT = pygame.font.SysFont("timesnewroman", 22)
BIG_FONT = pygame.font.SysFont("timesnewroman", 32, bold=True)
OUTRO_FONT = pygame.font.SysFont("comicsansms", 36, bold=True)

# Game variables
score = 0
question_index = 0
wrong_streak = 0
player_pos = 0
questions = random.sample(questions, 18)
player_name = ""

# -------------------- LOAD ASSETS --------------------
player_img = pygame.image.load("dog.png").convert_alpha()
player_img = pygame.transform.scale(player_img, (int(50*1.5), int(50*1.5)))
happy_img = pygame.image.load("happy.jpg").convert()
happy_img = pygame.transform.scale(happy_img, (1200, 1200))  # 8x larger
sad_img = pygame.image.load("sad.jpg").convert()
sad_img = pygame.transform.scale(sad_img, (1200, 1200))      # 8x larger

pygame.mixer.music.load("intro_music.wav")
correct_sound = pygame.mixer.Sound("correct.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")
win_sound = pygame.mixer.Sound("win.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# -------------------- HELPERS --------------------
def safe_quit():
    pygame.quit()
    sys.exit()

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for w in words:
        test_line = current + w + " "
        if font.size(test_line)[0] > max_width and current:
            lines.append(current.strip())
            current = w + " "
        else:
            current = test_line
    if current:
        lines.append(current.strip())
    return lines

# -------------------- DRAW GRID WITH START/END --------------------
def draw_grid_with_labels():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            color = TILE_COLORS[(row*GRID_SIZE + col) % 2]
            x = MARGIN + col * BLOCK_SIZE
            y = MARGIN + (GRID_SIZE - 1 - row) * BLOCK_SIZE
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(screen, color, rect)
            # Draw thin black border for each cell
            pygame.draw.rect(screen, (0,0,0), rect, 1)

    # START label below bottom-left cell
    start_x = MARGIN + BLOCK_SIZE//2
    start_y = MARGIN + (GRID_SIZE-1)*BLOCK_SIZE + BLOCK_SIZE + 10
    start_text = STAT_FONT.render("START", True, STAT_TEXT)
    screen.blit(start_text, (start_x - start_text.get_width()//2, start_y))

    # END label above top-right cell
    end_x = MARGIN + (GRID_SIZE-1)*BLOCK_SIZE + BLOCK_SIZE//2
    end_y = MARGIN - 30
    end_text = STAT_FONT.render("END", True, STAT_TEXT)
    screen.blit(end_text, (end_x - end_text.get_width()//2, end_y))


# -------------------- DRAW STATS --------------------
def draw_stats():
    panel_x = MARGIN + GRID_SIZE * BLOCK_SIZE + 30
    panel_y = MARGIN
    stats = [
        f"Score: {score}", f"Current Block: {player_pos+1}",
        f"Wrong Streak: {wrong_streak}", f"Remaining: {len(questions)-question_index}"
    ]
    for i, text in enumerate(stats):
        col = i % 2
        row = i // 2
        rect = pygame.Rect(panel_x + col*180, panel_y + row*35, 170, 30)
        pygame.draw.rect(screen, STAT_BG, rect, border_radius=8)
        pygame.draw.rect(screen, STAT_TEXT, rect, 1, border_radius=8)
        text_surf = STAT_FONT.render(text, True, STAT_TEXT)
        screen.blit(text_surf, (rect.x + rect.width//2 - text_surf.get_width()//2,
                                rect.y + rect.height//2 - text_surf.get_height()//2))

# -------------------- DRAW QUIT BUTTON --------------------
def draw_quit_button():
    quit_rect = pygame.Rect(WIDTH-150, HEIGHT-60, 120, 40)
    mouse_pos = pygame.mouse.get_pos()
    hover = quit_rect.collidepoint(mouse_pos)
    color = BUTTON_HOVER if hover else QUIT_COLOR
    pygame.draw.rect(screen, color, quit_rect, border_radius=8)
    pygame.draw.rect(screen, STAT_TEXT, quit_rect, 1, border_radius=8)
    text_surf = STAT_FONT.render("QUIT", True, STAT_TEXT)
    screen.blit(text_surf, (quit_rect.x + quit_rect.width//2 - text_surf.get_width()//2,
                            quit_rect.y + quit_rect.height//2 - text_surf.get_height()//2))
    return quit_rect

# -------------------- DRAW PLAYER --------------------
def draw_player(x=None, y=None):
    if x is None or y is None:
        row = player_pos // GRID_SIZE
        col = player_pos % GRID_SIZE
        x = MARGIN + col*BLOCK_SIZE + BLOCK_SIZE//2 - player_img.get_width()//2
        y = MARGIN + (GRID_SIZE-1-row)*BLOCK_SIZE + BLOCK_SIZE//2 - player_img.get_height()//2
    screen.blit(player_img,(x,y))

# -------------------- DRAW QUESTION & ANSWERS --------------------
def draw_question(q_obj, hover_key=None, clicked_key=None):
    padding = 20
    start_x = MARGIN + GRID_SIZE*BLOCK_SIZE + 30
    max_width = WIDTH - start_x - RIGHT_MARGIN
    max_height = HEIGHT - 2*MARGIN

    # Wrap question text dynamically to fit inside max_width
    question_lines = wrap_text(q_obj['q'], QA_FONT, max_width - 2*padding)

    # Wrap each answer dynamically
    answer_lines = []
    for key, opt in q_obj['options'].items():
        answer_lines.append(wrap_text(f"{key}. {opt}", QA_FONT, max_width - 2*padding))

    # Calculate total height
    total_answer_height = sum([len(lines)*25 + 10 for lines in answer_lines]) + len(answer_lines)*10
    question_height = len(question_lines)*25 + 2*padding
    bubble_height = question_height + total_answer_height + 40

    # Ensure the bubble does not exceed available height
    if bubble_height > max_height:
        scale = max_height / bubble_height
        bubble_height = max_height
        # Optionally scale font sizes if needed, or allow scrolling (can be added)

    bubble_width = max_width
    start_y = HEIGHT//2 - bubble_height//2
    qa_rect = pygame.Rect(start_x, start_y, bubble_width, bubble_height)

    # Draw transparent background covering answers
    s = pygame.Surface((bubble_width, bubble_height), pygame.SRCALPHA)
    s.fill(QA_BG)
    screen.blit(s, (start_x, start_y))

    # Draw question text centered
    text_start_y = qa_rect.y + padding
    for i, line in enumerate(question_lines):
        text_surf = QA_FONT.render(line, True, TEXT_COLOR)
        screen.blit(text_surf, (qa_rect.x + bubble_width//2 - text_surf.get_width()//2,
                                text_start_y + i*25))

    # Draw answer bubbles
    buttons = []
    y_offset = qa_rect.y + question_height + 10
    for idx, (key, opt) in enumerate(q_obj['options'].items()):
        opt_lines = answer_lines[idx]
        btn_height = len(opt_lines)*25 + 10
        rect = pygame.Rect(qa_rect.x + padding, y_offset, bubble_width - 2*padding, btn_height)

        # Hover animation
        scale = 1.05 if hover_key == key else 1
        scaled_width = rect.width * scale
        scaled_height = rect.height * scale
        scaled_x = rect.centerx - scaled_width/2
        scaled_y = rect.centery - scaled_height/2
        scaled_rect = pygame.Rect(scaled_x, scaled_y, scaled_width, scaled_height)

        # Color for correct/incorrect
        color = BUTTON_COLOR
        if clicked_key:
            if key == q_obj['answer']:
                color = CORRECT_COLOR
            elif key == clicked_key:
                color = WRONG_COLOR
        elif hover_key == key:
            color = BUTTON_HOVER

        pygame.draw.rect(screen, color, scaled_rect, border_radius=8)
        pygame.draw.rect(screen, STAT_TEXT, scaled_rect, 1, border_radius=8)

        # Draw wrapped answer text centered
        line_offset = 5
        for i, line in enumerate(opt_lines):
            text_surf = QA_FONT.render(line, True, TEXT_COLOR)
            screen.blit(text_surf, (scaled_rect.x + scaled_rect.width//2 - text_surf.get_width()//2,
                                    scaled_rect.y + line_offset + i*25))
        buttons.append((scaled_rect, key))
        y_offset += btn_height + 10

    quit_rect = draw_quit_button()
    return buttons, quit_rect

# -------------------- INTRO SCREEN --------------------
def intro_screen():
    global player_name
    pygame.mixer.music.play(-1)
    input_active = True
    name_text = ""
    while input_active:
        screen.fill(INTRO_BG)
        title_surf = TITLE_FONT.render("Welcome Players!", True, TEXT_COLOR)
        screen.blit(title_surf,(WIDTH//2-title_surf.get_width()//2,150))
        prompt_surf = STAT_FONT.render("Enter your name and press START:", True, TEXT_COLOR)
        screen.blit(prompt_surf,(WIDTH//2-prompt_surf.get_width()//2,250))

        # Name input box
        input_rect = pygame.Rect(WIDTH//2-150,300,300,40)
        pygame.draw.rect(screen, NAME_BG,input_rect,border_radius=10)
        pygame.draw.rect(screen, NAME_BORDER,input_rect,2,border_radius=10)
        name_surf = STAT_FONT.render(name_text, True, TEXT_COLOR)
        screen.blit(name_surf,(input_rect.x+input_rect.width//2 - name_surf.get_width()//2,
                            input_rect.y+5))

        # Start button
        start_rect = pygame.Rect(WIDTH//2-60, 360, 120, 40)
        mouse_pos = pygame.mouse.get_pos()
        hover = start_rect.collidepoint(mouse_pos)
        color = BUTTON_HOVER if hover else BUTTON_COLOR
        pygame.draw.rect(screen, color, start_rect, border_radius=8)
        pygame.draw.rect(screen, STAT_TEXT, start_rect, 1, border_radius=8)
        start_text = STAT_FONT.render("START", True, STAT_TEXT)
        screen.blit(start_text, (start_rect.x + start_rect.width//2 - start_text.get_width()//2,
                                start_rect.y + start_rect.height//2 - start_text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                safe_quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    name_text = name_text[:-1]
                elif event.key==pygame.K_RETURN and name_text.strip() != "":
                    player_name = name_text.strip()
                    input_active = False
                else:
                    if len(name_text)<15:
                        name_text += event.unicode
            if event.type==pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos) and name_text.strip()!="":
                    player_name = name_text.strip()
                    input_active=False


# -------------------- GAME OVER SCREEN --------------------
def game_over_screen():
    pygame.mixer.music.stop()
    won = score >= len(questions)//2
    face_img = happy_img if won else sad_img
    showing=True
    phrase = "WELL DONE!" if won else "TRY AGAIN!"
    while showing:
        screen.fill(BG_COLOR)
        # Center face
        face_x = WIDTH//2 - face_img.get_width()//2
        face_y = HEIGHT//2 - face_img.get_height()//2
        screen.blit(face_img, (face_x, face_y))

        # Score at top
        score_surf = STAT_FONT.render(f"Final Score: {score}/{len(questions)}", True, STAT_TEXT)
        screen.blit(score_surf, (WIDTH//2-score_surf.get_width()//2, 50))

        # Phrase bubble at bottom
        bubble_width, bubble_height = 300, 60
        bubble_rect = pygame.Rect(WIDTH//2 - bubble_width//2, HEIGHT-100, bubble_width, bubble_height)
        s = pygame.Surface((bubble_width,bubble_height),pygame.SRCALPHA)
        s.fill((0,0,255,120))
        screen.blit(s, (bubble_rect.x, bubble_rect.y))
        text_surf = OUTRO_FONT.render(phrase, True, TEXT_COLOR)
        screen.blit(text_surf, (bubble_rect.x + bubble_rect.width//2 - text_surf.get_width()//2,
                                bubble_rect.y + bubble_rect.height//2 - text_surf.get_height()//2))

        # Quit button
        quit_rect = draw_quit_button()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                showing=False
            if event.type==pygame.MOUSEBUTTONDOWN and quit_rect.collidepoint(event.pos):
                showing=False

# -------------------- HOP PLAYER --------------------
def hop_player_to(new_pos):
    global player_pos
    start_row = player_pos // GRID_SIZE
    start_col = player_pos % GRID_SIZE
    end_row = new_pos // GRID_SIZE
    end_col = new_pos % GRID_SIZE
    start_x = MARGIN + start_col*BLOCK_SIZE + BLOCK_SIZE//2 - player_img.get_width()//2
    start_y = MARGIN + (GRID_SIZE-1-start_row)*BLOCK_SIZE + BLOCK_SIZE//2 - player_img.get_height()//2
    end_x = MARGIN + end_col*BLOCK_SIZE + BLOCK_SIZE//2 - player_img.get_width()//2
    end_y = MARGIN + (GRID_SIZE-1-end_row)*BLOCK_SIZE + BLOCK_SIZE//2 - player_img.get_height()//2

    steps = 15
    for i in range(1, steps+1):
        t = i/steps
        y_offset = -20*abs((t-0.5)*2)
        x = start_x + (end_x-start_x)*t
        y = start_y + (end_y-start_y)*t + y_offset
        screen.fill(BG_COLOR)
        draw_grid_with_labels()
        draw_stats()
        draw_question(questions[question_index] if question_index < len(questions) else questions[-1])
        draw_player(x,y)
        pygame.display.flip()
        pygame.time.wait(30)
    player_pos = new_pos

# -------------------- MAIN GAME --------------------
def main_game():
    global score, question_index, wrong_streak, player_pos
    running = True
    while running and question_index < len(questions):
        current_question = questions[question_index]

        screen.fill(BG_COLOR)
        draw_grid_with_labels()
        draw_stats()
        buttons, quit_rect = draw_question(current_question)
        draw_player()
        pygame.display.flip()

        hover_key = None
        waiting = True

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    safe_quit()
                elif event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    hover_key = None
                    for rect, key in buttons:
                        if rect.collidepoint(pos):
                            hover_key = key
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if quit_rect.collidepoint(pos):
                        safe_quit()
                    for rect, key in buttons:
                        if rect.collidepoint(pos):
                            clicked_key = key
                            correct = clicked_key == current_question['answer']
                            if correct:
                                correct_sound.play()
                                score += 1
                                wrong_streak = 0
                                hop_player_to(min(player_pos + 1, 8))
                            else:
                                wrong_sound.play()
                                wrong_streak += 1
                                if wrong_streak == 2:
                                    wrong_streak = 0
                                    if player_pos == 0:
                                        running = False
                                    else:
                                        hop_player_to(max(player_pos - 1, 0))
                            # Show feedback
                            draw_grid_with_labels()
                            draw_stats()
                            draw_question(current_question, clicked_key=clicked_key)
                            draw_player()
                            pygame.display.flip()
                            pygame.time.wait(800)
                            question_index += 1
                            waiting = False
            # Redraw
            screen.fill(BG_COLOR)
            draw_grid_with_labels()
            draw_stats()
            if question_index < len(questions):
                draw_question(questions[question_index], hover_key=hover_key)
            draw_player()
            pygame.display.flip()
    game_over_screen()

# -------------------- RUN --------------------
intro_screen()
main_game()
safe_quit()
