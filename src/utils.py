
import json as cjson
import random 
import time
import threading 
import multiprocessing 
from sys import *
from discord_webhook import *
from .console import *
from src.modules.libs.http import *
from src.modules.libs.sockets import *
from src.modules.libs.request import *
from src.modules.libs.aiohttp import *
from src.cogs.features import *
from src.input.useragent import *

with open("./Config/config.json", "r+") as fp:
    data = cjson.load(fp)
    process = data["performance"]["process"]
    threads = data["performance"]["threads"]
    requestMethod = data["request"]["module"]
    requestTimeout = data["request"]["timeout"]
    requestProxied = data["request"]["proxyLess"]
    groupIdMethod = data["groupRanges"]["method"]
    groupId_start = data["groupRanges"]["min"]
    groupId_end = data["groupRanges"]["max"]
    batchSize = data["groupRanges"]["batchsize"]
    webhookUrl = data["webhook"]["url"]
    ping = data["webhook"]["groupPing"]
    proxyYN = data["proxy"]["scrapeProxies"]
    proxySources = data["proxy"]["sources"]
    del data
    # very unethical method ik, too lazy.
    
class Proxy:
    def __init__(self) -> None:
        self.pathToFile = "./Config/proxies.txt"
        
    def randomProxy(self) -> str:
        with open(self.pathToFile, "r+") as reader:
            return random.choice(reader.read().splitlines())
    
    def getProxyamt(self) -> int:
        with open(self.pathToFile, "r+") as grabber:
            return len(grabber.read().splitlines())
            
    def gen(self) -> str:
        return self.randomProxy()

class RoHttp:
    def __init__(self) -> None:
        global requestMethod
        global requestProxied
        global requestTimeout
        
        self.request = requestMethod
        self.timeout = requestTimeout
        self.proxyless = requestProxied
        self.proxy = Proxy()
        self.useragents = UserAgents()
        self.sock = SocketReq()
        self.http = HttpReq()
        self.asyncreq = AsyncReq()
        self.defreq = DefaultReq()
        
    def methodParser(self) -> None:
        if self.request == "socket":
            client = self.sock 
        elif self.request == "httpx":
            client = self.http 
        elif self.request == "aiohttp":
            client = self.asyncreq
        elif self.request == "requests":
            client = self.defreq 
            
        else:
            fatal("Unsupported request module, please recheck the configuration.")
            exit(0)
        return client
        
    def Request(self, url: str) -> None:
        client = self.methodParser()
        try:
            if self.proxyless is False:
                req = client.get(url, headers={"User-Agent": self.useragents.gen()}, proxy=self.proxy.gen(), timeout=self.timeout)
                return req.text
            elif self.proxyless:
                req = client.get(url, headers={"User-Agent": self.useragents}, timeout=self.timeout)
                return req.text
            else:
                fatal("Unsupported proxy type, recheck configuration.")
                exit(0)
        except Exception:
            pass
    
    def webScrapingReq(self, url: str) -> None:
        client = self.methodParser()
        try:
            req = client.get(url, headers={"User-Agent": self.useragents.gen()}, timeout=self.timeout)
            return req.text
        except Exception:
            pass
            
class ProxyScraper:
    def __init__(self) -> None:
        self.proxyList = []
        self.Sources = proxySources
        self.timeout = 5
        self.proxyFile = "./Config/proxies.txt"
        
    def scrapeProxies(self) -> None:
        client = RoHttp()
        try:
            for source in self.Sources:
                req = client.webScrapingReq(source)
                self.proxyList.append(req)
                
            sorted(set(self.proxyList))
            
            config(f"Scraped proxies from {len(self.Sources)} sources.")
        except Exception as err:
            fatal(err)
    
    def run(self) -> None:
        self.scrapeProxies()
        with open(self.proxyFile, "w+") as writer:
            for proxy in self.proxyList:
                writer.write(proxy)

class GroupID:
    def __init__(self):
        global groupIdMethod

        self.start_id = groupId_start
        self.end_id = groupId_end
        self.batch_size = batchSize
        self.id_iter = None
        self.id_iter_mp_lock = multiprocessing.Lock()
        self.id_iter_lock = threading.Lock()

    def sorted_gen(self) -> str:
        with self.id_iter_mp_lock:
            with self.id_iter_lock:
                if not self.id_iter:
                    if self.end_id > 17400000:
                        self.id_iter = iter(range(32000000, 34000000 + self.batch_size))
                    else:
                        self.id_iter = iter(range(self.start_id, self.end_id + self.batch_size))
                try:
                    group_ids = [next(self.id_iter) for _ in range(self.batch_size)]
                    return ','.join(str(gid) for gid in group_ids)
                except StopIteration:
                    raise

        return self.gen()

    def rand_gen(self) -> str:
        try:
            if self.end_id > 17400000:
                return [str(random.randint(32000000, 34000000)) for _ in range(self.batch_size)]
            else:
                return [str(random.randint(self.start_id, self.end_id)) for _ in range(self.batch_size)]
        except Exception as err:
            fatal(err)
            return []

    def gen(self) -> None:
        if groupIdMethod["sortedIds"] == True:
            return self.sorted_gen()
        elif groupIdMethod["randomIds"] == True:
            return ",".join(self.rand_gen())
        else:
            fatal("Unsupported group id method, please recheck the config.json file, exiting...")
            exit()

class Detectors:
    def __init__(self, groupId: int) -> None:
        self.group = groupId
        
    def clothings(self) -> int:
        return fclothings(self.group)
    
    def robux(self) -> int:
        return frobux(self.group)
    
    def gamevisits(self) -> int:
        return fgamevisits(self.group)
         
class Discord:
    def __init__(self, name: str, id: int, members: int) -> None:
        self.pingYN = ping 
        
        if self.pingYN == True:
            dping = "@everyone"
        else:
            dping = ""
            
        self.webhook = DiscordWebhook(
            url=webhookUrl,
            username="RoSpeed v2.5",
            content=dping,
            rate_limit_retry=True
            )
        self.name = name 
        self.id = id 
        self.members = members
        self.feat = Detectors(self.id)
        self.clothings = self.feat.clothings()
        self.robux = self.feat.robux()
        self.gvisits = self.feat.gamevisits()
        
    def embed(self) -> None:
        embed = DiscordEmbed(
            title="New Group Found!",
            url=f"https://www.roblox.com/groups/{self.id}/-",
            color=491519
        )
        embed.set_author(
            name = "RoSpeed",
            icon_url = "https://i.ibb.co/YXDYq2s/images-5-removebg-preview.png"
         )
        embed.set_thumbnail(url = "https://i.ibb.co/YXDYq2s/images-5-removebg-preview.png")
        embed.set_footer(
            text = "© Made by @realnovak | RoSpeed",
            icon_url = "https://i.ibb.co/YXDYq2s/images-5-removebg-preview.png"
        )
        embed.add_embed_field(
            name = "Group ID",
            value = str(self.id)
        )
        embed.add_embed_field(
            name = "Group Name",
            value = str(self.name)
        )
        embed.add_embed_field(
            name = "Group Members",
            value = str(self.members)
        )
        embed.add_embed_field(
            name = "Group Funds",
            value = str(self.robux)
        )
        embed.add_embed_field(
            name = "Group Clothings",
            value = str(self.clothings)
        )
        embed.add_embed_field(
            name = "Group G-Visits",
            value = str(self.gvisits)
        )
        
        return embed
    
    def send(self) -> None:
        self.webhook.add_embed(self.embed())
        try:
            self.webhook.execute()
            log("Successfully sent to Discord.")
        except Exception as err:
            fatal(f"Unknown error occured: {err}")
