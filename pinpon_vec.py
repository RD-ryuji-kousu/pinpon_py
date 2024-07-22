from ast import Pass
from pickle import INT
import sys
import pygame
import math
import time
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



def ball_refrection(ball, ball_v, bar, rally, ball_a, ballV0):
#ボールとバーの反射
    p = ball + ball_v
    if ball_v.x > 0:        #バーにX軸が接触しない場合を除外
        if p.x < bar.x or ball.x >= bar.x: 
             return None
    else:
        if p.x > bar.x or ball.x <= bar.x:
            return None
    bar1 = bar.y + 33.5
    bar2 = bar.y + 66.5
    bar3 = bar.y + 100
    ball_vec = ball_v.y/ball_v.x        
    ball_line = (bar.x - ball.x)*ball_vec + ball.y      #バーとの交点を求める
    if bar.y <= ball_line <= bar1:
        if ball_v.y > 0:
            ball_v.y = -ball_v.y
            ball_v.x = -ball_v.x
        elif ball_v.y < 0:
            ball_v.y = 0
            ball_v.x = -(ball_v.x * math.sqrt(2))
        elif ball_v.y == 0:
            ball_v.x = -(ball_v.x /math.sqrt(2))
            ball_v.y = -ball_v.x
        d = pygame.Vector2(bar.x, ball_line)            #本来突き抜ける距離を基に、反射後の位置を求める
        p -= d
        p.x = -p.x
        d += p
        rally+=1
        if rally % 10 == 0 and rally >= 10:
            ball_v = ballV0 * (1.0 + ball_a/10)
            ball_a+=1
        return d, ball_v, rally, ball_a
    elif bar1 < ball_line <= bar2:
        p = ball + ball_v
        d = pygame.Vector2(bar.x, ball_line)            #本来突き抜ける距離を基に、反射後の位置を求める
        p -= d
        p.x = -p.x
        d += p
        ball_v.x = -ball_v.x
        rally+=1
        if rally % 10 == 0 and rally >= 10:
            ball_v = ballV0 * (1.0 + ball_a/10)
            ball_a+=1
        return d, ball_v, rally, ball_a
    elif bar2 < ball_line <= bar3:
        
        if(ball_v.y < 0):
            ball_v.y = -ball_v.y
            ball_v.x = -ball_v.x
        elif(ball_v.y > 0):
            ball_v.y = 0
            ball_v.x = -(ball_v.x * math.sqrt(2))
        elif ball_v.y == 0:
            ball_v.x = -(ball_v.x /math.sqrt(2))
            ball_v.y = ball_v.x
            if ball_v.y < 0:
                ball_v.y = -ball_v.y
        d = pygame.Vector2(bar.x, ball_line)            #本来突き抜ける距離を基に、反射後の位置を求める
        p -= d
        p.x = -p.x
        d += p
        rally += 1
        if rally % 10 == 0 and rally >= 10:
            ball_v = ballV0 * (1.0 + ball_a/10)
            ball_a+=1
        return d, ball_v, rally, ball_a
    return None

        
def ball_refrection_border(ball, ball_v):
#上下のラインとボールの反射
    if ball_v.y == 0:       #ボールが平行移動している場合はのぞく
        return None
    ball_vec = ball_v.x/ball_v.y
    p = ball + ball_v
    if ball.y >= BORDER_LINE_UY and p.y >= BORDER_LINE_UY :         #上のラインとボールが接触しているかどうか
        ball_line_upper = (BORDER_LINE_UY - ball.y) * ball_vec + ball.x
        if BORDER_LINE_UX <= ball_line_upper <= BORDER_LINE_DX:    
            d = pygame.Vector2(ball_line_upper, BORDER_LINE_UY)     #突き抜けた量を基に反射後の位置を決める
            p -= d
            p.y = -p.y
            d += p
            return d
    if ball.y <= BORDER_LINE_DY and p.y <= BORDER_LINE_DY :         #下のライスとボールが接触しているかどうか
        ball_line_under = (BORDER_LINE_DY - ball.y) * ball_vec + ball.x
        if BORDER_LINE_UX <= ball_line_under <= BORDER_LINE_DX:
            d = pygame.Vector2(ball_line_under, BORDER_LINE_DY)    #突き抜けた量を基に反射後の位置を決める
            p -= d
            p.y = -p.y
            d += p
            return d
    return None

def calc_ball(ball, ball_v, bar1, bar2, score_1, score_2, rally, ball_a, ballV0):
#ボールの挙動

    collsion1 = ball_refrection(ball,ball_v,bar1, rally, ball_a, ballV0)
    if collsion1 != None:               #bar1と反射した
        ball, ball_v, rally, ball_a= collsion1
               #ボールの速度の向きを変える
    collsion2 = ball_refrection(ball,ball_v,bar2, rally, ball_a, ballV0)
    if collsion2 != None:               #bar2と反射した
        ball, ball_v, rally, ball_a = collsion2

    collsion3 = ball_refrection_border(ball,ball_v)
    if collsion3 != None:               #上下どちらかのラインと反射した
        ball = collsion3
        ball_v.y = -ball_v.y
    if collsion1 == None and collsion2 == None and collsion3 == None:   #どことも反射していない場合ボールを動かす
        ball += ball_v
   


    if ball.x < POINT_BORDER_LINE1:         #プレイヤー側のボーダーラインを超えた
        ball.xy = BALL_XF, BALL_YF          #ボールを初期位置にもどす
        score_2 += 1                        #CPUが得点を得る
    elif ball.x > POINT_BORDER_LINE2:       #CPU側のボーダーラインを超えた
        ball.xy = BALL_XF, BALL_YF          #ボールを初期位置にもどす
        score_1 += 1                        #プレイヤーが得点を得る
    

    return ball, ball_v, score_1, score_2, rally, ball_a
            
def calc_player(bar1_y, bar1_dy):
    bar1_y += bar1_dy                   #bar1の位置を入力された分動かす
    if bar1_y >= 360.: bar1_y = 360.    #bar1は460を超えない
    elif bar1_y <= 10. : bar1_y = 10.   #bar1は10を超えない
    return bar1_y
    
def calc_ai(bar2, ball, ball_v):
    if ball_v.x > 0 :
        dy = ball.y - bar2.y - 49.9
        if dy > 80: bar2.y += 8.3
        elif dy > 50: bar2.y += 4.3
        elif dy > 30: bar2.y += 2.3
        elif dy > 10: bar2.y += 1.3
        elif dy < -80: bar2.y -= 8.3
        elif dy < -50: bar2.y -= 4.3
        elif dy < -30: bar2.y -= 2.3
        elif dy < -10: bar2.y -= 1.3

    if bar2.y >= 420.: bar2.y = 420.
    elif bar2.y <= 10.: bar2.y = 10.
    return bar2.y



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


ballV0 = pygame.Vector2(BALL_VXF, BALL_VYF) * time_sec
ballv_vec.xy *= time_sec

rally = 0
ball_a = 1
start = 0

score_1 = 0
score_2 = 0
score_1_prev = 0
score_2_prev = 0
needed = 3
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
            screen.blit(font.render(str(int(rally)), True,White), (320, 40) )
        if start == 0:
            
            if needed != 0:
                ballv_vec.xy = 0, 0
                screen.blit(font.render(str(int(needed)), True,White), (320, 240) )
                time.sleep(1)
                needed -= 1
            else:
                ballv_vec.x, ballv_vec.y = BALL_VXF * time_sec, BALL_VYF * time_sec
                ballV0.x, ballV0.y = BALL_VXF * time_sec, BALL_VYF * time_sec
                start = 1
        for event in pygame.event.get():
            if event. type == QUIT:     #×が押された場合終了する
                pygame.quit()
                sys. exit()
            if event.type == KEYDOWN:   #キーの上か下が押し続けられている場合bar1を加算する
                if event.key == K_UP:
                    bar1.y -= 2.
                elif event.key == K_DOWN:
                    bar1.y += 2.
            elif event.type == KEYUP:
                if event.key == K_UP:
                    bar1_v = 0
                elif event.key == K_DOWN:
                    bar1_v = 0
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[K_UP]:
                bar1_v -= 10.
            if pressed_keys[K_DOWN]:
                bar1_v += 10

        bar1_vec.y = calc_player(bar1_vec.y,bar1_v)
        passtime = clock.tick(60)

        score_1_prev = score_1
        score_2_prev = score_2

        bar2_vec.y = calc_ai(bar2_vec, ball_vec, ballv_vec)
        ball_vec, ballv_vec, score_1, score_2, rally, ball_a = calc_ball(ball_vec, ballv_vec, bar1_vec, bar2_vec, score_1, score_2, rally, ball_a, ballV0)

        if score_1 != score_1_prev or score_2 != score_2_prev:
            rally = 0
            ball_a = 0
            ballv_vec = ballV0
            needed, start = 3, 0
        if score_1 == 5:            #どちらか先に五点取った方の勝ち
            draw_game_over_screen(text1)
            game_state = 'over'
        if score_2 == 5:
            draw_game_over_screen(text2)
            game_state = 'over'
        
        
       
        
        elif game_state == 'over':

            keys = pygame.key.get_pressed()

            if keys[pygame.K_r]:    #ゲームオーバー時Rを押すとリスタート
                bar1_vec.xy, bar1_v = (BAR1_XF, BAR1_YF), BAR1_VYF
                bar2_vec.xy, bar2_v = (BAR2_XF, BAR2_YF), BAR2_VYF
                ball_vec.xy = (BALL_XF, BALL_YF)
                score_1, score_2,score_1_prev, score_2_prev = 0, 0, 0, 0
                ballV0 = pygame.Vector2(BALL_VXF, BALL_VYF) * time_sec
                start, needed = 0, 3

                game_state = 'game'
            if keys[pygame.K_q]:    #Qを押すと終了
                pygame.quit()
                quit()
                
        pygame.display.update()            