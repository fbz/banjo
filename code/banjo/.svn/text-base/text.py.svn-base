#!/usr/bin/python
# -*- coding: utf-8 -*-


# Text generator for PIC+VGA
# resolution = 25x16, letter size = 4x7


class FontError(Exception):
    pass

class Font:

    _data   = {}
    _width  = None
    _height = None
    _file   = None

    def __init__(self, file):
        self._parse(file)

    def raw_data(self):
        return self._data

    def letters(self):
        return self._data.keys()

    def _parse(self, file):
        self._file = file
        
        lines = "".join(open(file, 'r').readlines()).split("#-")

        width, height = tuple([int(x) for x in lines[0].split('X')])

        letter = "None"
        
        for L in lines[1:]:
            L = [l.rstrip() for l in L[:-1].split("\n")]
            letter = L[0]
            if len(letter) == 0:
                continue
            if letter[0] == "%":
                # special case; if its a %, specify the char as a number.
                if letter[1] == "%":
                    letter = "%"
                else:
                    letter = chr(int(letter[1:]))
                    
            assert len(letter) == 1, "Protocol error: unknown symbol: '%s'" % letter
            lines = L[1:]
            assert len(lines) == height, "Protocol error: invalid nr of lines in letter %s" % letter
            self._data[letter] = []
            #print letter, [len(x) for x in lines]
            for d in lines:
                row = [0] * width
                for i in range(len(d)):
                    if d[i] == 'X':
                        row[i] = 1
                self._data[letter].append(row)

        self._width  = width
        self._height = height

    def width(self):
        return self._width

    def height(self):
        return self._height

    def render(self, grid, text, pos=(0,0), center=False):
        """ renders left-aligned text. wraps if it doesnt fit. """
        ox = pos[0]
        oy = pos[1]
        first = True

        text = self.mapchars(text)

        if center:
            ox += grid.get_cols()/2 - (len(text)*(self._width+1))/2
        for letter in text:
            if letter == ' ' and first:
                continue
            if letter in self._data:
                for y in range(self._height):
                    for i in range(self._width):
                        if self._data[letter][y][i] == 1:
                            grid.set(ox+i, oy+y, True)

            if not center and (ox + self._width+self._width) >= grid.get_cols():
                oy += self._height + 1
                ox = pos[0]
                first = True
            else:
                ox += self._width+1
                first = False

        if not first:
            oy += self._height
        return ox, oy


    def substitute(self, text, replace = ""):
        """ Given a string, uppercases it and substitutes all letters
        in the string which are not part of the font by the given
        character."""
        s = []
        text = text.upper()
        for letter in text:
            if letter not in self.letters():
                s.append(replace)
            else:
                s.append(letter)
        return "".join(s)


    def mapchars(self, s):
        import unicodedata
        return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
        # mapping = [ (u"í", "i"), (u"ì", "i"), (u"ï", "i"), (u"è", "e"), (u"ë", "e"), (u"é", "e"), (u"à", "a"), (u"ä", "a"), (u"á", "a"), (u"ò", "o"), (u"ö", "o"), (u"ó", "o"), (u"ñ", "n"), (u"Í", "I"), (u"Ì", "I"), (u"Ï", "I"), (u"È", "E"), (u"Ë", "E"), (u"É", "E"), (u"À", "A"), (u"Ä", "A"), (u"Á", "A"), (u"Ò", "O"), (u"Ö", "O"), (u"Ó", "O"), (u"Ñ", "N")]
        # for frm,to in mapping:
        #     s = s.replace(frm, to)
        # return s



    def getBDFGlyphData(self, letter):
        data = []
        for y in range(self._height):
            val = 0
            for x in range(self._width):
                bit = 1 << (8-(x+1))
                if self._data[letter][y][x] == 1:
                    val += bit
            data.append("%02X" % val)
        print letter, data
        return data


    def writeBDF(self, name, fn):
        from bdflib import model, writer
        f = model.Font(name, 64, 96,96)
        for letter in self._data:
            f.new_glyph_from_data(letter, self.getBDFGlyphData(letter), 0, 0, self._width, self._height, 0, ord(letter))
            if letter == letter.lower():
                continue
            letter = letter.lower()
            f.new_glyph_from_data(letter, self.getBDFGlyphData(letter.upper()), 0, 0, self._width, self._height, 0, ord(letter))

        fp = open(fn, "w")
        writer.write_bdf(f, fp)
        fp.close()
