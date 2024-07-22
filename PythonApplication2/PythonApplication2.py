from ast import Pass
import sys
import pygame
from pygame.locals import *


BALL_XF, BALL_YF, BALL_VXF, BALL_VYF, BALL_R = 320., 240., 250., 250., 10
BAR1_XF, BAR1_YF, BAR1_VYF, BAR2_XF, BAR2_YF, BAR2_VYF = 50., 240., 0., 590., 240., 0
RESPORN_BALL_POINT_X, RESOPRN_BALL_POINT_Y = 320., 240.
POINT_BORDER_LINE1, POINT_BORDER_LINE2 = 20., 620.
BAR_COLLISION_X, BAR_COLLISION_Y, BAR_WEIGHT, BAR_HEIGHT, BAR_LINE_WEIGHT = 20, 50, 3, 100, 2
BORDER_LINE_UX, BORDER_LINE_UY, BORDER_LINE_DX, BORDER_LINE_DY, BORDER_LINE_WEIGHT = 20, 460, 620, 20, 2
SCORE_POS_1, SCORE_POS_2 = (250, 10), (450, 10)




White = pygame.Color('white')
Black = pygame.Color('black')



def ball_refrection(ball, ball_v, bar):
    p = ball + ball_v
    if ball_v.x > 0:
        if p.x < bar.x or ball.x >= bar.x: 
             return None
    else:
        if p.x > bar.x or ball.x <= bar.x:
            return None
    bar1 = bar.y + 100.
    ball_vec = ball_v.y/ball_v.x        #ŒX‚«
    ball_line = (bar.x - ball.x)*ball_vec + ball.y
    if bar.y <= ball_line <= bar1:
       
        d = pygame.Vector2(bar.x, ball_line)
        p -= d
        p.x = -p.x
        d += p
        return d
    return None

        
def ball_refrection_border(ball, ball_v):
    ball_vec = ball_v.x/ball_v.y
    p = ball + ball_v
    flag = 0
    if ball.y >= BORDER_LINE_UY and p.y >= BORDER_LINE_UY :
        ball_line_upper = (BORDER_LINE_UY - ball.y) * ball_vec + ball.x
        if BORDER_LINE_UX <= ball_line_upper <= BORDER_LINE_DX:
            d = pygame.Vector2(ball_line_upper, BORDER_LINE_UY)
            p -= d
            p.y = -p.y
            d += p
            return d
    if ball.y <= BORDER_LINE_DY and p.y <= BORDER_LINE_DY :
        ball_line_under = (BORDER_LINE_DY - ball.y) * ball_vec + ball.x
        if BORDER_LINE_UX <= ball_line_under <= BORDER_LINE_DX:
            d = pygame.Vector2(ball_line_under, BORDER_LINE_DY)
            p -= d
            p.y = -p.y
            d += p
            return d
    return None

def calc_ball(ball, ball_v, bar1, bar2, score_1, score_2):
#ƒ{[ƒ‹‚Ì‹““®

    collsion1 = ball_refrection(ball,ball_v,bar1)
    if collsion1 != None:
        ball = collsion1
        ball_v.x = -ball_v.x
    collsion2 = ball_refrection(ball,ball_v,bar2)
    if collsion2 != None:
        ball = collsion2
        ball_v.x = -ball_v.x
    collsion3 = ball_refrection_border(ball,ball_v)
    if collsion3 != None:
        ball = collsion3
        ball_v.y = -ball_v.y
    if collsion1 == None and collsion2 == None and collsion3 == None:
        ball += ball_v
   


    if ball.x < POINT_BORDER_LINE1:
        ball.xy = BALL_XF, BALL_YF 
        score_2 += 1
    elif ball.x > POINT_BORDER_LINE2:
        ball.xy = BALL_XF, BALL_YF
        score_1 += 1
    

    return ball, ball_v, score_1, score_2
            
def calc_player(bar1_y, bar1_dy):
    bar1_y += bar1_dy
    if bar1_y >= 460.: bar1_y = 460.
    elif bar1_y <= 10. : bar1_y = 10.
    return bar1_y
    
def calc_ai(bar2, ball):
    dy = ball.y - bar2.y
    if dy > 80: bar2.y += 20
    elif dy > 50: bar2.y += 15
    elif dy > 30: bar2.y += 12
    elif dy > 10: bar2.y += 8
    elif dy < -80: bar2.y -= 20
    elif dy < -50: bar2.y -= 15
    elif dy < -30: bar2.y -= 12
    elif dy < -10: bar2.y -= 8

    if bar2.y >= 420.: bar2.y = 420.
    elif bar2.y <= 10.: bar2.y = 10.
    return bar2.y


def calc_score(ball_x, score1, score2):
    if ball_x < 20:
        score2 += 1
    if ball_x >620:
        score1 += 1
    return score1, score2



def draw_game_over_screen(text1):
    screen_width = 640
    screen_height = 480
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont('arial', 40)
    title = font.render('Game Over', True, White)
    restart_button = font.render('R - Restart', True, White)
    quit_button = font.render('Q - Quit', True, White)
    result = font.render(text1, True,White)
    screen.blit(result, (screen_width/2 - result.get_width(), screen_height - 100))
    screen.blit(title, (screen_width/2 - title.get_width()/2, screen_height/2 - title.get_height()/3))
    screen.blit(restart_button, (screen_width/2 - restart_button.get_width()/2, screen_height/1.9 + restart_button.get_height()))
    screen.blit(quit_button, (screen_width/2 - quit_button.get_width()/2, screen_height/2 + quit_button.get_height()/2))
    pygame.display.update()            
            

pygame.init()
screen = pygame.display.set_mode((640, 480))
font = pygame.font.SysFont(None,40)
bar1_vec = pygame.Vector2(BAR1_XF, BAR1_YF)
bar1_v = BAR1_VYF
bar2_vec = pygame.Vector2(BAR2_XF, BAR2_YF)
bar2_v = BAR2_VYF
ball_vec = pygame.Vector2(BALL_XF, BALL_YF)
ballv_vec = pygame.Vector2(BALL_VXF,BALL_VYF)
clock=pygame.time.Clock()
time_passed = clock.tick(60)
time_sec = time_passed / 1000.0

ballv_vec.xy *= time_sec

score_1 = 0
score_2 = 0


text1 = 'You Win'
text2 = 'You Lose'

game_state = 'game'

while True:
        if game_state == 'game':
            screen.fill(Black)
            line_ux = pygame.draw.line(screen,White,(BORDER_LINE_DX,BORDER_LINE_DY),(BORDER_LINE_UX,BORDER_LINE_DY),BORDER_LINE_WEIGHT)
            line_dx = pygame.draw.line(screen,White,(BORDER_LINE_DX,BORDER_LINE_UY),(BORDER_LINE_UX,BORDER_LINE_UY),BORDER_LINE_WEIGHT)
            line_uy = pygame.draw.line(screen,White,(BORDER_LINE_DX,BORDER_LINE_UY),(BORDER_LINE_DX,BORDER_LINE_DY),BORDER_LINE_WEIGHT)
            line_dy = pygame.draw.line(screen,White,(BORDER_LINE_UX,BORDER_LINE_UY),(BORDER_LINE_UX,BORDER_LINE_DY),BORDER_LINE_WEIGHT)
            bar1 = pygame.draw.rect(screen,White,Rect(bar1_vec.x, bar1_vec.y, BAR_WEIGHT,BAR_HEIGHT),BAR_LINE_WEIGHT)
            bar2 = pygame.draw.rect(screen,White,Rect(bar2_vec.x, bar2_vec.y,BAR_WEIGHT,BAR_HEIGHT),BAR_LINE_WEIGHT)
            pygame.draw.rect(screen,White,Rect(ball_vec.x,ball_vec.y,BALL_R,BALL_R))
            screen.blit(font.render(str(score_1), True,White),SCORE_POS_1)
            screen.blit(font.render(str(score_2), True,White),SCORE_POS_2)

        for event in pygame.event.get():
            if event. type == QUIT:
                pygame.quit()
                sys. exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    bar1_v -= 10.
                elif event.key == K_DOWN:
                    bar1_v += 10.
            elif event.type == KEYUP:
                if event.key == K_UP:
                    bar1_v = 0.
                elif event.key == K_DOWN:
                    bar1_v = 0.



        bar1_vec.y = calc_player(bar1_vec.y,bar1_v)
        passtime = clock.tick(60)


        #score_1, score_2 = calc_score(ball_vec.x, score_1, score_2)
        bar2_vec.y = calc_ai(bar2_vec, ball_vec)
        ball_vec, ballv_vec, score_1, score_2 = calc_ball(ball_vec, ballv_vec, bar1_vec, bar2_vec, score_1, score_2)

        if score_1 == 5:
            draw_game_over_screen(text1)
            game_state = 'over'
        if score_2 == 5:
            draw_game_over_screen(text2)
            game_state = 'over'
        
        
       
        
        elif game_state == 'over':

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:
                bar1_vec.xy, bar1_v = (BAR1_XF, BAR1_YF), BAR1_VYF
                bar2_vec.xy, bar2_v = (BAR2_XF, BAR2_YF), BAR2_VYF
                ball_vec.xy = (BALL_XF, BALL_YF)
                score_1, score_2 = 0, 0

                game_state = 'game'
            if keys[pygame.K_q]:
                pygame.quit()
                quit()
                
        pygame.display.update()            