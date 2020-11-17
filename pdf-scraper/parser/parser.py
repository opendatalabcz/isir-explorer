import re
import regex
from parser.errors import NoSplitterFound

class Parser:

    RE_KC_AMOUNT = "^((:?[0-9]+ )*(:?[0-9]+)(:?,[0-9]+)? Kč)$"
    RE_PERCENT = "^([0-9]+(?:,[0-9]+)?[\s]?%)$"
    RE_INT = "^[0-9]+$"

    def textBetween(self, txt, start, end):
        part = self.textAfter(txt, start)
        return part.split(end, 2)[0].strip()

    def textBefore(self, txt, end):
        return txt.split(end, 2)[0].strip()

    def textAfter(self, txt, start):
        parts = txt.split(start)
        if len(parts) > 2:
            parts.pop(0)
            return start.join(parts).strip()
        else:
            return parts[-1].strip()

    def removeSpaces(self, txt):
        return re.sub(' +', ' ', txt)

    def numbersOnly(self, txt):
        return re.sub("[^0-9]", "", txt)

    def textBlock(self, txt):
        return self.removeSpaces(txt.replace('\n', ' ')).strip()

    def priceValue(self, txt):
        return re.sub("[^0-9,.]", "", txt).replace(',', '.')

    def reMatch(self, txt, reg):
        return re.match(reg, txt)

    def fieldText(self, txt, reg):
        match = re.compile(reg, re.MULTILINE).search(txt)
        if not match:
            return ""
        
        matchStart = match.span(0)[0]
        matchEnd = match.span(0)[1]

        fieldName = match.group(0)

        offset = 0
        for c in fieldName:
            if c == ' ':
                offset+=1
            else:
                break

        txt = txt[matchEnd:]
        lines = txt.split('\n')
        res = [lines.pop(0)]
        for line in lines:
            if regex.match('^[/s]{0,'+str(offset)+'}([0-9]+ )?([\w\p{L}]+ )*([\w\p{L}]+):', line, flags=regex.UNICODE):
                break
            res.append(line)
        return '\n'.join(res)

    def reLineTextAfter(self, txt, reg):
        """Ve víceřádkovém textu najde řádek, jehož začátek odpovídá zadanému regulárnímu výrazu
        a vrátí text nacházející se v takovém řádku za částí nalezenou regulárním výrazem.

        Args:
            txt (string): víceřádkový text
            reg (string): regulární výraz
        """

        reg+="(.*)$"
        match = re.compile(reg, re.MULTILINE).search(txt)
        if not match:
            return ""
        else:
            return match[1].strip()

    def reTextAfter(self, txt, reg, multiline=False, allow_no_match=True, keep_split=False):
        reg = reg if not keep_split else "("+reg+")"
        l = self.reSplitText(txt, reg, keep_split=keep_split, multiline=multiline, split_pos=0)
        if len(l) == 1:
            # No matches
            if allow_no_match:
                return txt
            else:
                raise NoSplitterFound()
        l.pop(0) #remove text before 1st splitter
        res = ''.join(l)
        return res.strip()

    def reTextBefore(self, txt, reg, multiline=False, allow_no_match=True, keep_split=False):
        reg = reg if not keep_split else "("+reg+")"
        l = self.reSplitText(txt, reg, keep_split=keep_split, multiline=multiline, split_pos=1)
        if len(l) == 1:
            # No matches
            if allow_no_match:
                return txt
            else:
                raise NoSplitterFound()
        return l.pop(0).strip()

    def reTextBetween(self, txt, regA, regB, multiline=True, keep_split=False):
        after = self.reTextAfter(txt, regA, multiline, False, keep_split)
        before = self.reTextBefore(after, regB, multiline, False, keep_split)
        return before

    def reSplitText(self, txt, reg, keep_split=True, multiline=True, split_pos=0):
        """Rozdelit text dle regularniho vyrazu

        Args:
            txt (str): Vstupní text
            reg (str): Regulární výraz, dle kterého text rozdělit
            keep_split (bool, optional): Zda se má zachovat dělící řetězec obsažen regulárním výrazem.
                pro prozdělení. Defaults to True.
            multiline (bool, optional): Víceřádková operace. Defaults to True.
            split_pos (int, optional): 0=splitter zahrnut v lichych indexech, 1=v sudych. Defaults to 0.

        Returns:
            list: Vysledne casti textu po rozdeleni.
        """
        if multiline:
            parts = re.compile(reg, re.MULTILINE).split(txt)
        else:
            parts = re.compile(reg).split(txt)

        if keep_split:
            res = [parts.pop(0)]
            for i,p in enumerate(parts):
                if i % 2 == split_pos:
                    res.append(p)
                else:
                    res[-1] += p
            return res

        return parts

    def reTextColumn(self, txt, reg):
        lines = txt.split('\n')
        reg = re.compile(reg)
        pos = None
        for line in lines:
            res = reg.search(line)
            if res:
                pos = (res.start(), res.end())
                break

        if pos is None:
            return ""
        
        outLines = []
        for line in lines:
            outLines.append(line[pos[0]:pos[1]])

        return '\n'.join(outLines)
