import random
import pygame, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()


#music and sfx

pygame.mixer.music.set_volume(0.75)
pygame.mixer.music.load('pong.mp3')
bounceSound = pygame.mixer.Sound('bounce.wav')
RPWON = pygame.mixer.Sound('RightPlayerWon.mp3')
LPWON = pygame.mixer.Sound('LeftPlayerWon.mp3')
GOAL = pygame.mixer.Sound('LostPoint.wav')
Border = pygame.mixer.Sound('BorderBounce.wav')

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)


BigFont = pygame.font.SysFont("Arial", 26)
SmallFont = pygame.font.SysFont("Arial", 16)
MediumFont = pygame.font.SysFont("Arial", 20)

#pitch
WIDTH = 600
HEIGHT = 500
INTERFACE_HEIGHT = 50 + 5 # 5 is line thickness
PITCH_HEIGHT = HEIGHT - INTERFACE_HEIGHT;

#elements
BALL_RADIUS = 10
PAD_WIDTH = 10
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
ball_pos = [0,0]
ball_vel = [0,0]
l_paddle_vel = 0
r_paddle_vel = 0
leftScore = 0
rightScore = 0
ball_speed_modifier = 0.3
hard_mode = 0
max_ball_vel = 8.5
paddlesVelocity = 8
solo_mode = 0



#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 64)
pygame.display.set_caption('PONG!!!')



def draw_text(text,font,color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)



# define event handlers
def round_init():
    global l_paddle_pos, r_paddle_pos, l_paddle_vel, r_paddle_vel,leftScore,rightScore,hard_mode, solo_mode  # these are floats
  
   
    pygame.mixer.music.play(-1) # -1 for infinite loop 0 for single play
    l_paddle_pos = [HALF_PAD_WIDTH - 1,HEIGHT - PITCH_HEIGHT//2]
    r_paddle_pos = [WIDTH + 1 - HALF_PAD_WIDTH,HEIGHT-PITCH_HEIGHT//2]
    leftScore = 0
    rightScore = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    #ball starting position
    
    ball_pos = [WIDTH//2,PITCH_HEIGHT//2 + INTERFACE_HEIGHT]
    
    #ball random starting velocity
    horz = random.randrange(3,5)

    direction = random.choice([-1.5, 1.5])

    vert = random.randrange(1,3) /1.2 * direction;
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]




#draw function of canvas
def draw(canvas):
    global l_paddle_pos, r_paddle_pos, ball_pos, ball_vel, leftScore, rightScore, max_ball_vel, solo_mode
     
#draw pitch
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH // 2,INTERFACE_HEIGHT],[WIDTH // 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH//2, INTERFACE_HEIGHT],[PAD_WIDTH//2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH//2, INTERFACE_HEIGHT],[WIDTH - PAD_WIDTH//2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [0, INTERFACE_HEIGHT],[WIDTH, INTERFACE_HEIGHT], 5)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, PITCH_HEIGHT//2 + INTERFACE_HEIGHT], 70, 1)
    
 #draw paddles and ball
    pygame.draw.circle(canvas, RED , ball_pos, BALL_RADIUS, 0)
    pygame.draw.polygon(canvas, GREEN, [[l_paddle_pos[0] - HALF_PAD_WIDTH, l_paddle_pos[1] - HALF_PAD_HEIGHT], [l_paddle_pos[0] - HALF_PAD_WIDTH, l_paddle_pos[1] + HALF_PAD_HEIGHT], [l_paddle_pos[0] + HALF_PAD_WIDTH, l_paddle_pos[1] + HALF_PAD_HEIGHT], [l_paddle_pos[0] + HALF_PAD_WIDTH, l_paddle_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[r_paddle_pos[0] - HALF_PAD_WIDTH, r_paddle_pos[1] - HALF_PAD_HEIGHT], [r_paddle_pos[0] - HALF_PAD_WIDTH, r_paddle_pos[1] + HALF_PAD_HEIGHT], [r_paddle_pos[0] + HALF_PAD_WIDTH, r_paddle_pos[1] + HALF_PAD_HEIGHT], [r_paddle_pos[0] + HALF_PAD_WIDTH, r_paddle_pos[1] - HALF_PAD_HEIGHT]], 0)

    # update paddle's vertical position, keep paddle on the screen
    if l_paddle_pos[1] > INTERFACE_HEIGHT + HALF_PAD_HEIGHT and l_paddle_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        l_paddle_pos[1] += l_paddle_vel
    elif l_paddle_pos[1] <= INTERFACE_HEIGHT + HALF_PAD_HEIGHT and l_paddle_vel > 0:
        l_paddle_pos[1] += l_paddle_vel
    elif l_paddle_pos[1] >= HEIGHT - HALF_PAD_HEIGHT  and l_paddle_vel < 0:
        l_paddle_pos[1] += l_paddle_vel
    
    if r_paddle_pos[1] > INTERFACE_HEIGHT + HALF_PAD_HEIGHT and r_paddle_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        r_paddle_pos[1] += r_paddle_vel
    elif r_paddle_pos[1] <= INTERFACE_HEIGHT  + HALF_PAD_HEIGHT  and r_paddle_vel > 0:
        r_paddle_pos[1] += r_paddle_vel
    elif r_paddle_pos[1] >= HEIGHT - HALF_PAD_HEIGHT and r_paddle_vel < 0:        
        r_paddle_pos[1] += r_paddle_vel

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])


   
    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= INTERFACE_HEIGHT + BALL_RADIUS + 5 :  # 5 is line thickness
        ball_vel[1] = - ball_vel[1]
        Border.play()
        if hard_mode == 1:
            ball_vel[1] += ball_speed_modifier
            ball_vel[0] *= 1.1

    if int(ball_pos[1]) >= HEIGHT - BALL_RADIUS -1:
        ball_vel[1] = -ball_vel[1]
        Border.play()
        if hard_mode == 1:           
            ball_vel[1] -= ball_speed_modifier
            ball_vel[0] *= 1.1
            
    
    #ball collison check on lines and paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(l_paddle_pos[1] - HALF_PAD_HEIGHT,l_paddle_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        bounceSound.play()

        if abs(ball_vel[1]) < max_ball_vel and abs(ball_vel[0]) < max_ball_vel:
            ball_vel[0] += ball_speed_modifier
            ball_vel[1] += ball_speed_modifier
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        leftScore += 1
        GOAL.play()
        ball_init(False)
        
    if int(ball_pos[0]) >= WIDTH - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(r_paddle_pos[1] - HALF_PAD_HEIGHT,r_paddle_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        bounceSound.play()


        if abs(ball_vel[1]) < max_ball_vel and abs(ball_vel[0]) < max_ball_vel :
            ball_vel[0] -= ball_speed_modifier
            ball_vel[1] -= ball_speed_modifier
    elif int(ball_pos[0]) >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        rightScore += 1
        GOAL.play()
        ball_init(True)

    if rightScore >9:
        LPWON.play()
        round_init()

    if leftScore > 9:
        RPWON.play()
        round_init()
   
    draw_text(str(rightScore) + " Score " + str(leftScore),BigFont,BLUE, window,253,10)

    draw_text("Press 'R' for Restart",SmallFont,RED, window,10,7)


    if solo_mode == 0:
        draw_text("Press 'M' for Singleplayer",MediumFont,GREEN, window,400,12)
       

    if solo_mode == 1:
        draw_text("Press 'M' for Multiplayer",MediumFont,GREEN, window,400,12)
    
   
   
    if hard_mode == 0:
        draw_text("Press 'H' for Hard Mode",SmallFont,RED, window,10,25)
       

    if hard_mode == 1:
        draw_text("Press 'E' for Easy Mode",SmallFont,GREEN, window,10,25)


    #enemy brain


    if solo_mode == 1:

        if hard_mode == 0:

            offset = random.randrange(8,90)

        if hard_mode == 1:
             offset = random.randrange(2,60)
        
        if ball_pos[1] > INTERFACE_HEIGHT +HALF_PAD_HEIGHT and ball_pos[1] < HEIGHT - HALF_PAD_HEIGHT:

            
                 if ball_pos[1] - r_paddle_pos[1] > offset or r_paddle_pos[1] - ball_pos[1] > offset:
                         r_paddle_pos[1] = ball_pos[1]
        
      

   
    
    
#keydown handler  # paddles speed
def keydown(event):
    global l_paddle_vel, r_paddle_vel, hard_mode, ball_speed_modifier, solo_mode
    
   

    if event.key == K_UP:
        if solo_mode == 0:
             r_paddle_vel = -paddlesVelocity
    elif event.key == K_DOWN:
        if solo_mode == 0:
             r_paddle_vel = paddlesVelocity
       

    elif event.key == K_w:
        l_paddle_vel = -paddlesVelocity
    elif event.key == K_s:
        l_paddle_vel = paddlesVelocity 
    elif event.key == K_r:    ##press r for restart
        round_init()
    elif event.key == K_m:
        if solo_mode == 0:
           solo_mode = 1
        elif solo_mode == 1:
           solo_mode = 0

    elif hard_mode == 0:
        if event.key == K_h:    ##press h for hard mode
            paddlesVelocity + 5
            ball_speed_modifier *= 1.5
            hard_mode = 1

    elif hard_mode == 1:
        if event.key == K_e:
            paddlesVelocity - 5
            ball_speed_modifier /= 1.5
            hard_mode = 0

   
  
            


#keyup handler
def keyup(event):
    global l_paddle_vel, r_paddle_vel
    
    if event.key in (K_w, K_s):
        l_paddle_vel = 0
    elif event.key in (K_UP, K_DOWN):
        if solo_mode == 0:
            r_paddle_vel = 0

round_init()



#game loop
while True:

    draw(window)
    

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            
            
    pygame.display.update()
    fps.tick(60)
    
    
