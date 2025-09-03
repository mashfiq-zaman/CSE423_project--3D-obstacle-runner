#Rahat Ahmed -22101689

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
health=[]
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

#scenes
objects=[]
count=40
respan=num_tiles*tiles_l*2
x1=(tiles_s*tiles_l)//2+80
sky_t=0
sky_color=[0.2,0.5,0.9]
meteors=[]

# --- stability: initialize floating message used by show_floating_text ---
floating_msg = None  

def player1():
    glPushMatrix()
    glTranslatef(*player)
    glRotatef(180,0,0,1)
    glColor3f(*p_color)
    glPushMatrix()
    glTranslatef(0,0,p_size)       
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
        glColor3f(1, 0, 0)  
        glutSolidSphere(ob['size']//6, 8, 8)
        glPopMatrix()                                                    
        glPushMatrix()
        glTranslatef(-ob['size']//5, -ob['size']//2, ob['size'])  
        glColor3f(1, 0, 0)  
        glutSolidSphere(ob['size']//6, 8, 8)
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
        glRotatef(-angle, 0, 0, 1) 
        glPushMatrix()
        glTranslatef(-ob['size']//2, ob['size']//2, ob['size']//1.5)
        glColor3f(1, 0, 0)  
        glutSolidSphere(ob['size']//4, 10, 10)
        glPopMatrix()                                                 
        glPushMatrix()
        glTranslatef(ob['size']//2, ob['size']//2, ob['size']//1.5)
        glColor3f(1, 0, 0) 
        glutSolidSphere(ob['size']//4, 10, 10)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.2, 0.2, 0.2)  
        glutSolidSphere(ob['size'], 20, 20)
        glPopMatrix()  
        glPushMatrix()
        glTranslatef(-ob['size']//2, ob['size'], ob['size']//2)
        glRotatef(-90, 1, 0, 0)          
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

def show_floating_text(text,duration=2.5):
    global floating_msg
    floating_msg = {'text': text,'expires_at':time.time()+duration}

def clear_floating_text():
    global floating_msg
    floating_msg = None

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glDisable(GL_DEPTH_TEST)
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
    glEnable(GL_DEPTH_TEST)

# >>> MY FEATURE: player color selection (menu) (BEGIN) Rahat Ahmed Jobu
def keyboardListener(key, x, y):
    global jump, player_z, game_state, p_color
    k = key.lower()

    if game_state=="menu":
        if k == b'g':      
            p_color = [0.5, 0.5, 0.5]
        elif k == b'r':    
            p_color = [1, 0, 0]
        elif k == b'b':    
            p_color = [0, 0, 1]
        elif k == b'\r':   
            start_game()
        return

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
            player_z = jump_speed
            jump = True
    elif k==b'r':
        restart_game()
    elif k==b'p':
        if game_state=="playing":
            game_state="paused"
            show_floating_text("Game Paused",3.0)
        elif game_state=="paused":
            game_state="playing"
            show_floating_text("Resumed",2.5)
# >>> MY FEATURE: player color selection (menu) (END) Rahat Ahmed

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, w/h, 0.2, 3000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(player[0], player[1]-300, player[2]+120,
              player[0], player[1]+50, player[2]+20, 0, 0, 1)

def start_game():
    global game_state, game_timer, collected, hp, player, player_z, jump
    collected = 0
    hp = 100
    player[:] = [0, -200, 0]
    player_z = 0
    jump = False
    game_state="playing"
    game_timer=30.0
    restart_game()

def restart_game():
    global obstacle, health, hp, player, player_z, jump, level, speed, meteors, checkpoint, collected
    obstacle.clear()
    health.clear()
    checkpoint.clear()
    collected = 0
    hp= 100
    level = 1
    speed = 220
    player[:] = [0, -200, 0]
    player_z = 0
    jump = False
    init_floor()           
    meteors.clear()
    show_floating_text("Game started",2.5)
    init_checkpoints()     

# >>> MY FEATURE: moving platforms (BEGIN) Rahat Ahmed
def init_floor():
    floor.clear()
    for i in range(num_tiles):
        floor.append({'y': i*tiles_l, 'color': [random.random(), random.random(), random.random()]})

def floors():
    half_size = tiles_s // 2
    glBegin(GL_QUADS)
    for tile in floor:
        y0 = tile['y']
        glColor3f(*tile['color'])
        for ix in range(-half_size, half_size):
            for iy in range(-half_size, half_size):
                x_left  = ix * tiles_l
                x_right = (ix + 1) * tiles_l
                y_bot   = iy * tiles_l + y0
                y_top   = (iy + 1) * tiles_l + y0
                glVertex3f(x_left,  y_bot, 0)
                glVertex3f(x_right, y_bot, 0)
                glVertex3f(x_right, y_top, 0)
                glVertex3f(x_left,  y_top, 0)
    glEnd()
# >>> MY FEATURE: moving platforms (END) Rahat Ahmed

# >>> MY FEATURE: checkpoints (BEGIN) Rahat Ahmed
def init_checkpoints():
    checkpoint.clear()

def s_checkpoints(y):
    road = random.choice(movement)
    checkpoint.append({
        'x': road,
        'y': y,
        'z': p_size,
        'collected': False,
        'angle': 0.0
    })

def create_checkpoints(cp):
    glPushMatrix()
    glTranslatef(cp['x'], cp['y'], cp['z'])
    glColor3f(1,1,1)
    glRotatef(cp['angle'], 0,0,1)
    glutSolidCube(p_size)
    glPopMatrix()

def update_checkpoints(dt):
    global collected
    remove_cp = []
    for i in checkpoint:
        i['y'] -= speed * dt
        i['angle'] += 90 * dt
        if not i['collected']:
            if abs(i['x'] - player[0]) < p_size and abs(i['y'] - player[1]) < p_size and player[2] < p_size:
                i['collected'] = True
                collected += 1
                show_floating_text(f"Checkpoint Collected! ({collected})", 2.5)
        if i['y'] < player[1] - 200:
            remove_cp.append(i)
    for j in remove_cp:
        if j in checkpoint:
            checkpoint.remove(j)
# >>> MY FEATURE: checkpoints (END)

def showScreen():
    glClearColor(*sky_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0,0,w,h)
    setupCamera()

    floors()  # >>> MY FEATURE Rahat Ahmed

    if game_state=="menu":
        draw_text(w//2-120,h//2+40,"  Obstacle Game ",GLUT_BITMAP_HELVETICA_18)
        draw_text(w//2-250,h//2+10," Choose Player Color: G -Grey  R -Red  B -Blue",GLUT_BITMAP_HELVETICA_18)
        draw_text(w//2-120,h//2-50,"Press Enter to Start",GLUT_BITMAP_HELVETICA_18)
        draw_text(w//2-120,h//2-30,"Red block is health ",GLUT_BITMAP_HELVETICA_18)
        draw_text(w//2-160,h//2-10,"Collect white checkpoints",GLUT_BITMAP_HELVETICA_18)
    else:
        for i in obstacle:
            create_obstacle(i)

        for cp in checkpoint:
            if not cp['collected']:
                create_checkpoints(cp)

        player1()
        draw_text(10,h-30,f"HP: {int(hp)}")
        draw_text(10,h-50,f"Level: {level}")
        draw_text(10,h-70,f"Time: {int(game_timer)}")   # >>> MY FEATURE Rahat Ahmed
        draw_text(10,h-90,f"Checkpoints: {collected}") # >>> MY FEATURE Rahat Ahmed
        if floating_msg:
            draw_text(w//2-180,h-40,floating_msg['text'])
    glutSwapBuffers()

def idle():
    global last_time, player, player_z, jump, obstacle, health, hp, level, speed, game_state, game_timer
    now = time.time()
    dt = now - last_time
    last_time = now

    if game_state!="playing":
        glutPostRedisplay()
        return

    # >>> MY FEATURE: level timer & progression
    game_timer -= dt
    if game_timer <= 0:
        if level == 1:
            level = 2; speed = 280; game_timer = 30.0
            obstacle.clear(); health.clear()
            show_floating_text("Level 2!", 2.0)
        elif level == 2:
            level = 3; speed = 330; game_timer = 40.0
            obstacle.clear(); health.clear()
            show_floating_text("Level 3!", 2.0)
        else:
            show_floating_text(f"YEEE! You Have Done It! Congratulations! Checkpoints: {collected}", 7.0)
            game_state="finished"

    # >>> MY FEATURE: move floor + spawn checkpoints
    for t in floor:
        t['y'] -= speed * dt
        if t['y'] < -num_tiles * tiles_l:
            t['y'] += num_tiles * tiles_l
            t['color'] = [random.random(), random.random(), random.random()]
            if random.random() < 0.4:
                s_obstacles(t['y'] + num_tiles*tiles_l/2)
            if random.random() < 0.05:
                s_checkpoints(t['y'] + num_tiles*tiles_l/2)

    if jump:
        player_z += gravity*dt
        player[2] += player_z*dt
        if player[2]<=0:
            player[2]=0
            player_z=0
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

    update_checkpoints(dt)  # >>> MY FEATURE Rahat Ahmed

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
    init_checkpoints()  

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutIdleFunc(idle)
    last_time=time.time()
    glutMainLoop()

if __name__=="__main__":
    main()
