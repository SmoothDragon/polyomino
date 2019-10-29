#!/usr/bin/env python3

if __name__ == '__main__':
    import sys
    from polyomino import BitPolyomino

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        piece = BitPolyomino.from_file(filename)
        if BitPolyomino.cubable_hexomino(piece):
            print('can fold')
        else:
            print('cannot fold')

