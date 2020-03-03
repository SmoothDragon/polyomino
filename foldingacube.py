#!/usr/bin/env python3

if __name__ == '__main__':
    import sys
    from polyomino import Polyomino

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        piece = Polyomino.from_file(filename)
        if Polyomino.cubable_hexomino(piece):
            print('can fold')
        else:
            print('cannot fold')

