import math
import pygame
import pygame.mixer
import random
# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 255, 255)
 
# Size of bricks
brick_width = 40
brick_height = 25
 
class Brick(pygame.sprite.Sprite):
    
    #This class represents each brick, made using the Sprite class in Pygame
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([brick_width, brick_height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
 
        # Move the top left of the rectangle to x,y.
        self.rect.x = x
        self.rect.y = y
 
 
class Ball(pygame.sprite.Sprite):
    
    #This class represents the ball, made using the Sprite class in Pygame
    speed = 12.0
 
    # Float point on grid of where the ball is
    x = 0.0
    y = 250.0
 
    # Direction of ball
    direction = 200
    width, height = 10, 10
     
    def __init__(self):
        
        #defines parameters of ball
        super().__init__()
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
    def bounce(self, diff):
        #Bounce the ball off the paddle
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
 
    def update(self):
        #Update position of the ball
        direction_radians = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        #Move the ball to new point
        self.rect.x = self.x
        self.rect.y = self.y
 
        #Bounce off the top of the screen
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
 
        #Bounce off the left of the screen
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
 
        #Bounce of the right side of the screen
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1
 
        #Fall off the bottom edge of the screen
        if self.y > 600:
            return True
        else:
            return False
 
 
class Paddle(pygame.sprite.Sprite):
    
    #This class represents the mouse controlled bar at the bottom
    def __init__(self):
        super().__init__()
        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((white))
 
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        self.rect.x = 0
        self.rect.y = self.screenheight-self.height - 15
 
    def update(self):
        #Update paddle position and keep it on screen
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width
            

def main():
    #initialize pygame and pygame.mixer modules and create the screen
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode([800, 600])
    
    #background music for game
#    pygame.display.set_caption("BrickBreaker Final Project")
#    pygame.mixer.music.load('screen.mp3')
   # pygame.mixer.music.play(-1)

    #opening screen; defines rules of game and starts game if mousebutton is clicked
    red = (255,0,0)
    end_it = False
    while end_it ==False:
        screen.fill(black)
        font = pygame.font.SysFont("Britannic Bold", 35)
        label1 = font.render("Welcome to BrickBreaker - Use mouse to move the paddle", 1, red) 
        label2 = font.render("and try to bounce the ball", 1, red)
        label3 = font.render("in order to break all of the bricks without" , 1, red)
        label4 = font.render("letting the ball touch the bottom of the screen", 1, red)
        label5 = font.render("CLICK THE MOUSE TO START THE GAME", 1, red)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                end_it = True
        screen.blit(label1, (100,200))
        screen.blit(label2,(100,250))
        screen.blit(label3,(100,300))
        screen.blit(label4,(100,350))
        screen.blit(label5,(100,400))
        
        pygame.display.flip()

    #Make mouse disappear when over window
    pygame.mouse.set_visible(0)

    font = pygame.font.Font(None, 65)
    background = pygame.Surface(screen.get_size())

    #Create sprite lists
    bricks = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()

    #Create the player paddle object
    paddle = Paddle()
    allsprites.add(paddle)

    #Create the ball
    ball = Ball()
    allsprites.add(ball)
    balls.add(ball)

    #Create brick formations using Brick class
    top = 10
    #sets i to random number; depending on value, chooses one of four levels
    i = random.randrange(1, 5)
    
    #four levels varying in design and difficulty
    if i == 1:
        print("Level 1")
        for row in range(5):
            for column in range(0, 19):
                brick = Brick(blue, column * (brick_width + 2) + 1, top)
                bricks.add(brick)
                allsprites.add(brick)
            #Move next row down
            top += brick_height + 2

    elif i == 2:
        print("Level 2")
        for row in range(6):
            for column in range(0,12):
                col1, col2, col3 = random.randrange(30, 255), random.randrange(30, 255), random.randrange(30,255)
                randcolor = (col1, col2, col3)
                brick = Brick(randcolor, column * (brick_width + 2) + 150, top)
                bricks.add(brick)
                allsprites.add(brick)
            top += brick_height + 2
    elif i == 3:
        print("Level 3")
        for row in range(8):
            if row % 2 == 0:
                for column in range(0,19):
                    col1, col2, col3 = random.randrange(30,255), random.randrange(30, 255), random.randrange(30, 255)
                    randcolor = (col1, col2, col3)
                    brick = Brick(randcolor, column * (brick_width + 2) +1, top)
                    bricks.add(brick)
                    allsprites.add(brick)
                top += brick_height + 2
            else:
                for column in range (0,15):
                    col1, col2, col3 = random.randrange(30, 255), random.randrange(30, 255), random.randrange(30, 255)
                    randcolor = (col1, col2, col3)
                    brick = Brick(randcolor, column * (brick_width + 2) + (brick_width*2), top)
                    bricks.add(brick)
                    allsprites.add(brick)
                top += brick_height + 2
    elif i == 4:
        print("Level 4")
        for row in range(8):
            if row %2 == 0:
                continue
            else:
                for column in range(0,19):
                    col1, col2, col3 = random.randrange(30,255), random.randrange(30, 255), random.randrange(30, 255)
                    randcolor = (col1, col2, col3)
                    brick = Brick(randcolor, column * (brick_width + 2) +1, top)
                    bricks.add(brick)
                    allsprites.add(brick)
                top += brick_height + 50

    #Clock to time ball speed
    clock = pygame.time.Clock()

    game_over = False
    exit_program = False

    #actual game
    while not exit_program:

        #Set clock speed at 30
        clock.tick(30)

        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_program = True

        # Update  ball and paddle position as long as the game is not over.
        if not game_over:
            # Update the player and ball positions
            paddle.update()
            game_over = ball.update()

        #If ball hits bottom of screen, print game over
        if game_over:
            text = font.render("Game Over", True, white)
            text2 = font.render("Press Space to Restart", True, white)
            textpos2 = text.get_rect(centerx=background.get_width()/2-125)
            textpos2.top = 400
            textpos = text.get_rect(centerx=background.get_width()/2)
            textpos.top = 300
            screen.blit(text, textpos)
            screen.blit(text2, textpos2)
            
            #restarts game if space is pressed
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()

        # Check if ball hits paddle and bounce in appropriate direction
        if pygame.sprite.spritecollide(paddle, balls, False):
            diff = (paddle.rect.x + paddle.width/2) - (ball.rect.x + ball.width/2)
            ball.rect.y = screen.get_height() - paddle.rect.height - ball.rect.height - 1
            ball.bounce(diff)

        # Check for ball hitting bricks
        delbricks = pygame.sprite.spritecollide(ball, bricks, True)

        # If ball hits a brick, bounce the ball
        if len(delbricks) > 0:
            ball.bounce(0)

            # Game ends if all the bricks are gone
            if len(bricks) == 0:
                game_over = True

        allsprites.draw(screen)

        #Show game to player
        pygame.display.flip()

    pygame.quit()
main()
