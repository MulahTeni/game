import pygame
import random

# Velocity of ball
def velocity_generate():

    number = random.randint(-100, 100)
    if number < 0:
        number -= random.randint(200, 300)
    else:
        number += random.randint(200, 300)
        
    return number


# Update velocity through time
def update_velocity(velocity):

    if velocity<0:
        velocity -= 1
    else:
        velocity += 1

    return velocity


# Player class
class Player(object):

    def __init__(self, color, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 20, 120)
        self.color = color
        self.score = 0

    def move(self, d):
        self.rect.y += d
        # If you collide with a wall, move out based on velocity
        if self.rect.colliderect(walls[0].rect):
            # Moving up; Hit the bottom side of the wall
            self.rect.bottom = walls[1].rect.top - 1

        if self.rect.colliderect(walls[1].rect):
            # Moving down; Hit the top side of the wall
            self.rect.top = walls[0].rect.bottom + 1


# Ball class
class Ball(object):

    def __init__(self):
        self.x_coor = screen.get_width() / 2
        self.y_coor = screen.get_height() / 2
        self.centre = pygame.Vector2(self.x_coor, self.y_coor)
        self.radius = 15

        self.x_vel = velocity_generate()
        self.y_vel = velocity_generate()

        self.rect = pygame.Rect(self.x_coor - self.radius, self.y_coor - self.radius, self.radius * 2, self.radius * 2)


    def __del__(self):
        pass

    def auto_move(self):
        self.x_vel = update_velocity(self.x_vel)
        self.y_vel = update_velocity(self.y_vel)

        self.x_coor += int(self.x_vel * dt)
        self.y_coor += int(self.y_vel * dt)
        self.centre = pygame.Vector2(self.x_coor, self.y_coor)

        # Update the rectangle based on the new center position
        self.rect.center = self.centre

        # Check for collisions with walls and adjust velocity accordingly
        if self.rect.colliderect(walls[0].rect):
            # Handle collision with the top wall
            self.y_coor = walls[0].rect.bottom + self.radius
            self.y_vel = abs(self.y_vel)

        if self.rect.colliderect(walls[1].rect):
            # Handle collision with the bottom wall
            self.y_coor = walls[1].rect.top - self.radius
            self.y_vel = -abs(self.y_vel)

        if self.rect.colliderect(walls[2].rect):
            player2.score += 1
            return True

        if self.rect.colliderect(walls[3].rect):
            player1.score += 1
            return True

        if self.rect.colliderect(player1.rect):
            self.x_coor = player1.rect.right + self.radius
            self.x_vel = abs(self.x_vel)

        if self.rect.colliderect(player2.rect):
            self.x_coor = player2.rect.left - self.radius
            self.x_vel = -abs(self.x_vel)

        return False

# Outer Frame
class Frame(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos)



# Game setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
dt = clock.tick(60) / 1000

player1 = Player("red", (40, screen.get_height()/2 - 60))
player2 = Player("blue", (screen.get_width() - 60, screen.get_height()/2 - 60))


ball = Ball()

frame = [[0, 0, screen.get_width(), 10], [0, screen.get_height()-9, screen.get_width(), 10],
            [0, 0, 10, screen.get_height()], [screen.get_width()-9, 0, 10, screen.get_height()]]

walls = []

for wall in frame:
    Frame(wall)



running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    if keys[pygame.K_w]:
        player1.move(-300 * dt)
    if keys[pygame.K_s]:
        player1.move(300 * dt)

    if keys[pygame.K_UP]:
        player2.move(-300 * dt)
    if keys[pygame.K_DOWN]:
        player2.move(300 * dt)

    i=0
    for wall in walls:
        if i<2:
            i += 1
            pygame.draw.rect(screen, "purple", wall.rect)
        else:
            pygame.draw.rect(screen, "green", wall.rect)

    pygame.draw.rect(screen, player1.color, player1.rect)
    pygame.draw.rect(screen, player2.color, player2.rect)

    pygame.draw.circle(screen, "black", ball.centre, ball.radius)

    font = pygame.font.Font(None, 36)
    p1_score_text = font.render(f'Red Player Score: {player1.score}', True, (0, 0, 0))
    p2_score_text = font.render(f'Blue Player Score: {player2.score}', True, (0, 0, 0))

    screen.blit(p1_score_text, (20, 20))
    screen.blit(p2_score_text, (screen.get_width()-270, 20))

    if ball.auto_move():
        del ball
        ball = Ball()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
