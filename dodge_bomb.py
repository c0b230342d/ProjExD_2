import os
import random
import time
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def move_kk() -> dict:
    """
    戻り値：辞書（押下キーに対する移動量の合計タプルをキー）
    """
    # kk = tuple(x)
    MODEL = {  # 各方向のこうかとんのsurfaceの辞書
        (-5, 0): pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0),
        (-5, +5): pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0),
        (0, +5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), -90, 2.0),
        (+5, +5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), -45, 2.0),
        (+5, 0): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 0, 2.0),
        (+5, -5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 45, 2.0),
        (0, -5): pg.transform.rotozoom(pg.transform.flip(pg.image.load("fig/3.png"), True, False), 90, 2.0),
        (-5, -5): pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0),
    }
    return MODEL


def add_accs_scale() -> tuple:
    accs = [a for a in range(1, 11)]
    bb_images = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_images.append(bb_img)
    return accs, bb_images


def game_over(screen) -> None:
    """
    引数：displayのサイズ
    黒い画面と文字、こうかとんの表示と5秒間の表示をさせる
    """
    black_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(black_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    black_img.set_alpha(100)
    black_rct = black_img.get_rect()
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Gmae Over",
                    True, (255, 255, 255))
    kk_cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    screen.blit(black_img, black_rct)
    screen.blit(txt, [WIDTH/2-120, HEIGHT/2])
    screen.blit(kk_cry_img, [WIDTH/4+50, HEIGHT/2])
    screen.blit(kk_cry_img, [WIDTH*3/4, HEIGHT/2])
    pg.display.update()
    time.sleep(5)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):  # 衝突判定
            game_over(screen)
            print("はい、増税！")
            return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if sum_mv != [0, 0]:
            kk_img = move_kk()[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1.05
        if not tate:
            vy *= -1.05

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
