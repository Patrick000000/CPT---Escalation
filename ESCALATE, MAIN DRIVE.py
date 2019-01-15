import pygame, time, sys, random, math
import pygame.freetype
import pygame.gfxdraw


WHITE = (255, 255, 255)


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1300,600))
my_font = pygame.font.SysFont('Consolas', 60)
my_font2 = pygame.font.SysFont('Consolas', 20)
pygame.display.set_caption('Escalate')


# -General/game
fps = 120

# -Physics, movement, geometry
Died = [False, False]
Left = True
moving = False
initial_ball_angle = 180
ball_rad = 10
ball_speed = 8
ball_yloc = 300

# -Player data
# [0] = Player 1
# [1] = Player 2
player_width = 20
player_length = [120, 120]
player_mana = [200, 200]
player_mana_display = [100, 100]
player_speed = [6, 6]

# -Start Menu
started = False

# -Time
    # -for the timer def
timer_status = [False, False, False]
    # -for the timer def
seconds = 0
    # -for the timer def
frames = 0
    # -for the timer def
ind_frames = [0, 0]
    # -for the timer def
mana_recovery = 0


# -Abilities variables:
# [0] = Player 1
# [1] = Player 2

Railgun_Pl = [True, True]
Railgun_lvl = [1, 1]
Railgun_toggle = [False, False]
R_bounce_prt1 = [False, False]
R_bounce_prt2 = [False, False]
railgun_mana_collector = [False, False]
railgun_cost = 40

blink_pl = [True, True]
blink_lvl = [1, 1]
blink_button = [False, False]
counter1 = [0, 0, 0]
counter2 = [0, 0, 0]
cardinal_dir = [False, False]
slow_effect = False
blink_cost = 30

shield_pl = [True, True]
shield_damage = [0, 0]
shield_lvl = [3, 3]
shield_toggle = [False, False]
shield_loc1 = [0, 0]
shield_loc2 = [0, 0]
shield_cost = 35   # -The thing cycle through twice so shield cost is actually shield_cost*2

growth_pl = [False, False]
growth_lvl = [3, 1]

speed_pl = [False, False]
speed_lvl = [3, 1]

def speed():
    global player_speed, speed_lvl

    if growth_pl[0] is True:
        if speed_lvl[0] == 1:
            player_speed[0] = 6
        if speed_lvl[0] == 2:
            player_speed[0] = 7
        if speed_lvl[0] == 3:
            player_speed[0] = 9
    if growth_pl[1] is True:
        if speed_lvl[1] == 1:
            player_speed[1] = 6
        if speed_lvl[1] == 2:
            player_speed[1] = 7
        if speed_lvl[1] == 3:
            player_speed[1] = 9

def growth():
    global growth_pl, growth_lvl

    if growth_pl[0] is True:
        if growth_lvl[0] == 1:
            player_length[0] = 130
        if growth_lvl[0] == 2:
            player_length[0] = 140
        if growth_lvl[0] == 3:
            player_length[0] = 200
    if growth_pl[1] is True:
        if growth_lvl[1] == 1:
            player_length[1] = 130
        if growth_lvl[1] == 2:
            player_length[1] = 140
        if growth_lvl[1] == 3:
            player_length[1] = 140

def blink(lvl, x, paddle_y, paddle_y2, ball_y):
    global blink_button, counter1, counter2, slow_effect, timer_status

    y1 = [0, 0, 0]
    y2 = [0, 0, 0]

    if blink_pl[0] is True:
        if x > 650 and lvl == 1:
            counter1[0] = 0
        if x > 650 and lvl == 2:
            counter1[1] = 0
        if x > 650 and lvl == 3:
            counter1[2] = 0
    if blink_pl[1] is True:
        if x < 650 and lvl == 1:
            counter2[0] = 0
        if x < 650 and lvl == 2:
            counter2[1] = 0
        if x < 650 and lvl == 3:
            counter2[2] = 0

    if blink_pl[0] is True and x < 650:
        if lvl == 1 and counter1[0] < 2 and blink_button[0] is True and Left is True:
            y1[0] = paddle_y + player_length[0]/2
            counter1[0] += 1
            if player_mana[0] - blink_cost < 0:
                player_mana[0] = player_mana[0] - (player_mana[0] - (blink_cost - player_mana[0]))
            else:
                player_mana[0] -= blink_cost
            blink_button[0] = False
            timer_status[0] = True
            return y1[0]
        if lvl == 2 and counter1[1] < 3 and blink_button[0] is True and Left is True:
            y1[1] = paddle_y + player_length[0]/2
            counter1[1] += 1
            if player_mana[0] - blink_cost < 0:
                player_mana[0] = player_mana[0] - (player_mana[0] - (blink_cost - player_mana[0]))
            else:
                player_mana[0] -= blink_cost
            blink_button[0] = False
            timer_status[0] = True
            return y1[1]
        if lvl == 3 and counter1[2] < 4 and blink_button[0] is True and Left is True:
            y1[2] = paddle_y + player_length[0]/2
            counter1[2] += 1
            if player_mana[0] - blink_cost < 0:
                player_mana[0] = player_mana[0] - (player_mana[0] - (blink_cost - player_mana[0]))
            else:
                player_mana[0] -= blink_cost
            blink_button[0] = False
            timer_status[0] = True
            return y1[2]
        else:
            return ball_y

    if blink_pl[1] is True and x > 650:
        if lvl == 1 and counter2[0] < 2 and blink_button[1] is True and Left is False:
            y2[0] = paddle_y2 + player_length[1] / 2
            counter2[0] += 1
            if player_mana[1] - blink_cost < 0:
                player_mana[1] = player_mana[1] - (player_mana[1] - (blink_cost - player_mana[1]))
            else:
                player_mana[1] -= blink_cost
            blink_button[1] = False
            timer_status[0] = True
            return y2[0]
        if lvl == 2 and counter2[1] < 3 and blink_button[1] is True and Left is False:
            y2[1] = paddle_y2 + player_length[1] / 2
            counter2[1] += 1
            if player_mana[1] - blink_cost < 0:
                player_mana[1] = player_mana[1] - (player_mana[1] - (blink_cost - player_mana[1]))
            else:
                player_mana[1] -= blink_cost
            blink_button[1] = False
            timer_status[0] = True
            return y2[1]
        if lvl == 3 and counter2[2] < 4 and blink_button[1] is True and Left is False:
            y2[2] = paddle_y2 + player_length[1] / 2
            counter2[2] += 1
            if player_mana[1] - blink_cost < 0:
                player_mana[1] = player_mana[1] - (player_mana[1] - (blink_cost - player_mana[1]))
            else:
                player_mana[1] -= blink_cost
            blink_button[1] = False
            timer_status[0] = True
            return y2[2]
        else:
            return ball_y
    else:
        return ball_y


def Railgun():
    global railgun_mana_collector

    if Railgun_Pl[0] is True:
        if Left is True and R_bounce_prt2[0] is True and Railgun_toggle[0] is True:
            Railgun_toggle[0] = False
            R_bounce_prt1[0] = False
            R_bounce_prt2[0] = False
        if Died[1] is True:
            Railgun_toggle[0] = False
            R_bounce_prt1[0] = False
            R_bounce_prt2[0] = False
            Died[1] = False
            Died[0] = False
            print('hoy')

    if Railgun_Pl[1] is True:
        if Left is False and R_bounce_prt2[1] is True and Railgun_toggle[1] is True:
            Railgun_toggle[1] = False
            R_bounce_prt1[1] = False
            R_bounce_prt2[1] = False
        if Died[0] is True:
            Railgun_toggle[1] = False
            R_bounce_prt1[1] = False
            R_bounce_prt2[1] = False
            Died[1] = False
            Died[0] = False


def shield(lvl):
    global shield_pl, shield_damage, shield_toggle, player_length, player_width, player_mana
    key = pygame.key
    pygame.event.pump()

    size_y = [0, 0]

    if key.get_pressed()[pygame.K_q] and player_mana[0] > shield_cost:
        shield_toggle[0] = True
        if ind_frames[0] < 2:
            timer_status[1] = True
    if key.get_pressed()[pygame.K_PAGEUP] and player_mana[1] > shield_cost:
        shield_toggle[1] = True
        if ind_frames[1] < 2:
            timer_status[2] = True

    if lvl == 1:
        size_y[0] = player_length[0]
        size_y[1] = player_length[1]
    if lvl == 2:
        size_y[0] = player_length[0] + 50
        size_y[1] = player_length[1] + 50
    if lvl == 3:
        size_y[0] = player_length[0] + 100
        size_y[1] = player_length[1] + 100

    return size_y[0], size_y[1]


def display_mana():
    global player_mana

    pygame.draw.rect(screen, (0, 0, 0), (0, 0, 200, 20), 1)
    pygame.gfxdraw.box(screen, pygame.Rect(0, 0, player_mana[0], 20), (50, 50, 100, 127))

    pygame.draw.rect(screen, (0, 0, 0), (1100, 0, 200, 20), 1)
    pygame.gfxdraw.box(screen, pygame.Rect(1100, 0, player_mana[1], 20), (50, 50, 100, 127))


def timer():
    global fps, frames, seconds, timer_status, ind_frames, mana_recovery

    mana_recovery += 1
    if mana_recovery > 60:
        mana_recovery = 0
        if player_mana[0] > 200:
            player_mana[0] -= (player_mana[0] - 200)
        elif player_mana[0] < 200:
            player_mana[0] += 3
        if player_mana[1] > 200:
            player_mana[1] -= (player_mana[1] - 200)
        elif player_mana[1] < 200:
            player_mana[1] += 3

    if timer_status[2] is True:
        ind_frames[1] += 1
    if timer_status[1] is True:
        ind_frames[0] += 1

    if timer_status[0] is True:
        if frames < fps:
            frames += 1
        if frames >= fps:
            seconds += 1
            frames = 0


def ang_paddles(widest_point, option, midpoint_num, midpoint_length, hit):

    if option == 1:
        if midpoint_length >= hit:
            difference = midpoint_length - hit
            increment = (90 - widest_point)/midpoint_num
            degrees_deviation = difference * increment
            scaled_num = degrees_deviation
            return scaled_num
        if midpoint_length <= hit:
            difference = hit - midpoint_length
            increment2 = (90 - widest_point)/midpoint_num
            degrees_deviation2 = difference * increment2
            scaled_num2 = 360 - degrees_deviation2
            return scaled_num2

    elif option == 2:
        if midpoint_length >= hit:
            difference = midpoint_length - hit
            increment3 = (90 - widest_point)/midpoint_num
            degrees_deviation3 = difference * increment3
            scaled_num3 = 180 - degrees_deviation3
            return scaled_num3
        if midpoint_length <= hit:
            difference = hit - midpoint_length
            increment4 = (90 - widest_point)/midpoint_num
            degrees_deviation4 = difference * increment4
            scaled_num4 = 180 + degrees_deviation4
            return scaled_num4


class Player1:
    def __init__(self, x, y, r, g, b, width, w):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.width = width
        self.w = w

    def display_p(self):

        pygame.draw.rect(screen, (self.r, self.g, self.b), (int(self.x), int(self.y), self.width, player_length[0]), self.w)

    def move(self):
        global player_speed

        key = pygame.key
        pygame.event.pump()

        if key.get_pressed()[pygame.K_a] and self.y > 0:
            self.y -= player_speed[0]
        if key.get_pressed()[pygame.K_d] and self.y < 600 - player_length[0]:
            self.y += player_speed[0]


class Player2:
    def __init__(self, x, y, r, g, b, width, w):
        self.x = x
        self.y = y
        self.r = r
        self.g = g
        self.b = b
        self.width = width
        self.w = w

    def display_p(self):
        pygame.draw.rect(screen, (self.r, self.g, self.b), (int(self.x), int(self.y), self.width, player_length[1]), self.w)

    def move(self):
        key = pygame.key
        pygame.event.pump()

        if key.get_pressed()[pygame.K_RIGHT] and self.y > 0:
            self.y -= player_speed[1]
        if key.get_pressed()[pygame.K_LEFT] and self.y < 600 - player_length[1]:
            self.y += player_speed[1]


player_list = []
PL1 = Player1(0, 300, 0, 0, 255, player_width, 0)
PL2 = Player2(1280, 300, 0, 0, 255, player_width, 0)
player_list.append(PL1)
player_list.append(PL2)

transfer_x1 = PL1.x
transfer_y1 = PL1.y
transfer_x2 = PL2.x
transfer_y2 = PL2.y


class MainBall:
    def __init__(self, x11, y11, r, g, b, ra, w, angle, spd):
        self.x11 = x11
        self.y11 = y11
        self.r = r
        self.g = g
        self.b = b
        self.ra = ra
        self.w = w
        self.angle = angle
        self.spd = spd

    def display_circle(self):
        pygame.draw.circle(screen, (self.r, self.g, self.b), (int(self.x11), int(self.y11)), self.ra, self.w)

    def move_circle(self, Pla1, Pla2):
        global player_length, ball_rad, Left, ball_speed, R_bounce_prt1, R_bounce_prt2, Died, ball_yloc, coo_collector,\
            shield_damage, railgun_mana_collector, Railgun_lvl

        key = pygame.key
        pygame.event.pump()

        inst_x1 = Pla1.x
        inst_y1 = Pla1.y
        inst_x2 = Pla2.x
        inst_y2 = Pla2.y

        # -angle bounce physics ---

        # -for walls
        if self.angle > 360:
            self.angle = self.angle % 360

        if self.y11-ball_rad < 0:
            if self.angle >= 90 and self.angle <= 180 and Left is True:
                self.angle = 360 - self.angle
                self.y11 += ball_speed
            if self.angle >= 0 and self.angle < 90 and Left is False:
                self.angle = 360 - self.angle
                self.y11 += ball_speed

        if self.y11 + ball_rad > 600:
            if self.angle > 180 and self.angle < 270 and Left is True:
                self.angle = 360 - self.angle
                self.y11 -= ball_speed
            if self.angle > 270 and self.angle <= 360 and Left is False:
                self.angle = 360 - self.angle
                self.y11 -= ball_speed


        if self.x11 < 0:
            self.x11 = 650
            self.y11 = 300
            if self.angle >= 90 and self.angle <= 270:
                self.angle = 180
            Died[0] = True

        if self.x11 > 1300:
            self.x11 = 650
            self.y11 = 300
            if self.angle > 270 and self.angle <= 360 or self.angle > 0 and self.angle < 90:
                self.angle = 0
            Died[1] = True
        # ---


        # -for paddles
        if self.x11-ball_rad < 20 and self.y11 + ball_rad > inst_y1 and self.y11 - ball_rad < inst_y1 + player_length[0]:
            if self.angle > 360:
                self.angle = self.angle % 360
            self.angle = ang_paddles(30, 1, player_length[0]/2, inst_y1 + (player_length[0]/2), self.y11)
            if Left is True:
                Left = False
            if R_bounce_prt1[0] is True:
                R_bounce_prt2[0] = True


        if self.x11+ball_rad > 1280 and self.y11 + ball_rad > inst_y2 and self.y11 - ball_rad < inst_y2 + player_length[1]:
            if self.angle > 360:
                self.angle = self.angle % 360
            self.angle = ang_paddles(30, 2, player_length[1]/2, inst_y2 + (player_length[1]/2), self.y11)
            if Left is False:
                    Left = True
            if R_bounce_prt1[1] is True:
                R_bounce_prt2[1] = True
        # ---


        # -blink effects ---
        self.y11 = blink(3, self.x11, inst_y1, inst_y2, self.y11)
        if self.x11 > 650:
            cardinal_dir[1] = True
            cardinal_dir[0] = False
        if self.x11 < 650:
            cardinal_dir[0] = True
            cardinal_dir[1] = False
        if slow_effect is True:
            self.spd = ball_speed - (ball_speed/2)
        if slow_effect is False:
            self.spd = ball_speed

        # -railgun effects ---
        Railgun()
        if R_bounce_prt2[0] is True and Railgun_toggle[0] is True:
            if Railgun_lvl[0] == 1:
                self.spd = 12
            if Railgun_lvl[0] == 2:
                self.spd = 15
            if Railgun_lvl[0] == 3:
                self.spd = 18
            self.angle = 0
        if R_bounce_prt2[1] is True and Railgun_toggle[1] is True:
            if Railgun_lvl[1] == 1:
                self.spd = 12
            if Railgun_lvl[1] == 2:
                self.spd = 15
            if Railgun_lvl[1] == 3:
                self.spd = 18
            self.angle = 180

        if Railgun_toggle[0] is True:
            if railgun_mana_collector[0] is True:
                if player_mana[0] - railgun_cost < 0:
                    player_mana[0] = player_mana[0] - (player_mana[0] - (railgun_cost - player_mana[0]))
                else:
                    player_mana[0] -= railgun_cost
                railgun_mana_collector[0] = False
        if Railgun_toggle[1] is True:
            if railgun_mana_collector[1] is True:
                if player_mana[1] - railgun_cost < 0:
                    player_mana[1] = player_mana[1] - (player_mana[1] - (railgun_cost - player_mana[1]))
                else:
                    player_mana[1] -= railgun_cost
                railgun_mana_collector[1] = False

        # -shield effects ---
        shield(shield_lvl[0])
        if shield_toggle[0] is True and shield_pl[0] is True:
            y = shield(shield_lvl[0])[0]

            if ind_frames[0] < 2:
                shield_loc1[0] = 50
                shield_loc1[1] = inst_y1
                if player_mana[0] - shield_cost < 0:
                    player_mana[0] = player_mana[0] - (player_mana[0]-(shield_cost - player_mana[0]))
                else:
                    player_mana[0] -= shield_cost
            if ind_frames[0] >= 2:
                timer_status[1] = False

            if shield_loc1[1] + y > 600:
                difference = (shield_loc1[1] + y) - 600
                shield_loc1[1] -= difference
            pygame.gfxdraw.box(screen, pygame.Rect(shield_loc1[0], shield_loc1[1], 10, y), (100, 0, 0, 127))

            if self.x11 - ball_rad < shield_loc1[0] + 10 and self.y11 + ball_rad > shield_loc1[
                1] and self.y11 - ball_rad < shield_loc1[1] + y and Left is True:
                if self.angle > 360:
                    self.angle = self.angle % 360
                self.angle = ang_paddles(20, 1, y / 2, shield_loc1[1] + (y / 2), self.y11)
                if Left is True:
                    Left = False
                if R_bounce_prt1[0] is True:
                    R_bounce_prt2[0] = True
                shield_damage[0] += 1

            if shield_lvl[0] == 1 and shield_damage[0] >= 3 or shield_lvl[0] == 2 and shield_damage[0] > 3 or \
                    shield_lvl[0] == 3 and shield_damage[0] > 4:
                shield_toggle[0] = False
                timer_status[1] = False
                ind_frames[0] = 0
                shield_damage[0] = 0

        shield(shield_lvl[1])
        if shield_toggle[1] is True and shield_pl[1] is True:
            y2 = shield(shield_lvl[1])[1]

            if ind_frames[1] < 2:
                shield_loc2[0] = 1250
                shield_loc2[1] = inst_y2
                if player_mana[1] - shield_cost < 0:
                    player_mana[1] = player_mana[1] - (player_mana[1]-(shield_cost - player_mana[1]))
                else:
                    player_mana[1] -= shield_cost
            if ind_frames[1] >= 2:
                timer_status[2] = False

            if shield_loc2[1] + y2 > 600:
                difference2 = (shield_loc2[1] + y2) - 600
                shield_loc2[1] -= difference2
            pygame.gfxdraw.box(screen, pygame.Rect(shield_loc2[0], shield_loc2[1], 10, y2), (100, 0, 0, 127))

            if self.x11 + ball_rad > shield_loc2[0] and self.y11 + ball_rad > shield_loc2[1] and \
                    self.y11 - ball_rad < shield_loc2[1] + y2 and Left is False:
                if self.angle > 360:
                    self.angle = self.angle % 360
                self.angle = ang_paddles(20, 2, y2 / 2, shield_loc2[1] + (y2 / 2), self.y11)
                if Left is False:
                    Left = True
                if R_bounce_prt1[1] is True:
                    R_bounce_prt2[1] = True
                shield_damage[1] += 1

            if shield_lvl[1] == 1 and shield_damage[1] >= 3 or shield_lvl[1] == 2 and shield_damage[1] > 3 or \
                    shield_lvl[1] == 3 and shield_damage[1] > 4:
                shield_toggle[1] = False
                timer_status[2] = False
                ind_frames[1] = 0
                shield_damage[1] = 0

        # -ball moving math ---

        angle1 = math.radians(self.angle)

        if moving is True:
            self.x11 += math.cos(angle1) * self.spd
            self.y11 -= math.sin(angle1) * self.spd

        # -------

r1 = 0
r2 = 0
r3 = 0

ball = MainBall(650, ball_yloc, 0, 150, 200, ball_rad, 0, initial_ball_angle, ball_speed)


def starting():
    global Menu, started, r1, r2, r3
    pygame.event.pump()
    key = pygame.key

    title = my_font.render('E S C A L A T E', False, (23, 0, 45))
    start = my_font2.render('S T A R T', False, (r1, r2, r3))
    intro = my_font2.render('I N T R O', False, (23, 0, 45))

    mouse = pygame.mouse
    x = mouse.get_pos()[0]
    y = mouse.get_pos()[1]

    screen.fill(WHITE)
    screen.blit(title, (402.5, 100))
    screen.blit(start, (600.5, 300))
    screen.blit(intro, (600.5, 355))

    if x >= 600.5 and x <= 699.5 and y >= 300 and y <= 321:
        if r1 < 200:
            r1 += 12
        if r2 < 200:
            r2 += 12
        if r3 < 250:
            r3 += 18
    else:
        if r1 > 1:
            r1 -= 12
        if r2 > 1:
            r2 -= 12
        if r3 > 1:
            r3 -= 18


pygame.display.flip()

clock = pygame.time.Clock()
while 1:

    mouse = pygame.mouse
    x = mouse.get_pos()[0]
    y = mouse.get_pos()[1]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and x >= 600.5 and x <= 699.5 and y >= 300 and y <= 321:
            started = True

        # -Toggles

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and player_mana[0] >= railgun_cost:
                Railgun_toggle[0] = True
                R_bounce_prt1[0] = True
                if Railgun_toggle[0] is True:
                    railgun_mana_collector[0] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP and player_mana[1] >= railgun_cost:
                Railgun_toggle[1] = True
                R_bounce_prt1[1] = True
                if Railgun_toggle[1] is True:
                    railgun_mana_collector[1] = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_k:
                moving = not moving

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_e and Left is True and player_mana[0] > blink_cost:
                if cardinal_dir[0] is True:
                    blink_button[0] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEDOWN and Left is False and player_mana[1] > blink_cost:
                if cardinal_dir[1] is True:
                    blink_button[1] = True

    timer()
    if timer_status[0] is True:
        slow_effect = True
        if seconds > 1:
            slow_effect = False
            timer_status[0] = False
            seconds = 0

    if started is False:
        starting()

    if started is True:

        screen.fill(WHITE)
        for player in player_list:
            player.display_p()
            player.move()

        ball.display_circle()
        ball.move_circle(PL1, PL2)
        display_mana()
        growth()
        speed()

    time_passed = clock.tick(fps)
    pygame.display.update()












