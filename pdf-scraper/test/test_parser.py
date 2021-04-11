from isir_explorer.scraper.parser.parser import Parser
from isir_explorer.scraper.parser.errors import NoSplitterFound
import pytest

def test_textBetween():
    p = Parser()
    inputTxt = "test a start b c b start d 123 az zy zx end 456 end 896"
    res = p.textBetween(inputTxt, "start", "end")
    assert res == "b c b start d 123 az zy zx"

def test_textBetween_chybi_konec():
    p = Parser()
    inputTxt = "test a start b c b"
    res = p.textBetween(inputTxt, "start", "end")
    assert res == "b c b"

def test_textBetween_chybi_zacatek():
    p = Parser()
    inputTxt = "test a b c b end 123"
    res = p.textBetween(inputTxt, "start", "end")
    assert res == "test a b c b"

def test_textBefore():
    p = Parser()
    inputTxt = "test a b c b end 123"
    res = p.textBefore(inputTxt, "end")
    assert res == "test a b c b"

def test_textAfter():
    p = Parser()
    inputTxt = "test a b c b end 123 end 456"
    res = p.textAfter(inputTxt, "end")
    assert res == "123 end 456"

def test_removeSpaces():
    p = Parser()
    inputTxt = " test    a b c    b end  123   end 456"
    res = p.removeSpaces(inputTxt)
    assert res == " test a b c b end 123 end 456"

def test_numbersOnly():
    p = Parser()
    inputTxt = " test    a b c    b end  123   end 456"
    res = p.numbersOnly(inputTxt, False)
    assert res == "123456"

def test_numbersOnly_toInt():
    p = Parser()
    inputTxt = " test    a b c    b end  123   end 456"
    res = p.numbersOnly(inputTxt, True)
    assert res == 123456

def test_numbersOnly_noNum():
    p = Parser()
    inputTxt = " test    a b c    b end   end "
    res = p.numbersOnly(inputTxt, True)
    assert res is None

def test_textBlock():
    p = Parser()
    inputTxt = """
                        Lorem ipsum dolor sit amet,
                        consectetuer adipiscing elit.
                        Donec vitae arcu. Duis condimentum
                        augue id magna semper rutrum.
                        Duis bibendum, lectus ut viverra
                        rhoncus, dolor nunc faucibus
                        libero, eget facilisis enim
                        ipsum id lacus."""
    res = p.textBlock(inputTxt)
    assert res == "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Donec vitae arcu. Duis condimentum augue id magna semper rutrum. Duis bibendum, lectus ut viverra rhoncus, dolor nunc faucibus libero, eget facilisis enim ipsum id lacus."
    
def test_priceValue():
    p = Parser()
    inputTxt = " test  18 855,00  a b c    b end   end "
    res = p.priceValue(inputTxt)
    assert res == 18855.0
    assert p.priceValue("18") == 18
    assert p.priceValue("c18.") == 18
    assert p.priceValue("c18.,8") is None

def test_fieldText():
    p = Parser()
    inputTxt = """
12 Test:           1112,77
13 Důvod vzniku:  Lorem ipsum
                         dolor sit amet,
                         consectetuer adipiscing
                         elit.
      
14 Test:                    444
      
    """
    res = p.fieldText(inputTxt, "^[\s]*[0-9]+ Důvod vzniku:")
    assert res.replace(' ', '').replace('\n','') == 'Loremipsumdolorsitamet,consectetueradipiscingelit.'

def test_reLineTextAfter():
    p = Parser()
    inputTxt = "  Výše zálohy 1000"
    res = p.reLineTextAfter(inputTxt, "^[\s]*Výše zálohy")
    assert res == "1000"
    
def test_reLineTextAfter_noMatch():
    p = Parser()
    inputTxt = "  Lorem ipsum 1000"
    res = p.reLineTextAfter(inputTxt, "^[\s]*Výše zálohy")
    assert res == ""

def test_reTextAfter():
    p = Parser()
    inputTxt = """
  12 Test:           1112,77
   Odůvodnění:  Lorem ipsum
                         dolor sit amet.
      
    """
    res = p.reTextAfter(inputTxt, "^[\s]*Odůvodnění:", True)
    assert res.replace(' ', '').replace('\n','') == 'Loremipsumdolorsitamet.'

def test_reTextAfter_noMultiline():
    p = Parser()
    inputTxt = """
   Odůvodnění:  Lorem ipsum\n
                         dolor sit amet.
      
    """
    res = p.reTextAfter(inputTxt, "^[\s]*Odůvodnění:", False)
    assert res.replace(' ', '').replace('\n','') == 'Loremipsumdolorsitamet.'
    inputTxt = """
   12 Test:           1112,77
   Odůvodnění:  Lorem ipsum\n
                         dolor sit amet.
      
    """
    res = p.reTextAfter(inputTxt, "^[\s]*Odůvodnění:", False)
    assert res.replace(' ', '').replace('\n','') == '12Test:1112,77Odůvodnění:Loremipsumdolorsitamet.'

def test_reTextAfter_noMatch():
    p = Parser()
    inputTxt = """
   12 Test:           1112,77
   Odůvodnění:  Lorem ipsum\n
                         dolor sit amet.
      
    """
    with pytest.raises(NoSplitterFound):
        res = p.reTextAfter(inputTxt, "^[\s]*Odůvodnění:", False, False)

def test_reTextAfter_keepSplit():
    p = Parser()
    inputTxt = """
  12 Test:           1112,77
   Odůvodnění:  Lorem ipsum
                         dolor sit amet.
      
    """
    res = p.reTextAfter(inputTxt, "^[\s]*Odůvodnění:", True, False, True)
    assert res.replace(' ', '').replace('\n','') == 'Odůvodnění:Loremipsumdolorsitamet.'

def test_reTextBefore():
    p = Parser()
    inputTxt = """
  12 Test:           1112,77
   Odůvodnění:  Lorem ipsum
                         dolor sit amet.
      
    """
    res = p.reTextBefore(inputTxt, "^[\s]*Odůvodnění:", True)
    assert res.replace(' ', '').replace('\n','') == '12Test:1112,77'

def test_reTextBefore_noMultiline():
    p = Parser()
    inputTxt = """Test Odůvodnění:  Lorem ipsum\n
                         dolor sit amet.
      
    """
    res = p.reTextBefore(inputTxt, "Odůvodnění:", False)
    assert res.replace(' ', '').replace('\n','') == 'Test'
    inputTxt = """
    Test
   Odůvodnění:  Lorem ipsum\n
                         dolor sit amet.
      
    """
    res = p.reTextBefore(inputTxt, "^[\s]*Odůvodnění:", False)
    assert res.replace(' ', '').replace('\n','') == 'TestOdůvodnění:Loremipsumdolorsitamet.'
    inputTxt = """
   12 Test:           1112,77
   Odůvodnění:  Lorem ipsum\n
                         dolor sit amet.
      
    """
    res = p.reTextBefore(inputTxt, "^[\s]*Odůvodnění:", False)
    assert res.replace(' ', '').replace('\n','') == '12Test:1112,77Odůvodnění:Loremipsumdolorsitamet.'

def test_reTextBefore_noMatch():
    p = Parser()
    inputTxt = """
   12 Test:           1112,77
   Odůvodnění:  Lorem ipsum\n
                         dolor sit amet.
      
    """
    with pytest.raises(NoSplitterFound):
        res = p.reTextBefore(inputTxt, "^[\s]*Odůvodnění:", False, False)

def test_reTextBefore_keepSplit():
    p = Parser()
    inputTxt = """
  12 Test:           1112,77
   Odůvodnění:  Lorem ipsum
                         dolor sit amet.
      
    """
    res = p.reTextBefore(inputTxt, "^[\s]*Odůvodnění:", True, False, True)
    assert res.replace(' ', '').replace('\n','') == '12Test:1112,77Odůvodnění:'

def test_reTextBetween():
    p = Parser()
    inputTxt = """
Lorem ipsum
                         dolor sit amet.
  Dlužník           1112,77
   Věřitel  Lorem ipsum
                         dolor sit amet.
      
    """
    res = p.reTextBetween(inputTxt, "^[\s]+Dlužník", "^[\s]+Věřitel")
    assert res.replace(' ', '').replace('\n','') == '1112,77'

def test_reSplitText():
    p = Parser()
    inputTxt = "Test    12,2%  14%  13 % ----"
    res = p.reSplitText(inputTxt, "[0-9]+(?:,[0-9]+)?[\s]?%")
    assert len(res) == 4

def test_reSplitText_keepSplit():
    p = Parser()
    inputTxt = "A|||B||C|D"
    res = p.reSplitText(inputTxt, "[|]+")
    assert len(res) == 4
    res = p.reSplitText(inputTxt, "[|]+", False)
    assert len(res) == 4
    assert res == ['A', 'B', 'C', 'D']

def test_reSplitText_splitPos():
    p = Parser()
    inputTxt = "A|||B||C|D"
    res = p.reSplitText(inputTxt, "[|]+", split_pos=1)
    assert len(res) == 4
    assert res == ['A|||', 'B||', 'C|', 'D']
    res = p.reSplitText(inputTxt, "[|]+", split_pos=0)
    assert len(res) == 4
    assert res == ['A', '|||B', '||C', '|D']
    res = p.reSplitText(inputTxt, "[|]+", False, split_pos=1)
    assert len(res) == 4
    assert res == ['A', 'B', 'C', 'D']

def test_reTextColumn():
    p = Parser()
    inputTxt = """
     ===SLOUPEC A===   ============SLOUPEC B================  ===SLOUPEC C===
           1            Lorem ipsum dolor sit amet,
           12           consectetuer adipiscing elit.
        14              Donec vitae arcu. Duis condimentum
                  16    augue id magna semper rutrum.
           10           Duis bibendum, lectus ut viverra
         11             rhoncus, dolor nunc faucibus
           11           libero, eget facilisis enim
                        ipsum id lacus."""

    res = p.reTextColumn(inputTxt, "===SLOUPEC A===")
    assert res.replace(' ', '').replace('\n','') == "===SLOUPECA===1121416101111"

    res = p.reTextColumn(inputTxt, "============SLOUPEC B================")
    assert res.replace(' ', '').replace('\n','') == "============SLOUPECB================Loremipsumdolorsitamet,consectetueradipiscingelit.Donecvitaearcu.Duiscondimentumaugueidmagnasemperrutrum.Duisbibendum,lectusutviverrarhoncus,dolornuncfaucibuslibero,egetfacilisisenimipsumidlacus."

    res = p.reTextColumn(inputTxt, "===SLOUPEC C===")
    assert res.replace(' ', '').replace('\n','') == "===SLOUPECC==="