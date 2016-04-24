'''

Refactoring code to be more readable, organized, and efficient.
Add in pause
Add in turrent animation/rotation
'''
from tower import *
from projectiles import *
from creep import *
from button import *

import pygame

#Initialize for pygame...
pygame.font.init() #without this I can't use font class
clock =  pygame.time.Clock()

#CONSTANTS
BACGKROUND_COLOR = (255,255,255) #White
BACK_GROUND_IMAGE = pygame.image.load("Map2.png") #Load drawn image for level

#Main window game is stored in
GAMEWINDOW_WIDTH = 600
GAMEWINDOW_HEIGHT = 600

UI_RIGHT_PANEL = pygame.image.load("RightPanel.png")
MENU_IMAGE = pygame.image.load("button2.png")
MENU_WIDTH = 200
MENU_HEIGHT = 200

MENUSCREEN = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))

SCREEN = pygame.display.set_mode((GAMEWINDOW_WIDTH, GAMEWINDOW_HEIGHT))
#Frames per second, using in conjunction with pygame.clock.tick
FPS = 60

#Game variables
selected_object = None
game_running = True #is it?
gameover = False
pause = False
#Player variables
player_lives = 10
player_currency = 199
creepwave = 0

#Pathing
pathlist = []
path_Rect_attributes = [[40,0,40,200],[40,200,200,40],[240,200,40,200],[40,360,200,40],[40,400,40,200]]


#Creating sprite containers
selected_item_list = pygame.sprite.Group()
button_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
creep_list = pygame.sprite.OrderedUpdates() #This is so the list loops in order it was created
tower_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


def display_player_stats(SCREEN):
    font = pygame.font.SysFont("serif", 25)
    live_text = font.render("Lives: %s" % player_lives, True, (0,0,0))
    currency_text = font.render("$: %s" % player_currency, True, (0,0,0))

    SCREEN.blit(live_text, [475,0])
    SCREEN.blit(currency_text, [475, 50])

def tooltip(SCREEN, tower):
    font = pygame.font.SysFont("serif", 25)
    tooltip = tower.tooltip
    tooltip_text = font.render(tooltip, True, (0,0,0))

    SCREEN.blit(tooltip_text, [475,450])


def check_cursor_collision(position):
    #Creating a Rect that is 20width by 20height (Same as tower width height
    mouserect = pygame.Rect(position[0], position[1], 20, 20)
    mouserect.center = position

    for path in pathlist:
        if path.colliderect(mouserect):
            return False
    for tower in tower_list:
        if tower.rect.colliderect(mouserect):
            return False
    return True

def valid_build(position):
    for path in pathlist:
        if path.collidepoint(position):
            return False
    for tower in tower_list:
        if tower.rect.collidepoint(position):
            return False
        else:
            return True
    return True

#Create buttons
but = Button(500,150,"BasicCannon.png", True)
send_creep_button = Button(480,500,"UI_Send_Creep_Button.png", False)
button_list.add(but, send_creep_button)
all_sprites_list.add(but,send_creep_button)

def spawn_creep(hp):
    for n in range(0, -600, -40):
        c = Creep((50,n),hp+1)
        creep_list.add(c)
        all_sprites_list.add(c)

for n in path_Rect_attributes:
    #Loop through predefined attributes to create path
    #Create a Rect object with the attributes and add them into a list we can loop to check for collision
    a = pygame.Rect(n[0], n[1], n[2], n[3])
    pathlist.append(a)

#Main game loop
while game_running == True:
    for event in pygame.event.get():
        #Mouse position variable...
        current_mouse_pos = pygame.mouse.get_pos()

        #If user clicks the X in window
        if event.type == pygame.QUIT:
            game_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if pause == False:
                    pause = True
                else:
                    pause = False


        #Handling User Input
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #event.button 1, Left : 2, Middle : 3, Right
            #If user left clicks....(event.button 1
            if pause == False:
                if event.button == 1:
                    #If user has an item selected...
                    if selected_item_list:
                        #If cursor collides with Rect or sprites
                        if check_cursor_collision(current_mouse_pos):
                            for item in selected_item_list:
                                cost = item.cost
                                type = item.towertype
                                item.kill()
                            if player_currency >= cost:
                                player_currency -= cost
                                tower = Tower(event.pos[0],event.pos[1], type)
                                tower_list.add(tower)
                                all_sprites_list.add(tower)

                    for button in button_list:
                        #Left click -> on button
                        if button.tower:
                            if button.rect.collidepoint(current_mouse_pos):
                                #Button clicked...because collision on left click
                                tower = Tower(current_mouse_pos[0], current_mouse_pos[1], button.build)
                                selected_item_list.add(tower)
                                all_sprites_list.add(tower)


    if pause == False:
    #Updates cursor sprite to current position of mouse
        for item in selected_item_list:
            item.rect.center = current_mouse_pos

        for tower in tower_list:
            if tower.can_shoot():
                for creep in creep_list:
                    #If creep in range...
                    if tower.detect_target(creep):
                        #Create bullet sprite
                        bullet = Bullet(tower.rect.center, creep.rect.center)
                        bullet_list.add(bullet)
                        all_sprites_list.add(bullet)
                        #Make bullet move to target
                        tower.shoot()
                        #Need break so tower doesn't shoot at all creep in range simultaneously
                        break


        #Creep functions
        for creep in creep_list:
            #If creep is dead...
            if creep.hp <= 0:
                #Add reward to player currency
                player_currency += creep.reward
                #Remove sprite...
                creep_list.remove(creep)
                all_sprites_list.remove(creep)
            #if creep reaches exit, boolean value
            elif creep.exit:
                #Remove life and creep
                player_lives -= 1
                creep.kill()
                #Check if player loses
                if player_lives <= 0:
                    gameover = True
            for bullet in bullet_list:
                #If bullet hits creeps sprite
                if pygame.sprite.collide_rect(creep, bullet):
                    creep.hp -= bullet.damage
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)


        #Bullet functions
        for bullet in bullet_list:
            #if bullet stops....
            if bullet.bullet_stopped():
                #Remove it...
                bullet_list.remove(bullet)
                all_sprites_list.remove(bullet)

        #Button functions
        for button in button_list:
            #If cursor collides with button...
            if button.rect.collidepoint(current_mouse_pos):
                #Toggle hover image using a boolean
                pass


        if not creep_list:
            spawn_creep(1)


        SCREEN.fill((100,100,100))
        SCREEN.blit(BACK_GROUND_IMAGE,(0,0))
        SCREEN.blit(UI_RIGHT_PANEL,(450,0))
        all_sprites_list.update()
        all_sprites_list.draw(SCREEN)


    #Not sure if I can put this somewhere else, I may just have hover and draw options here for selected items or make a new class called selected items...
        display_player_stats(SCREEN)

        for button in button_list:
            if button.rect.collidepoint(current_mouse_pos) and button.tower:
                pass

        for item in selected_item_list:
            if check_cursor_collision(item.rect.center):
                #print " Valid"
                pygame.draw.circle(SCREEN,(0,255,0), item.rect.center, item.range, 3)
            else:
                #print "Not valid"
                pygame.draw.circle(SCREEN,(255,0,0), item.rect.center, item.range, 3)

        for tower in tower_list:
            #Show tower range when mouse hovering and no selected item
            if tower.rect.collidepoint(current_mouse_pos) and not selected_item_list:
                tower.tower_selected(SCREEN)
                tower.draw_tower_range(SCREEN)





    clock.tick(FPS)
    pygame.display.flip()