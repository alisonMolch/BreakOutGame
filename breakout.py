# breakout.py
# Jake Zeisel jaz48, Alison Molchadsky
# 12/10/2014
"""Primary module for Breakout application

This module contains the App controller class for the Breakout application.
There should not be any need for additional classes in this module.
If you need more classes, 99% of the time they belong in either the gameplay
module or the models module. If you are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from gameplay import *
from game2d import *


# PRIMARY RULE: Breakout can only access attributes in gameplay.py via getters/setters
# Breakout is NOT allowed to access anything in models.py
        

class Breakout(GameApp):
    """Instance is a Breakout App
    
    This class extends GameApp and implements the various methods necessary 
    for processing the player inputs and starting/running a game.
    
        Method init starts up the game.
        
        Method update either changes the state or updates the Gameplay object
        
        Method draw displays the Gameplay object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the init method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Gameplay.
    Gameplay should have a minimum of two methods: updatePaddle(touch) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView, it is inherited from GameApp]:
            the game view, used in drawing (see examples from class)
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
            the current state of the game represented a value from constants.py
        _last   [GPoint, or None if mouse button is not pressed]:
            the last mouse position (if Button was pressed)
        _game   [GModel, or None if there is no game currently active]: 
            the game controller, which manages the paddle, ball, and bricks
    
    ADDITIONAL INVARIANTS: Attribute _game is only None if _state is STATE_INACTIVE.
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _message[instance of Glabel or none]
                message that initializes the game
        _time [Float]
                time in increments of 1/60 to keep track of countdown in seconds
        _livesmessage [A glabel object]
                shows on the top left of the screen how many lives are left
                
    """         
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # GAMEAPP METHODS
    def init(self):
        """Initialize the game state.
        
        This method is distinct from the built-in initializer __init__.
        This method is called once the game is running. You should use
        it to initialize any game specific attributes.
        
        This method should initialize any state attributes as necessary 
        to statisfy invariants. When done, set the _state to STATE_INACTIVE
        and create a message (in attribute _mssg) saying that the user should 
        press to play a game."""
        self._last = None
        self._state = STATE_INACTIVE
        self._message = GLabel(x = (GAME_WIDTH/2), y = (GAME_HEIGHT/2),\
                               text='Click If You Want to Die'\
                    ,bold=True, font_size=30,halign='center',valign='bottom')
        self._game = None
        self._time = 0
        self._livesmessage = None

    def update_state_countdown(self):
        """helper method for update() if in state_countdown. Depending on the time
        the message changes, counting down from 3. When time is 3 the state changes
        to state_active and the ball initializer is called."""
        if self._time >= 3.0:
            self._state = STATE_ACTIVE
            self._game.makeball()
            self._time = 0
        else:
            self._time = self._time + 1.0/60.0
        if self._time<=1:
                self._message = GLabel(x = (GAME_WIDTH/2),y=(GAME_HEIGHT/2),\
                    text = 'Treis',\
                    bold = True, font_size = 40-(self._time*60)*.5, halign = 'center', valign\
                                   ='bottom')
        if self._time<2 and self._time >= 1:
                self._message = GLabel(x = (GAME_WIDTH/2),y=(GAME_HEIGHT/2),\
                    text = 'Dos',\
                    bold = True, font_size = 40-((self._time-1)*60)*.5, \
                    halign = 'center', valign='bottom')
        if self._time<=3 and self._time >=2:
                self._message = GLabel(x = (GAME_WIDTH/2),y=(GAME_HEIGHT/2),\
                    text = 'UNO',\
                    bold = True, font_size = 40-((self._time-2)*60)*.5, \
                    halign = 'center', valign ='bottom')
    
    def active(self):
        """helper function for update(). Creates a Glabel object that displays
        the amount of lives left. Updates the movement of the ball and paddle.
        Detects collisions with the ball, wall, brick, and paddle. Removes the bricks
        that the ball collided with and changes the velocity of the ball if there
        is a collision."""
        self._livesmessage = GLabel(x = (GAME_WIDTH/12),y=590,\
                text ='Lives  '+str(self._game.getTries()), bold=True,\
                font_size=15,halign='center',valign='bottom', font = 'Time.ttf')
        self._game.updatePaddle(self.view.touch)
        self._game.updateball()
        self._game.checkwalls()
        self._game.updatespeed()
        self._game.checkbrickpaddle()
        self._game.removebrick()
    
    def win(self):
        """Helper function for update() when state is state_win and
        the player has won the game. Changes the message that notifies the
        player that he has won. If there is a click, the state changes to
        state_countdown and the game starts over."""
        self._message=GLabel(x = (GAME_WIDTH/2), y = (GAME_HEIGHT/2),\
                            text='You Win! click to play again', font='Zapfino.ttf'\
                    ,bold=True, font_size=30,halign='center',valign='bottom')
        if self._last==None and self.view.touch:
            self._state = STATE_COUNTDOWN
            self._game=Gameplay(wall = BrickWall(), tries = 3)
    
    def lose(self):
        """Helper function for update() when state is state_lose and
        the player has lost the game. Changes the message that notifies the player
        that he has lost. If there is a click, the state changes to state_countdown
        and the game starts over with a full brickwall and 3 tries."""
        self._message = GLabel(x = (GAME_WIDTH/2),y=(GAME_HEIGHT/2),\
                    text = 'LOSER! Click To Play Again', bold = True\
                    , font_size = 30, halign = 'center', valign = 'bottom'\
                        ,font='Zapfino.ttf')
        if self._last == None and self.view.touch:
            self._state = STATE_COUNTDOWN
            self._game = Gameplay(wall = BrickWall(), tries = 3)

    def inactive(self):
        """Helper funtions for update() when state is state_inactive.
        if there is a touch then state changes to state_countdown and
        the game is initialized."""
        if self._last == None and self.view.touch:
            self._state = STATE_COUNTDOWN
            self._game = Gameplay()
            
    def paused(self):
        """Helper fuction for update() when state is state_paused. Changes
        the message informing the player how many lives he has left.
        If there is a touch the the state switches to state_countdown and the
        game continues."""
        if self._game.getTries() == 1:
                self._message = GLabel(x = (GAME_WIDTH/2),y=(GAME_HEIGHT/2),\
                    text = str(self._game.getTries()) +' Life Left     (click)',\
                    bold = True, font_size = 30, halign = 'center', valign\
                                   ='bottom')
        else:
            self._message = GLabel(x = (GAME_WIDTH/2),y=(GAME_HEIGHT/2),\
                text = str(self._game.getTries()) +' Lives Left    (click)',\
                bold = True, font_size = 30, halign = 'center', valign\
                                ='bottom')
        if self._last == None and self.view.touch:
            self._state = STATE_COUNTDOWN
        
    def update(self,dt):
        """Animate a single frame in the game.
        
        It is the method that does most of the work. Of course, it should
        rely on helper methods in order to keep the method short and easy
        to read.  Some of the helper methods belong in this class, but most
        of the others belong in class Gameplay.
        
        The first thing this method should do is to check the state of the
        game. We recommend that you have a helper method for every single
        state: STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE.
        The game does different things in each state.
        
        In STATE_INACTIVE, the method checks to see if the player clicks
        the mouse (_last is None, but view.touch is not None). If so, it 
        (re)starts the game and switches to STATE_COUNTDOWN.
        
        STATE_PAUSED is similar to STATE_INACTIVE. However, instead of 
        restarting the game, it simply switches to STATE_COUNTDOWN.
        
        In STATE_COUNTDOWN, the game counts down until the ball is served.
        The player is allowed to move the paddle, but there is no ball.
        Paddle movement should be handled by class Gameplay (NOT in this class).
        This state should delay at least one second.
        
        In STATE_ACTIVE, the game plays normally.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Gameplay (NOT in this class).
        Gameplay should have methods named updatePaddle and updateBall.
        
        While in STATE_ACTIVE, if the ball goes off the screen and there
        are tries left, it switches to STATE_PAUSED.  If the ball is lost 
        with no tries left, or there are no bricks left on the screen, the
        game is over and it switches to STATE_WIN. If the ball is
        lost and there are no tries left then it switches
        to STATE_LOSE, which if there is a touch switches to state
        countdown and the game restarts. All of these checks
        should be in Gameplay, NOT in this class.
        
        You are allowed to add more states if you wish. Should you do so,
        you should describe them here.
        
        Precondition: dt is the time since last update (a float).  This
        parameter can be safely ignored. It is only relevant for debugging
        if your game is running really slowly. If dt > 0.5, you have a 
        framerate problem because you are trying to do something too complex."""
        if self._state == STATE_INACTIVE:
            self.inactive()
        if self._state == STATE_COUNTDOWN:
            self._game.updatePaddle(self.view.touch)
            self.update_state_countdown()
        if self._state == STATE_ACTIVE:
            self.active()
        if self._state == STATE_ACTIVE and self._game.loseball():
            if (self._game.getTries()-1)>= 1:
                self._game.setTries()
                self._state = STATE_PAUSED
            else:
                self._state = STATE_LOSEGAME
        if self._state == STATE_PAUSED:
            self.paused()
        if self._state == STATE_LOSEGAME:
            self.lose()
        if self._state == STATE_ACTIVE and self._game.no_wall():
            self._state = STATE_WIN
        if self._state == STATE_WIN:
             self.win()
        self._laststate = self._state
        self._last = self.view.touch
        
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject. 
        To draw a GObject g, simply use the method g.draw(view).  It is 
        that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are
        attributes in Gameplay. In order to draw them, you either need to
        add getters for these attributes or you need to add a draw method
        to class Gameplay.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        if self._state == STATE_INACTIVE:
            self._message.draw(self.view)
        if self._state == STATE_COUNTDOWN:
            self._game.draw(self.view)
            self._message.draw(self.view)
        if self._state == STATE_ACTIVE:
            self._livesmessage.draw(self.view)
            self._game.draw(self.view)
        if self._state == STATE_PAUSED:
            self._game.draw(self.view)
            self._message.draw(self.view)
        if self._state == STATE_LOSEGAME:
            self._message.draw(self.view)
        if self._state == STATE_WIN:
            self._message.draw(self.view)
    
