import numpy as np
import pygame
import random


pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800 , 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BRUH=(0, 255, 255)
BLUE = (0,0,255)
GREEN = (0,255,0)
# # Game variables
# FPS = 60
# clock = pygame.time.Clock()
# score = 0

# # Create the screen
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Catch the Falling Object")

action_dic = {
    0:"left",
    1:"stay",
    2:"right",
}
class Player:
    def __init__(self):
        self.width = 100
        self.height = 20
        self.x = random.randint(0, (SCREEN_WIDTH - self.width-1)) # (SCREEN_WIDTH - self.width) // 2
        self.y = SCREEN_HEIGHT - self.height - 10
        self.speed = 35
        self.score = 0
        self.speed_increment = 0.05
        self.bruh_move = False
        self.doing_good = True
 

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed
            self.bruh_move = False
        else: 
            self.bruh_move = True

    def move_right(self):
        if self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
            self.bruh_move = False
        else: 
            self.bruh_move = True

    def set_score(self, new_score):
        # if new_score > self.score:
        #     self.speed +=  0.05
        # else:
        #     self.speed -=  0.05

        self.score = new_score

    def draw(self,screen):
        
        if self.doing_good:
            pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
            

class FallingObject:
    def __init__(self   ) :
        
        
        self.width = 50
        self.height = 50
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        self.speed = 30
        self.speed_increment = 0.05

    def move(self):
        self.y += self.speed

    def reset(self, is_on_flor=False):
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height
        # if is_on_flor:
        #     self.speed -= self.speed * 0.5
        # else:
        #     self.speed += self.speed * 0.5

    def draw(self,screen):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height)) 
        # pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width*0.5, self.height*0.5)) 




class Game:

    def __init__(self, *args, **kwargs):
        self.player:Player = None;
        self.falling_object:FallingObject = None;
        self.score:int = None;
        self.game_over:int = None;
        self.max_iteration:int = None;
        self.move_source = ""
        self.reset()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Catch the Falling Object")
        self.FPS = 60
        
        self.clock = pygame.time.Clock()
        self.width_sum =  self.falling_object.width // 2 + self.player.width // 2
        
    def reset(self):
        self.score = 0
        self.player = Player()
        self.falling_object = FallingObject()
        self.game_over = False
        self.max_iteration = 10


    def get_differs(self):
        player_senter = self.player.x + self.player.width // 2
        falling_object_senter = self.falling_object.x + self.falling_object.width // 2
        
        return player_senter - falling_object_senter 

    def play_step(self, action):
        # Handle user input events (e.g., quit game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Store old player and falling object positions
        self.old_player_center = self.player.x + self.player.width // 2
        self.old_falling_object_center = self.falling_object.x + self.falling_object.width // 2

        # Perform player movement based on the action
        self._move(action)

        # Calculate new player and falling object positions
        self.new_player_center = self.player.x + self.player.width // 2
        self.new_falling_object_center = self.falling_object.x + self.falling_object.width // 2

        # Calculate the change in distance (reward calculation)
        self.old_distance = abs(self.old_player_center - self.old_falling_object_center)
        self.new_distance = abs(self.new_player_center - self.new_falling_object_center)


        # is inside ? 



        if self.new_distance < self.old_distance:
            self.reward = 1.0  # no reward and no parchment for getting closer
            self.player.doing_good = True
        else:
            self.player.doing_good = False
            self.reward = -1.0  # parchment for moving away or not improving

        if abs(self.get_differs()) < self.width_sum: # is_inside
            self.reward = 2.0  # reward for get 
            self.player.doing_good = True

        # Update game UI, clock tick, etc.
        self._update_ui()
        self.clock.tick(self.FPS)

        # Determine if the game is over (e.g., based on player's state)

        # Return reward, game over flag, and current score
        return self.reward, self.game_over, self.player.score

    def _update_ui(self):
        self.screen.fill(BLACK)

        self.falling_object.draw(self.screen)
        self.player.draw(self.screen)
        

        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.player.score}", True, WHITE)
        self.screen.blit(text, (10, 10))
        
        text = font.render(f"reword: {self.reward:.5f}", True, WHITE)
        self.screen.blit(text, (10, 40))
        
        text = font.render(f"The action is [{action_dic[self.the_move]}]", True, WHITE)
        self.screen.blit(text, (10, 70))
        
        
        text = font.render(f"player speed : {self.player.speed:.3f}", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH - text.get_size()[0] - 20, 10))
        
        text = font.render(f"move source : {self.move_source}", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH - text.get_size()[0] - 20, 70))
        
        text = font.render(
            f"object speed : {self.falling_object.speed:.3f}", True, WHITE
        )
        self.screen.blit(text, (SCREEN_WIDTH - text.get_size()[0] - 20, 40))
        
        pygame.display.flip()


    def _move(self, __action):
        action =  np.argmax(__action)
        self.the_move = action
        if action == 0 :
            self.player.move_left()
        elif action == 2  :
            self.player.move_right()

        self.falling_object.move()
        
        if self.falling_object.y > SCREEN_HEIGHT:
            self.falling_object.reset(is_on_flor=True)
            self.player.set_score(self.player.score - 1)
            self.falling_object.speed += self.falling_object.speed_increment
            self.max_iteration -= 1 
        elif (
            self.falling_object.y + self.falling_object.height > self.player.y
            and self.falling_object.x + self.falling_object.width > self.player.x
            and self.falling_object.x < self.player.x + self.player.width
        ):
            self.falling_object.reset(is_on_flor=False)
            self.player.set_score(self.player.score + 1)
            self.falling_object.speed += self.falling_object.speed_increment
            self.max_iteration -= 1
        self.game_over = (self.falling_object.speed >= SCREEN_HEIGHT) | (abs( self.falling_object.speed ) <  0.1) # | (abs(self.score) == 10 ) | (self.max_iteration == 0 ) 



    
def main():
    
    # Initialize Pygame
    pygame.init()

    # Screen dimensions
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # Game variables
    FPS = 60
    clock = pygame.time.Clock()
    score = 0

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Catch the Falling Object")



    # Create player and falling object instances
    player = Player()
    falling_object = FallingObject()

# Main game loop
    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()

        falling_object.move()
        if falling_object.y > SCREEN_HEIGHT:
            falling_object.reset(is_on_flor=True)
            player.set_score(player.score - 1)
            falling_object.speed += falling_object.speed_increment

        if (
            falling_object.y + falling_object.height > player.y
            and falling_object.x + falling_object.width > player.x
            and falling_object.x < player.x + player.width
        ):
            falling_object.reset(is_on_flor=False)
            player.set_score(player.score + 1)
            falling_object.speed += falling_object.speed_increment

        player.draw()
        falling_object.draw()

        # Display player.score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {player.score}", True, WHITE)
        screen.blit(text, (10, 10))
        text = font.render(f"player speed : {player.speed:.3f}", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - text.get_size()[0] - 20, 10))
        text = font.render(f"object speed : {falling_object.speed:.3f}", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - text.get_size()[0] - 20, 40))
        text = font.render(f"player speed : {player.score}", True, WHITE)
        if falling_object.speed >= SCREEN_HEIGHT:
            font = pygame.font.Font(None, 72)
            text = font.render("You Win!", True, WHITE)
            screen.blit(
                text,
                (
                    SCREEN_WIDTH // 2 - text.get_width() // 2,
                    SCREEN_HEIGHT // 2 - text.get_height() // 2,
                ),
            )
            pygame.display.flip()
            pygame.time.delay(2000)
            running = False
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
