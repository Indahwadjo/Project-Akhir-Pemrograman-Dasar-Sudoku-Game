import pygame
from pygame import mixer
import time
import random
import os

class SudokuGame:
    def __init__(self):
        pygame.init()
        mixer.init()

        self.WHITE = (225, 255, 225)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.green = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.GREY = (200, 200, 200)

        self.WIDTH = 605
        self.HEIGHT = 660
        self.SQUARE_SIZE = self.WIDTH // 9
        self.FPS = 24

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Sudoku by IRAMA ✨")

        base_dir = os.path.dirname(__file__)
        assets_dir = os.path.join(base_dir, 'assets')
        sounds_dir = os.path.join(base_dir, 'sounds')

        try:
            self.background = pygame.image.load(os.path.join(assets_dir, 'background.png'))
            self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        except:
            print("gaada background")
            self.background = None

        try:
            self.trophy = pygame.image.load(os.path.join(assets_dir, 'piala.png'))
            self.trophy = pygame.transform.scale(self.trophy, (500, 500))
        except:
            print("gaada piala")
            self.trophy = None

        try:
            self.new_game_btn = pygame.image.load(os.path.join(assets_dir, 'new game.png'))
            self.quit_btn = pygame.image.load(os.path.join(assets_dir, 'quit.png'))
            self.easy_btn = pygame.image.load(os.path.join(assets_dir, 'easy.png'))
            self.medium_btn = pygame.image.load(os.path.join(assets_dir, 'medium.png'))
            self.hard_btn = pygame.image.load(os.path.join(assets_dir, 'hard.png'))
            self.play_again_btn = pygame.image.load(os.path.join(assets_dir, 'play again.png'))
            self.button_width = 360
            self.button_height = 60
            self.new_game_btn = pygame.transform.scale(self.new_game_btn, (self.button_width, self.button_height))
            self.quit_btn = pygame.transform.scale(self.quit_btn, (self.button_width, self.button_height))
            self.easy_btn = pygame.transform.scale(self.easy_btn, (self.button_width, self.button_height))
            self.medium_btn = pygame.transform.scale(self.medium_btn, (self.button_width, self.button_height))
            self.hard_btn = pygame.transform.scale(self.hard_btn, (self.button_width, self.button_height))
            self.play_again_btn = pygame.transform.scale(self.play_again_btn, (self.button_width, self.button_height))
        except:
            print("gaada button")
            self.new_game_btn = self.quit_btn = self.easy_btn = self.medium_btn = self.hard_btn = self.play_again_btn = None
        
        try:
            self.sudoku_game = pygame.image.load(os.path.join(assets_dir, 'sudoku game baru.png'))
            self.select_difficulty = pygame.image.load(os.path.join(assets_dir, 'select difficulty.png'))
            self.button_width2 = 600
            self.button_height2 = 100
            self.sudoku_game = pygame.transform.scale(self.sudoku_game, (self.button_width2, self.button_height))
            self.select_difficulty = pygame.transform.scale(self.select_difficulty, (self.button_width2, self.button_height2))
        except:
            print("gaada judul")
            self.sudoku_game = self.select_difficulty = None

        self.font = pygame.font.Font("minecraft.ttf", 30)
        self.font_2 = pygame.font.Font("minecraft.ttf", 36)
        self.score_font = pygame.font.Font("minecraft.ttf", 30)

        try:
            self.correct_sound = mixer.Sound(os.path.join(sounds_dir, 'correct.wav'))
            self.wrong_sound = mixer.Sound(os.path.join(sounds_dir, 'Wrong.mp3'))
            self.win_sound = mixer.Sound(os.path.join(sounds_dir, 'win.mp3'))
        except:
            print("gaada sound")
            self.correct_sound = self.wrong_sound = self.win_sound = None

        self.start_time = 0
        self.elapsed_time = 0
        self.score = 0
        self.score_font = self.score_font
        self.board = None
        self.solution = None
        self.selected = None
        self.wrong_move = False
        self.difficulty = None

    def draw_background(self):
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(self.WHITE)

    def format_time(self,seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{int(minutes):02}:{int(seconds):02}"

    def calculate_score(self,input_type):
        global score
        if input_type == 'correct':
            self.score += 5
        elif input_type == 'incorrect':
            self.score = max(0, self.score - 7)
        return self.score

    def generate_puzzle(self,level):
        def shuffle_numbers():
            numbers = list(range(1, 10))
            random.shuffle(numbers)
            return numbers

        self.board = [[0 for _ in range(9)] for _ in range(9)]

        numbers = shuffle_numbers()
        for i in range(9):
            self.board[i][i] = numbers[i]

        self.solve_sudoku(self.board)

        self.solution = [row[:] for row in self.board]

        if level == 'easy':
            num_remove = 2
        elif level == 'medium':
            num_remove = 37
        else:
            num_remove = 47

        removed_positions = set()
        while len(removed_positions) < num_remove:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if (row, col) not in removed_positions:
                removed_positions.add((row, col))
                self.board[row][col] = 0
        
        return self.board, self.solution

    def solve_sudoku(self,board):
        def is_valid(board, pos, num):
            row, col = pos
            if num in self.board[row]:
                return False
            if num in [self.board[i][col] for i in range(9)]:
                return False
            box_x, box_y = row // 3, col // 3
            for i in range(box_x * 3, (box_x + 1) * 3):
                for j in range(box_y * 3, (box_y + 1) * 3):
                    if self.board[i][j] == num:
                        return False
            return True

        def find_empty(board):
            for i in range(9):
                for j in range(9):
                    if self.board[i][j] == 0:
                        return (i, j)
            return None

        empty = find_empty(self.board)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if is_valid(self.board, (row, col), num):
                self.board[row][col] = num
                if self.solve_sudoku(self.board):
                    return True
                self.board[row][col] = 0
        return False

    def draw_grid(self):
        self.draw_background()
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 2
            pygame.draw.line(self.screen, self.BLACK,
                             (i * self.SQUARE_SIZE, 0),
                             (i * self.SQUARE_SIZE, self.WIDTH), line_width)
            pygame.draw.line(self.screen, self.BLACK,
                             (0, i * self.SQUARE_SIZE),
                             (self.WIDTH, i * self.SQUARE_SIZE), line_width)
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    text = self.font_2.render(str(self.board[i][j]), True, self.BLACK)
                    self.screen.blit(text, (j * self.SQUARE_SIZE + 20, i * self.SQUARE_SIZE + 10))

        if self.selected:
            row, col = self.selected
            color = self.RED if self.wrong_move else self.BLUE
            pygame.draw.rect(self.screen, color,
                             (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE), 4)

        elapsed_seconds = time.time() - self.start_time
        stopwatch_text = self.font.render("Time: " + self.format_time(elapsed_seconds), True, self.BLACK)
        self.screen.blit(stopwatch_text, (10, self.WIDTH + 10))

        self.score_text = self.score_font.render(f"Score: {self.score}", True, self.BLACK)
        self.screen.blit(self.score_text, (self.WIDTH - 150, self.WIDTH + 10))


    def draw_button(self, button_image, y_position, text=None):
        if button_image is None:
            color = self.GREY
            button_width, button_height = 300, 50
            button_x = (self.WIDTH - button_width) // 2
            button = pygame.Rect(button_x, y_position, button_width, button_height)
            pygame.draw.rect(self.screen, color, button, border_radius=20)
            if text:
                button_text = self.font.render(text, True, self.BLACK)
                text_rect = button_text.get_rect(center=button.center)
                self.screen.blit(button_text, text_rect)
        else:
            button_x = (self.WIDTH // 4.75)
            button = pygame.Rect(button_x, y_position, self.button_width, self.button_height)
            self.screen.blit(button_image, button)
            return button

    def choose_difficulty(self):
        self.screen.blit(self.background, (0, 0))
        if self.select_difficulty:
            title_rect = self.select_difficulty.get_rect(center=(self.WIDTH//2, 100))
            self.screen.blit(self.select_difficulty, title_rect)

        easy_button = self.draw_button(self.easy_btn, 250)
        medium_button = self.draw_button(self.medium_btn, 350)
        hard_button = self.draw_button(self.hard_btn, 450)
        
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if easy_button.collidepoint(mouse_pos):
                        return 'easy'
                    if medium_button.collidepoint(mouse_pos):
                        return 'medium'
                    if hard_button.collidepoint(mouse_pos):
                        return 'hard'

    def main_menu(self):
        self.screen.blit(self.background, (0, 0))
        if self.sudoku_game:
            title_rect = self.sudoku_game.get_rect(center=(self.WIDTH//2, 100))
            self.screen.blit(self.sudoku_game, title_rect)

        start_button = self.draw_button(self.new_game_btn, 250)
        quit_button = self.draw_button(self.quit_btn, 350)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):
                        return 'start'
                    elif quit_button.collidepoint(mouse_pos):
                        return pygame.quit()

    def animate_confetti(self):
        particles = []
        for _ in range(200):
            x = random.randint(0, self.WIDTH)
            y = random.randint(0, self.HEIGHT)
            color = random.choice([self.RED, self.BLUE, self.GREY, self.green])
            size = random.randint(3, 7)
            speed = random.uniform(1, 5)
            particles.append([x, y, size, speed, color])

        for _ in range(380):
            self.screen.blit(self.background, (0, 0))
            for p in particles:
                p[1] += p[3]
                pygame.draw.circle(self.screen, p[4], (p[0], int(p[1])), p[2])
            pygame.display.flip()
            pygame.time.delay(7)


    def is_game_won(self,board, solution):
        return self.board == self.solution

    def show_win_screen(self, level, board):
        self.screen.blit(self.background, (0, 0))
        self.win_sound.play()
        self.animate_confetti()

        final_time = time.time() - self.start_time
        formatted_time = self.format_time(final_time)

        if self.trophy:
            trophy_rect = self.trophy.get_rect()
            trophy_rect.centerx = self.WIDTH // 2
            trophy_rect.top = 40
            self.screen.blit(self.trophy, trophy_rect)
            title_y = 100
        else:
            title_y = 150

        title_text = self.font.render("CONGRATULATIONS, YOU WIN!", True, self.BLACK)
        title_rect = title_text.get_rect(center=(self.WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)

        score_y = 300 if self.trophy else 200
        time_y = 350 if self.trophy else 250

        score_text = self.font.render(f"Final Score: {self.score}", True, self.BLACK)
        score_rect = score_text.get_rect(center=(self.WIDTH//2, 300))
        self.screen.blit(score_text, score_rect)

        time_text = self.font.render(f"Completion Time: {formatted_time}", True, self.BLACK)
        time_rect = time_text.get_rect(center=(self.WIDTH//2, 350))
        self.screen.blit(time_text, time_rect)

        play_again_button = self.draw_button(self.play_again_btn, self.HEIGHT // 2 + 150)
        quit_button = self.draw_button(self.quit_btn, self.HEIGHT // 2 + 230)

        pygame.display.update()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_button.collidepoint(event.pos):
                        waiting = False
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        exit()
    def start(self):
        self.run_game()
        return self.run_game()

    def run_game(self):
        clock = pygame.time.Clock()  
        while True:
            menu_choice = self.main_menu()
            level = self.choose_difficulty()
            self.board, self.solution = self.generate_puzzle(level)
            self.start_time = time.time()
            self.score = 0
            self.selected = (0, 0)
            self.wrong_move = False
            running = True

            last_score_reduction = time.time()
            score_reduction_interval = 45
            score_reduction_amount = 5

            while running:
                clock.tick(self.FPS)
                current_time = time.time()
                if current_time - last_score_reduction >= score_reduction_interval:
                    self.score = max(0, self.score - score_reduction_amount)
                    last_score_reduction = current_time
            
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = pos[1] // self.SQUARE_SIZE, pos[0] // self.SQUARE_SIZE
                        if row < 9 and col < 9:
                            self.selected = (row, col)

                    if event.type == pygame.KEYDOWN:
                        if pygame.K_1 <= event.key <= pygame.K_9:
                            num = event.key - pygame.K_0
                        elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                            num = event.key - pygame.K_KP1 + 1
                        else:
                            num = None

                        if self.selected and num:
                            row, col = self.selected
                            if self.solution[row][col] == num:
                                self.board[row][col] = num
                                self.correct_sound.play()
                                self.wrong_move = False
                                self.score = self.calculate_score('correct')
                            else:
                                self.wrong_sound.play()
                                self.wrong_move = True
                                self.score = self.calculate_score('incorrect')
                self.draw_grid()
                pygame.display.flip()

                if self.is_game_won(self.board, self.solution):
                    end_time = time.time() - self.start_time
                    self.show_win_screen(level, self.board)
                    running = False
                    return
                elif menu_choice == 'quit':
                    pygame.quit()

if __name__ == "__main__":
    game = SudokuGame()
    game.start()