import re
import logging

class IsirDecryptor:

    # Povolené znaky mimo základní ASCII rozsah
    KNOWN_CHARS = set(
        [
            'á','ą','ä','č','ě','é','ę','ď','í','ì','ň','ń','ó','ř','š','ť','ú','ů','ü','ý','ž',
            'Á','Č','Ć','Ě','É','È','Í','Ř','Š','Ť','Ů','Ú','Ň','Ý','Ž','–', '²', '½', '€'
        ]
    )

    # Tabulka pro nahrazení znaků s diakritikou a jiných speciálních znaků
    REPLACE = [
        ([195, 136], 'á'),
        ([199, 140], 'ą'),
        ([195, 138], 'ä'),
        ([199, 143], 'č'),
        ([199, 148], 'ě'),
        ([195, 143], 'é'),
        ([199, 151], 'ę'),
        ([199, 146], 'ď'),
        ([195, 147], 'í'),
        ([195, 150], 'ì'),
        ([199, 170], 'ň'),
        ([199, 169], 'ń'),
        ([195, 152], 'ó'),
        ([199, 178], 'ř'),
        ([195, 157], 'š'),
        ([199, 184], 'ť'),
        ([195, 158], 'ú'),
        ([199, 190], 'ů'),
        ([195, 160], 'ü'),
        ([195, 162], 'ý'),
        ([195, 164], 'ž'),    
        ([194, 171], 'Á'), #195 129, same code as for Ú
        ([198, 142], 'Č'),
        ([198, 141], 'Ć'),
        ([198, 147], 'Ě'),
        ([194, 178], 'É'),
        ([194, 181], 'È'),       
        ([194, 182], 'Í'),
        ([198, 178], 'Ř'),
        ([195, 128], 'Š'),
        ([198, 184], 'Ť'),
        ([198, 190], 'Ů'),
        ([195, 129], 'Ú'),
        ([198, 170], 'Ň'),
        ([195, 133], 'Ý'),
        ([195, 135], 'Ž'),
        ([205, 131], ' '), # oddelovac radu
        ([205, 130], '-'), # ‑
        ([194, 164], '²'), # metry ctverecni / vymera pozemku
        ([194, 155], '½'),
        ([195, 187], '€'),
        
        ('?', ' '),
        ([0x7f], ')')
    ]

    SHIFT = 31

    def __init__(self, logger = None):
        self.logger = logger
        if logger is None:
            self.logger = logging.getLogger()
        super().__init__()


    def decrypt(self, txtBytes):
        txtByteArray = bytearray()

        for i, b in enumerate(txtBytes):

            # keep newlines
            if b!=10 and b < 128-self.SHIFT:
                b += self.SHIFT

            txtByteArray.append(b)

        txtBytes = bytes(txtByteArray)
        self.inBytes = txtBytes
        self.outBytes = txtByteArray

        regexParts = []
        replacements = {}
        for replacement in self.REPLACE:
            if isinstance(replacement[0], list):
                b = bytes(replacement[0])
            else:
                b = replacement[0].encode('utf-8')
            regexPart=''.join('\\x{:02x}'.format(x) for x in b)
            
            replacements[b] = replacement[1].encode('utf-8')
            regexParts.append(regexPart)

        regexString = '('+'|'.join(regexParts)+')'

        def foo(matchObj):
            return replacements[matchObj[0]]

        txtBytes = re.sub(regexString.encode('utf-8'), foo, txtBytes)

        txtBytes = txtBytes.replace(b'?',b' ')

        res = txtBytes.decode('utf-8')

        # log unknown characters
        for i,c in enumerate(res):
            if ord(c) >= 128 and c not in self.KNOWN_CHARS:
                txtPart = res[max(0,i-10):i+10].replace('\n',' ')
                codes = c.encode('utf-8')
                strCodes = ', '.join(map(str, codes))

                self.logger.warning(f"Neznamny znak: '{c}' ({ord(c)}, [{strCodes}]), v textu '{txtPart}'")

        return res
