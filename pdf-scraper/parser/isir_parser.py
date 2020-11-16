from parser.parser import Parser
from parser.model.parts.spisova_znacka import SpisovaZnacka
from parser.errors import NoSplitterFound, UnreadableDocument
import re


class IsirParser(Parser):

    def __init__(self, data):
        super().__init__()
        self.txt = data
        self.lines = None

    def spisovaZnacka(self, txt):
        part1 = self.textBefore(txt, "INS")
        soudSenat = part1.split(" ", 2)

        part2 = self.textAfter(txt, "INS").split("/", 2)

        znacka = SpisovaZnacka()
        znacka.Soud = soudSenat[0].strip()
        znacka.Senat = soudSenat[1].strip()
        znacka.Ins = "INS"
        znacka.Cislo = part2[0].strip()
        znacka.Rok = part2[1].strip()
        return znacka

    def removeVersionLine(self):
        temp = []
        for line in self.lines:
            res = re.match('^[\s]{10,}(?:Stránka [0-9]+ z [0-9]+)?[\s]+Verze ([A-Za-z0-9\-]+)$', line)
            if res:
                # Ulozit verzi pokud jeste neni nastavena
                if self.model.Metadata.Verze is None:
                    self.model.Metadata.Verze = res[1]
            else:
                temp.append(line)
        self.lines = temp
        self.txt = '\n'.join(temp)

    def extractDocument(self):
        pass

    def run(self):
        self.model.Metadata.Typ = self.model.TYP_DOKUMENTU

        # Pokud pdf obsahuje vice typu dokumentu, vybrat text toho aktualniho
        try:
            self.extractDocument()
        except NoSplitterFound:
            raise UnreadableDocument()

        # Odstrani radky v zapati stranek s informaci o verzi dokumentu
        self.removeVersionLine()