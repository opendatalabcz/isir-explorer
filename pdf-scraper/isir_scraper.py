import subprocess
import os
from isir_decryptor import IsirDecryptor
from parser.prihlaska_pohledavky import PrihlaskaParser
from parser.prehledovy_list import PrehledovyListParser
from parser.zprava_pro_oddluzeni import ZpravaProOddluzeniParser
from parser.zprava_plneni_oddluzeni import ZpravaPlneniOddluzeniParser
from parser.zprava_splneni_oddluzeni import ZpravaSplneniOddluzeniParser

class IsirScraper:
    
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
        #parser = PrihlaskaParser(data)
        #parser = PrehledovyListParser(data)
        #parser = ZpravaProOddluzeniParser(data)
        #parser = ZpravaPlneniOddluzeniParser(data)
        parser = ZpravaSplneniOddluzeniParser(data)
        parser.run()

        # Save output
        output = parser.model.toJSON()
        self.config['_out'].write(output)

