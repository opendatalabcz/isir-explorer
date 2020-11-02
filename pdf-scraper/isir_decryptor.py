import re

class IsirDecryptor:

    # Povolené znaky mimo základní ASCII rozsah
    KNOWN_CHARS = set(
        [
            'á','č','ě','é','ď','í','ì','ň','ó','ř','š','ť','ú','ů','ü','ý','ž',
            'Á','Č','Ć','Ě','È','Í','Ř','Š','Ů','Ú','Ý','Ž','–'
        ]
    )

    # Tabulka pro nahrazení znaků s diakritikou a jiných speciálních znaků
    REPLACE = [
        ([195, 136], 'á'),
        ([199, 143], 'č'),
        ([199, 148], 'ě'),
        ([195, 143], 'é'),
        ([199, 146], 'ď'),
        ([195, 147], 'í'),
        ([195, 150], 'ì'),
        ([199, 170], 'ň'),
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
        ([194, 181], 'È'),       
        ([194, 182], 'Í'),
        ([198, 178], 'Ř'),
        ([195, 128], 'Š'),
        ([198, 190], 'Ů'),
        ([195, 129], 'Ú'),
        ([195, 133], 'Ý'),
        ([195, 135], 'Ž'),
        ([205, 131], ' '), #oddelovac radu
        ([205, 130], '-'), #‑
        ('?', ' '),
        ([0x7f], ')')
    ]

    SHIFT = 31

    def __init__(self):
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

                print(f"Unknown char: '{c}' ({ord(c)}, [{strCodes}]), used in text '{txtPart}'")

        return res
