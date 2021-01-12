#CS - 1445 Asteroids Project.
#Nichola Burkett and Alex O'Neill.
#12_13_2018.

import matplotlib.pyplot as plt
from matplotlib import transforms 
import numpy as np
import time

#Creating the "SUPER CLASS" SpaceObject. 
class SpaceObject:
    def __init__(self):       
        #Assigning intial values to SpaceObject.  
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.size = 1
        self.color = 'w'
        self.draw()
    #Drawing the SpaceObject.        
    def draw(self):
        self.h = plt.plot(self.position[0], self.position[1], '.w')[0]       
    #Redrawing the figure.       
    def redraw(self):
        self.h.set_xdata([self.position[0]])
        self.h.set_ydata([self.position[1]])
        self.h.set_markersize(self.size)
        self.h.set_color(self.color)       
    #Updating the figure.       
    def update(self, dt):
        self.position = self.position + self.velocity * dt + 0.5 * self.acceleration * dt **2       
        #This is where we wrap the world for the SpaceObjects. 
        if self.position[0] < -10:
            self.position[0] = 10
        elif self.position[0] > 10:
            self.position[0] = -10
        if self.position[1] < -10:
            self.position[1] = 10
        elif self.position[1] > 10:
            self.position[1] = -10
            
        self.velocity = self.velocity + self.acceleration * dt
        self.redraw()       
    #The collides function for any SpaceObject.       
    def collides(self, space_object):
        displacement = self.position - space_object.position
        distance = np.sqrt(sum(displacement**2))
        if distance < self.radius + space_object.radius:
            return True

#Asteroid class and attributes. 
class Asteroid(SpaceObject):
    global level   
    #Assigning initial values to Asteroid. 
    def __init__(self, size = 30):
        SpaceObject.__init__(self)
        self.position = np.zeros(2,)
        self.position[0] = np.random.uniform(-10, 10)
        self.position[1] = np.random.uniform(-10, -9)
        self.color = 'w'
        np.random.uniform(-10, 10, (2,))
        heading = np.random.uniform(0, 2*np.pi)       
        #Here we set the speed of the asteroids depending on the LEVEL. 
        if level == 1:
            speed = size / 10
        elif level == 2:
            speed = (size / 10) * 1.5
        elif level == 3:
            speed = (size / 10) * 2
        elif level == 4:
            speed = (size / 10) * 1.8
        else:
            speed = (size / 10) * 1.5
            
        self.velocity = speed * np.array([np.cos(heading), np.sin(heading)])
        self.size = size
        self.radius = np.sqrt(self.size/np.pi) / 12
        
        #Here we assign a HIT value. 
        self.hit = 0       
    #Drawing the figure.         
    def draw(self):
        print(self.size)
        self.h = plt.plot(self.position[0], self.position[1], marker = 'o', color = self.color, markersize = self.size)[0]

#Spaceship class and atributes.                           
class SpaceShip(SpaceObject):
    global t_value
    global level
    #Initializing the ship and its features. 
    def __init__(self):
        self.size = 2
        self.radius = ((self.size/np.pi)**(1/2)) 
        self.heading = 0
        self.boost = False
        self.boost_reverse = False  
        self.turn_right = False 
        self.turn_left = False
        self.tele_left = 3
        SpaceObject.__init__(self)       
    #Drawing the figure.       
    def draw(self):
        x = self.position[0]
        y = self.position[1]
        dx = self.size * np.cos(np.deg2rad(self.heading))
        dy= self.size * np.sin(np.deg2rad(self.heading))
        lines = plt.plot(x, y, '*r')
        self.h_star = lines[0]
        lines = plt.plot([x, x+dx], [y, y+dy], '-r')
        self.h_nose = lines[0]       
    #Redrawing the figure.        
    def redraw(self):
        x = self.position[0]
        y = self.position[1]
        dx = self.size * np.cos(np.deg2rad(self.heading))
        dy = self.size * np.sin(np.deg2rad(self.heading))
        self.h_star.set_xdata([x])
        self.h_star.set_ydata([y])
        self.h_nose.set_xdata([x, x+dx])
        self.h_nose.set_ydata([y, y+dy])
    #Here is our teleportation function.         
    def tele(self):       
        self.position = np.random.uniform(-10, 10, (2,))
        
    #Functions for our ship...consists of turning and boosting. 
    def restore(self):
        self.hit += 20
           
    def turn_right_on(self):
        self.turn_right = True

    def turn_left_on(self):
        self.turn_left = True
        
    def turn_left_off(self):
        self.turn_left = False
        
    def turn_right_off(self):
        self.turn_right = False
    
    def boost_on(self):
        self.boost = True

    def boost_reverse_on(self):
        self.boost_reverse = True

    def boost_off(self):
        self.boost = False

    def boost_reverse_off(self):
        self.boost_reverse = False
        
    #Updating the ship's position and more.        
    def update(self, dt): 
        #Turning left.       
        if self.turn_left:
            self.heading += 15           
        #Turning right. 
        elif self.turn_right:
            self.heading -= 15           
        #Boost.             
        if self.boost:
            a = 3
            ax = a * np.cos(np.deg2rad(self.heading))
            ay = a * np.sin(np.deg2rad(self.heading))
            self.acceleration = np.array([ax, ay])          
        #Reverse boost.                 
        elif self.boost_reverse == True:
            a = -3
            ax = a * np.cos(np.deg2rad(self.heading))
            ay = a * np.sin(np.deg2rad(self.heading))
            self.acceleration = np.array([ax, ay])           
        else:
            self.acceleration = np.array([0.0, 0.0])

        SpaceObject.update(self, dt)

#Creating and assigning values to the class Bullets. 
class Bullet(SpaceObject):
    bullets = []
    global level
    #Assigning initial values for Bullets.
    def __init__(self, ship):
        SpaceObject.__init__(self) 
        self.fire = False
        self.size = 15
        self.radius = np.sqrt(self.size/np.pi) /2
        self.position = ship.position
        self.heading = np.deg2rad(ship.heading)
        speed = 10
        self.velocity =  speed * np.array([np.cos(self.heading), np.sin(self.heading)])       
    #Delete function       
    def delete(self):
        del self       
    #This is the fire method.    
    def fire_go(self):
        self.fire = True       
    #Updating the figure. 
    def update(self, dt):
        #Selection statments regarding the bullets and WRAPING them. 
        if self.fire == True:
            self.size = 5
            if self.position[0] < -10:
                del self
                return
            elif self.position[0] > 10:
                del self
                return
            if self.position[1] < -10:
                del self
                return
            elif self.position[1] > 10:
                del self
                return
            
        #Not sure why this is here but is seems to work just fine.......IDK.
        #Sets the acceleration for the bullets.
        a = 3
        ax = a * np.cos(self.heading)
        ay = a * np.sin(self.heading)
        self.acceleration = np.array([ax, ay]) 
        self.position = self.position + self.velocity * dt + 0.5 * self.acceleration * dt **2

        #Selection statments regarding the LEVEl the player is on and the color of the bullets. 
        if level == 1:
            self.color = 'w'
        elif level == 2:
            self.color = 'r'
        elif level == 3:
            self.color = 'g'
        elif level == 4:
            self.color = 'y'
        else:
            self.color = 'm'
            
        self.redraw() 

#Updating the game!!!!
def update_game(asteroids, bullets, timer, plt):
    global score
    global lives_left
    global t_value
    global level
    global ship
    global s_score
    global lives_l    
    ship.update(0.1)       
    #Updating the bullets list. 
    for x in range(len(bullets)):
        bullets[x].update(0.1)
    #Detecting if any collions have occured between ship and asteroids.
    #And updating the asteroids.
    for j in range(len(asteroids)):
        if ship.collides(asteroids[j]):
            lives_left -= 1           
            #This is where we redraw the TEXT.
            lives_l.set_text('lives left: %d' % lives_left)           
            #Here... if the ship gets hit we randomly relocate it. 
            ship.position = np.random.uniform(-10, 10, (2,))           
        else:
            asteroids[j].update(0.1)
            
    #Creating empty lists for the deleted bullets. 
    del_bul = []      
    del_ast = []
    
    #Checking for bullet to asteroid collisions.
    for j in range(len(bullets)):   
        for i in range(len(asteroids)):
            if bullets[j].collides(asteroids[i]):
                score += 500
                s_score.set_text('Score: %d' % score)
                del_bul.append(j)              
                asteroids[i].size *= .75
                asteroids[i].hit += 1
                asteroids[i].hit = int(asteroids[i].hit)
                
                #Here we assign the asteroids color based on the HIT value. 
                if asteroids[i].hit == 1:
                    asteroids[i].color = 'g'                  
                elif asteroids[i].hit   == 2:
                    asteroids[i].color = 'y'
                elif asteroids[i].hit == 3:
                    asteroids[i].color = 'r'
                else:
                    del_ast.append(i)
                
    #This is the code to remove bullets and asteroids after impact.
    for y in reversed(del_bul):
        bullets[y].h.remove()
        del bullets[y]
    for k in reversed(del_ast):
        asteroids[k].h.remove()
        del asteroids[k]
        
    #This is where we detect if we WIN the level and move on to the next. 
    if len(asteroids) == 0:
        level += 1
        plt.clf()
        time.sleep(2)
        #This is where we call our GAME LOOP function. 
        start_next_level(level, timer)       
    #Selection statments for our LIVES.     
    if lives_left <= 0:
                plt.clf()
                im = plt.imread("gameOver2.png")
                plt.imshow(im, origin = 'upper',  extent = [10, -10, 10, -10])
                timer.stop()        
        
    #Deleting bullets if they go out of bounds "off the screen".
    for j in range(len(bullets)):
        if bullets[j].position[0] < -10:
            del bullets[j]
            break
        elif bullets[j].position[0] > 10:
            del bullets[j]
            break
        if bullets[j].position[1] < -10:
            del bullets[j]
            break
        elif bullets[j].position[1] > 10:
            del bullets[j]
            break

    plt.draw()

#Creating our game loop function.
def start_next_level(level, timer):
    global asteroids
    global num_asteroids
    global ship
    global lives_left
    global lives_l
    global s_score
    global tele_value
    global t_value
    global score
    global current_level
    #Selection statments to determin the LEVEL the player is on. 
    if level == 2:       
        im = plt.imread("level_2.png")
        plt.imshow(im, origin = 'upper', zorder = 0, extent = [10, -10, 10, -10])
        ship = SpaceShip()     
        tele_value = plt.text(10,-7, 'Teleports Left: %d' % t_value, color = 'w', zorder = 2)
        lives_l = plt.text(10, -9, 'Lives Left: %d ' % lives_left, color = 'w', zorder = 2)
        s_score = plt.text(10, -8, 'Score: %d' % score, color = 'w', zorder = 2)
        current_level = plt.text(10, -6, 'Level: %d' % level, color = 'w', zorder = 2) 
        num_asteroids = np.random.randint(4, 6)
        
        for i in range(num_asteroids):       
            size = np.random.randint(10, 41)
            asteroids.append(Asteroid(size))

    elif level == 3:
        im = plt.imread("level_3.png")
        plt.imshow(im, origin = 'upper', zorder = 0, extent = [10, -10, 10, -10])
        ship = SpaceShip()
        tele_value =  plt.text(10,-7, 'Teleports Left: %d' % t_value, color = 'w', zorder = 2)
        lives_l = plt.text(10, -9, 'Lives Left: %d ' % lives_left, color = 'w', zorder = 2)
        s_score = plt.text(10, -8, 'Score: %d' % score, color = 'w', zorder = 2)
        current_level = plt.text(10, -6, 'Level: %d' % level, color = 'w', zorder = 2) 
        num_asteroids = np.random.randint(6, 8)
        
        for i in range(num_asteroids):       
            size = np.random.randint(10, 41)
            asteroids.append(Asteroid(size))
         
    elif level == 4:
        im = plt.imread("level_4.png")
        plt.imshow(im, origin = 'upper', zorder = 0, extent = [10, -10, 10, -10])
        ship = SpaceShip()
        tele_value =  plt.text(10,-7, 'Teleports Left: %d' % t_value, color = 'w', zorder = 2)
        lives_l = plt.text(10, -9, 'Lives Left: %d ' % lives_left, color = 'w', zorder = 2)
        s_score = plt.text(10, -8, 'Score: %d' % score, color = 'w', zorder = 2)
        current_level = plt.text(10, -6, 'Level: %d' % level, color = 'w', zorder = 2) 
        num_asteroids = np.random.randint(7, 10)
        
        for i in range(num_asteroids):       
            size = np.random.randint(10, 41)
            asteroids.append(Asteroid(size))
            
    elif level ==5:
        im = plt.imread("level_5.png")
        plt.imshow(im, origin = 'upper', zorder = 0, extent = [10, -10, 10, -10])
        ship = SpaceShip()
        tele_value =  plt.text(10,-7, 'Teleports Left: %d' % t_value, color = 'w', zorder = 2)
        lives_l = plt.text(10, -9, 'Lives Left: %d ' % lives_left, color = 'w', zorder = 2)
        s_score = plt.text(10, -8, 'Score: %d' % score, color = 'w', zorder = 2)
        current_level = plt.text(10, -6, 'Level: %d' % level, color = 'w', zorder = 2)       
        num_asteroids = np.random.randint(10, 12)
              
        for i in range(num_asteroids):       
            size = np.random.randint(10, 41)
            asteroids.append(Asteroid(size))
            
    #This is where we detect if the player WINS the game. 
    else:
        timer.stop()
        plt.clf()
        im = plt.imread("youWin.png")
        plt.imshow(im, origin = 'upper',  extent = [10, -10, 10, -10])
        print('Your score was: %d' % score)
        
        
    #Selection statments to determine SIZE of the asteroids. 
    if level == 2:
        size = np.random.randint(8, 31)
        asteroids.append(Asteroid(size)) 
    elif level == 3:
        size = np.random.randint(6, 21)
        asteroids.append(Asteroid(size))
    elif level == 4:
         size = np.random.randint(6, 11)
         asteroids.append(Asteroid(size))
    else:
        size = np.random.randint(6, 10)
        asteroids.append(Asteroid(size))

    def key_press(event):
        if event.key == 'right':
            ship.turn_right_on()
        elif event.key == 'left':
            ship.turn_left_on()
        elif event.key == 'up':
            ship.boost_on()
        elif event.key == 'down':
            ship.boost_reverse_on()
        elif event.key == ' ':
            #Here we limit the amount of bullets that can be shot at one time. 
            if level == 1:
                if len(bullets) < 15:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)
            elif level == 2:
                if len(bullets) < 10:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)
            elif level == 3:
                if len(bullets) < 5:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)
            elif level == 4:
                if len(bullets) < 5:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)
            else:
                if len(bullets) < 3:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)           
        elif event.key == 't':
            if t_value > 0:
                reduce_t() 
                ship.tele()
        elif event.key == 's':
            ship.restore()
            
    def key_release(event):
        if event.key == 'up':
            ship.boost_off()
        elif event.key == 'down':
            ship.boost_reverse_off()
        elif event.key == 'left':
            ship.turn_left_off()
        elif event.key == 'right':
            ship.turn_right_off()
            
#Our MAIN function.    
def main():
    global lives_left
    global level
    global score
    global t_value
    global lives_l
    global s_score
    global tele_value 
    global num_asteroids
    global asteroids
    global ship
    global current_level
    lives_left = 5
    score = 0
    t_value = 3
    level = 1
    #Plotting the figure for level 1. 
    fig, ax= plt.subplots()
    ax.set_facecolor('k')
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    #This is where we give it the cool background.   
    im = plt.imread("space4.png")
    plt.imshow(im, origin = 'upper', zorder = 0, extent = [10, -10, 10, -10])      
    ship = SpaceShip()
    #These are the initial displays for the players information. 
    tele_value =  plt.text(-9, 7, 'Teleports Left: %d' % t_value, color = 'w')
    lives_l = plt.text(-9, 9, 'Lives Left: %d ' % lives_left, color = 'w')
    s_score = plt.text(-9, 8, 'Score: %d' % score, color = 'w')
    current_level = plt.text(-9, 6, 'Level: %d' % level, color = 'w') 
    #Creating the random asteroids and the empty lists. 
    num_asteroids = np.random.randint(3, 4)
    asteroids = []
    bullets = []
    #Assigning random size to asteroids for level 1.
    for i in range(num_asteroids):       
        size = np.random.randint(10, 41)
        asteroids.append(Asteroid(size))           
    #This is where we reduce the t_value.       
    def reduce_t():
        global t_value
        t_value -= 1
        tele_value.set_text('Teleports left: %d' % t_value)       
    def key_press(event):
        if event.key == 'right':
            ship.turn_right_on()
        elif event.key == 'left':
            ship.turn_left_on()
        elif event.key == 'up':
            ship.boost_on()
        elif event.key == 'down':
            ship.boost_reverse_on()
        elif event.key == ' ':
            #Here we limit the amount of bullets that can be shot at one time. 
            if level == 1:
                if len(bullets) < 15:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)
            elif level == 2:
                if len(bullets) < 10:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)
            elif level == 3:
                if len(bullets) < 5:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)
            elif level == 4:
                if len(bullets) < 5:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)
            else:
                if len(bullets) < 3:
                    bullet = Bullet(ship)
                    bullet.fire_go()
                    bullets.append(bullet)           
        elif event.key == 't':
            if t_value > 0:
                reduce_t() 
                ship.tele()
        elif event.key == 's':
            ship.restore() 
                
    def key_release(event):
        if event.key == 'up':
            ship.boost_off()
        elif event.key == 'down':
            ship.boost_reverse_off()
        elif event.key == 'left':
            ship.turn_left_off()
        elif event.key == 'right':
            ship.turn_right_off()

    fig.canvas.mpl_connect('key_press_event', key_press)
    fig.canvas.mpl_connect('key_release_event', key_release)
    timer = fig.canvas.new_timer(interval=100)
    timer.add_callback(update_game, asteroids, bullets, timer, plt)
    timer.start()
    plt.show() 

if __name__ == '__main__':
    main()
