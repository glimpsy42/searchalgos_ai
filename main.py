import pygame
import sys
from gridstuff import rows, cols, make_grid, place_walls
from algoss import bfs, dfs, ucs, dls, iddfs, bidirectional

# colrs
white = (255,255,255)
black = (0,0,0)
green = (0,200,0)
red = (220,30,30)
blue = (50,100,255)
gray = (170,170,170)
yellow = (255,230,0)
lgray = (220,220,220)
dgray = (100,100,100)
orange = (255,165,0)
btnclr = (70,130,180)
btnhvr = (100,160,210)

# sizes n stuff
cell_sz = 28
margin = 2
topbar = 60
bottombar = 100
grid_w = cols*(cell_sz+margin)+margin
grid_h = rows*(cell_sz+margin)+margin
win_w = grid_w + 20
win_h = topbar + grid_h + bottombar + 10
delay = 60

pygame.init()
screen = pygame.display.set_mode((win_w, win_h))
pygame.display.set_caption("search algos assignment")
clk = pygame.time.Clock()
fnt = pygame.font.SysFont("arial", 16)
bigfnt = pygame.font.SysFont("arial", 20, bold=True)
smfnt = pygame.font.SysFont("arial", 13)
tinyfnt = pygame.font.SysFont("arial", 11)

# algos
algonames = ["BFS","DFS","UCS","DLS","IDDFS","Bidirectional"]
algofuncs = [bfs, dfs, ucs, dls, iddfs, bidirectional]
cur_algo = 0

# grid setup
grid = make_grid()
startpos = (1,1)
targetpos = (rows-2, cols-2)
grid[startpos[0]][startpos[1]] = 2
grid[targetpos[0]][targetpos[1]] = 3
place_walls(grid, count=50)
grid[startpos[0]][startpos[1]] = 2
grid[targetpos[0]][targetpos[1]] = 3

# state varibles
frontr = set()
explrd = set()
finalpath = None
is_running = False
searchgen = None
done = False
stattxt = "pick algo and press start"

def draw():
    screen.fill(lgray)
    # title
    t = bigfnt.render("search algos assignment", True, black)
    screen.blit(t, (win_w//2 - t.get_width()//2, 8))
    # algo name
    a = fnt.render("Algo: "+algonames[cur_algo], True, dgray)
    screen.blit(a, (15, 35))
    # draw grid cells
    ox = 10
    oy = topbar
    for r in range(rows):
        for c in range(cols):
            x = ox + c*(cell_sz+margin)+margin
            y = oy + r*(cell_sz+margin)+margin
            pos = (r,c)
            cell = grid[r][c]
            if finalpath and pos in finalpath:
                clr = yellow
            elif pos == startpos:
                clr = green
            elif pos == targetpos:
                clr = red
            elif cell == 1:
                clr = black
            elif pos in explrd:
                clr = gray
            elif pos in frontr:
                clr = blue
            else:
                clr = white
            pygame.draw.rect(screen, clr, (x,y,cell_sz,cell_sz))
            pygame.draw.rect(screen, lgray, (x,y,cell_sz,cell_sz), 1)
    # buttons
    draw_btns()
    # status
    s = smfnt.render(stattxt, True, black)
    screen.blit(s, (15, topbar+grid_h+52))
    # credts at bottom
    cr = tinyfnt.render("made by ahmed & aleeza (23f0623 & 23f0736)", True, dgray)
    screen.blit(cr, (win_w//2 - cr.get_width()//2, topbar+grid_h+bottombar-8))
    pygame.display.flip()

def draw_btns():
    yp = topbar+grid_h+8
    bw = 80
    bh = 32
    sx = 10
    mouse = pygame.mouse.get_pos()
    # prev
    pr = pygame.Rect(sx, yp, 50, bh)
    h = pr.collidepoint(mouse)
    pygame.draw.rect(screen, btnhvr if h else btnclr, pr, border_radius=5)
    t = fnt.render("<", True, white)
    screen.blit(t, (pr.centerx-t.get_width()//2, pr.centery-t.get_height()//2))
    # nxt
    nr = pygame.Rect(sx+60, yp, 50, bh)
    h = nr.collidepoint(mouse)
    pygame.draw.rect(screen, btnhvr if h else btnclr, nr, border_radius=5)
    t = fnt.render(">", True, white)
    screen.blit(t, (nr.centerx-t.get_width()//2, nr.centery-t.get_height()//2))
    # start btn
    sr = pygame.Rect(sx+130, yp, bw, bh)
    h = sr.collidepoint(mouse)
    pygame.draw.rect(screen, btnhvr if h else green, sr, border_radius=5)
    t = fnt.render("Start", True, white)
    screen.blit(t, (sr.centerx-t.get_width()//2, sr.centery-t.get_height()//2))
    # reset btn
    rr = pygame.Rect(sx+220, yp, bw, bh)
    h = rr.collidepoint(mouse)
    pygame.draw.rect(screen, btnhvr if h else orange, rr, border_radius=5)
    t = fnt.render("Reset", True, white)
    screen.blit(t, (rr.centerx-t.get_width()//2, rr.centery-t.get_height()//2))

def get_btns():
    yp = topbar+grid_h+8
    bw = 80
    bh = 32
    sx = 10
    return (pygame.Rect(sx,yp,50,bh), pygame.Rect(sx+60,yp,50,bh),
            pygame.Rect(sx+130,yp,bw,bh), pygame.Rect(sx+220,yp,bw,bh))

def reset():
    global grid,frontr,explrd,finalpath,is_running,searchgen,done,stattxt
    grid = make_grid()
    grid[startpos[0]][startpos[1]] = 2
    grid[targetpos[0]][targetpos[1]] = 3
    place_walls(grid, count=50)
    grid[startpos[0]][startpos[1]] = 2
    grid[targetpos[0]][targetpos[1]] = 3
    frontr = set()
    explrd = set()
    finalpath = None
    is_running = False
    searchgen = None
    done = False
    stattxt = "grid reset. pick algo and press start"

def startsearch():
    global searchgen,is_running,done,frontr,explrd,finalpath,stattxt
    frontr = set()
    explrd = set()
    finalpath = None
    done = False
    algo = algofuncs[cur_algo]
    if cur_algo == 3:
        searchgen = algo(grid, startpos, targetpos, limit=25)
    elif cur_algo == 4:
        searchgen = algo(grid, startpos, targetpos, max_depth=35)
    else:
        searchgen = algo(grid, startpos, targetpos)
    is_running = True
    stattxt = "running " + algonames[cur_algo] + "..."

def step():
    global frontr,explrd,finalpath,is_running,done,stattxt,searchgen
    if searchgen is None:
        return
    try:
        f, e, path = next(searchgen)
        frontr = set(f)
        explrd = e
        if path is not None:
            if len(path) > 0:
                finalpath = set(path)
                stattxt = algonames[cur_algo]+" found path! length: "+str(len(path))
            else:
                finalpath = None
                stattxt = algonames[cur_algo]+" - no path found!"
            is_running = False
            done = True
    except StopIteration:
        is_running = False
        done = True
        if finalpath is None:
            stattxt = algonames[cur_algo]+" - no path found"

# main loop
last_t = 0
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            mx,my = ev.pos
            pr,nr,sr,rr = get_btns()
            if pr.collidepoint(mx,my) and not is_running:
                cur_algo = (cur_algo-1) % len(algonames)
                stattxt = "selected: "+algonames[cur_algo]
            elif nr.collidepoint(mx,my) and not is_running:
                cur_algo = (cur_algo+1) % len(algonames)
                stattxt = "selected: "+algonames[cur_algo]
            elif sr.collidepoint(mx,my) and not is_running:
                startsearch()
            elif rr.collidepoint(mx,my):
                reset()
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE and not is_running:
                startsearch()
            if ev.key == pygame.K_r:
                reset()
    now = pygame.time.get_ticks()
    if is_running and now - last_t > delay:
        step()
        last_t = now
    draw()
    clk.tick(60)