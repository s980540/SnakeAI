import pygame
import random
import numpy as np
import pandas as pd

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 800
dis_height = 800

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game with AI')

clock = pygame.time.Clock()
snake_block = 40
snake_speed = 15
# snake_speed = 2

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Directions dictionary
directions = {
    0: [-snake_block, 0],  # left
    1: [snake_block, 0],   # right
    2: [0, -snake_block],  # up
    3: [0, snake_block]    # down
}

# List to store data
data = []

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

def your_score(count, score):
    value = score_font.render("Count: " + str(count) + ", Your Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def record_data(snake_Head, foodx, foody, action):
    state = [snake_Head[0], snake_Head[1], foodx, foody]
    data.append(state + [action])

def ai_move(snake_Head, foodx, foody, x1_change, y1_change):
    if snake_Head[0] < foodx:
        x1_change = snake_block
        y1_change = 0
    elif snake_Head[0] > foodx:
        x1_change = -snake_block
        y1_change = 0
    elif snake_Head[1] < foody:
        y1_change = snake_block
        x1_change = 0
    elif snake_Head[1] > foody:
        y1_change = -snake_block
        x1_change = 0
    return x1_change, y1_change

def gameLoop(game_count):
    game_close = False
    game_over = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    direction = 1  # start moving right

    while not game_close:

        while game_over:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            your_score(game_count, Length_of_snake - 1)
            pygame.display.update()
            print(f"Count: {game_count}, Score: {Length_of_snake - 1}")

            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_q:
            #             game_close = True
            #             game_over = False
            #         if event.key == pygame.K_c:
            #             gameLoop()
            # gameLoop()
            return False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # game_close = True
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    # game_close = True
                    return True

        # Change direction randomly every frame
        # direction = random.choice([0, 1, 2, 3])
        x1_change, y1_change = ai_move([x1, y1], foodx, foody, x1_change, y1_change)

        # # Change direction based on the current direction
        # if direction == 0:  # left
        #     x1_change = -snake_block
        #     y1_change = 0
        # elif direction == 1:  # right
        #     x1_change = snake_block
        #     y1_change = 0
        # elif direction == 2:  # up
        #     y1_change = -snake_block
        #     x1_change = 0
        # elif direction == 3:  # down
        #     y1_change = snake_block
        #     x1_change = 0

        record_data([x1, y1], foodx, foody, direction)

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_over = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(white)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over = True

        our_snake(snake_block, snake_List)
        your_score(game_count, Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        clock.tick(snake_speed)

    # pygame.quit()

    # Save data to CSV
    df = pd.DataFrame(data, columns=['snake_x', 'snake_y', 'food_x', 'food_y', 'action'])
    df.to_csv('snake_data.csv', index=False)

    # quit()
    return False

# Main loop to keep collecting data until 'Q' is pressed
def main():
    game_count = 0
    # while True:
    #     gameLoop()
    #     # Check for 'Q' key press to quit
    #     for event in pygame.event.get():
    #         if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
    #             # Save data to CSV
    #             df = pd.DataFrame(data, columns=['snake_x', 'snake_y', 'food_x', 'food_y', 'action'])
    #             df.to_csv('snake_data.csv', index=False)
    #             pygame.quit()
    #             quit()
    game_close = False
    while not game_close:
        game_count += 1
        game_close = gameLoop(game_count)

    pygame.quit()
    quit()

main()
