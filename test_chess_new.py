from chess import chess_new 
from chess.chess_new import V
import pytest

# chess_new.get_sign(5)

def test_get_sign():
    assert chess_new.get_sign(5) == 1
    assert chess_new.get_sign(-5) == -1
    assert chess_new.get_sign(0) == 0


def test_safe_divide():
    assert chess_new.safe_divide(27, 9) == 3
    assert chess_new.safe_divide(-18, 3) == -6
    assert chess_new.safe_divide(0, -6) == 0
    assert chess_new.safe_divide(-9, -0) == 0

def test_vector():
    assert chess_new.V(1,3) == chess_new.V(1,3)
    assert chess_new.V(1,3) == chess_new.V('d', 7)
    assert chess_new.V(1,3) == chess_new.V('d7')
    assert chess_new.V(-2,3) * chess_new.V(-4,3) == chess_new.V(8,9)
    assert chess_new.V(1,3)* 3 == chess_new.V(3,9)
    assert chess_new.V(1,3)* -2 == chess_new.V(-2,-6)
    assert chess_new.V(1,3) - 2 == chess_new.V(-1,1)
    assert chess_new.V(1,3) + 2 == chess_new.V(3,5)
    assert chess_new.V(1,3) + chess_new.V(-4,3) == chess_new.V(-3,6)
    assert chess_new.V(1,3).to_print() == 'd7'

def test_ruleset_pawn_20():
    ruleset = chess_new.RuleSet()   
    assert ruleset.get_available_step(20, ruleset.board,
        _print=2) == {'to': [V(2,3), V(3,3)], 'from': V(1,3)}

    ruleset.move_figure(V('c2'), V('c6') )

    assert ruleset.get_available_step(20, ruleset.board,
        _print=2) == {'to': [V(2,3), V(3,3), V(2,2)], 'from': V(1,3)}


def test_ruleset_pawn_12():
    ruleset = chess_new.RuleSet()   
    assert ruleset.get_available_step(12, ruleset.board,
        _print=2) == {'to': [V(5,3), V(4,3)], 'from': V(6,3)}
    ruleset.move_figure(V('c7'), V('c3') )

    assert ruleset.get_available_step(12, ruleset.board,
        _print=2) == {'to': [V(5,3), V(4,3), V(5,2)], 'from': V(6,3)}


def test_ruleset_knight():
    ruleset = chess_new.RuleSet()   
    assert ruleset.get_available_step(7, ruleset.board,
        _print=2) == {'to': [V(5,5), V(5,7)], 'from': V(7,6)}

    ruleset.move_figure(21, 13)

    assert ruleset.get_available_step(7, ruleset.board,
        _print=2) == {'to': [V(5,5), V(5,7), V(6,4)], 'from': V(7,6)}


def test_ruleset_move():
    ruleset = chess_new.RuleSet()   
    ruleset2 = chess_new.RuleSet()   

    ruleset.move_figure(21, 13)
    assert ruleset.board != ruleset2.board

    ruleset2.move_figure(V('e7'), V('e2'))
    assert ruleset.board == ruleset2.board
