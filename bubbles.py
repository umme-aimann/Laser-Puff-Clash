import pygame
pygame.init()

fps = 60
width = 900
height = 500
WIN = pygame.display.set_mode((width, height))
PLAYER_WIDTH, PLAYER_HEIGHT = 155, 200

# Import images
Bg_image=pygame.image.load("assets/townsville.jpg")
Bubbles_image = pygame.image.load("assets/bubbles.png")
Blossoms_image = pygame.image.load("assets/blossoms.png")
Small_Blue_Laser = pygame.image.load("assets/blue_laser.png")
Small_Red_Laser = pygame.image.load("assets/red_laser.png")
BUBBLES = pygame.transform.scale(Bubbles_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
BLOSSOMS = pygame.transform.scale(Blossoms_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
TOWNSVILLE = pygame.transform.scale(Bg_image, (width, height))
#scaling image of lasers
BLUE_LASER = pygame.transform.scale(Small_Blue_Laser, (70, 40))
RED_LASER = pygame.transform.scale(Small_Red_Laser, (40, 40))
# Define font and font color
FONT = pygame.font.SysFont('comicsans', 30)
BLACK = (0, 0, 0)

# Initial positions and velocities
bubbles_x, bubbles_y = 20, 50
blossom_x, blossom_y = width - 200, 50
bubbles_life = 100
blossom_life = 100
VEL = 5
LASER_VEL = 12
# Custom events
BUBBLES_HIT = pygame.USEREVENT + 1
BLOSSOM_HIT = pygame.USEREVENT + 2



def draw_window(red_lasers, blue_lasers):
    # Show images
    WIN.blit(TOWNSVILLE, (0, 0))
    WIN.blit(BUBBLES, (bubbles_x, bubbles_y))
    WIN.blit(BLOSSOMS, (blossom_x, blossom_y))
    # Show text
    red_text = FONT.render("Blossom Life: " + str(blossom_life), 1, BLACK)
    blue_text = FONT.render("Bubbles Life: " + str(bubbles_life), 1, BLACK)
    WIN.blit(red_text, (width - red_text.get_width() - 10, 10))
    WIN.blit(blue_text, (10, 10))
    #show lasers
    for laser in red_lasers:
        WIN.blit(RED_LASER, (laser.x, laser.y))
    for laser in blue_lasers:
        WIN.blit(BLUE_LASER, (laser.x, laser.y))
    pygame.display.update()

def handle_bubbles_movement(keys):
    global bubbles_x, bubbles_y
    if keys[pygame.K_w] and bubbles_y - VEL > 0:  # Up
        bubbles_y -= VEL
    if keys[pygame.K_s] and bubbles_y + VEL + PLAYER_HEIGHT < height:  # Down
        bubbles_y += VEL
    if keys[pygame.K_a] and bubbles_x - VEL > 0:  # Left
        bubbles_x -= VEL
    if keys[pygame.K_d] and bubbles_x + VEL + PLAYER_WIDTH < width:  # Right
        bubbles_x += VEL

def handle_blossom_movement(keys):
    global blossom_x, blossom_y
    if keys[pygame.K_UP] and (blossom_y - VEL) > 0:  # Up
        blossom_y -= VEL
    if keys[pygame.K_DOWN] and (blossom_y + VEL + PLAYER_HEIGHT) < height:  # Down
        blossom_y += VEL
    if keys[pygame.K_LEFT] and (blossom_x - VEL) > 0:  # Left
        blossom_x -= VEL
    if keys[pygame.K_RIGHT] and (blossom_x + VEL + PLAYER_WIDTH) < width:  # Right
        blossom_x += VEL

def handle_lasers(red_lasers, blue_lasers):
    global bubbles_life, blossom_life
    for laser in red_lasers:
        laser.x -= LASER_VEL
        if laser.colliderect(pygame.Rect(bubbles_x, bubbles_y, PLAYER_WIDTH, PLAYER_HEIGHT)):
            pygame.event.post(pygame.event.Event(BUBBLES_HIT))
            red_lasers.remove(laser)
        elif laser.x > width:
            red_lasers.remove(laser)

    for laser in blue_lasers:
        laser.x += LASER_VEL
        if laser.colliderect(pygame.Rect(blossom_x, blossom_y, PLAYER_WIDTH, PLAYER_HEIGHT)):
            pygame.event.post(pygame.event.Event(BLOSSOM_HIT))
            blue_lasers.remove(laser)
        elif laser.x > width:
            blue_lasers.remove(laser)

def draw_winner(text):
    draw_text = FONT.render(text, 1, BLACK)
    WIN.blit(draw_text, (width // 2 - draw_text.get_width() // 2, height // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    global bubbles_life, blossom_life, bubbles_x, bubbles_y, blossom_x, blossom_y
    clock = pygame.time.Clock()
    red_lasers = []
    blue_lasers = []
    run = True
    while run:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    laser = pygame.Rect(blossom_x, blossom_y + PLAYER_HEIGHT // 2 - 5, 20, 10)
                    red_lasers.append(laser)
                if event.key == pygame.K_LCTRL:
                    laser = pygame.Rect(bubbles_x + PLAYER_WIDTH, bubbles_y + PLAYER_HEIGHT // 2 - 5, 20, 10)
                    blue_lasers.append(laser)
            if event.type == BUBBLES_HIT:
                bubbles_life -= 5
            if event.type == BLOSSOM_HIT:
                blossom_life -= 5
            

        keys = pygame.key.get_pressed()
        handle_bubbles_movement(keys)
        handle_blossom_movement(keys)
        handle_lasers(red_lasers, blue_lasers)
        draw_window(red_lasers, blue_lasers)

        if bubbles_life <= 0:
            draw_winner("Blossom Wins!")
            run= False

        if blossom_life <= 0:
            draw_winner("Bubbles Wins!")
            run= False


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                

if __name__ == "__main__":
    main()
