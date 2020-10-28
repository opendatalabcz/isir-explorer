from parser.parser import Parser
from parser.model.parts.spisova_znacka import SpisovaZnacka


class IsirParser(Parser):

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
