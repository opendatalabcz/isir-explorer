import re


class Parser:

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
        return txt.replace(' ', '').replace(',', '.')

    def reMatch(self, txt, reg):
        return re.match(reg, txt)

    def reTextAfter(self, txt, reg):
        l = re.compile(reg).split(txt)
        if len(l) == 1:
            return txt #no matches
        l.pop(0) #remove text before 1st splitter
        res = ''.join(l)
        return res.strip()

    def reSplitText(self, txt, reg, keepSplit=True):
        parts = re.compile(reg, re.MULTILINE).split(txt)

        if keepSplit:
            res = [parts.pop(0)]
            for i,p in enumerate(parts):
                if i % 2 == 0:
                    res.append(p)
                else:
                    res[-1] += p
            return res

        return parts