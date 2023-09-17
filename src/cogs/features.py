import requests
import numpy as np
import orjson as json
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.exceptions import RequestException

roblox_cookie = {".ROBLOSECURITY": "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_EB7F4755301ADC555ED4C77B6C3F1023AEB130283431E3FD3D6997D99A0744B07AAB9F296877594CC3B34D844715286FF9EB6B8A7E09EC47CDD656EFBFA173305B9D134F5B5FAF1FC3DAAC35F40C64D8371C95B3CDB218ACD0C5ACFB7FE63419A724BC29BB91CCB7E4C9DD38752741ACBD368115868A0911A34234D66F64EFCED7244E2833AA2FE17BA6C998EE0FA01478E6719E921CEA4A17C7DC53C8CD8829BDA488910DB83909CB3653CB26D62AB57573544416CCF59A13D7188E9D85DA96B2F9394877765DB28B6EBC49203534CFE199D911F921C653F715C9EBDC9D8B68656ED9E77E7FABB83B378F36DCF0369C4B318AE774F97F29E3C84158D18802DFDD29A27EAD457C5725C7E2F5303D5A227F58C29DBD382B678D919A6B91FBC6E30E79B24AC89D6CE3229F3E81EEDEC919E88F876BEEC9A89F2FF51B12875A509A31E72D27A9EFA044102F3C7A36911C53E4B156551EEF8B074ADF609E245E266C8BB5F101C7DCB111F8028BB63B2379E232B79CD8BFBDCA3401CF13C777BDF3A4C95212642A6FABD1041BAC52C2B9E003C80CB23B"}

def retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """
    retry session function that retries a request in case of connection errors or status codes
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def get_page(url):
    try:
        response = retry_session().get(url)
        check = response.json()
        if "data" in check:
            clothings = np.array(check['data'])
        else:
            clothings = np.array([])

        if "nextPageCursor" in check and check['nextPageCursor']:
            return clothings, check['nextPageCursor']
        else:
            return clothings, ""
    except RequestException as e:
        print(f"Error requesting page {url}: {e}")
        return np.array([]), ""

def fclothings(id):
    clothings = 0
    cursor = None


    url = f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30"
    clothings_data, cursor = get_page(url)
    clothings += len(clothings_data)


    while cursor:
        urls = [
            f"https://catalog.roblox.com/v1/search/items/details?Category=3&CreatorTargetId={id}&CreatorType=2&Limit=30&cursor={cursor}" for _ in range(10)
        ]
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(get_page, urls))

        for result in results:
            clothings_data, cursor = result
            clothings += len(clothings_data)

    return clothings

def frobux(id):
    global roblox_cookie
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        session = requests.Session()
        session.mount('https://', HTTPAdapter(max_retries=retries))
        try:
            future = executor.submit(session.get, f'https://economy.roblox.com/v1/groups/{id}/currency', cookies=roblox_cookie, timeout=5)
        except RequestException as e:
            print(e)
            return 0
        
        try:
            response = future.result()
            data = json.loads(response.text)
            if "robux" in data:
                robux = data.get("robux", 0)
            else:
                robux = 0
        except RequestException as e:
            print(e)
            return 0
    
    return robux

def fgamevisits(id):
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session = requests.Session()
    session.mount('https://', HTTPAdapter(max_retries=retries))

    with ThreadPoolExecutor(max_workers=10) as executor:
        future = executor.submit(session.get, f'https://games.roblox.com/v2/groups/{id}/games?accessFilter=All&sortOrder=Asc&limit=100', timeout=5)

        try:
            response = future.result()
            os = response.json()
            if "data" in os:
                data = os["data"]
            else:
                data = 0

        except requests.exceptions.RequestException as e:
            print(e)
            return 0

    if not data:
        return 0

    visits = np.array([game["placeVisits"] for game in data])
    total_visits = np.sum(visits)
    
    return total_visits