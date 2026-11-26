"""Wikimedia Commons helper: search files / file info (license, artist) / download a scaled image."""
import sys, json, time, re, urllib.request, urllib.parse
UA = {"User-Agent": "NotJustYouExplainer/1.0 (https://github.com/chris61ds-alt/explainer-kit; educational reels)"}
API = "https://commons.wikimedia.org/w/api.php"
def get(params, tries=4):
    url = API + "?" + urllib.parse.urlencode(dict(params, format="json"))
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r: return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(8 * (i + 1)); continue
            raise
    raise SystemExit("rate limited")
def strip(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h or "")).strip()
def info(titles, width=1600):
    d = get(dict(action="query", titles="|".join(titles), prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=width))
    out = []
    for p in d["query"]["pages"].values():
        if "imageinfo" not in p: out.append(dict(title=p["title"], missing=True)); continue
        ii = p["imageinfo"][0]; m = ii["extmetadata"]
        out.append(dict(title=p["title"], w=ii["width"], h=ii["height"], thumb=ii.get("thumburl"), page=ii["descriptionurl"],
                        license=strip(m.get("LicenseShortName", {}).get("value")), artist=strip(m.get("Artist", {}).get("value"))[:80],
                        date=strip(m.get("DateTimeOriginal", {}).get("value"))[:40], desc=strip(m.get("ImageDescription", {}).get("value"))[:120]))
    return out
def search(q, n=8):
    d = get(dict(action="query", generator="search", gsrsearch=q, gsrnamespace=6, gsrlimit=n, prop="imageinfo", iiprop="size|extmetadata"))
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)):
        ii = p["imageinfo"][0]; m = ii["extmetadata"]
        print(f'{p["title"][5:90]} | {ii["width"]}x{ii["height"]} | {strip(m.get("LicenseShortName",{}).get("value"))} | {strip(m.get("Artist",{}).get("value"))[:40]}')
def download(url, path):
    url = url.split("?")[0].replace("//thumb.wikimedia.org/", "//upload.wikimedia.org/")
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: open(path, "wb").write(r.read())
if __name__ == "__main__":
    if sys.argv[1] == "search":
        for q in sys.argv[2:]: print("##", q); search(q); time.sleep(1.5)
    elif sys.argv[1] == "info": print(json.dumps(info(sys.argv[2:]), indent=1, ensure_ascii=False))
