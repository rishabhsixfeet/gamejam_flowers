
import pygame

import action
import colors
import event as e
import manager
import rabbit
from terrain import Terrain
import unit

class Obstacle( unit.Unit ):
    
    def __init__( self, terrain ):
        unit.Unit.__init__( self, terrain )

        self.active_listeners = manager.init_listener()
        self.active_listeners.update( [
            (e.AI_SKIP,      self.action_skip)
        ] )
    
    def action_skip( self, event):
        e.Event( e.NEXT_ACTIVE )

    def end_turn( self ):
        #print self.counter
        if self.counter >= 1:
            self.counter -= 1

    def update( self, dt ):
        if unit.Unit.active() is self:
            e.Event( e.AI_SKIP )
        if self.counter <= 0:
            e.Event( e.DEATH, target=self )
    
        
class Thorn(Obstacle):
    def __init__( self, terrain ):
        Obstacle.__init__(self, terrain)

    def draw( self, screen ):
        screen.blit(colors.THORN, self.terrain)
        unit.Unit.draw( self, screen )

class Poison(Obstacle):
    def __init__( self, terrain ):
        Obstacle.__init__(self, terrain)

    def draw( self, screen ):
        screen.blit(colors.POISON, self.terrain)
        unit.Unit.draw( self, screen )
    
class Flower( unit.Unit ):

    def __init__( self, terrain ):
        unit.Unit.__init__( self, terrain )

        self.active_listeners = manager.init_listener()
        self.active_listeners.update( [
            (e.FLOWER_UP,    self.action_up),
            (e.FLOWER_DOWN,  self.action_down),
            (e.FLOWER_LEFT,  self.action_left),
            (e.FLOWER_RIGHT, self.action_right),
            (e.FLOWER_SKIP,  self.action_skip),
        ] )

        self.growth = 5

    def _action_direction( self, action_terrain ):
        if action_terrain is not None:
            action.Action( action_terrain, self )

    def action_up( self, event ):
        action_terrain = self.terrain.up_terrain()
        return self._action_direction( action_terrain )

    def action_down( self, event ):
        action_terrain = self.terrain.down_terrain()
        return self._action_direction( action_terrain )

    def action_left( self, event ):
        action_terrain = self.terrain.left_terrain()
        return self._action_direction( action_terrain )

    def action_right( self, event ):
        action_terrain = self.terrain.right_terrain()
        return self._action_direction( action_terrain )
    
    def action_skip( self, event):
        e.Event( e.NEXT_ACTIVE )

    def end_turn( self ):
        self.growth += (1 - self.hit)
        unit.Unit.end_turn( self )
        if self.is_surrounded( Flower ):
            self.growth -= 2

    def update( self, dt ):
        if self.terrain.contains_unit( rabbit.Rabbit ):
            #e.Event( e.DEATH, target=self )
            pass
        if self.growth < 1:
            e.Event(e.DEATH, target = self)

    def draw( self, screen ):
        screen.blit(colors.FLOWER, self.terrain)
        unit.Unit.draw( self, screen )
        self.draw_number( screen )

