
import orjson as json
from .console import *
from .utils import *

class Roblox:
    def __init__(self):
        self.group = GroupID()
        self.proxyfunc = Proxy()
        self.found = []

    def singleGroup(self, groupId: int) -> bool:
        client = RoHttp()
        retries = 3

        while retries > 0:
            try:
                req = client.Request(f"https://groups.roblox.com/v1/groups/{groupId}")
                resp = json.loads(req)
                if (resp["owner"] is None) and ("isLocked" not in resp) and (resp["publicEntryAllowed"]):
                    discord = Discord(resp["name"], groupId, resp["memberCount"])
                    discord.send()
                    return True
                else:
                    return False
            except Exception:
                retries -= 1

        return False

    def batchGroup(self) -> None:
        client = RoHttp()

        try:
            self.gid = self.group.gen()
            req = client.Request(f"https://groups.roblox.com/v2/groups?groupIds={self.gid}")
            resp = json.loads(req)["data"]

            for datas in resp:
                try:
                    groupId = datas["id"]
                    ownerBool = datas["owner"]
                    nameStr = datas["name"]
                except:
                    return

                if (ownerBool is None) and (groupId not in self.found):
                    dCheck = self.singleGroup(int(groupId))

                    if dCheck:
                        ok(f"Found Group -> {groupId}")
                        self.found.append(groupId)
                    else:
                        warn(f"Invalid Group -> {groupId}")
        except Exception:
            pass

    def run(self) -> None:
            try:
                self.batchGroup()
            except Exception:
                pass

