"""Author: Rixin Yang
   Date: May 1, 2018
   Description: Creates a module used for the game "Super Break-Out."
"""

#Import needed module
import pygame, random

class Ball(pygame.sprite.Sprite):
    '''This class defines the sprite the Ball.'''
    
    def __init__(self, screen, bounce, drop):
        '''This initializer takes a screen surface, and two sounds as 
        parameters. Initializes the image, rect attributes, sounds, and x,y 
        direction of the ball.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Set the data attributes for the Ball
        self.image = pygame.image.load("ball.png")
        self.__bounce = bounce
        self.__drop = drop
        self.rect = self.image.get_rect()
        self.rect.center = (screen.get_width()/2,screen.get_height()/2)
 
        # Instance variables to keep track of the screen surface
        # and set the initial x and y vector for the ball.
        self.__screen = screen
        self.__dx = 0
        self.__dy = -2
 
    def change_direction(self, sprite, player = 0):
        '''This method accepts an sprite object that is hit, and a boolean 
        value defaulted as 0 as parameters to see what is the cause of the
        change in direction. If not caused by player, reverse y direction 
        appropriately the to randomized y vector depending on vertical part hit.
        Otherwise, if caused by player, change the y direction up only and 
        play the bounce sound. The x vector will also be changed depending on 
        which horizontal part of the sprite is hit. left, right, or center.'''
        
        #Randomize direction vector.
        random_dx = random.randrange(5,7)
        random_dy = random.randrange(7,10) 
        
        #Change x direction appropriately depending on hit. 
        #If hit close to corners (1/4 end), change direction to the corner's 
        #direction
        if self.rect.centerx >= (sprite.rect.centerx+(1.0/4.0*sprite.rect.width)):
            self.__dx = random_dx
        elif self.rect.centerx < (sprite.rect.centerx-(1.0/4.0*sprite.rect.width)):
            self.__dx = -random_dx
        #If hit is near center, continue the x direction as usual 
        else:
            if self.__dx >= 0:
                self.__dx = random_dx
            elif self.__dx < 0 :
                self.__dx = -random_dx        

        #If bounce not caused by player change y appropriately to 
        #the random y vector 
        if not player:
            if self.rect.centery > sprite.rect.centery:
                self.__dy = -random_dy
            elif self.rect.centery < sprite.rect.centery:
                self.__dy = random_dy
        #If changed by player, bounce only up with appropriate random x vector 
        else:                   
            self.__dy = random_dy
        
        #Play the bounce sound effect after direction change
        self.__bounce.play()
            
    def reset(self):
        '''This method resets the ball position to the middle of the screen.
        and set its speed vectors to a reset ball speed. After, play the drop 
        sound to indicate a life loss.'''
        
        #Reset position
        self.rect.center = (self.__screen.get_width()/2,\
                            self.__screen.get_height()/2+75)
        
        #Reset speed
        self.__dx = 0
        self.__dy = -2
        
        #Play drop sound effect
        self.__drop.play()
        
             
    def update(self):
        '''This method will be called automatically to reposition the
        ball sprite on the screen.'''
        
        # Check if we have reached the left or right end of the screen where
        # the wall sprites are.
        # If not, then keep moving the ball in the same x direction.
        if ((self.rect.left > 5) and (self.__dx <= 0)) or\
           ((self.rect.right < self.__screen.get_width()-5) and\
            (self.__dx >= 0)):
            self.rect.left += self.__dx
        # If yes, then reverse the x direction and play bounce for change. 
        else:
            self.__dx = -self.__dx
            self.__bounce.play()
             
        # Check if we have reached the top of the wall sprite or bottom.
        # If not, then keep moving the ball in the same y direction.
        if not ((self.rect.top <= 56) and (self.__dy > 0)):
            self.rect.top -= self.__dy
        # If yes, then reverse the y direction and play bounce for change. 
        else:
            self.__dy = -self.__dy
            self.__bounce.play()

class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for Player 1 and Player 2 if appropriate'''
    
    def __init__(self, screen, player_num):
        '''This initializer takes a screen surface, and player number as
        parameters. Depending on the player number it loads the appropriate
        image and positions it on the bottom of the screen.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Define player number and sound as instance variable
        self.__player_num = player_num
         
        # Define the image and rect attributes.
        self.image = pygame.image.load("paddle"+str(player_num)+".png")
        self.rect = self.image.get_rect()
 
        # If we are initializing a sprite for player 1, 
        # position it 45 pixels from bottom.
        if player_num == 1:
            self.rect.top = screen.get_height()-self.rect.height-45
        # Otherwise, position it 10 pixels from the bottom of the screen.
        else:
            self.rect.top = screen.get_height()-self.rect.height-10
 
        # Center the player vertically in the window and set paddle stationary.
        self.rect.left = screen.get_height()/2 + 50
        self.__screen = screen
        self.__dx = 0
      
    def change_direction(self, xy_change):
        '''This method takes a (x,y) tuple as a parameter, extracts the 
        y element from it, and uses this to set the players x direction.'''
        
        self.__dx = xy_change[0]*10
        
    def half_mode(self):
        '''This method makes the player 2x smaller in width to increase 
        difficulty after half of the bricks has been destroyed.'''
        
        #Create temp center coord before changing image rect.
        temp_center = self.rect.center
        #Change image rect
        self.image = pygame.image.load("paddle"+str(self.__player_num)+\
                                       "_short.png")
        #Reset hitbox and coordinate
        self.rect = self.image.get_rect()
        self.rect.center = temp_center
         
    def update(self):
        '''This method will be called automatically to reposition the
        player sprite on the screen.'''
        
        # Check if we have reached the left or right of the wall sprites.
        # If not, then keep moving the player in the same x direction.
        if ((self.rect.left > 5) and (self.__dx < 0)) or\
           ((self.rect.right < self.__screen.get_width()-5) and\
            (self.__dx > 0)):
            self.rect.left += self.__dx
        # If yes, then we don't change the x position of the player at all.


class End_zone(pygame.sprite.Sprite):
    '''This class defines the sprite for our left and right end zones'''
    
    def __init__(self, screen, y_position):
        '''This initializer takes a screen surface, and y position  as
        parameters. This will be used to set the EndZone for the game. This
        EndZone will be at the bottom of the screen.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Our endzone sprite will be a 1 pixel high black line.
        self.image = pygame.Surface((screen.get_width(), 1))
        self.image = self.image.convert()
        self.image.fill((0, 0, 0))
         
        # Set the rect attributes for the endzone
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = y_position

class Score_keeper(pygame.sprite.Sprite):
    '''This class defines a label sprite to display the score and lives.'''
    
    def __init__(self):
        '''This initializer loads the custom font "LemonMilkbold", and
        sets the starting score to 0 and lives to 3.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Load our custom font, and initialize the starting score and lives.
        self.__font = pygame.font.Font("LemonMilkbold.otf", 25)
        self.__score = 0
        self.__life = 3
        self.__goal = 9**9
         
    def scored(self, score):
        '''This method accpets one parameter for score and adds the 
        score for the players'''
        
        self.__score += score
 
    def lose_life(self):
        '''This method decrease the lives remaining for players'''
        
        self.__life -= 1
     
    def winner(self):
        '''The game is over when player reaches total points.
        This method returns 0 if the game is not over yet, 1 if players has
        won, or 2 if players lose all lives.'''
        
        if self.__score == self.__goal:
            return 1
        elif self.__life == 0:
            return 2
        else:
            return 0   
    
    def get_life(self):
        '''This method return number of lives left.'''
        
        return self.__life
    
    def set_goal(self, score):
        '''This method set the total score needed to win the game to determine 
        when the game is over.'''
        
        self.__goal = score
 
    def update(self):
        '''This method will be called automatically to display 
        the current score and lives at the top of the game window.'''
        
        #Set message, image and rect properties.
        message = "Score:  %d            Lives:  %d" %\
            (self.__score, self.__life)
        self.image = self.__font.render(message, 1, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (300, 20)
        
class Life(pygame.sprite.Sprite):
    '''This class defines a sprite to display lives in a image.'''
    
    def __init__(self, life_num):
        '''This initializer accepts the life image's position and loads the 
        image for a life and set it's rect properties appropriately to its 
        position number.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.image.load("life.png")
        self.rect = self.image.get_rect()
        self.rect.center = (475+life_num*25, 20)
 
    def lose_life(self):
        '''This method swtich image to empty heart image to indicate a loss of
        life.'''
        
        self.image = pygame.image.load("empty_life.png")  
        
class Brick(pygame.sprite.Sprite):
    '''Bricks class inherits from the Sprite class, used for hitting in game.'''
    
    def __init__(self, x_position, y_position, file_name, score):
        '''This initializer accepts  x and y positions, file name and the score 
        of the brick as parameters. loads the image for the brick with its 
        file_name parameter and set it's rect properties with xy pos parameters
        The score parameter is used to set the score yield when the brick is 
        destroyed.'''        
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the image, rect and other attributes for the bricks
        self.__score = score
        self.image = pygame.image.load(file_name)
        self.rect = self.image.get_rect()
        self.rect.top = y_position 
        self.rect.left = x_position
    
    def get_score(self):
        '''This method returns the score value of the brick.'''
        
        return self.__score
    
    def move_down(self):
        '''This method moves down the sprite vertically by 1 pixel.'''
        
        self.rect.top += 1
         
        

    
    
