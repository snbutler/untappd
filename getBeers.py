import code
import requests
from   sys      import stderr
from   argparse import ArgumentParser
from   untappd  import *


if __name__ == "__main__":

    parser = ArgumentParser("Get all check-ins")
    parser.add_argument("user", help="Untappd username")
    parser.add_argument("keys", help="keyfile")
    args = parser.parse_args()

    baseUrl = "https://api.untappd.com/"
    actUrl  = baseUrl+"v4/user/checkins/{}"

    keys = {}
    with open(args.keys) as f:
        for l in f:
            (k, val) = l.strip().split(" ")
            keys[k] = val

    #auth = "client_id={}&client_secret={}".format(keys["apiId"], keys["apiSecret"])
    auth = "access_token={}".format(keys["authToken"])
    url = actUrl.format(args.user)+"?"+auth

    r = requests.get(url)
    j = r.json()
    try:
        while j["response"] and j["response"]["checkins"]["count"] > 0:
            for b in j["response"]["checkins"]["items"]:
                s = "{}, \"{}\",  \"{}\", {}".format(b["created_at"], b["brewery"]["brewery_name"].encode("utf-8"), b["beer"]["beer_name"].encode("utf-8"), b["beer"]["beer_abv"])
                print(s)
            nextUrl = j["response"]["pagination"]["next_url"] + "&" + auth
            r = requests.get(nextUrl)
            j = r.json()
    except Exception as e:
        print("error!")
        code.interact(local=locals())
