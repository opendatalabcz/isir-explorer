import asyncio
import os
import sys
import json
import logging
import subprocess
from .isir_decryptor import IsirDecryptor
from .parser.prihlaska_pohledavky import PrihlaskaParser
from .parser.prehledovy_list import PrehledovyListParser
from .parser.zprava_pro_oddluzeni import ZpravaProOddluzeniParser
from .parser.zprava_plneni_oddluzeni import ZpravaPlneniOddluzeniParser
from .parser.zprava_splneni_oddluzeni import ZpravaSplneniOddluzeniParser
from .parser.errors import UnreadableDocument

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
        self.logger = None

        base = os.path.basename(self.filename)
        parts = os.path.splitext(base)
        self.document_name = parts[0]

        self.tmp_path = self.config['tmp_dir']
        self.tmpDir()
        self.setupLogging()

    def setupLogging(self):
        self.logger = logging.getLogger()
        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")

        if self.config['debug']:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)
            self.logger.addHandler(consoleHandler)

    def tmpDir(self):
        if not os.path.exists(self.tmp_path):
            os.makedirs(self.tmp_path)

    @staticmethod
    def getParserByName(name):
        if not name:
            return None
        name = name.lower()
        for key in IsirScraper.PARSER_TYPES:
            if name == key.lower():
                return IsirScraper.PARSER_TYPES[key]
        return None
    
    async def readDocument(self, input_path, multidoc=True):
        output_path = self.tmp_path+'/'+self.document_name
        process = await asyncio.create_subprocess_exec(
            self.config['pdftotext'],
            "-layout",
            "-nodiag",
            "-nopgbrk",
            input_path,
            output_path,
            stderr=subprocess.DEVNULL
        )
        retcode = await process.wait()

        if retcode != 0:
            print(f"Nepodarila se konverze pdftotext, retval: {retcode}", file=sys.stderr)
            return

        with open(output_path, 'rb') as f:
            txtBytes = f.read()

        decryptor = IsirDecryptor(self.logger)
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
            except:
                self.logger.exception("Parser error")
                # Neukladat vystup pokud behem parsovani nastala chyba
                continue

            documents.append(parser.model)

            # Pokud neni aktivni --multidoc, zastavit hledani po prvnim parsovanem dokumentu
            if not multidoc:
                break

        return documents

    async def run(self):
        # To text
        documents = await self.readDocument(
            self.filename,
            multidoc=self.config['multidoc'],
        )
        
        if not documents:
            print("Necitelny dokument", file=sys.stderr)
            exit(1)

        # Pokud neni aktivni --multidoc, zobrazit vzdy jen prvni dokument
        if not self.config['multidoc']:
            documents = documents[0]

        # Save output
        output = json.dumps(documents, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
        self.config['_out'].write(output)

