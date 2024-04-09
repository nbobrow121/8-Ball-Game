import phylib;
import sqlite3;
import os;
import math;
import random;

################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;

# add more here
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;

FRAME_RATE = 0.01;
################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg id="svg-container" width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################
class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################
class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]);



class RollingBall(phylib.phylib_object):

    def __init__(self, number, pos, vel, acc):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_ROLLING_BALL, number, pos, vel, acc, 0.0, 0.0);

        self.__class__ = RollingBall;

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number]);



class Hole(phylib.phylib_object):

    def __init__(self, pos):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HOLE, None, pos, None, None, 0.0, 0.0);

        self.__class__ = Hole;

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS);



class HCushion(phylib.phylib_object):

    def __init__(self, y):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_HCUSHION, None, None, None, None, 0.0, y);

        self.__class__ = HCushion;

    def svg(self):
        if self.obj.hcushion.y == 0:
            YCushion = -25;
        else:
            YCushion = 2700;
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (YCushion);



class VCushion(phylib.phylib_object):

    def __init__(self, x):
        phylib.phylib_object.__init__(self, phylib.PHYLIB_VCUSHION, None, None, None, None, x, 0.0);

        self.__class__ = VCushion;

    def svg(self):
        if self.obj.vcushion.x == 0:
            XCushion = -25;
        else:
            XCushion = 1350;
        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (XCushion);



################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here

    def svg(self):
        string = HEADER;
        for obj in self:
            if(obj):
                string += obj.svg();

        string += FOOTER;
        return string;


    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create4 a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                          Coordinate(0,0),
                                          Coordinate(0,0),
                                          Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                       Coordinate( ball.obj.still_ball.pos.x,
                                       ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def cueBall( self ):
        cueBallPosition = None
        for ball in self:
            
            if isinstance( ball, StillBall ) and ball.obj.still_ball.number == 0:
                cueBallPosition = ball
        
        return cueBallPosition
    
    def curBall(self, i ):
        curBall = False
        
        for ball in self:
            
            if isinstance(ball, StillBall) and ball.obj.still_ball.number == i:
                 curBall = True
        
        return curBall
    
class Database():

    def __init__( self, reset=False ):
        if reset and os.path.exists('phylib.db'):
             os.remove('phylib.db')

        self.conn = sqlite3.connect('phylib.db')
        self.createDB()

    def createDB(self):

        cur = self.conn.cursor();

        cur.execute( """CREATE TABLE IF NOT EXISTS Ball
                        (BALLID INTEGER PRIMARY KEY AUTOINCREMENT,
                         BALLNO INTEGER NOT NULL,
                         XPOS FLOAT NOT NULL,
                         YPOS FLOAT NOT NULL,
                         XVEL FLOAT,
                         YVEL FLOAT)""")

        cur.execute( """CREATE TABLE IF NOT EXISTS TTable
                        (TABLEID INTEGER PRIMARY KEY AUTOINCREMENT,
                         TIME FLOAT NOT NULL)""")

        cur.execute( """CREATE TABLE IF NOT EXISTS BallTable
                        (BALLID INTEGER NOT NULL,
                         TABLEID INTEGER NOT NULL,
                         FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
                         FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID))""")

        cur.execute( """CREATE TABLE IF NOT EXISTS Shot
                        (SHOTID INTEGER PRIMARY KEY AUTOINCREMENT,
                         PLAYERID INTEGER NOT NULL,
                         GAMEID INTEGER NOT NULL,
                         FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                         FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))""")

        cur.execute( """CREATE TABLE IF NOT EXISTS TableShot
                        (TABLEID INTEGER NOT NULL,
                         SHOTID INTEGER NOT NULL,
                         FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                         FOREIGN KEY (SHOTID) REFERENCES Shot(SHOTID))""")

        cur.execute( """CREATE TABLE IF NOT EXISTS Game
                        (GAMEID INTEGER PRIMARY KEY AUTOINCREMENT,
                         GAMENAME VARCHAR(64) NOT NULL)""")

        cur.execute( """CREATE TABLE IF NOT EXISTS Player
                        (PLAYERID INTEGER PRIMARY KEY AUTOINCREMENT,
                         GAMEID INTEGER NOT NULL,
                         PLAYERNAME VARCHAR(64) NOT NULL,
                         FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID))""")

        cur.execute("""CREATE INDEX IF NOT EXISTS idx_tableid ON TTable (TABLEID)""")
        cur.execute("""CREATE INDEX IF NOT EXISTS ballid ON Ball (BALLID)""")

        cur.close()
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()

    def readTable( self, tableID ):
        cur = self.conn.cursor()
        table = Table()

        ballsOnTable = cur.execute("""SELECT Ball.BALLID, Ball.BALLNO, Ball.XPOS, Ball.YPOS, Ball.XVEL, Ball.YVEL, TTable.TIME
                                   FROM BallTable
                                   INNER JOIN Ball ON Ball.BALLID = BallTable.BALLID
                                   INNER JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
                                   WHERE BallTable.TABLEID = ?""", (tableID + 1,)).fetchall()

        if not ballsOnTable:
            return None

        for ball_info in ballsOnTable:
            ballID, ballNO, xPos, yPos, xVel, yVel, time = ball_info
            pos = Coordinate(xPos, yPos)

            if xVel is None and yVel is None:
                ball = StillBall(ballNO, pos)

            else:
                vel = Coordinate(xVel, yVel)
                length = phylib.phylib_length(vel)

                if length > VEL_EPSILON:
                    xAcc = (-xVel / length) * DRAG
                    yAcc = (-yVel / length) * DRAG

                acc = Coordinate(xAcc, yAcc)
                ball = RollingBall(ballNO, pos, vel, acc)

            table += ball

        table.time = ballsOnTable[0][-1]

        cur.close()
        self.conn.commit()

        return table

    def cueMiss(self, table):
        cueBall = table.cueBall()
        
        if cueBall is None:
            pos = Coordinate(TABLE_WIDTH/2.0 + random.uniform(-3.0, 3.0),
                            TABLE_LENGTH - TABLE_WIDTH/2.0)
            
            sb  = StillBall(0, pos)
            table += sb
        
        return table 

    def writeTable( self, table ):
        cur = self.conn.cursor()
        
        cur.execute("""INSERT INTO TTable (TIME) VALUES (?)""", (table.time,))
        
        tableID = cur.lastrowid

        table = self.cueMiss(table)

        dataForBalls = []
        
        for ball in table:
            
            if isinstance(ball, StillBall) or isinstance(ball, RollingBall):
                
                if isinstance(ball, StillBall):
                    dataForBalls.append((ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y, None, None))
                
                elif isinstance(ball, RollingBall):
                    dataForBalls.append((ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y,
                                    ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
        
        cur.executemany("""INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) VALUES (?,?,?,?,?)""", dataForBalls)

        max_ball_id = cur.execute("SELECT MAX(BALLID) FROM Ball").fetchone()[0]
        
        ballID = cur.lastrowid - len(dataForBalls) + 1
        dataForBalls = [(ballID, tableID) for ballID in range(ballID, cur.lastrowid + 1)]
        
        cur.executemany("""INSERT INTO BallTable (BALLID, TABLEID) VALUES (?,?)""", dataForBalls)

        cur.close()

        return tableID - 1

    def getGame ( self, gameID ):
        cur = self.conn.cursor()

        cur.execute("""SELECT Game.GAMENAME, p1.PLAYERNAME as p1name, p2.PLAYERNAME as p2name
                        FROM GAME, Player p1
                        JOIN Player p2 ON p1.GAMEID = p2.GAMEID
                        WHERE Game.GAMEID = ? and p1.PLAYERNAME != p2.PLAYERNAME""", (gameID,))

        gameInfo = cur.fetchone()

        cur.close()
        self.conn.commit()

        if gameInfo:
            return gameInfo
        else:
            return (None, None, None)

    def setGame (self, gameName, player1Name, player2Name):
        cur = self.conn.cursor();
        
        cur.execute("INSERT INTO Game (GAMENAME) VALUES (?)", (gameName,))
        
        gameID = cur.lastrowid

        cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player1Name))
        cur.execute("INSERT INTO Player (GAMEID, PLAYERNAME) VALUES (?, ?)", (gameID, player2Name))

        cur.close()
        self.conn.commit()
        
        return gameID - 1

    def newShot(self, gameID, playerName):
        cur = self.conn.cursor();
        
        pID = cur.execute("SELECT PLAYERID FROM Player WHERE PLAYERNAME = ?", (playerName,)).fetchone()

        cur.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (pID[0], gameID+1))
        
        shotID = cur.lastrowid

        cur.close()
        self.conn.commit()
        
        return shotID

class Game():
    def __init__(self, gameID=None, gameName=None, player1Name=None, player2Name=None):
        
        if gameID is not None:
            
            if not isinstance(gameID, int) or any(param is not None for param in [gameName, player1Name, player2Name]):
                raise TypeError("Invalid parameters for initializing with gameID.")
            
            self.db = Database(False)
            self.gameID = gameID
            
            self.gameName, self.player1Name, self.player2Name = self.db.getGame(gameID + 1)
        
        elif all(isinstance(name, str) for name in [gameName, player1Name, player2Name]):
            self.db = Database(True)
            
            self.gameID = self.db.setGame(gameName, player1Name, player2Name)
            self.gameName, self.player1Name, self.player2Name = gameName, player1Name, player2Name
        
        else:
            raise TypeError("Invalid parameter combination for game initialization.")
        

    def shoot(self, gameName, playerName, table, xvel, yvel):
        shotID = self.db.newShot(self.gameID, playerName)

        cueBallPosition = table.cueBall()

        if cueBallPosition is not None:
            xpos, ypos = cueBallPosition.obj.still_ball.pos.x, cueBallPosition.obj.still_ball.pos.y

            cueBallPosition.type = phylib.PHYLIB_ROLLING_BALL

            cueBallPosition.obj.rolling_ball.pos.x, cueBallPosition.obj.rolling_ball.pos.y = xpos, ypos
            cueBallPosition.obj.rolling_ball.vel.x, cueBallPosition.obj.rolling_ball.vel.y = xvel, yvel

            velocity = Coordinate(xvel, yvel)
            length = phylib.phylib_length(velocity)

            if (length > VEL_EPSILON):
                cueBallPosition.obj.rolling_ball.acc.x = (-xvel / length) * DRAG
                cueBallPosition.obj.rolling_ball.acc.y = (-yvel / length) * DRAG

            cueBallPosition.obj.rolling_ball.number = 0

        cur = self.db.conn.cursor()

        while table.segment():
            startTime, endTime = table.time, table.segment().time

            segmentLength = endTime - startTime
            segmentTime = math.floor(segmentLength / FRAME_RATE)

            for i in range(segmentTime):
                time = FRAME_RATE*i
                newTable = table.roll(time)
                newTable.time = table.time + time
                newTableID = self.db.writeTable(newTable)

                cur.execute("INSERT INTO TableShot (TABLEID, SHOTID) VALUES (?, ?)", (newTableID + 1, shotID))

            table = table.segment()

        self.db.conn.commit()
        
    def ballsLeft(self, table, i):
        
        for i in range(1 + i, 7 + i):
            
            if(table.curBall(i) == True):
                return False
        
        return True   
                
    def isGameOver(self, table):
        
        if self.ballsLeft(table, 0) == True or self.ballsLeft(table, 8) == True or (table.curBall(8) == False):
            
            return True
        
def setupTable():
        def nudge():
            return 0 #random.uniform( -1.5, 1.5 )

        table = Table()

        #1
        pos = Coordinate(TABLE_WIDTH / 2.0, TABLE_WIDTH / 2.0)
        sb = StillBall(1, pos)
        table += sb

        #2
        pos = Coordinate(TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0 + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(2, pos)
        table += sb

        #3 
        pos = Coordinate(TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0 + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)/2.0*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(3, pos)
        table += sb

        #4
        pos = Coordinate(TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0) + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(4, pos)
        table += sb

        #8
        pos = Coordinate(TABLE_WIDTH/2.0  + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(8, pos)
        table += sb
 
        #6
        pos = Coordinate(TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0) + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(6, pos)
        table += sb

        #7
        pos = Coordinate(TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)/2.0 + nudge(), 
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*1.5*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(7, pos)
        table += sb

        #5
        pos = Coordinate(TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)/2.0 + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*1.5*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(5, pos)
        table += sb

        #9
        pos = Coordinate(TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)*1.5 + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*1.5*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(9, pos)
        table += sb

        #10
        pos = Coordinate(TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)*1.5 + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*1.5*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(10, pos)
        table += sb

        #11
        pos = Coordinate(TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0) + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*2*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(11, pos)
        table += sb

        #12
        pos = Coordinate(TABLE_WIDTH/2.0 + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*2*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(12, pos)
        table += sb
 
        #13
        pos = Coordinate(TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0) + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*2*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(13, pos)
        table += sb

        #14
        pos = Coordinate(TABLE_WIDTH/2.0 - (BALL_DIAMETER+4.0)*2 + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*2*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(14, pos)
        table += sb
 
        #15
        pos = Coordinate(TABLE_WIDTH/2.0 + (BALL_DIAMETER+4.0)*2 + nudge(),
                         TABLE_WIDTH/2.0 - math.sqrt(3.0)*2*(BALL_DIAMETER+4.0) + nudge())
        sb = StillBall(15, pos)
        table += sb

        #Cue Ball 
        pos = Coordinate(TABLE_WIDTH/2.0 + random.uniform(-3.0, 3.0),
                        TABLE_LENGTH - TABLE_WIDTH/2.0)
        sb  = StillBall(0, pos)

        table += sb
        return table

#End of file