import re
import regex
from .errors import NoSplitterFound


class Parser:
    """Parser třída se základními funkcemi pro zpracování textového výstupu
    pdftotext a pro extrakci polí z formulářů.
    """

    #: :obj:`str` :
    #: Regulární výraz pro částku v korunách
    RE_KC_AMOUNT = "^((:?[0-9]+ )*(:?[0-9]+)(:?,[0-9]+)? Kč)$"

    #: :obj:`str` :
    #: Regulární výraz pro hodnotu v procentech
    RE_PERCENT = "^([0-9]+(?:,[0-9]+)?[\s]?%)$"

    #: :obj:`str` :
    #: Regulární výraz pro celočíselnou hodnotu
    RE_INT = "^[0-9]+$"

    def textBetween(self, txt, start, end):
        """Text vymezený prvními výskyty hleadných řetězců.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        start: :class:`str`
            Hledaný řetězec určující začátek výstupu.
        end: :class:`str`
            Hledaný řetězec určující konec výstupu.
        """
        part = self.textAfter(txt, start)
        return part.split(end, 2)[0].strip()

    def textBefore(self, txt, end):
        """Text před prvním výskytem hleadného výrazu.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        start: :class:`str`
            Hledaný řetězec určující konec výstupu.
        """
        return txt.split(end, 2)[0].strip()

    def textAfter(self, txt, start):
        """Text za prvním výskytem hleadného výrazu.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        start: :class:`str`
            Hledaný řetězec určující začátek výstupu.
        """
        parts = txt.split(start)
        if len(parts) > 2:
            parts.pop(0)
            return start.join(parts).strip()
        else:
            return parts[-1].strip()

    def removeSpaces(self, txt):
        """Odstraní z textu duplicitní mezery.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        """
        return re.sub(' +', ' ', txt)

    def numbersOnly(self, txt, toInt=True):
        """Z textu vrátí pouze číselné hodnoty.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        toInt: :class:`bool`
            Vrátit hodnotu jako datový typ int. Pokud vstupní řetězec neobsahuje
            žádné číselné hodnoty, výstupem konverze je None.
            Výchozí je True.
        """
        s = re.sub("[^0-9]", "", txt)
        if toInt:
            if "" == s:
                return None
            return int(s)
        else:
            return s

    def textBlock(self, txt):
        """Odstraní duplicitní mezery a nahradí odřádkování v textu mezerami.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        """
        return self.removeSpaces(txt.replace('\n', ' ')).strip()

    def priceValue(self, txt):
        """Standardizace číselné hodnoty z textu.

        Odstraní z textu nečíselné znaky, zachovány jsou desetinné čárky/tečky.
        Nahradí desetinnou čárku tečkou. Řetězec je následně převeden na číselnou
        hodnotu typu float.

        Pokud vstupní text neobsahuje číselnou hodnotu a nebo není možné
        text převést na typ float, je vrácen None.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        """
        s = re.sub("[^0-9,.]", "", txt).replace(',', '.')
        try:
            return float(s)
        except ValueError:
            return None

    def reMatch(self, txt, reg):
        """Vrací výsledek aplikace regulárního výrazu na zadaný text.

        Parametry
        ---------
        txt: :class:`str`
            Text.
        reg: :class:`str`
            Regulární výraz.
        """
        return re.match(reg, txt)

    def fieldText(self, txt, reg):
        """Vrátí obsah položky ve formuláři určené zadaným regulárním výrazem.

        Čte obsah pole formuláře specifikovaného prvním výskytem regulárního výrazu nadpisu.
        Text je čten vpravo od nadpisu pole a následně řádky pod nadpisem až dokud není
        v textu nelzen nadpis dalšího formulářového pole.

        Parametry
        ---------
        txt: :class:`str`
            Víceřádkový text.
        reg: :class:`str`
            Regulární výraz.
        """
        match = re.compile(reg, re.MULTILINE).search(txt)
        if not match:
            return ""

        matchStart = match.span(0)[0]
        matchEnd = match.span(0)[1]

        fieldName = match.group(0)

        offset = 0
        for c in fieldName:
            if c == ' ':
                offset += 1
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
        a vrátí text nacházející se v tomto řádku za částí nalezenou regulárním výrazem.

        Parametry
        ---------
        txt: :class:`str`
            Víceřádkový text.
        reg: :class:`str`
            Regulární výraz.
        """

        reg += "(.*)$"
        match = re.compile(reg, re.MULTILINE).search(txt)
        if not match:
            return ""
        else:
            return match[1].strip()

    def reTextAfter(self, txt, reg, multiline=False, allow_no_match=True, keep_split=False):
        """Vrátí text za prvním výskytem regulárního výrazu

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        reg: :class:`str`
            Regulární výraz definující začátek textu.
        multiline: :class:`bool`
            Zda se mají regulární výrazy aplikovat ve víceřádkovém režimu.
            Výchozí je True.
        allow_no_match: :class:`bool`
            Pokud je True a regulární výraz nenajde žádnou shodu, výstupem je vtupní text bez změny.
            Pokud je False a regulární výraz nenajde žádnou shodu, funkce generuje :class:`NoSplitterFound`.
            Výchozí je True.
        keep_split: :class:`bool`
            Zda se mají ve výstupním textu zachovat okrajové texty definované regulárním výrazem.
            Výchozí je False.

        Raises
        -------
        NoSplitterFound
            Pokud se regulární výraz nepodaří vyhledat a allow_no_match je False.
        """
        l = self.reSplitText(txt, reg, keep_split=keep_split,
                             multiline=multiline, split_pos=0)
        if len(l) == 1:
            # No matches
            if allow_no_match:
                return txt
            else:
                raise NoSplitterFound()
        l.pop(0)  # remove text before 1st splitter
        res = ''.join(l)
        return res.strip()

    def reTextBefore(self, txt, reg, multiline=False, allow_no_match=True, keep_split=False):
        """Vrátí text před prvním výskytem regulárního výrazu

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        reg: :class:`str`
            Regulární výraz definující konec textu.
        multiline: :class:`bool`
            Zda se mají regulární výrazy aplikovat ve víceřádkovém režimu.
            Výchozí je True.
        allow_no_match: :class:`bool`
            Pokud je True a regulární výraz nenajde žádnou shodu, výstupem je vtupní text bez změny.
            Pokud je False a regulární výraz nenajde žádnou shodu, funkce generuje :class:`NoSplitterFound`.
            Výchozí je True.
        keep_split: :class:`bool`
            Zda se mají ve výstupním textu zachovat okrajové texty definované regulárním výrazem.
            Výchozí je False.

        Raises
        -------
        NoSplitterFound
            Pokud se regulární výraz nepodaří vyhledat a allow_no_match je False.
        """
        l = self.reSplitText(txt, reg, keep_split=keep_split,
                             multiline=multiline, split_pos=1)
        if len(l) == 1:
            # No matches
            if allow_no_match:
                return txt
            else:
                raise NoSplitterFound()
        return l.pop(0).strip()

    def reTextBetween(self, txt, regA, regB, multiline=True, keep_split=False):
        """Vrátí text mezi dvěma hledanými texty, zadanými regulárními výrazy.

        Text za prvním výskytem výrazu regA se rozdělí dle prvního výskutu regB a je vrácen
        text před regB.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        regA: :class:`str`
            Regulární výraz definující začátek textu.
        regB: :class:`str`
            Regulární výraz definující konec textu.
        multiline: :class:`bool`
            Zda se mají regulární výrazy aplikovat ve víceřádkovém režimu.
            Výchozí je True.
        keep_split: :class:`bool`
            Zda se mají ve výstupním textu zachovat okrajové texty definované regulárním výrazem.
            Výchozí je False.

        Raises
        -------
        NoSplitterFound
            Pokud se jeden z regulárních výrazů nepodaří vyhledat.
        """
        after = self.reTextAfter(txt, regA, multiline, False, keep_split)
        before = self.reTextBefore(after, regB, multiline, False, keep_split)
        return before

    def reSplitText(self, txt, reg, keep_split=True, multiline=True, split_pos=0):
        """Rozdělit text dle regulárního výrazu.

        Parametry
        ---------
        txt: :class:`str`
            Vstupní text.
        reg: :class:`str`
            Regulární výraz, dle kterého text rozdělit. Nesmí obsahovat capturing groups.
        keep_split: :class:`bool`
            Zda se má zachovat dělící řetězec obsažen regulárním výrazem.
            Výchozí je True.
        split_pos: :class:`int`
            Pokud je keep_split=True, nastavení určuje, kam má být umístěn dělící řetězec.
            0 = dělící řetězec zahrnut v lichých indexech výstupního rozdělení
            1 = dělící řetězec zahrnut v sudých indexech výstupního rozdělení
            Výchozí hodnota je 0.
        """

        # Pridat globalni capturing group
        reg = reg if not keep_split else "("+reg+")"

        if multiline:
            parts = re.compile(reg, re.MULTILINE).split(txt)
        else:
            parts = re.compile(reg).split(txt)

        if keep_split:
            res = [parts.pop(0)]
            for i, p in enumerate(parts):
                if i % 2 == split_pos:
                    res.append(p)
                else:
                    res[-1] += p
            return res

        return parts

    def reTextColumn(self, txt, reg):
        """
        Z víceřádkového textu vrátí text udpovídající sloupci definovaném prvním výskytem
        regulárního výrazu.
        Pokud není hledaný výraz v textu nalezen, je vrácen prázdný řetězec.

        Parametry
        ---------
        txt: :class:`str`
            Víceřádkový text.
        reg: :class:`str`
            Regulární výraz určující pozici a šířku sloupce.
        """
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
