import pygame,os,sys

pygame.font.init()
pygame.mixer.init()
pygame.init()

WIDTH,HEIGHT= 900,600
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
FPS = 60
VEL = 2
BULLET_VEL = 3
MAX_BULLETS = 3


BORDER = pygame.Rect(WIDTH//2 - 5,0,10,HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND= pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

pygame.display.set_caption("Shooter Game")

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

spaceship_width,spaceship_height = 55,40

HEALTH_FONT = pygame.font.SysFont("comicsansms",42)
WIN_FONT = pygame.font.SysFont("comicsansms",100)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png')).convert_alpha()
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(spaceship_width,spaceship_height)),90)
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png')).convert_alpha()
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(spaceship_width,spaceship_height)),270)

SPACE_BACKGROUND = pygame.image.load(os.path.join('Assets','space.png'))
SPACE_BACKGROUND = pygame.transform.scale(SPACE_BACKGROUND,(WIDTH,HEIGHT))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def draw_winner(text):
    win_text = WIN_FONT.render(text,True,WHITE)
    screen.blit(win_text,(WIDTH//2 - win_text.get_width()//2,HEIGHT//2 - win_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def draw_screen(red_rect,yellow_rect,red_bullets,yellow_bullets,red_health,yellow_health):
    
    screen.blit(SPACE_BACKGROUND,(0,0))
    pygame.draw.rect(screen,BLACK,BORDER)

    red_health_text = HEALTH_FONT.render(f"Health: {red_health}",True,WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}",True,WHITE)

    screen.blit(red_health_text,(WIDTH - red_health_text.get_width() - 10,10))
    screen.blit(yellow_health_text,(10,10))
    screen.blit(YELLOW_SPACESHIP,yellow_rect)
    screen.blit(RED_SPACESHIP,red_rect)

    for bullet in red_bullets:
        pygame.draw.rect(screen,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(screen,YELLOW,bullet)
    pygame.display.update()



def yellow_handle_movement(keys_pressed,yellow_rect):
    if keys_pressed[pygame.K_w] and yellow_rect.y - VEL >= 0:
        yellow_rect.y -= VEL
    if keys_pressed[pygame.K_s] and yellow_rect.y + VEL + yellow_rect.height <= HEIGHT:
        yellow_rect.y += VEL
    if keys_pressed[pygame.K_a] and yellow_rect.x - VEL >= 0:
        yellow_rect.x -= VEL
    if keys_pressed[pygame.K_d] and yellow_rect.x + VEL + yellow_rect.width <= BORDER.x:
        yellow_rect.x += VEL



def red_handle_movement(keys_pressed,red_rect):
    if keys_pressed[pygame.K_UP] and red_rect.y - VEL >= 0:
        red_rect.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red_rect.y + VEL + red_rect.height <= HEIGHT:
        red_rect.y += VEL
    if keys_pressed[pygame.K_LEFT] and red_rect.x - VEL >= BORDER.right:
        red_rect.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red_rect.x + red_rect.width + VEL <= WIDTH:
        red_rect.x += VEL



def move_bullets(yellow_bullets,red_bullets,yellow_rect,red_rect):
    for bullet in list(yellow_bullets):
        bullet.x += BULLET_VEL
        if red_rect.colliderect(bullet):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in list(red_bullets):
        bullet.x -= BULLET_VEL
        if yellow_rect.colliderect(bullet):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x < 0:
            red_bullets.remove(bullet)



    
def main():
    

    red_rect = RED_SPACESHIP.get_rect(topleft=(700,300))
    yellow_rect = YELLOW_SPACESHIP.get_rect(topleft=(100,300))
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow_rect.right,yellow_rect.centery -2,10,5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red_rect.left - 10,red_rect.centery -2,10,5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
        
        
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
        

        winner_text = None
        if red_health <= 0:
            winner_text = "YELLOW WINS!"

        if yellow_health <= 0:
            winner_text = "RED WINS!"


        if winner_text:
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed,yellow_rect)
        red_handle_movement(keys_pressed,red_rect)


        move_bullets(yellow_bullets,red_bullets,yellow_rect,red_rect)







        draw_screen(red_rect,yellow_rect,red_bullets,yellow_bullets,red_health,yellow_health)
        clock.tick(FPS)

    
    main()


if __name__ == "__main__":
    
    main()







