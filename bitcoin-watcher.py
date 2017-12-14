import sys, time, requests, argparse
from gi.repository import Notify
from bs4 import BeautifulSoup as bs

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--exchange", metavar='1: bitcoin.co.id, 2:luno.com, default:1', default=1, type=int,
                    help='Exchange Trade')
parser.add_argument("-s", "--socks", metavar='socks5://host:port', type=str, help='SOCKS Proxy')
parser.add_argument("-t", "--time", metavar='interval time, default: 10', default=10, type=int, help='Interval Time')
args = parser.parse_args()

if args.time < 10:
    print("Error: Minimum interval 30 seconds")
    sys.exit(1)

if not args.socks:
    args.proxy = None

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
}

proxy = {
    "http": args.socks,
    "https": args.socks
}

while True:
    try:
        if args.exchange == 1:
            req = requests.get("https://www.bitcoin.co.id/", headers=headers, proxies=proxy)
            soup = bs(req.text, "lxml")
            btctoidr = soup.find_all("span", {"class": "text-white alt-font home-price"})[0].text.split()[3]
            Notify.init("BTC -> IDR")
            notip = Notify.Notification.new("bitcoin.co.id | XBTIDR", btctoidr, "dialog-information")
            notip.show()
        elif args.exchange == 2:
            req = requests.get("https://api.mybitx.com/api/1/ticker?pair=XBTIDR", headers=headers, proxies=proxy)
            btctoidr = req.json()['ask']
            Notify.init("BTC -> IDR")
            notip = Notify.Notification.new("luno.com | XBTIDR", btctoidr, "dialog-information")
            notip.show()
    except:
        print "Unexpected error:", sys.exc_info()
        pass
    time.sleep(args.time)
