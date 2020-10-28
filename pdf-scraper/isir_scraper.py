import subprocess
import os
from isir_decryptor import IsirDecryptor
from parser.prihlaska_pohledavky import PrihlaskaParser


class IsirScraper:
    
    def __init__(self, filename):
        self.filename = filename

        base = os.path.basename(self.filename)
        parts = os.path.splitext(base)
        self.document_name = parts[0]

        self.tmp_path = '/tmp/isir'
        self.tmpDir()

    def tmpDir(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)
    
    def run(self):
        # To text
        output_path = self.tmp_path+'/'+self.document_name
        subprocess.run(["/home/tumapav3//bin/pdftotext2", "-layout", "-nopgbrk", self.filename, output_path])

        with open(output_path, 'rb') as f:
            txtBytes = f.read()

        decryptor = IsirDecryptor()
        data = decryptor.decrypt(txtBytes)
        
        with open(output_path+".dec", "w") as f:
            f.write(data)

        # Parse
        # Zatím pouze přihláška pohledávky 5-a
        parser = PrihlaskaParser(data)
        parser.run()

        # Save output
        output = parser.model.toJSON()
        with open(output_path+".json", "w") as f:
            f.write(output)

