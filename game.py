import arcade
import random

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Ping Pong, управляем клавишами W и S "
BALL_RADIUS = 10
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8
BALL_SPEED_X = 5
BALL_SPEED_Y = 4
SCORE_TO_WIN = 5


class Ball:
    def __init__(self):
        self.change_y = None
        self.change_x = None
        self.center_y = None
        self.center_x = None
        self.reset()

    def reset(self):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.change_x = BALL_SPEED_X * random.choice([-1, 1])
        self.change_y = BALL_SPEED_Y * random.choice([-1, 1])

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Отскок от верхней и нижней стенки
        if self.center_y <= BALL_RADIUS or self.center_y >= SCREEN_HEIGHT - BALL_RADIUS:
            self.change_y *= -1

    def draw(self):
        arcade.draw_circle_filled(self.center_x, self.center_y, BALL_RADIUS, arcade.color.YELLOW)


class Paddle:
    def __init__(self, x, y, color):
        self.center_x = x
        self.center_y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.speed = PADDLE_SPEED
        self.score = 0
        self.color = color

    def move_up(self):
        if self.center_y < SCREEN_HEIGHT - self.height // 2:
            self.center_y += self.speed

    def move_down(self):
        if self.center_y > self.height // 2:
            self.center_y -= self.speed

    def draw(self):
        points = (
            (self.center_x - self.width // 2, self.center_y - self.height // 2),
            (self.center_x + self.width // 2, self.center_y - self.height // 2),
            (self.center_x + self.width // 2, self.center_y + self.height // 2),
            (self.center_x - self.width // 2, self.center_y + self.height // 2)
        )
        arcade.draw_polygon_filled(points, self.color)


class PingPong(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.ball = Ball()
        self.player1 = Paddle(30, SCREEN_HEIGHT // 2, arcade.color.BLUE)
        self.player2 = Paddle(SCREEN_WIDTH - 30, SCREEN_HEIGHT // 2, arcade.color.RED)

        # Text объекты для счета
        self.player1_score_text = arcade.Text(
            text="0",
            x=SCREEN_WIDTH // 4,
            y=SCREEN_HEIGHT - 50,
            color=arcade.color.BLUE,
            font_size=36,
            anchor_x="center"
        )

        self.player2_score_text = arcade.Text(
            text="0",
            x=3 * SCREEN_WIDTH // 4,
            y=SCREEN_HEIGHT - 50,
            color=arcade.color.RED,
            font_size=36,
            anchor_x="center"
        )

        # Text объекты для сообщения о победе
        self.win_text = arcade.Text(
            text="",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2,
            color=arcade.color.WHITE,
            font_size=48,
            anchor_x="center",
            anchor_y="center"
        )

        self.restart_text = arcade.Text(
            text="Press R to restart",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 - 60,
            color=arcade.color.WHITE,
            font_size=24,
            anchor_x="center",
            anchor_y="center"
        )

        # Флаги для плавного движения
        self.player1_up_pressed = False
        self.player1_down_pressed = False

        self.game_over = False

    def on_draw(self):
        self.clear()

        # Рисуем центральную линию (пунктирную)
        for i in range(0, SCREEN_HEIGHT, 20):
            arcade.draw_line(
                SCREEN_WIDTH // 2, i,
                SCREEN_WIDTH // 2, i + 10,
                arcade.color.WHITE, 2
            )

        # Рисуем объекты
        self.ball.draw()
        self.player1.draw()
        self.player2.draw()

        # Обновляем и рисуем текст счета
        self.player1_score_text.text = str(self.player1.score)
        self.player2_score_text.text = str(self.player2.score)
        self.player1_score_text.draw()
        self.player2_score_text.draw()

        # Сообщение о победе
        if self.game_over:
            if self.player1.score >= SCORE_TO_WIN:
                self.win_text.text = "Player 1 Wins!"
                self.win_text.color = arcade.color.BLUE
            else:
                self.win_text.text = "Player 2 Wins!"
                self.win_text.color = arcade.color.RED

            self.win_text.draw()
            self.restart_text.draw()

    def on_update(self, delta_time):
        if self.game_over:
            return

        # Движение ракетки игрока 1 при удержании клавиш
        if self.player1_up_pressed:
            self.player1.move_up()
        if self.player1_down_pressed:
            self.player1.move_down()

        self.ball.update()

        # Проверка столкновения с ракетками
        if (self.ball.center_x - BALL_RADIUS <= self.player1.center_x + PADDLE_WIDTH // 2 and
                self.player1.center_y - PADDLE_HEIGHT // 2 <= self.ball.center_y <= self.player1.center_y +
                PADDLE_HEIGHT // 2 and
                self.ball.change_x < 0):
            self.ball.change_x = abs(self.ball.change_x)  # Движение вправо
            # Добавляем немного случайности для усложнения игры
            self.ball.change_y += random.uniform(-1.5, 1.5)

        if (self.ball.center_x + BALL_RADIUS >= self.player2.center_x - PADDLE_WIDTH // 2 and
                self.player2.center_y - PADDLE_HEIGHT // 2 <= self.ball.center_y <= self.player2.center_y +
                PADDLE_HEIGHT // 2 and
                self.ball.change_x > 0):
            self.ball.change_x = -abs(self.ball.change_x)  # Движение влево
            # Добавляем немного случайности для усложнения игры
            self.ball.change_y += random.uniform(-1.5, 1.5)

        # Проверка гола
        if self.ball.center_x < 0:
            self.player2.score += 1
            self.check_win()
            self.ball.reset()

        elif self.ball.center_x > SCREEN_WIDTH:
            self.player1.score += 1
            self.check_win()
            self.ball.reset()

        # Простой ИИ для второго игрока
        if self.ball.center_y > self.player2.center_y + 20:
            self.player2.move_up()
        elif self.ball.center_y < self.player2.center_y - 20:
            self.player2.move_down()

    def check_win(self):
        if self.player1.score >= SCORE_TO_WIN or self.player2.score >= SCORE_TO_WIN:
            self.game_over = True

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player1_up_pressed = True
        elif key == arcade.key.S:
            self.player1_down_pressed = True
        elif key == arcade.key.R and self.game_over:
            self.restart_game()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.player1_up_pressed = False
        elif key == arcade.key.S:
            self.player1_down_pressed = False

    def restart_game(self):
        self.ball.reset()
        self.player1.score = 0
        self.player2.score = 0
        self.player1.center_y = SCREEN_HEIGHT // 2
        self.player2.center_y = SCREEN_HEIGHT // 2
        self.game_over = False


def main():
    game = PingPong()
    arcade.run()


if __name__ == "__main__":
    main()

