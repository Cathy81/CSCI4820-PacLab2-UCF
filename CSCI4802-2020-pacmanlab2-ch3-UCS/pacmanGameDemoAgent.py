#using AIMA-PYTHON to solve pacman,single capsule, BFS, and DFS

import pygame, sys, random, math

from pygame.locals import *
from maze_graph import *
from Pacman import *
from pacmanGame import *
from agent import SearchAgent

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, SCORE_SURF, SCORE_RECT, SOLVE_SURF, SOLVE_RECT
    global walls, pacmanPos,capsulePos,game,pacman,score, scoreText
    score=0
    filename=".\\layouts\\tinyMaze.lay"
    if(len(sys.argv)>1):
        print(sys.argv[1])
        sAgent=sys.argv[1]
    else:
        sAgent=""
    game=PacGame(filename)

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((game.WINDOWWIDTH, game.WINDOWHEIGHT))

    strS=game.strS
    pygame.display.set_caption('PacMan')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    scoreText='SCORE:'+str(score)
    SCORE_SURF, SCORE_RECT = makeText(scoreText, TEXTCOLOR, BGCOLOR, 10, game.WINDOWHEIGHT - 40)
    DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT)
    game.genMaze()
    pacmanPos=game.pacmanPos

    walls=game.walls
    game.drawWall(DISPLAYSURF)
    pacman=Pacman(pacmanPos,0,PACCOLOR,PAC_SIZE,0,walls,game.MAZE_WIDTH,game.MAZE_HEIGHT)
    pacman.drawPacman(DISPLAYSURF)
    game.drawCapsule(DISPLAYSURF)
    agent=SearchAgent(game,sAgent)
    pygame.time.wait(1000)
    slideTo = None  # the direction, if any, a tile should slide
    while True:# main game loop
         for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                print("# of visited nodes: ", agent.numVisited)
                pygame.quit()
                sys.exit()
            elif(len(sys.argv)<2):
                print('Enter one argument: bfs, dfs..')
                break;
            scores=0
            while(game.capsulePos):
                agent.get_actions()
                while(len(agent.actionSeq)>0):
                    (pac_action, new_pos) = agent.get_action()
                    if new_pos in game.capsulePos:
                        index=game.capsulePos.index(new_pos)
                        game.capsulePos.pop(index)
       #             while (pac_actions):
                    slideTo = pac_action
                    if slideTo:
                        slideAnimation(pacman, slideTo, "Ok", 8)  #
                    scores+=1
                    game.pacmanPos.pop(0)
                    game.pacmanPos.append(new_pos)
                    pygame.display.update()
                    FPSCLOCK.tick(FPS)
                    scoreText = 'SCORE:' + str(scores)
                    SCORE_SURF, SCORE_RECT = makeText(scoreText, TEXTCOLOR, BGCOLOR, 10, game.WINDOWHEIGHT - 40)
                    DISPLAYSURF.blit(SCORE_SURF, SCORE_RECT)

         pygame.display.update()
         FPSCLOCK.tick(FPS)

def makeText(text, color, bgcolor, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def slideAnimation(pacman, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.
     # prepare the base surface
    baseSurf = DISPLAYSURF.copy()
    (x,y) = pacman.pos[0]
    #pygame.draw.rect(DISPLAYSURF, YELLOW, ((x)*WALL_RADIUS,(y)*WALL_RADIUS,PAC_SIZE*2,PAC_SIZE*2))
    xTop,yTop=x * PAC_SIZE* 2, y*PAC_SIZE*2

    #yTop=y * radius * 2, radius * 2, radius * 2)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (xTop,yTop, PAC_SIZE * 2, PAC_SIZE * 2))
    (xEnd, yEnd) =pacman.makeMove(direction)#pop the initial pos in makeMove
   # pacman.pos.append((xEnd, yEnd))
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    pacman.drawPacman(baseSurf) #open widely

    DISPLAYSURF.blit(baseSurf, (0, 0))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pacman.drawPacman(DISPLAYSURF)
    game.drawCapsule(DISPLAYSURF)

if __name__ == '__main__':
    main()
