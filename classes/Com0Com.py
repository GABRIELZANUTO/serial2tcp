import subprocess
import re
import time
from log import LogManager

class Com0Com:
    def __init__(self):
        self.log = LogManager()
        self.path = r"C:\Program Files (x86)\com0com"
        self.baseComand = "setupc "
        self.odd = False
        self.CNCA = (-1, '', '') 
        self.CNCB = (-1, '', '')  
    

    def _listPorts(self):
        comando = self.baseComand + 'list'
        resultado = subprocess.run(comando, cwd=self.path, capture_output=True, text=True, shell=True)

        for linha in resultado.stdout.strip().splitlines():
            linha = linha.strip()
            match = re.match(r'(CNCA|CNCB)(\d+)', linha)
            if match:
                tipo, num = match.groups()
                num = int(num)
                identificador = f"{tipo}{num}"
                com_match = re.search(r'RealPortName=(COM\d+)', linha)
                if not com_match:
                    com_match = re.search(r'PortName=(COM\d+)', linha)
                if com_match:
                    com = com_match.group(1)
                    if tipo == 'CNCA' and num > self.CNCA[0]:
                        self.CNCA = (num, identificador, com)
                    elif tipo == 'CNCB' and num > self.CNCB[0]:
                        self.CNCB = (num, identificador, com)

    def CreatePair(self):
        comand = self.baseComand + 'install PortName=COM# PortName=COM#'
        subprocess.run(comand, cwd=self.path, shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        self.log.write('[COM0COM] Criou par de portas seriais')

        self._listPorts()

        comand = self.baseComand + f'change {self.CNCA[1]} HiddenMode=yes'
        subprocess.run(comand, cwd=self.path, shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        self.log.write(f'[COM0COM] Escondeu porta {self.CNCA[2]}')

        comand = self.baseComand + f'change {self.CNCA[1]} PortName={self.CNCA[2]}'
        subprocess.run(comand, cwd=self.path, shell=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(3)
        

