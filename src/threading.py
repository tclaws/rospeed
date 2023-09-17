
from time import sleep 
from sys import exit 
from multiprocessing import Process 
from threading import Thread
from .utils import *
from .roblox import *
from .console import *
from src.input.useragent import *

class RoSpeed:
    def __init__(self):
        global process
        global threads 
        global proxyYN
        
        self.process = process
        self.threads = threads
        self.proxyYN = proxyYN
        self.proxies = Proxy()
        self.RoSpeed = Roblox()
        self.BrowserAgents = UserAgents()

    def run_ro_speed(self):
        while True:
            self.RoSpeed.run()

    def run_threadfunc(self):
        try: 
            threads = []
            for _ in range(self.threads):
                t = Thread(target=self.run_ro_speed)
                threads.append(t)
                t.start()
            
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            exit(0)

    def run_procfunc(self):
        try:
            processes = []
            for _ in range(self.process):
                p = Process(target=self.run_threadfunc)
                processes.append(p)
                p.start()
            
            for p in processes:
                p.join()
        except KeyboardInterrupt:
            exit(0)

    def main(self):
        global requestMethod
        clear()
        logo()

        if self.proxyYN:
            ps = ProxyScraper()
            ps.run()

        if "nt" in os.name:
            setTitle("RoSpeed v2.5 | Group Finder")

        config(f"Loaded {self.proxies.getProxyamt()} proxies.")
        config(f"Loaded {self.BrowserAgents.getAmount()} Browser Agents.")
        config(f"Using '{requestMethod}' I/O model.\n")
        
        boot("Starting RoSpeed..")
        time.sleep(3.5)

        self.run_procfunc()
