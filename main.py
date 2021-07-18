# Game ends if: 
# 1. Player successfully shoots all balloons (Player wins)
# 2. Balloon hits the player (Player loses)
# 3. Time over (Player loses)

import pygame
import os

#########################################################################
# initialization
pygame.init()

# screen dimensions
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

# screen title
pygame.display.set_caption("Nado Pang")

# FPS
clock = pygame.time.Clock()
###########################################################################

current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = os.path.join(current_path, 'images') # images 폴더 위치 반환

# loads background image
background = pygame.image.load(os.path.join(image_path, 'background.png'))

# creates the stage
stage = pygame.image.load(os.path.join(image_path, 'stage.png'))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해 사용

# creates a character
character = pygame.image.load(os.path.join(image_path, 'character.png'))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# character's moving direction
character_to_x = 0

# character speed
character_speed = 5

# creates the character's weapon
weapon = pygame.image.load(os.path.join(image_path, 'weapon.png'))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = [] # uses a list cuz multiple weapons can be shoot at once

# weapon speed
weapon_speed = 10

# creates balloons
ball_images = [
    pygame.image.load(os.path.join(image_path, 'balloon1.png')), 
    pygame.image.load(os.path.join(image_path, 'balloon2.png')), 
    pygame.image.load(os.path.join(image_path, 'balloon3.png')), 
    pygame.image.load(os.path.join(image_path, 'balloon4.png'))
]

# balloon speed (diff size of balloons have diff speed)
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3 에 해당하는 값

# stores balls in a list
balls = []

# creates the first balloon
balls.append({
    'pos_x': 50,
    'pos_y': 50, 
    'img_idx': 0, # starts off with the biggest balloon (ball's img idx)
    'to_x': 3,
    'to_y': -6,
    'init_spd_y': ball_speed_y[0]}) # initial speed of y 


# stores index of the weapon & ball to be removed later
weapon_to_remove = -1
ball_to_remove = -1

# declares text font
game_font = pygame.font.Font(None, 40)
total_time = 10
start_ticks = pygame.time.get_ticks() # starting time

# end game message on screen:
# TimeOut(시간 초과), Mission Complete(성공), Game Over(캐릭터 공에 맞음)
game_result = "Game Over"

running = True
while running:
    dt = clock.tick(30) # 게임화면의 초당 프레임 수를 설정, dt stands for delta

    # events (keyboard, mouse, etc.)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 

        # character's move
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: # 무기 발사
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # character's position
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # weapon's position
    weapons = [[w[0], w[1] - weapon_speed] for w in weapons] # weapon moves upward

    # weapon disappears if it hits screen
    weapons = [  [w[0], w[1]] for w in weapons if w[1] > 0  ]

    # balloon position
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # balloon bounces off the walls
        if ball_pos_x < 0 or ball_pos_x > (screen_width - ball_width):
            ball_val['to_x'] *= -1

        # balloon bounces off the stage(ground)
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val['to_y'] = ball_val['init_spd_y']
        else:
            ball_val['to_y'] += 0.5

        ball_val['pos_x'] += ball_val['to_x']
        ball_val['pos_y'] += ball_val['to_y']

    # update character rect
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val['pos_x']
        ball_pos_y = ball_val['pos_y']
        ball_img_idx = ball_val['img_idx']

        # update balloon rect
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_val['pos_x']
        ball_rect.top = ball_val['pos_y']

        # checks if the character and balloon collide
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # checks 
        for weapon_idx, weapon_val in enumerate(weapons): 
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]
        
            # update weapon rect
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # checks if the weapon and balloons collide
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # weapon to be disappeared
                ball_to_remove = ball_idx # ball to be disappeared

                # balloons become half its orginal size (unless they're alr the smallest)
                if ball_img_idx < 3:
                    # get ball size
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # smaller ball's info
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # smaller ball bouncing off to LEFT
                    balls.append({
                        'pos_x': ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        'pos_y': ball_pos_y + (ball_height / 2) - (small_ball_height / 2), 
                        'img_idx': ball_img_idx + 1, # starts off with the biggest balloon (공의 이미지 인덱스)
                        'to_x': -3,
                        'to_y': -6,
                        'init_spd_y': ball_speed_y[ball_img_idx + 1]}) # y 최초 속도  
                    
                    # smaller ball bouncing off to RIGHT
                    balls.append({
                        'pos_x': ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        'pos_y': ball_pos_y + (ball_height / 2) - (small_ball_height / 2), 
                        'img_idx': ball_img_idx + 1, # starts off with the biggest balloon (공의 이미지 인덱스)
                        'to_x': 3,
                        'to_y': -6,
                        'init_spd_y': ball_speed_y[ball_img_idx + 1]}) # y 최초 속도  
                    
                break
        else: 
            continue # for loop continues on and on
        break # double break's (only executed after the break from a previous for loop) 

    # delete balloons or weapons
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # game ends if there are no more balloons to shoot
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # display everything on screen 
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val['pos_x']
        ball_pos_y = val['pos_y']
        ball_img_idx = val['img_idx']
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    # calculates elapsed time
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render('Time : {}'.format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # game ends if game time exceeded
    if total_time - elapsed_time <= 0:
        game_result = 'Time Over'
        running = False
      
    pygame.display.update() # updates display screen

# game end message ('game over')
msg = game_font.render(game_result, True, (255, 255, 0)) # 노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update() # updates display screen


pygame.time.delay(2000) # prevents from screen being instantly close

# quits pygame
pygame.quit()