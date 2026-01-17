from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json, re

app = FastAPI()

# static 配信
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")

# 単語読み込み
with open("vocab.json", encoding="utf-8") as f:
    vocab = json.load(f)

id2 = {int(x["id"]): x for x in vocab}

@app.get("/vocab")
def get_vocab(start: int = Query(1), end: int = Query(2000)):
    # 念のため入れ替え
    if start > end:
        start, end = end, start

    filtered = []
    for x in vocab:
        xid = int(x["id"])
        if start <= xid <= end:
            filtered.append({"id": xid, "en": x["en"]})
    return filtered

@app.post("/check")
def check(d: dict):
    item = id2.get(int(d["id"]))
    if not item:
        return {"correct": False, "correct_examples": []}

    user = re.sub(r"\s+", "", str(d.get("user", "")))  # 空白除去
    ok = user in [re.sub(r"\s+", "", j) for j in item.get("ja", [])]

    return {"correct": ok, "correct_examples": item.get("ja", [])}

# favicon の 404 を消したいなら（任意）
@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")  # 置いてないならこの関数は消してOK
