from pprint import pprint
from .chess_new import V, Game, RuleSet, get_sign, get_sign_zero, safe_divide
import pytest
# import chess_new
# from chess_new import V, Game, RuleSet

# get_sign(5)

def test_get_sign_zero():
    assert get_sign_zero(5) == 1
    assert get_sign_zero(-5) == -1
    assert get_sign_zero(0) == 0

def test_get_sign():
    assert get_sign(0,5) == 1
    assert get_sign(-5,0) == 1
    assert get_sign(5,0) == -1
    assert get_sign(0,-5) == -1

def test_safe_divide():
    assert safe_divide(27, 9) == 3
    assert safe_divide(-18, 3) == -6
    assert safe_divide(0, -6) == 0
    assert safe_divide(-9, -0) == 0

def test_vector():
    assert V(1,3) == V(1,3)
    assert V(1,3) == V('d', 7)
    assert V(1,3) == V('d7')
    assert V(-2,3) * V(-4,3) == V(8,9)
    assert V(1,3)* 3 == V(3,9)
    assert V(1,3)* -2 == V(-2,-6)
    assert V(1,3) - 2 == V(-1,1)
    assert V(1,3) + 2 == V(3,5)
    assert V(1,3) + V(-4,3) == V(-3,6)
    assert V(1,3).to_print() == 'd7'

def test_ruleset_pawn_20():
    ruleset = RuleSet()   
    figures = ruleset.fig_state
    figure_id = 20
    assert ruleset.get_available_step(figure_id, figures, ruleset.board,
        _print=2) == {'to': [V(2,3), V(3,3)], 'from': V(1,3), 'score': {}}

    ruleset.move_figure(V('c2'), V('c6'), ruleset._board )
    # ruleset.prettify(ruleset._board)
    # ruleset._board
    assert ruleset.get_available_step(figure_id, figures, ruleset._board,
        _print=2) == {'to': [V(2,3), V(3,3), V(2,2)], 'from': V(1,3), 'score': {'c6':10}}


def test_ruleset_pawn_12():
    ruleset = RuleSet()   
    figures = ruleset.fig_state
    figure_id = 12
    assert ruleset.get_available_step(figure_id, figures, ruleset._board,
        _print=2) == {'to': [V(5,3), V(4,3)], 'from': V(6,3), 'score': {}}
    ruleset.move_figure(V('c7'), V('c3'), ruleset._board)

    assert ruleset.get_available_step(figure_id, figures, ruleset._board,
        _print=2) == {'to': [V(5,3), V(4,3), V(5,2)], 'from': V(6,3), 'score': {'c3':10}}


def test_ruleset_knight():
    ruleset = RuleSet()   
    figures = ruleset.fig_state
    figure_id = 7
    assert ruleset.get_available_step(figure_id, figures, ruleset._board,
        _print=2) == {'to': [V(5,5), V(5,7)], 'from': V(7,6), 'score': {}}

    ruleset.move_figure(21, 13, ruleset._board)

    assert ruleset.get_available_step(figure_id, figures, ruleset._board,
        _print=2) == {'to': [V(5,5), V(5,7), V(6,4)], 'from': V(7,6), 'score': {'e2': 10}}


def test_ruleset_move():
    ruleset = RuleSet()   
    ruleset2 = RuleSet()   
    ruleset.move_figure(21, 13, ruleset._board)
    assert ruleset._board != ruleset2._board

    ruleset2.move_figure(V('e7'), V('e2'), ruleset2._board)
    assert ruleset._board == ruleset2._board

def test_ruleset_all():
    moves_example = {
                    1: {'from': V(7,0), 'score': {}, 'to': []},
                    2: {'from': V(7,1), 'score': {}, 'to': [V(5,0), V(5,2)]},
                    3: {'from': V(7,2), 'score': {}, 'to': []},
                    4: {'from': V(7,3), 'score': {}, 'to': []},
                    5: {'from': V(7,4), 'score': {}, 'to': []},
                    6: {'from': V(7,5), 'score': {}, 'to': []},
                    7: {'from': V(7,6), 'score': {}, 'to': [V(5,5), V(5,7)]},
                    8: {'from': V(7,7), 'score': {}, 'to': []},
                    9: {'from': V(6,0), 'score': {}, 'to': [V(5,0), V(4,0)]},
                    10: {'from': V(6,1), 'score': {}, 'to': [V(5,1), V(4,1)]},
                    11: {'from': V(6,2), 'score': {}, 'to': [V(5,2), V(4,2)]},
                    12: {'from': V(6,3), 'score': {}, 'to': [V(5,3), V(4,3)]},
                    13: {'from': V(6,4), 'score': {}, 'to': [V(5,4), V(4,4)]},
                    14: {'from': V(6,5), 'score': {}, 'to': [V(5,5), V(4,5)]},
                    15: {'from': V(6,6), 'score': {}, 'to': [V(5,6), V(4,6)]},
                    16: {'from': V(6,7), 'score': {}, 'to': [V(5,7), V(4,7)]},
                    17: {'from': V(1,0), 'score': {}, 'to': [V(2,0), V(3,0)]},
                    18: {'from': V(1,1), 'score': {}, 'to': [V(2,1), V(3,1)]},
                    19: {'from': V(1,2), 'score': {}, 'to': [V(2,2), V(3,2)]},
                    20: {'from': V(1,3), 'score': {}, 'to': [V(2,3), V(3,3)]},
                    21: {'from': V(1,4), 'score': {}, 'to': [V(2,4), V(3,4)]},
                    22: {'from': V(1,5), 'score': {}, 'to': [V(2,5), V(3,5)]},
                    23: {'from': V(1,6), 'score': {}, 'to': [V(2,6), V(3,6)]},
                    24: {'from': V(1,7), 'score': {}, 'to': [V(2,7), V(3,7)]},
                    25: {'from': V(0,0), 'score': {}, 'to': []},
                    26: {'from': V(0,1), 'score': {}, 'to': [V(2,2), V(2,0)]},
                    27: {'from': V(0,2), 'score': {}, 'to': []},
                    28: {'from': V(0,3), 'score': {}, 'to': []},
                    29: {'from': V(0,4), 'score': {}, 'to': []},
                    30: {'from': V(0,5), 'score': {}, 'to': []},
                    31: {'from': V(0,6), 'score': {}, 'to': [V(2,7), V(2,5)]},
                    32: {'from': V(0,7), 'score': {}, 'to': []}
                    }

    colors = ['white', 'black']
    moves = {}
    game = Game('white')
    ruleset = RuleSet()
    for color in colors:
        figures = game.get_all_figures(color)
        for figure_id, figure  in figures.items():
            moves[figure_id] = ruleset.get_available_step(figure_id, figures, ruleset._board)
    assert moves == moves_example


