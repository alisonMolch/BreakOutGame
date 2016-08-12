# gameplay.py
# Jake Zeisel jaz48, Alison Molchadsky
# 12/10/2014
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Gameplay represent a single game.  If you want to restart a new game,
you are expected to make a new instance of Gameplay.

The subcontroller Gameplay manages the paddle, ball, and bricks.  These are model
objects.  The ball and the bricks are represented by classes stored in models.py.
The paddle does not need a new class (unless you want one), as it is an instance
of GRectangle provided by game2d.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Gameplay can only access attributes in models.py via getters/setters
# Gameplay is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Gameplay(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the ball, removing any bricks as necessary.  When the game is
    won, it stops animating.  You should create a NEW instance of 
    Gameplay (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.
    
    INSTANCE ATTRIBUTES:
        _wall   [BrickWall]:  the bricks still remaining 
        _paddle [GRectangle]: the paddle to play with 
        _ball [Ball, or None if waiting for a serve]: 
            the ball to animate
        _last [GPoint, or None if mouse button is not pressed]:  
            last mouse position (if Button pressed)
        _tries  [int >= 0]:   the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in call Breakout. It is okay if you do, but
    you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or
    setter for any attribute that you need to access in Breakout.  Only add
    the getters and setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    might want to make a Paddle class for your paddle.  If you make changes,
    please change the invariants above.  Also, if you add more attributes,
    put them and their invariants below.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _lasttouch [GPoint attribute with x and y coordinate]
            the last position that was clicked
      """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def __init__(self,wall= BrickWall(), tries = 3):
        """Initializer: intializes the game. Parameter wall is assigned to
        attribute _wall and parameter tries is assigned to _tries. wall is
        the constructure Brickwall() by default and tries is 3 by default. Initializes
        _last as none and _ball as none. Initiliazes the paddle as a GRectangle with certain
        attributes specified in constants
        
        Precondition: wall is a list of GRectangles. tries is an int"""
        
        self._wall = wall
        self._last =None
        self._tries = tries
        self._paddle = GRectangle(x=GAME_WIDTH/2-PADDLE_WIDTH/2,y=PADDLE_OFFSET,width=PADDLE_WIDTH,\
                                  height=PADDLE_HEIGHT, fillcolor=colormodel.BLACK,\
                                  linecolor = colormodel.RED)
        self._ball = None

    def getTries(self):
        """Returns: the number of tries in the game"""
        return self._tries

    def setTries(self):
        """sets the number of tries to one less the number of tries.
        decreases the number of tries by one."""
        self._tries = self._tries-1

    def makeball(self):
        """Creates the ball by calling the Ball() constructor"""
        self._ball = Ball()

    def getlast(self):
        """Returns: the GPoint of the last touch"""
        return self._last

    def getpaddle(self):
        """Returns: the GRectangle associated with the paddle."""
        return self._paddle

    def getball(self):
        """Returns: the ball of this game."""
        return self._ball
    
    def draw(self,view):
        """Draws the gameplay objects [wall, paddle,and ball] to the view.
        Draws GObjects."""
        self._wall.draw(view)
        self._paddle.draw(view)
        if self._ball != None:
            self._ball.draw(view)
    
    
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL

    def updatePaddle(self, point):
        """Updates the x and y locations depending on the location of the
        last touch. The first touch must be in the paddle
        in order for it to affect the location of the paddle and the first touch does not
        move the paddle. This function ensures the the paddle does not teleport,
        if you click anywhere on the screen it will not move.
        
        Precondition:point is a GPoint object."""
        
        if point != None:
            if self._last == None and self._paddle.contains(point.x,point.y):
                self._last = point
            elif self._last != None:
                self._paddle.x = self._paddle.x - (self._last.x - point.x)
                self._paddle.x = min(self._paddle.x,GAME_WIDTH-PADDLE_WIDTH)
                self._paddle.x = max(self._paddle.x, 0)
                self._last = point
        else:
            self._last = None
            
    def updateball(self):
        """Updates the coordinates of the center of the ball by adding the velocity."""
        self._ball.setCenterX( self._ball.getcenterx() + self._ball.get_x_velocity())
        self._ball.setCenterY( self._ball.getcentery() + self._ball.get_y_velocity())

    def updatespeed(self):
        """Updates the speed of the if the ball collides with the paddle"""
        if self._getCollidingObject() == self._paddle:
            self._ball.set_y_velocity(self._ball.get_y_velocity() - ACCEL)
            self._ball.set_y_velocity(max(self._ball.get_y_velocity(),MAX_V))
            print self._ball.get_y_velocity()
        
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION

    def checkwalls(self):
        """Checks to see if the ball collides with the sides and the top
        of the screen. if it collides with the sides it sets the x velocity to -x velocity.
        if it collides with the top of the screen it sets the y velocity to -y velocity."""

        if self._ball.get_y_velocity() >= 0:
            if self._ball.getcentery() >= GAME_HEIGHT - BALL_RADIUS:
                self._ball.set_y_velocity( -(self._ball.get_y_velocity()))
        if self._ball.getcenterx() >=0:
            if self._ball.getcenterx() >= GAME_WIDTH - BALL_RADIUS:
                self._ball.set_x_velocity( -(self._ball.get_x_velocity()))
        if self._ball.get_x_velocity() <= 0:
            if self._ball.getcenterx() <= 0+BALL_RADIUS:
                self._ball.set_x_velocity( -(self._ball.get_x_velocity()))
                
    def checkbrickpaddle(self):
        """Checks if the ball collides with the brick or paddle. if it does it sets
        the y velocity to -y velocity. Also checks, if it hits the paddle, where it hits
        the paddle. If it hits the paddle 1/4 of the way from the edge coming from that
        same direction than it sets the x velocity to -x velocity so that the ball
        goes back the way it came."""
        if self._ball.getcenterx()<=(self._paddle.x+(PADDLE_WIDTH/4.0)) and \
                self._getCollidingObject()==self._paddle:
            self._ball.set_y_velocity(-1*(self._ball.get_y_velocity()))
            if self._ball.get_x_velocity()>0:
                self._ball.set_x_velocity(-1*(self._ball.get_x_velocity()))
        elif self._ball.getcenterx()>=(self._paddle.x+3.0*(PADDLE_WIDTH/4.0)) and \
                self._getCollidingObject()==self._paddle:
            self._ball.set_y_velocity(-1*(self._ball.get_y_velocity()))
            if self._ball.get_x_velocity()<0:
                self._ball.set_x_velocity(-1*(self._ball.get_x_velocity()))
        elif self._getCollidingObject()!=None:
            self._ball._vy = -self._ball._vy

    def _getCollidingObject(self):
        """Returns: GObject that has collided with the ball
    
    This method checks the four corners of the ball, one at a 
    time. If one of these points collides with either the paddle 
    or a brick, it stops the checking immediately and returns the 
    object involved in the collision. It returns None if no 
    collision occurred."""
        RIGHT_TOP_CORNER = GPoint(x =(self._ball.getcenterx()+BALL_RADIUS),y=\
                              (self._ball.getcentery()+BALL_RADIUS))
        LEFT_TOP_CORNER = GPoint(x =(self._ball.getcenterx()-BALL_RADIUS),y=\
                              (self._ball.getcentery()+BALL_RADIUS))
        LEFT_BOTTOM_CORNER = GPoint(x =(self._ball.getcenterx()-BALL_RADIUS),y=\
                              (self._ball.getcentery()-BALL_RADIUS))
        RIGHT_BOTTOM_CORNER = GPoint(x =(self._ball.getcenterx()+BALL_RADIUS),y=\
                              (self._ball.getcentery()-BALL_RADIUS))
        listbricks = self._wall.getbrickwall()
        for x in range(len(listbricks)):
            if listbricks[x].contains(x=RIGHT_TOP_CORNER.x,y=RIGHT_TOP_CORNER.y)\
               or listbricks[x].contains(x=LEFT_TOP_CORNER.x,y=LEFT_TOP_CORNER.y)\
               or listbricks[x].contains(x=LEFT_BOTTOM_CORNER.x,y=LEFT_BOTTOM_CORNER.y)\
               or listbricks[x].contains(x=RIGHT_BOTTOM_CORNER.x,y=RIGHT_BOTTOM_CORNER.y):
                return listbricks[x]
        if self._paddle.contains(x=RIGHT_TOP_CORNER.x,y=RIGHT_TOP_CORNER.y)\
           or self._paddle.contains(x=LEFT_TOP_CORNER.x,y=LEFT_TOP_CORNER.y)\
           or self._paddle.contains(x=LEFT_BOTTOM_CORNER.x,y=LEFT_BOTTOM_CORNER.y)\
           or self._paddle.contains(x=RIGHT_BOTTOM_CORNER.x,y=RIGHT_BOTTOM_CORNER.y):
            return self._paddle
        else:
            return None
     # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE   
    
    def loseball(self):
        """Returns: True if the ball has gone off the screen. if it does it sets the
        ball==NONE."""
        if self._ball.getcentery() <= 0 + BALL_RADIUS:
            self._ball = None
            return True
    
    def no_wall(self):
        """Returns: True if there are no bricks left. False otherwise."""
        if len(self._wall.getbrickwall())==0:
            return True
        else:
            return False
    
    def removebrick(self):
        """Removes the brick that the ball collided with. Also changes the
        colors of the bricks randomly. """
        brick = self._getCollidingObject()
        if brick != None and brick in self._wall.getbrickwall():
            self._wall.removebrick(self._getCollidingObject())
            self._wall.changecolors()

    

    
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE

