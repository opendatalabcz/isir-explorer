from isir_explorer.scraper.isir_decryptor import IsirDecryptor
import pytest

@pytest.mark.parametrize(
    ['vstup', 'vystup'],
    [
     ("",""),
     ("'Z[JDLÈPTPCB", "01 Fyzická osoba"),
     ("1Ʋ*)-«À,\"10)-&%«7,:", "PŘIHLÁŠKA POHLEDÁVKY"),
     ("ƎQǏF", "Č.p./č.e.:"),
     ("0CFD","Obec:"),
     ("14Ǝ","PSČ:"),
     ("6MJDF","Ulice:"),
     ("EBUVNOBSP[FOÓTFWZQMOÓ","datum narození se vyplní"),
     ("1ǲJIMÈÝLBQPIMFEÈWLZ","+Přihláška pohledávky"),
     ("1PIMFEÈWLBǏ ","Pohledávka č. 1"),
     ("5ZQQPIMFEÈWLZ","Typ pohledávky:"),
     ("7âÝFKJTUJOZ","Výše jistiny "),
     ("%ǾWPEW[OJLV","06 Důvod vzniku:"),
     ("7MBTUOPTUJQPIMFEÈWLZ","10 Vlastnosti pohledávky:"),
     ("1PIMFEÈWLB","Pohledávka:"),
     ("5ZQQPIMFEÈWLZ","Typ pohledávky:"),
     ("7âÝFKJTUJOZ	,Ǐ","Výše jistiny (Kč):"),
     ("7FS[F B","Verze 4-a"),
     ("4QMBUOÈ","Splatná:"),
     ("1PENÓOǔOÈ ","Podmíněná: "),
     ("1FOǔäJUÈ","Peněžitá:"),
     ("1PEǲÓ[FOÈ","Podřízená:"),
     (",Ǐ","540 Kč"),
     ("PEMFLVS[VƎ/#LFEOJTQMBUOPTUJQPIMFEÈWL","odle kurzu ČNB ke dni splatnosti pohledávk"),
    ],
)
def test_decode(vstup, vystup):
    d = IsirDecryptor()
    res = d.decrypt(bytes(vstup,"utf8"))
    print(res)
    assert res == vystup
