from ChessGame import Game

def demo():
    def wait_until_enter():
        a=input()
        while True:
            if a=="":
                return

    #wp1
    game.move_piece(from_x=0,from_y=6,to_x=1,to_y=5)

    wait_until_enter()

    #bp8
    game.move_piece(from_x=7,from_y=1,to_x=6,to_y=2)

    wait_until_enter()

    #wp1, wb1, wp3
    game.move_piece(from_x=1,from_y=5,to_x=0,to_y=5)
    game.move_piece(from_x=2,from_y=7,to_x=2,to_y=6)
    game.move_piece(from_x=2,from_y=5,to_x=1,to_y=5)
    game.move_piece(from_x=2,from_y=6,to_x=3,to_y=5)

    wait_until_enter()

    #bkt1, bp2
    game.move_piece(from_x=1,from_y=0,to_x=1,to_y=1)
    game.move_piece(from_x=1,from_y=1,to_x=1,to_y=2)

    wait_until_enter()

    #wb1
    game.move_piece(from_x=2,from_y=7,to_x=2,to_y=6)

    wait_until_enter()

    #br1
    game.move_piece(from_x=0,from_y=0,to_x=2,to_y=2)

    wait_until_enter()

    #wb1
    game.move_piece(from_x=2,from_y=6,to_x=2,to_y=4)

    wait_until_enter()

    #bP2
    game.move_piece(from_x=1, from_y=2, to_x=2, to_y=3)

    wait_until_enter()

    #wq
    game.move_piece(from_x=3,from_y=7,to_x=2,to_y=7)

    wait_until_enter()

    #bR1
    game.move_piece(from_x=2, from_y=2, to_x=3, to_y=3)

    wait_until_enter()

    #wq
    game.move_piece(from_x=2,from_y=7,to_x=2,to_y=4)
    game.move_piece(from_x=2,from_y=7,to_x=2,to_y=3)
    game.move_piece(from_x=2,from_y=7,to_x=2,to_y=5)

    wait_until_enter()

    #bKt2
    game.move_piece(from_x=6,from_y=0, to_x=7,to_y=4)

    wait_until_enter()

    #wq
    game.move_piece(from_x=2,from_y=5,to_x=6,to_y=1)
    game.move_piece(from_x=2,from_y=5,to_x=3,to_y=4)

    wait_until_enter()

    # bKt1
    game.move_piece(from_x=1,from_y=0, to_x=2, to_y=4)
    if game.move_failed:
        game.move_piece(from_x=1,from_y=0, to_x=1, to_y=4)

    wait_until_enter()

    #wq
    game.move_piece(from_x=3,from_y=4,to_x=6,to_y=1)

game = Game()

game.print_board()

# print(game.get_possible_moves_for_piece_at(x=3,y=7))

# demo()

#------------------

#game.print_board()

# g=game.get_board()
# for line in g:
#     print(line)

#------------------
