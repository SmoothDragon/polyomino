#!/usr/bin/env python3

class BitPolyomino:
    def str(x, b01='.#'):
        '''Transpose of 8x8 bit matrix
        >>> print(BitPolyomino.str(0x8888888ff))
        ########
        ...#...#
        ...#...#
        ...#...#
        ...#....
        ........
        ........
        ........
        '''
        value = ''.join(b01[(x >> i) & 1] for i in range(64))
        return '\n'.join(value[8*ii:8*(ii+1)] for ii in range(8))

    def from_file(filename, fill='#'):
        '''
        >>> BitPolyomino.cubable_hexomino(BitPolyomino.from_file('1.in'))
        False
        >>> BitPolyomino.cubable_hexomino(BitPolyomino.from_file('2.in'))
        True
        >>> BitPolyomino.cubable_hexomino(BitPolyomino.from_file('3.in'))
        False
        >>> BitPolyomino.cubable_hexomino(BitPolyomino.from_file('4.in'))
        True
        '''
        piece = 0
        with open(filename) as infile:
            for row, line in enumerate(infile):
                for col, ch in enumerate(line.strip()):
                    if ch == fill:
                        piece ^= 1 << (8*row + col)
        return piece

    @classmethod
    def cubable_hexomino(cls, piece):
        '''Given a piece, returns whether it can be made into a cube.
        >>> BitPolyomino.cubable_hexomino(1+256*15+(1<<18))
        True
        '''
        D = {63:False, 287:False, 543:False, 783:False, 798:False, 1055:False, 1295:False, 1551:False, 1799:False, 1805:False, 1806:False, 1820:True, 2319:False, 65807:False, 66311:False, 66318:False, 66823:False, 67331:False, 67333:False, 67334:False, 67340:True, 69377:True, 69378:True, 69380:True, 69384:True, 131599:False, 131854:False, 132867:False, 132869:False, 132876:True, 134659:True, 134914:True, 134916:True, 197134:False, 198156:True}
        piece = cls.canonical_d4(piece)
        if piece not in D:
            return False
        return D[piece]
        # Code to check answer
        for piece in D:
            print(cls.str(piece), piece, D[piece])


    @classmethod
    def extend_d4(cls, shapes):
        '''Return a list of polyominos with one more square added.
        >>> L = BitPolyomino.extend_d4([0x3]); print(sorted(L))  # 3
        [7, 259]
        >>> L = BitPolyomino.extend_d4(L); print(sorted(L))  # 4
        [15, 263, 519, 771, 774]
        >>> L = BitPolyomino.extend_d4(L); print(sorted(L))  # 5
        [31, 271, 527, 775, 782, 1287, 65799, 66310, 67329, 67330, 67332, 132866]
        >>> L = BitPolyomino.extend_d4(L); print(sorted(L))  # 6
        [63, 287, 543, 783, 798, 1055, 1295, 1551, 1799, 1805, 1806, 1820, 2319, 65807, 66311, 66318, 66823, 67331, 67333, 67334, 67340, 69377, 69378, 69380, 69384, 131599, 131854, 132867, 132869, 132876, 134659, 134914, 134916, 197134, 198156]
        '''
        found = set()
        for shape in shapes:
            shape = cls.justify(shape)
            shape = shape << 9
            if shape & (0xff818181818181ff):  # square border
                raise Exception('Polyomino too large')
            for ii in range(9,55):  # Skip first and last row
                if ((ii>>3) == 0) or ((ii>>3) == 7):
                    continue  # Skip first and last column
                if (shape >> ii) & 1 == 0:
                    continue  # ignore empty squares

                if (shape >> (ii-8)) & 1 == 0:  # square above
                    found.add(cls.canonical_d4(shape ^ (1 << (ii-8))))
                if (shape >> (ii+8)) & 1 == 0:  # square below
                    found.add(cls.canonical_d4(shape ^ (1 << (ii+8))))
                if (shape >> (ii-1)) & 1 == 0:  # square left
                    found.add(cls.canonical_d4(shape ^ (1 << (ii-1))))
                if (shape >> (ii+1)) & 1 == 0:  # square right
                    found.add(cls.canonical_d4(shape ^ (1 << (ii+1))))
        return found


    def transpose(x):
        '''Transpose of 8x8 bit matrix
        >>> BitPolyomino.transpose(0x8888888ff)
        1081146489872384257
        '''
        # transpose 1x1 blocks in 2x2 squares
        x ^= (x & 0x5500550055005500) >> 7
        x ^= (x & 0x00aa00aa00aa00aa) << 7
        x ^= (x & 0x5500550055005500) >> 7
        # transpose 2x2 blocks in 4x4 squares
        x ^= (x & 0x3333000033330000) >> 14
        x ^= (x & 0x0000cccc0000cccc) << 14
        x ^= (x & 0x3333000033330000) >> 14
        # transpose 4x4 blocks in 8x8 squares
        x ^= (x & 0x0f0f0f0f00000000) >> 28
        x ^= (x & 0x00000000f0f0f0f0) << 28
        x ^= (x & 0x0f0f0f0f00000000) >> 28
        return x

    def vertical_reflect(x):
        '''Reflect 8x8 bit matrix around horizontal axis
        >>> BitPolyomino.vertical_reflect(0x8888888ff)
        18413117194335420416
        '''
        # top and bottom halves switch
        x ^= (x & 0xffffffff00000000) >> 32
        x ^= (x & 0x00000000ffffffff) << 32
        x ^= (x & 0xffffffff00000000) >> 32
        # First and second fourths switch (and 3rd and 4th)
        x ^= (x & 0xffff0000ffff0000) >> 16
        x ^= (x & 0x0000ffff0000ffff) << 16
        x ^= (x & 0xffff0000ffff0000) >> 16
        # Adjacent rows swap
        x ^= (x & 0xff00ff00ff00ff00) >> 8
        x ^= (x & 0x00ff00ff00ff00ff) << 8
        x ^= (x & 0xff00ff00ff00ff00) >> 8
        return x

    def justify(x):
        '''Adjust polyomino to touch top and left side.
        '''
        # Can be sped up using leading zeros approach
        while x & 0xff == 0:
            x = x >> 8  # Move up one row
        while x & 0x0101010101010101 == 0:
            x = x >> 1  # Move left one column
        return x

    def justify_top(x):
        '''Adjust polyomino to touch top side.
        '''
        # Can be sped up using leading zeros approach
        while x & 0xff == 0:
            x = x >> 8  # Move up one row
        return x

    def justify_left(x):
        '''Adjust polyomino to touch left side.
        '''
        # Can be sped up using leading zeros approach
        while x & 0x0101010101010101 == 0:
            x = x >> 1  # Move left one column
        return x

    @classmethod
    def rotate(cls, x):
        '''Rotate 8x8 bit matrix 90 degrees counterclockwise.
        >>> BitPolyomino.rotate(0x8888888ff)
        72340301687095567
        '''
        return cls.vertical_reflect(cls.transpose(x))

    @classmethod
    def canonical_c4(cls, x):
        '''Return C_4 rotation with smallest integer
        >>> BitPolyomino.canonical_c4(0x8888888ff)
        36650387711
        '''
        x = cls.justify_top(x)
        x = cls.justify_left(x)
        best = x
        for ii in range(3):
            x = cls.transpose(x)
            x = cls.vertical_reflect(x)
            x = cls.justify_top(x)
            best = min(best, x)
        return best

    @classmethod
    def canonical_d4(cls, x):
        '''Return D_4 position with smallest integer
        >>> BitPolyomino.canonical_d4(0x8888888ff)
        36650387711
        '''
        x = cls.justify_top(x)
        x = cls.justify_left(x)
        best = x
        for ii in range(4):
            x = cls.transpose(x)
            best = min(best, x)
            if ii == 3:
                break
            x = cls.vertical_reflect(x)
            x = cls.justify_top(x)
            best = min(best, x)
        return best


if __name__ == '__main__':
    import doctest
    doctest.testmod()
