import sys, os, re, json, hashlib, zipfile, sqlite3, io
from bs4 import BeautifulSoup
from markdown import markdown
import chardet

PII_PATTERNS = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", re.I),
    "phone_pl": re.compile(r"(?:\+?48[\s-]?)?(?:\d{3}[\s-]?\d{3}[\s-]?\d{3})\b"),
    "iban_pl": re.compile(r"\bPL\d{26}\b"),
    "pesel": re.compile(r"\b\d{11}\b"),
    "credit_card": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
}
SECRET_PATTERNS = {
    "secrets": re.compile(r"(password|passwd|secret|token|api[_-]?key|Bearer\s+[A-Za-z0-9._-]+)", re.I)
}

TEXT_EXT = {".html",".htm",".md",".markdown",".txt",".xml",".json"}
SKIP_DIRS = re.compile(r"/(\.git|node_modules|\.cache|\.next|dist|build|venv|__pycache__)(/|$)")

def sha256(b: bytes)->str: return hashlib.sha256(b).hexdigest()

def detect_enc(data: bytes)->str:
    res = chardet.detect(data)
    return (res["encoding"] or "utf-8") if res["confidence"] and res["confidence"]>0.4 else "utf-8"

def to_text(path, data:str)->str:
    ext = os.path.splitext(path.lower())[1]
    if ext in [".html",".htm",".xml"]:
        parser = "lxml"  # fallback handled by bs4 internally
        soup = BeautifulSoup(data, parser)
        # text without script/style
        for t in soup(["script","style","noscript"]): t.extract()
        return soup.get_text("\n", strip=True)
    if ext in [".md",".markdown"]:
        # convert md->html->text
        html = markdown(data)
        soup = BeautifulSoup(html, "lxml")
        return soup.get_text("\n", strip=True)
    if ext==".json":
        try:
            obj = json.loads(data)
            out=[]
            def walk(x):
                if isinstance(x, dict):
                    for k,v in x.items(): walk(v)
                elif isinstance(x, list):
                    for v in x: walk(v)
                elif isinstance(x, str):
                    out.append(x)
            walk(obj)
            return "\n".join(out)
        except Exception:
            return data
    return data  # .txt default

def parse_html_meta(path, data:str):
    ext = os.path.splitext(path.lower())[1]
    if ext not in [".html",".htm",".xml"]: return {}
    soup = BeautifulSoup(data, "lxml")
    title = (soup.title.string.strip() if soup.title and soup.title.string else None)
    def first(sel):
        el = soup.select_one(sel)
        return el.get("content","").strip() if el else None
    h1 = soup.select_one("h1")
    lang = soup.html.get("lang").strip() if soup.html and soup.html.get("lang") else None
    canon = soup.find("link", rel=lambda v: v and "canonical" in v)
    metas = {}
    for m in soup.find_all("meta"):
        n = m.get("name") or m.get("property")
        c = m.get("content")
        if n and c: metas[n.strip().lower()] = c.strip()
    links=[]
    for a in soup.find_all("a", href=True):
        links.append({"href":a["href"], "text":(a.get_text(strip=True) or None), "rel":" ".join(a.get("rel",[]))})
    images=[]
    for img in soup.find_all("img", src=True):
        images.append({"src":img["src"], "alt":img.get("alt"), "w":img.get("width"), "h":img.get("height")})
    return {
        "title": title,
        "h1": h1.get_text(strip=True) if h1 else None,
        "lang": lang,
        "canonical": canon.get("href").strip() if canon and canon.get("href") else None,
        "meta": metas,
        "links": links,
        "images": images
    }

def mask_val(s: str):
    if not s: return s
    s = re.sub(r"\s+","",s)
    return s[:4]+"…"+s[-4:] if len(s)>8 else "…"

def pesel_valid(p):
    if not re.fullmatch(r"\d{11}", p): return False
    w = [1,3,7,9,1,3,7,9,1,3]
    s = sum(int(p[i])*w[i] for i in range(10))
    return (10 - (s % 10)) % 10 == int(p[-1])

def main():
    if len(sys.argv)<3:
        print("Usage: python analyze_zip.py <zip_path> <sqlite_path>")
        sys.exit(1)
    zip_path = sys.argv[1]
    db_path = sys.argv[2]

    z = zipfile.ZipFile(zip_path, "r")
    bad = z.testzip()  # returns first bad file or None
    integrity = {
        "zip": os.path.abspath(zip_path),
        "size_bytes": os.path.getsize(zip_path),
        "testzip_first_error": bad,
        "files_total": len(z.infolist())
    }

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript("""
    PRAGMA journal_mode=WAL;
    CREATE TABLE IF NOT EXISTS pages(
      id INTEGER PRIMARY KEY,
      path TEXT, sha256 TEXT, ext TEXT,
      title TEXT, h1 TEXT, lang TEXT, canonical TEXT,
      text TEXT, word_count INTEGER
    );
    CREATE TABLE IF NOT EXISTS meta(page_id INTEGER, name TEXT, content TEXT);
    CREATE TABLE IF NOT EXISTS links(src_id INTEGER, href TEXT, text TEXT, rel TEXT, is_onion INTEGER, is_internal_guess INTEGER);
    CREATE TABLE IF NOT EXISTS images(page_id INTEGER, src TEXT, alt TEXT, w TEXT, h TEXT);
    CREATE TABLE IF NOT EXISTS flags(page_id INTEGER, kind TEXT, value_masked TEXT, raw_hash TEXT);
    """)
    conn.commit()

    out_jsonl = open("catalog.jsonl","w", encoding="utf-8")
    flags_count=0
    pages_count=0

    # guess base root
    root_dirs = {i.filename.split("/")[0] for i in z.infolist() if "/" in i.filename}
    base_root = next(iter(sorted(root_dirs)), "")

    for info in z.infolist():
        name = info.filename
        if info.is_dir(): continue
        if SKIP_DIRS.search("/"+name): continue
        ext = os.path.splitext(name.lower())[1]
        if ext not in TEXT_EXT: continue

        raw = z.read(info)
        digest = sha256(raw)
        enc = detect_enc(raw)
        data = raw.decode(enc, errors="replace")

        # primary text + metadata
        text = to_text(name, data)
        wc = len(re.findall(r"\w+", text))
        meta = parse_html_meta(name, data) if ext in [".html",".htm",".xml"] else {}

        cur.execute(
            "INSERT INTO pages(path,sha256,ext,title,h1,lang,canonical,text,word_count) VALUES(?,?,?,?,?,?,?,?,?)",
            (name, digest, ext, meta.get("title"), meta.get("h1"), meta.get("lang"), meta.get("canonical"), text, wc)
        )
        page_id = cur.lastrowid
        pages_count += 1

        # meta
        for k,v in (meta.get("meta") or {}).items():
            cur.execute("INSERT INTO meta(page_id,name,content) VALUES(?,?,?)",(page_id,k,v))

        # links
        for a in (meta.get("links") or []):
            href=a.get("href") or ""
            is_onion = 1 if ".onion" in href else 0
            is_internal = 1 if (href.startswith("./") or href.startswith("../") or href.startswith("/") or (base_root and href.startswith(base_root))) else 0
            cur.execute("INSERT INTO links(src_id,href,text,rel,is_onion,is_internal_guess) VALUES(?,?,?,?,?,?)",
                        (page_id, href, a.get("text"), a.get("rel"), is_onion, is_internal))

        # images
        for im in (meta.get("images") or []):
            cur.execute("INSERT INTO images(page_id,src,alt,w,h) VALUES(?,?,?,?,?)",
                        (page_id, im.get("src"), im.get("alt"), im.get("w"), im.get("h")))

        # PII & secrets flags (masked)
        def add_flag(kind, val):
            nonlocal flags_count
            flags_count += 1
            cur.execute("INSERT INTO flags(page_id,kind,value_masked,raw_hash) VALUES(?,?,?,?)",
                        (page_id, kind, mask_val(val), sha256(val.encode("utf-8"))))

        for kind, pat in PII_PATTERNS.items():
            for m in pat.finditer(text):
                val = m.group(0)
                if kind=="pesel" and not pesel_valid(val): continue
                add_flag(kind, val)
        for kind, pat in SECRET_PATTERNS.items():
            for m in pat.finditer(text):
                add_flag(kind, m.group(0))

        # JSONL entry
        entry = {
            "path": name, "ext": ext, "sha256": digest,
            "title": meta.get("title"), "h1": meta.get("h1"),
            "canonical": meta.get("canonical"), "lang": meta.get("lang"),
            "word_count": wc
        }
        out_jsonl.write(json.dumps(entry, ensure_ascii=False)+"\n")

    conn.commit()
    out_jsonl.close()

    # write integrity report
    integrity.update({"pages_indexed": pages_count, "flags_total": flags_count})
    with open("integrity_report.json","w",encoding="utf-8") as f:
        json.dump(integrity, f, ensure_ascii=False, indent=2)

    print("OK:", os.path.abspath(db_path), "catalog.jsonl", "integrity_report.json")

if __name__=="__main__":
    main()
