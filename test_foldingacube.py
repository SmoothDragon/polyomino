#!/usr/bin/env python3

if __name__ == '__main__':
    from polyomino import Polyomino
    import os
    import os.path

    for root, dirs, files in os.walk('test'):
        if root == 'test':
            testfiles = [os.path.join(root, f) for f in files]

    for testfile in testfiles:
        base, ext = os.path.splitext(testfile)
        if ext != '.in':
            continue
        print('Testing: ', testfile)
        testoutfile = base + '.ans'

        piece = Polyomino.from_file(testfile)
        if Polyomino.cubable_hexomino(piece):
            output = 'can fold\n'
        else:
            output = 'cannot fold\n'
        with open(testoutfile) as infile:
            answer = infile.read()
        if answer == output:
            print('OK')
        else:
            print('Failed')
