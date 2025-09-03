# Author: Rafia (rafia289)
# Contribution markers: search for ">>> RAFIA FEATURE" to review my parts

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random, time, math
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

w,h= 1200,700
player=[0,-250,0] #load screen view
player_z=0
p_color=[0.4,0.5,0]
p_size=20
jump=False
jump_speed=450
gravity=-950
tiles_l=60
tiles_s=10
movement=[-240,-180,-120, -60,0,60, 120,180,240]

floor=[]
num_tiles=35
obstacle=[]

# >>> RAFIA FEATURE: health increase (data) (BEGIN)
health=[]
# >>> RAFIA FEATURE: health increase (data) (END)

checkpoint=[]
collected=0
hp=100
level=1
speed=220
msg=None
game_state="menu"
last_time=time.time()
game_time=30
y=5000

# >>> RAFIA FEATURE: scenery sideway (data) (BEGIN)
objects=[]
count=40
respan=num_tiles*tiles_l*2
x1=(tiles_s*tiles_l)//2+80
# >>> RAFIA FEATURE: scenery sideway (data) (END)

# >>> RAFIA FEATURE: sky meteor effect (data) (BEGIN)
sky_t=0
sky_color=[0.2,0.5,0.9]
meteors=[]
# >>> RAFIA FEATURE: sky meteor effect (data) (END)

def player1():
    glPushMatrix()
    glTranslatef(*player)
    glRotatef(180,0,0,1)
    glColor3f(*p_color)
    glPushMatrix()
    glTranslatef(0,0,p_size)       # player on the load screen player view witha cube
    glutSolidCube(p_size)
    glPopMatrix()
    glColor3f(1,0.8,0.6)
    glPushMatrix()
    glTranslatef(0,0,p_size*2)
    glutSolidSphere(p_size/2,16,16)
    glPopMatrix()
    glColor3f(0,0,1)
    glPushMatrix()
    glTranslatef(-p_size/3,-p_size/3,0)
    gluCylinder(gluNewQuadric(), p_size/4,p_size/4,p_size,10,10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(p_size/3,-p_size/3,0)
    gluCylinder(gluNewQuadric(), p_size/4,p_size/4,p_size,10,10)
    glPopMatrix()
    glPopMatrix()

def color():
    return[random.random(),random.random(),random.random()]

def init_floor():
    floor.clear()
    for i in range(num_tiles):                                     
        floor.append({'y': i*tiles_l, 'color': color()})            #makes the running effect

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, w, 0, h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def floors():
    half_size = tiles_s // 2
    glBegin(GL_QUADS)
    for i in floor:
        y = i['y']
        color_v = i['color']
        glColor3f(*color_v)
        for i in range(-half_size, half_size):
            for j in range(-half_size, half_size):
                x_left = i*tiles_l                       #draws colorful tiles in loop for endless road effect
                x_right = (i+1)*tiles_l
                y_bottom = j*tiles_l + y
                y_top = (j+1)*tiles_l + y
                glVertex3f(x_left, y_bottom, 0)
                glVertex3f(x_right, y_bottom, 0)
                glVertex3f(x_right, y_top, 0)
                glVertex3f(x_left, y_top, 0)
    glEnd()

def s_obstacles(y):
    road = random.choice(movement)
    if level==1:
        size = random.randint(20,30)
        damage = 10
        color = [0,1,0]
        ob_type = "tree"
    elif level==2:
        size = random.randint(20,30)
        damage = 25
        color = [0.7,0,0]
        ob_type = "spike"
    else:
        size = random.randint(20,30)
        damage = 33
        color = [0.7,0,0.7]
        ob_type = "monster"
    obstacle.append({'x': road, 'y': y, 'z': size//2, 'size': size, 'damage': damage, 'color': color, 'type': ob_type})

# >>> RAFIA FEATURE: health increase (spawn + draw) (BEGIN)
def s_health(y):
    road = random.choice(movement)
    size = 20
    health.append({'x': road, 'y': y, 'z': size//2, 'size': size, 'heal': 5})

def create_health(p):
    x = p['x']
    y = p['y']
    z = p['z']
    glColor3f(1,0,0)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(0.3,1,1)
    glutSolidCube(p['size'])
    glPopMatrix()                         #always rorates
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(1,0.3,1)
    glutSolidCube(p['size'])
    glPopMatrix()
# >>> RAFIA FEATURE: health increase (spawn + draw) (END)

def create_obstacle(ob):
    glPushMatrix()
    glTranslatef(ob['x'], ob['y'], ob['z'])
    glColor3f(*ob['color'])
    if ob['type'] == "tree":

        glPushMatrix()
        glTranslatef(0, 0, -ob['size'] // 2)
        glColor3f(0.25, 0.1, 0.05) 
        gluCylinder(gluNewQuadric(), ob['size'] // 8, ob['size'] // 10, ob['size'] * 1.5, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0, ob['size'])
        glColor3f(0.0, 0.3, 0.0)  
        glutSolidSphere(ob['size'] // 1.5, 16, 16)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(ob['size']//5, -ob['size']//2, ob['size'])  
        glColor3f(1, 0, 0)  # red
        glutSolidSphere(ob['size']//6, 8, 8 )
        glPopMatrix()                                                    ##red eyes
        glPushMatrix()
        glTranslatef(-ob['size']//5, -ob['size']//2, ob['size'])  
        glColor3f(1, 0, 0)  # red
        glutSolidSphere(ob['size']//6, 8, 8 )
        glPopMatrix()
    elif ob['type'] == "spike":
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.8, 0.0, 0.0)  
        glutSolidCone(ob['size']//2, ob['size'], 10, 10)
        glPopMatrix()

    elif ob['type'] == "monster":
        x = player[0] - ob['x']
        y = player[1] - ob['y']
        angle = math.degrees(math.atan2(y, x))  
        glPushMatrix()
        glRotatef(-angle, 0, 0, 1) ###for rotatinon toward player
             
        glPushMatrix()
        glTranslatef(-ob['size']//2, ob['size']//2, ob['size']//1.5)
        glColor3f(1, 0, 0)  
        glutSolidSphere(ob['size']//4, 10, 10)
        glPopMatrix()                                                 #eyes
        glPushMatrix()
        glTranslatef(ob['size']//2, ob['size']//2, ob['size']//1.5)
        glColor3f(1, 0, 0) 
        glutSolidSphere(ob['size']//4, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.2, 0.2, 0.2)  #body
        glutSolidSphere(ob['size'], 20, 20)
        glPopMatrix()  

        glPushMatrix()
        glTranslatef(-ob['size']//2, ob['size'], ob['size']//2)
        glRotatef(-90, 1, 0, 0)          #horn
        glColor3f(0.7, 0.7, 0.7)
        glutSolidCone(ob['size']//5, ob['size'], 10, 10)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(ob['size']//2, ob['size'], ob['size']//2)
        glRotatef(-90, 1, 0, 0)
        glColor3f(0.7, 0.7, 0.7)
        glutSolidCone(ob['size']//5, ob['size'], 10, 10)
        glPopMatrix()

        glPopMatrix() 
    glPopMatrix()

def init_checkpoints():
    global checkpoint
    checkpoint.clear()
def s_checkpoints(y):
    road = random.choice(movement)
    checkpoint.append({
        'x': road,
        'y': y,
        'z': p_size,
        'collected': False,
        'angle': 0
    })
def create_checkpoints(cp):
    glPushMatrix()
    glTranslatef(cp['x'], cp['y'], cp['z'])
    glColor3f(1,1,1)
    glRotatef(cp['angle'], 0,0,1)  # rotate 
    glutSolidCube(p_size)
    glPopMatrix()

def update_checkpoints(dt):
    global collected
    remove_cp = []
    for i in checkpoint:
        i['y'] -= speed * dt  
        i['angle'] += 90*dt  
        if not i["collected"]:
         if abs(i['x'] - player[0]) < p_size:
            if abs(i['y'] - player[1]) < p_size:   ###checks x y z value if its collided or not
                 if player[2] < p_size:  
                     i['collected'] = True
                     collected += 1
                     show_floating_text(f"Checkpoint Collected! ({collected})", 2.5)
        if i['y'] < player[1] - 200:
            remove_cp.append(i)   ##remove checkpoint if its passed
    for j in remove_cp:
        if j in checkpoint:
            checkpoint.remove(j)

def show_floating_text(text,duration=2.5):
    global floating_msg
    floating_msg = {'text': text,'expires_at':time.time()+duration}

def clear_floating_text():
    global floating_msg
    floating_msg = None

# >>> RAFIA FEATURE: scenery sideway (helpers) (BEGIN)
def random_x():
    base = x1 + random.randint(0, 80)
    return random.choice([-base, base])

def init_scenery():
    objects.clear()
    for i in range(count):
        y = i * (tiles_l * 2)
        objects.append(spawn_scenery(y))

def spawn_scenery(y):
    t = random.choice(["tree", "building", "mountain"])
    x = random_x()
    if t == "tree":
        size = random.randint(35, 75)
        return {'type': 'tree','x': x, 'y': y, 'z': size//2,'size': size, 'trunk_h': size, 'trunk_r': max(6, size//8),'leaf_r': max(18, size//2),'leaf_color': [0, 1, 0],'trunk_color': [0.55, 0.27,0.07]}
    if t == "building":
        size = random.randint(50, 110)
        floors = random.randint(2, 5)
        return {'type': 'building', 'x': x, 'y': y, 'z': size//2,'size': size, 'floors': floors,'color': [0.6 + random.random()*0.3, 0.6 + random.random()*0.3, 0.6 + random.random()*0.3]}
    base = random.randint(60, 120)
    height = random.randint(80, 180)
    return {'type': 'mountain', 'x': x, 'y': y, 'z': height//2, 'base': base, 'height': height, 'color': [0.5,0.4,0.35]}

def create_scenery(sc):
    glPushMatrix()
    glTranslatef(sc['x'], sc['y'], sc['z'])
    if sc['type'] == 'building':
        glColor3f(*sc['color'])
        glPushMatrix()
        glScalef(1.2, 1.0, 2.0 + 0.3*sc['floors'])
        glutSolidCube(sc['size'])
        glPopMatrix()
    elif sc['type'] == 'tree':
        glPushMatrix()
        glTranslatef(0, 0, -sc['size']//2)
        glColor3f(*sc['trunk_color'])
        gluCylinder(gluNewQuadric(), sc['trunk_r'], sc['trunk_r'], sc['trunk_h'], 12, 12)
        glPopMatrix()
        glColor3f(*sc['leaf_color'])
        glutSolidSphere(sc['leaf_r'], 18, 18)
    elif sc['type'] == 'mountain':
        glColor3f(*sc['color'])
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        glutSolidCone(sc['base'], sc['height'], 18, 18)
        glPopMatrix()
    glPopMatrix()
# >>> RAFIA FEATURE: scenery sideway (helpers) (END)

# >>> RAFIA FEATURE: sky meteor effect (logic) (BEGIN)
def spawn_meteor():
    if level != 3:
        return  

    y = player[1] + random.randint(800, 1500) 
    x = player[0] + random.randint(-300, 300)  
    z = player[2] + random.randint(300, 600)   # high in the sky
    size = random.randint(15, 25)
    speed_y = random.uniform(200, 350)         # falling toward player
    speed_z = random.uniform(50, 100)          # falling down
    meteors.append({'x': x, 'y': y, 'z': z, 'size': size, 'speed_y': speed_y, 'speed_z': speed_z})


def create_meteors(dt):
    remove = []
    for m in meteors:
        glPushMatrix()
        glColor3f(1.0, 0.8, 0.0)  # fiery color
        glTranslatef(m['x'], m['y'], m['z'])
        glutSolidSphere(m['size'], 16, 16)
        glPopMatrix()
        m['y'] -= m['speed_y'] * dt
        m['z'] -= m['speed_z'] * dt  # falling down
        if m['y'] < player[1] - 200 or m['z'] < 0:
            remove.append(m)
    for m in remove:
        meteors.remove(m)
    if random.random() < 0.3:
        spawn_meteor()
# >>> RAFIA FEATURE: sky meteor effect (logic) (END)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w/h, 0.2, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(player[0], player[1]-300, player[2]+120,
              player[0], player[1]+50, player[2]+20, 0, 0, 1)

def keyboardListener(key, x, y):
    global jump, z, game_state, p_color
    k = key.lower()
    if game_state=="menu":
      if k == b'g':  # Gray
        p_color = [0.5, 0.5, 0.5]
      elif k == b'r':  # Red
        p_color = [1, 0, 0]
      elif k == b'b':  # Blue
        p_color = [0, 0, 0]
      elif k==b'\r':
            start_game()
    elif k==b'p':
        if game_state=="playing":
                game_state="paused"
                show_floating_text("Game Paused",3.0)
        elif game_state=="paused":
                game_state="playing"
                show_floating_text("Resumed",2.5)
    else:
        if k==b'a':
            player[0]-=60
            if player[0]<movement[0]:
                player[0]=movement[0]
        elif k==b'd':                     
            player[0]+=60
            if player[0]>movement[-1]:
                player[0]=movement[-1]
        elif k==b' ':
            if not jump:
                z = jump_speed
                jump = True
        elif k==b'r':
            restart_game()

def start_game():
    global game_state, game_timer, collected
    collected = 0
    game_state="playing"
    game_timer=30.0
    restart_game()
    init_checkpoints()

def restart_game():
    global obstacle, health, hp, player, z, jump, level, speed, meteors, checkpoint, collected
    obstacle.clear()

    # >>> RAFIA FEATURE: reset (BEGIN)
    health.clear()
    checkpoint.clear()
    collected = 0
    hp= 100
    level = 1
    speed = 220
    player[:] = [0, -200, 0]
    z = 0
    jump = False
    # >>> RAFIA FEATURE: reset (END)

    init_floor()

    # >>> RAFIA FEATURE: scenery sideway (init) (BEGIN)
    init_scenery()
    # >>> RAFIA FEATURE: scenery sideway (init) (END)

    # >>> RAFIA FEATURE: sky meteor effect (reset) (BEGIN)
    meteors.clear()
    # >>> RAFIA FEATURE: sky meteor effect (reset) (END)

    show_floating_text("Game started",2.5)
    init_checkpoints()

# >>> RAFIA FEATURE: sky meteor effect (sky color anim) (BEGIN)
def change_sky(dt):
    global sky_t, sky_color
    sky_t += dt
    if level == 3:
        r = 0.5 + 0.5*math.sin(sky_t*5) + random.uniform(-0.2,0.2)
        g = 0.0 + 0.3*math.sin(sky_t*2) + random.uniform(-0.2,0.2)
        b = 0.1 + 0.3*math.sin(sky_t*3) + random.uniform(-0.2,0.2)
        sky_color = [max(0,min(1,r)), max(0,min(1,g)), max(0,min(1,b))]
    else:
        sky_color = [0.2, 0.5, 0.9]
# >>> RAFIA FEATURE: sky meteor effect (sky color anim) (END)

def showScreen():
    glClearColor(*sky_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0,0,w,h)
    setupCamera()

    # >>> RAFIA FEATURE: sky meteor effect (draw tick) (BEGIN)
    create_meteors(0)
    # >>> RAFIA FEATURE: sky meteor effect (draw tick) (END)

    floors()

    # >>> RAFIA FEATURE: scenery sideway (draw) (BEGIN)
    for i in objects:
        create_scenery(i)
    # >>> RAFIA FEATURE: scenery sideway (draw) (END)

    if game_state=="menu":
        draw_text(w//2-120,h//2+40,"  Obstacle Game ",GLUT_BITMAP_HELVETICA_18)
        draw_text(w//2-120,h//2+10," Choose Player Color: G -grey R -Red B -Black",GLUT_BITMAP_HELVETICA_18)
        draw_text(w//2-120,h//2-50,"Press Enter to Start",GLUT_BITMAP_HELVETICA_18)
        draw_text(w//2-120,h//2-30,"Red block is health ",GLUT_BITMAP_HELVETICA_18)
        draw_text(w//2-120,h//2-10,"collect white checkpoints",GLUT_BITMAP_HELVETICA_18)
    else:
        for i in obstacle:
            create_obstacle(i)

        # >>> RAFIA FEATURE: health increase (draw) (BEGIN)
        for i in health:
            create_health(i)
        # >>> RAFIA FEATURE: health increase (draw) (END)

        for i in checkpoint:
            if not i['collected']:
                create_checkpoints(i)
        player1()
        draw_text(10,h-30,f"HP: {int(hp)}")
        draw_text(10,h-50,f"Level: {level}")
        draw_text(10,h-70,f"Time: {int(game_timer)}")
        draw_text(10,h-90,f"Checkpoints: {collected}")
        if floating_msg:
            draw_text(w//2-180,h-40,floating_msg['text'])
    glutSwapBuffers()

def idle():
    global last_time, player, z, jump, obstacle, health, hp, level, speed, game_state, game_timer
    now = time.time()
    dt = now - last_time
    last_time = now
    if game_state!="playing":
        glutPostRedisplay()
        return

    # >>> RAFIA FEATURE: sky meteor effect (animate sky) (BEGIN)
    change_sky(dt)
    # >>> RAFIA FEATURE: sky meteor effect (animate sky) (END)

    game_timer -= dt
    if game_timer <= 0:
        if level == 1:
            level = 2
            speed = 280
            game_timer = 30.0
            obstacle.clear()
            health.clear()
            show_floating_text("Level 2!", 2.0)
        elif level == 2:
            level = 3
            speed = 330
            game_timer = 40.0
            obstacle.clear()
            health.clear()
            show_floating_text("Level 3!", 2.0)
        elif level == 3:
            # >>> RAFIA FEATURE: win screen final checkpoint (BEGIN)
            show_floating_text(f"YEEE! You Have Done It! Congratulations! Checkpoints: {collected}",7.0)
            game_state="finished"
            # >>> RAFIA FEATURE: win screen final checkpoint (END)

    for i in floor:
        i['y'] -= speed*dt
        if i['y']<-num_tiles*tiles_l:
            i['y'] += num_tiles*tiles_l
            i['color'] = color()
            if random.random()<0.4:
                s_obstacles(i['y'] + tiles_l*num_tiles/2)

            # >>> RAFIA FEATURE: health increase (spawn) (BEGIN)
            if random.random()<0.1:
                s_health(i['y'] + tiles_l*num_tiles/2)
            # >>> RAFIA FEATURE: health increase (spawn) (END)

    # >>> RAFIA FEATURE: scenery sideway (scroll/update) (BEGIN)
    for i in objects:
        i['y'] -= speed*dt
        if i['y'] < -respan:
            sc_new_y = i['y'] + respan + tiles_l*random.randint(4, 10)
            new_sc = spawn_scenery(sc_new_y)
            i.update(new_sc)
    # >>> RAFIA FEATURE: scenery sideway (scroll/update) (END)

    if jump:
        z += gravity*dt
        player[2] += z*dt
        if player[2]<=0:
            player[2]=0
            z=0
            jump=False

    remove_obs=[]
    for i in obstacle:
        i['y']-=speed*dt
        if abs(i['y']-player[1])<p_size and abs(i['x']-player[0])<p_size:
            if player[2]<p_size:
                hp-=i['damage']
                remove_obs.append(i)
                show_floating_text(f"-{i['damage']} HP",1.0)
                if hp<=0:
                    show_floating_text("Game Over!",3.0)
                    game_state="menu"
    for ob in remove_obs:
        if ob in obstacle:
            obstacle.remove(ob)

    # >>> RAFIA FEATURE: health increase (collect/heal) (BEGIN)
    remove_potion=[]
    for p in health:
        p['y']-=speed*dt
        if abs(p['y']-player[1])<p_size and abs(p['x']-player[0])<p_size:
            if player[2]<p_size:
                hp+=p['heal']
                if hp>100: hp=100
                remove_potion.append(p)
                show_floating_text(f"+{p['heal']} HP",1.0)
    for p in remove_potion:
        if p in health:
            health.remove(p)
    # >>> RAFIA FEATURE: health increase (collect/heal) (END)
            
    for i in floor:
     i['y'] -= speed*dt
     if i['y'] < -num_tiles*tiles_l:
        i['y'] += num_tiles*tiles_l
        i['color'] = color()
        if random.random() < 0.4:
            s_obstacles(i['y'] + num_tiles*tiles_l/2)

        # >>> RAFIA FEATURE: health increase (spawn 2nd loop) (BEGIN)
        if random.random() < 0.1:
            s_health(i['y'] + num_tiles*tiles_l/2)
        # >>> RAFIA FEATURE: health increase (spawn 2nd loop) (END)

        if random.random() < 0.05:
            s_checkpoints(i['y'] +num_tiles*tiles_l/2)

    update_checkpoints(dt)

    # >>> RAFIA FEATURE: sky meteor effect (tick) (BEGIN)
    if level == 3:
     create_meteors(dt)
    # >>> RAFIA FEATURE: sky meteor effect (tick) (END)

    glutPostRedisplay()

def main():
    global last_time
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(w, h)
    glutInitWindowPosition(150,0)
    glutCreateWindow(b"3D obstacle")
    glEnable(GL_DEPTH_TEST)
    init_floor()

    # >>> RAFIA FEATURE: scenery sideway (init at start) (BEGIN)
    init_scenery()
    # >>> RAFIA FEATURE: scenery sideway (init at start) (END)

    init_checkpoints()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(idle)
    last_time=time.time()
    glutMainLoop()

if __name__=="__main__":
    main()