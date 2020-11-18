import subprocess
import os
import sys
import json
from isir_decryptor import IsirDecryptor
from parser.prihlaska_pohledavky import PrihlaskaParser
from parser.prehledovy_list import PrehledovyListParser
from parser.zprava_pro_oddluzeni import ZpravaProOddluzeniParser
from parser.zprava_plneni_oddluzeni import ZpravaPlneniOddluzeniParser
from parser.zprava_splneni_oddluzeni import ZpravaSplneniOddluzeniParser
from parser.errors import UnreadableDocument

class IsirScraper:

    PARSER_TYPES = {
        "Prihlaska": PrihlaskaParser,
        "PrehledovyList": PrehledovyListParser,
        "ZpravaProOddluzeni": ZpravaProOddluzeniParser,
        "ZpravaPlneniOddluzeni": ZpravaPlneniOddluzeniParser,
        "ZpravaSplneniOddluzeni": ZpravaSplneniOddluzeniParser,
    }
    
    def __init__(self, filename, config):
        self.config = config
        self.filename = filename

        base = os.path.basename(self.filename)
        parts = os.path.splitext(base)
        self.document_name = parts[0]

        self.tmp_path = self.config['tmp_dir']
        self.tmpDir()

    def tmpDir(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    @staticmethod
    def getParserByName(name):
        name = name.lower()
        for key in IsirScraper.PARSER_TYPES:
            if name == key.lower():
                return IsirScraper.PARSER_TYPES[key]
        return None
    
    def run(self):
        # To text
        output_path = self.tmp_path+'/'+self.document_name
        subprocess.run([self.config['pdftotext'], "-layout", "-nodiag", "-nopgbrk", self.filename, output_path])

        with open(output_path, 'rb') as f:
            txtBytes = f.read()

        decryptor = IsirDecryptor()
        data = decryptor.decrypt(txtBytes)
        
        with open(output_path+".dec", "w") as f:
            f.write(data)

        # Parse
        documents = []
        if self.config['doctype']:
            # Use only the parser selected by the user
            parsers = [ self.getParserByName(self.config['doctype']) ]
        else:
            # Use all parser types (detect document type)
            parsers = self.PARSER_TYPES.values()

        for parserCls in parsers:
            parser = parserCls(data)

            try:
                parser.run()
            except UnreadableDocument:
                continue

            documents.append(parser.model)

            # Pokud neni aktivni --multidoc, zastavit hledani po prvnim parsovanem dokumentu
            if not self.config['multidoc']:
                break
        
        if not documents:
            print("Necitelny dokument", file=sys.stderr)
            exit(1)

        # Pokud neni aktivni --multidoc, zobrazit vzdy jen prvni dokument
        if not self.config['multidoc']:
            documents = documents[0]

        # Save output
        output = json.dumps(documents, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
        self.config['_out'].write(output)

