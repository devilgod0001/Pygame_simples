'''  1cm = 50 pixels (not actually)  '''

'''  radius must be more than aperture/2  '''

'''GADBAD IN APPLYSINGIVEANGLE fun.'''

'''  Sindhu, I want to make team of programmers to make a 2d game in UNITY. For that you have to learn C# through this link "https://www.youtube.com/watch?v=FPeGkedZykA&t=14174s"  '''

import pygame
from pygame.locals import *
from pygame import gfxdraw
from math import *
from numpy import array
pygame.init()

info = pygame.display.Info()

width = info.current_w
height = info.current_h
pole = [int(width/2), int(height/2)]


clock = pygame.time.Clock()
#screen = pygame.display.set_mode((width, height), FULLSCREEN)
screen = pygame.display.set_mode((width-100, height-100))

font = pygame.font.SysFont("consolas", 15, False)
text1 = font.render("Principal Axis", True, (10, 255, 100))
text2 = font.render("Pole", True, (0, 0, 255))
text3 = font.render("Flint Glass RI:1.66", True, (255, 255, 255))
warning = font.render(
    "Half of Aperture can never be greater than Radius of curvature", True, (255, 0, 0))

# When decided to use draw instead of gfxdraw
# lensrectside = 400
# lens_rect = Rect(((width-lensrectside)/2, (height-lensrectside)/2),
#                 (lensrectside, lensrectside))


'''  Apply snell's law  '''


def snell_law(insertpX, insertpY, centerX, centerY, refractive_index_initial, refractive_index_final, initial_slope):
    x1 = insertpX
    y1 = insertpY
    x2 = centerX
    y2 = centerY
    m1 = initial_slope
    if x2 - x1 != 0:
        m2 = (y2-y1)/(x2-x1)
    else:
        m2 = float(inf)

    a_o_incidence_slope = (m2-m1)/(1+m1*m2)
    if a_o_incidence_slope >= 0:
        a_o_incidence = atan(a_o_incidence_slope)
    else:
        a_o_incidence = pi - atan(a_o_incidence_slope)

    theta1_rad = a_o_incidence
    n1 = refractive_index_initial
    n2 = refractive_index_final

    theta2_rad = asin((n1*sin(theta1_rad))/n2)
    new_slope = tan(theta2_rad)

    return new_slope


'''  Get points of intersection of lens surface (say) and ray (say)  '''


def intersection(lineX1, lineY1, slope, circleX, circleY, radius):
    g = lineX1
    h = lineY1

    m = slope

    a = circleX
    b = circleY
    r = radius

    c = h - m*g

    root_value = -a*a*m*m + 2*a*b*m - 2*a*c*m - b*b + 2*b*c - c*c + m*m*r*r + r*r

    if root_value >= 0:

        X1 = (-sqrt(-a*a*m*m + 2*a*b*m - 2*a*c*m - b*b + 2*b *
                    c - c*c + m*m*r*r + r*r) + a + b*m - c*m)/(m*m + 1)
        Y1 = (-m*sqrt(-a*a*m*m + 2*a*b*m - 2*a*c*m - b*b + 2*b *
                      c - c*c + m*m*r*r + r*r) + a*m + b*m*m + c)/(m*m + 1)

        X2 = (sqrt(-a*a*m*m + 2*a*b*m - 2*a*c*m - b*b + 2*b *
                   c - c*c + m*m*r*r + r*r) + a + b*m - c*m)/(m*m + 1)
        Y2 = (m*sqrt(-a*a*m*m + 2*a*b*m - 2*a*c*m - b*b + 2*b *
                     c - c*c + m*m*r*r + r*r) + a*m + b*m*m + c)/(m*m + 1)

        return [True, X1, Y1, X2, Y2]

    else:

        return [False, None]


def draw_rays(rangeofslope, from_pt1, from_pt2, center1, center2, Cradius):
    '''
    rangeofslope --> sequence
    from_pt1 = starting point x value of ray
    from_pt2 = starting point y value of ray
    center1 = --> sequence --> first lens to interect
    center2 = --> sequence --> second lens to interect
    '''
    number = 1

    circle_pts = [center1, center2]
    for slope in range(rangeofslope[0], rangeofslope[1]):
        slope = tan(radians(slope))
        inter = intersection(from_pt1, from_pt2, slope,
                             circle_pts[0][0], circle_pts[0][1], Cradius)
        if inter[0] == True and inter[2] > pole[1]-lens.aperture/2 and inter[2] < pole[1]+lens.aperture/2:
            inter[1] = int(inter[1])
            inter[2] = int(inter[2])
            inter[3] = int(inter[3])
            inter[4] = int(inter[4])
            pygame.draw.line(screen, [0, 255, 255],
                             (from_pt1, from_pt2), (inter[1], inter[2]))

            refracted_slope = snell_law(
                inter[1], inter[2], circle_pts[0][0], circle_pts[0][1], 1, 1.66, slope)

            slope1 = refracted_slope

            inter1 = intersection(
                inter[1], inter[2], slope1, circle_pts[1][0], circle_pts[1][1], Cradius)
            if inter1[0] == True:
                inter1[1] = int(inter1[1])
                inter1[2] = int(inter1[2])
                inter1[3] = int(inter1[3])
                inter1[4] = int(inter1[4])
                pygame.draw.line(
                    screen, [0, 255, 255], (inter[1], inter[2]), (inter1[3], inter1[4]))

                

                
                
                refracted_slope1 = snell_law(
                    inter1[3], inter1[4], circle_pts[1][0], circle_pts[1][1], 1, 1.66, slope1)

                slope2 = -refracted_slope1

                xx = 1200
                yy = slope2*(xx - inter1[3]) + inter1[4]

                xx = int(xx)
                yy = int(yy)

                
                

                pygame.draw.line(screen, [0, 255, 255],
                                 (inter1[3], inter1[4]), (xx, yy))
                '''
                yyy = pole[1]
                if slope2!= 0:
                    xxx = ((yyy-inter1[4])/slope2) + inter1[3]
                    xxx = int(xxx)
                    yyy = int(yyy)
                    pygame.draw.circle(screen,[0,0,255],(xxx,yyy),5)'''

                



class Convex_lens:
    def __init__(self, radiusofC, focal_length, pole, aperture):
        self.radius = radiusofC
        self.f = focal_length
        self.pole = pole
        self.aperture = aperture
        self.CRx = int(self.pole[0]-sqrt(self.radius **
                                         2 - (self.aperture/2) ** 2))
        self.CLx = int(self.pole[0]+sqrt(self.radius **
                                         2 - (self.aperture/2) ** 2))
        self.Cy = self.pole[1]

    def draw(self, angle):

        # Right arc
        pygame.gfxdraw.arc(
            screen, self.CRx, self.Cy, self.radius, int(degrees(2*pi - angle)), int(degrees(2*pi + angle)), (255, 10, 10))
        # Left arc
        pygame.gfxdraw.arc(
            screen, self.CLx, self.Cy, self.radius, int(degrees(pi - angle)), int(degrees(pi + angle)), (255, 10, 10))

        # Principal Axis
        pygame.gfxdraw.hline(screen, 0, width, int(height/2), (10, 255, 100))
        screen.blit(
            text1, (10, int(height/2)+5))

        # Pole
        pygame.draw.circle(screen, (50, 50, 255), pole, 2)

        #screen.blit(text2, (pole[0]-text2.get_width()/2, pole[1]+5))
        screen.blit(text2, (int(pole[0]-text2.get_width()/2), int(pole[1]+5)))

        # Right COC point
        pygame.draw.circle(screen, (0, 0, 255), (self.CLx, self.Cy), 2)

        # Left COC point
        pygame.draw.circle(screen, (0, 0, 255), (self.CRx, self.Cy), 2)


class Object:
    def __init__(self, objectdistance, height):
        self.u = objectdistance
        self.ho = height
        self.x1 = pole[0]-self.u
        self.y1 = pole[1]-self.ho
        self.y2 = pole[1]

    def draw(self):

        pygame.gfxdraw.vline(
            screen, pole[0]-self.u, pole[1]-self.ho, pole[1], (255, 255, 255))


running = True
while running:
    clock.tick(20)

    screen.fill([0, 0, 0])
    # Text render
    screen.blit(warning, (10, 10))
    screen.blit(text3, (10, 30))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            pygame.quit()
            quit()

    lens = Convex_lens(250, 50, pole, 300)
    angle = atan((lens.aperture/2)/sqrt(lens.radius**2-(lens.aperture/2)**2))
    lens.draw(angle)

    mouse_pos = pygame.mouse.get_pos()
    mousex = mouse_pos[0]
    mousey = mouse_pos[1]

    mousex = pole[0] - mousex
    mousey = pole[1] - mousey

    obj = Object(mousex, mousey)
    obj.draw()
    '''
    for i in range(0,360):

        i = tan(radians(i))
        
        inter = intersection(obj.x1,obj.y1,i,lens.CLx,lens.Cy,lens.radius)

        if inter[0] and inter[2] > pole[1]-lens.aperture/2 and inter[2] < pole[1]+lens.aperture/2:

            inter[1] = int(inter[1])
            inter[2] = int(inter[2])
            inter[3] = int(inter[3])
            inter[4] = int(inter[4])

            pygame.draw.line(screen,[0,255,255],(obj.x1,obj.y1),(inter[1], inter[2]))
            #pygame.draw.circle(screen,[255,255,100],(inter[3],inter[4]),2)
            # '''

    draw_rays([0, 360], obj.x1, obj.y1, [lens.CLx, lens.Cy],
              [lens.CRx, lens.Cy], lens.radius)

    pygame.display.update()
