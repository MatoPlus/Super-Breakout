"""Author: Rixin Yang
   Date: May 1, 2018
   Description: Creates a game of break-out using the breakSprites and pygame 
   modules. Player 1 uses arrow keys and Player 2 uses joystick. Note that 
   player 2 will be created if joystick is detected. 
"""

# I - IMPORT AND INITIALIZE
import pygame, breakSprites
#pre_init reduces sound delay
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()
     
def main():
    '''This function defines the 'mainline logic' for the break-out game.'''
      
    # DISPLAY - set display resolution and caption.
    screen = pygame.display.set_mode((640, 480))    
    pygame.display.set_caption("Super Break-Out!")
     
    # ENTITIES - create background and gameover label.
    background = pygame.image.load("background.png").convert()
    screen.blit(background, (0, 0))
    overLabel = pygame.font.Font("LemonMilkbold.otf", 30).render("GAME OVER",\
                                                            1, (255, 255, 255))    
    
    # Create a list of Joystick objects.
    joysticks = []
    for joystick_no in range(pygame.joystick.get_count()):
        stick = pygame.joystick.Joystick(joystick_no)
        stick.init()
        joysticks.append(stick)  
        
    #Sound - loading and setting volume
    pygame.mixer.music.load("background.ogg")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    drop = pygame.mixer.Sound("drop.ogg")
    drop.set_volume(0.1)
    bounce = pygame.mixer.Sound("bounce.ogg")
    bounce.set_volume(0.2)
    half_way = pygame.mixer.Sound("half_way.ogg")
    half_way.set_volume(0.5)
    
    #Sprites for bricks - create 6 rows of 18 col bricks, with different image
    #each row.
    bricks = []
    colours = ["blue", "green", "orange", "yellow", "red", "violet"]
    y_pos = 200
    goal = 0 
    half_bricks = 6*18/2
    for row in range(6):
        y_pos -= 18
        x_pos = 5
        for col in range(18):
            goal += (row+1)
            bricks.append(breakSprites.Brick(x_pos, y_pos, \
                                             colours[row]+"_pad.png", row+1))
            x_pos += 35
    #Group up brick sprites
    brick_sprites = pygame.sprite.Group(bricks)
            
    #Life sprites creation, 3 lifes, append them in a list.
    lifes = []
    for life in range(1,4):
        lifes.append(breakSprites.Life(life))
        
    #Player sprite creation, append them in a list.
    players = []
    player1 = breakSprites.Player(screen, 1)
    players.append(player1)
    
    #Check to see if there should be a creation of a second player.
    if joysticks != []:
        player2 = breakSprites.Player(screen, 2)
        players.append(player2)
    
    # Sprites for: ScoreKeeper label, End Zone, and Ball
    score_keeper = breakSprites.Score_keeper()
    ball = breakSprites.Ball(screen, bounce, drop)
    endzone = breakSprites.End_zone(screen, screen.get_height())
    sprites = [score_keeper, endzone, ball]
    
    #All sprites groups up
    all_sprites = pygame.sprite.Group(sprites, bricks, lifes, players)

    # ASSIGN - assign important variables to start game.
    clock = pygame.time.Clock()
    keepGoing = True
    score_keeper.set_goal(goal)
    half_mode = False
     
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # LOOP
    while keepGoing:
     
        # TIME
        clock.tick(30)
     
        # EVENT HANDLING: p1 use arrow keys and p2 can use joystick 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False
            if event.type == pygame.JOYHATMOTION:
                player2.change_direction(event.value)
                
            #Get a list containing boolean values of pressed keys to their
            #position.
            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[pygame.K_LEFT]:
                player1.change_direction((-1, 0))
            if keys_pressed[pygame.K_RIGHT]:
                player1.change_direction((1, 0))
            if keys_pressed[pygame.K_ESCAPE]:
                keepGoing = False
            if not keys_pressed[pygame.K_LEFT] and\
               not keys_pressed[pygame.K_RIGHT]:
                player1.change_direction((0,0))
 
        # Check if ball goes to the endzone - lose life and reset ball
        if ball.rect.colliderect(endzone):
            score_keeper.lose_life()
            lifes[score_keeper.get_life()].lose_life() 
            if score_keeper.get_life() != 0:
                ball.reset()
        
        #Check if ball hits brick, make them disappear.
        hit_bricks = pygame.sprite.spritecollide(ball, brick_sprites, False)
        #for each brick hit, give the points appropriate and move all bricks 
        #down
        for hit_brick in hit_bricks:
            score_keeper.scored(hit_brick.get_score())
            ball.change_direction(hit_brick)
            hit_brick.kill()
            for brick in bricks:
                brick.move_down()
        
        #Check if time for half difficulty mode
        if len(brick_sprites) <= half_bricks and half_mode == False:
            #Enable half mode for all players.
            for player in players:
                player.half_mode()
            half_way.play()
            half_mode = True
            
        # Check if ball hits Players. Return the hit player in a list.
        hit_player = pygame.sprite.spritecollide(ball, players, False)
        if hit_player:
            #If ball hits the hit player above half of its center y, 
            #Change ball direction upwards left or right varies on position hit.
            if ball.rect.centery < hit_player[0].rect.centery:
                ball.change_direction(hit_player[0], 1)       
           
        # Check for game over (if a player gets all points or no more lives)
        check = score_keeper.winner()
        
        #Change game over screen and exit loop if appropriate
        if check:
            if check == 1:
                result = "WIN"
            else:
                result = "LOSE"
                drop.play()
            overLabel = pygame.font.Font("LemonMilkbold.otf", 30).render(\
                "GAME OVER: YOU %s" %result , 1, (255, 255, 255))
            keepGoing = False
                         
        # REFRESH SCREEN - clear previous sprites, update positions and display
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()
             
    # Unhide the mouse pointer - before closing window
    pygame.mouse.set_visible(True)
 
    # blit and flip game over screen after game is over
    screen.blit(overLabel, \
                (screen.get_width()/2-(overLabel.get_rect().width/2),\
                 screen.get_height()/2-(overLabel.get_rect().height/2)))
    pygame.display.flip()
    
    #Quit the game with delay to hear music fade
    pygame.mixer.music.fadeout(1000)
    pygame.time.delay(1000)
    pygame.quit()     
     
# Call the main function
main()    