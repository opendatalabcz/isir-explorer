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

    PARSER_TYPES = [
        PrihlaskaParser,
        PrehledovyListParser,
        ZpravaProOddluzeniParser,
        ZpravaPlneniOddluzeniParser,
        ZpravaSplneniOddluzeniParser,
    ]
    
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
        for parserCls in self.PARSER_TYPES:
            parser = parserCls(data)

            try:
                parser.run()
            except UnreadableDocument:
                continue

            documents.append(parser.model)
        
        if not documents:
            print("Necitelny dokument", file=sys.stderr)
            exit(1)

        # Save output
        output = json.dumps(documents, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
        self.config['_out'].write(output)

