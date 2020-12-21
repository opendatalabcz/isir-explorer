import asyncio
import os
import shutil
import re
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
from .parser.errors import UnreadableDocument, EmptyPdfPortfolio, NotPdfPortfolio

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

        self.is_empty = False
        self.tmp_path = self.config['tmp_dir'].rstrip("/")
        self.unpack_path = self.config['tmp_dir'] + "/unpack"
        self.unreadable_path = self.config['tmp_dir'] + "/unreadable"
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
        if not os.path.exists(self.unpack_path):
            os.makedirs(self.unpack_path)
        if self.config['save_unreadable'] and not os.path.exists(self.unreadable_path):
            os.makedirs(self.unreadable_path)

    @staticmethod
    def getParserByName(name):
        if not name:
            return None
        name = name.lower()
        for key in IsirScraper.PARSER_TYPES:
            if name == key.lower():
                return IsirScraper.PARSER_TYPES[key]
        return None
    
    async def unpackPdf(self, input_path):
        tmp_unpack_dir = self.unpack_path + "/" + self.document_name
        if not os.path.exists(tmp_unpack_dir):
            os.makedirs(tmp_unpack_dir)
        unpack_process = await asyncio.create_subprocess_exec(
            self.config['pdftk'],
            input_path,
            "unpack_files",
            "output",
            tmp_unpack_dir,
            stderr=subprocess.DEVNULL
        )
        retcode = await unpack_process.wait()
        files = os.listdir(tmp_unpack_dir)
        if files:
        
            if self.config['unpack_filter']:
                regex = re.compile(self.config['unpack_filter'])
                files = [i for i in files if not regex.match(i)]

            files = [tmp_unpack_dir + "/" + i for i in files]

            if not files:
                raise EmptyPdfPortfolio
            
            return files
        else:
            shutil.rmtree(tmp_unpack_dir)
            raise NotPdfPortfolio

    async def readDocument(self, input_path, **kwargs):
        # Zkusit pdf soubor rozbalit jako pdf-portfolio
        try:
            files = await self.unpackPdf(input_path)
        except NotPdfPortfolio:
            files = [input_path]
        except EmptyPdfPortfolio:
            self.is_empty = True
            return []
        except:
            self.logger.exception("Unpack error")
            return []

        documents = []
        for file in files:
            documents += await self.readDocumentSingle(file, **kwargs)

        if not documents and self.config['save_unreadable']:
            os.rename(input_path, self.unreadable_path + "/" + self.document_name + ".pdf")

        return documents

    async def readDocumentSingle(self, input_path, multidoc=True):
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
            return []

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
            msg = "Nečitelný dokument" if not self.is_empty else "Prázdný dokument"
            print(msg, file=sys.stderr)
            exit(1)

        # Pokud neni aktivni --multidoc, zobrazit vzdy jen prvni dokument
        if not self.config['multidoc']:
            documents = documents[0]

        # Save output
        output = json.dumps(documents, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)
        self.config['_out'].write(output)
