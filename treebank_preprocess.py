
import os
import pandas as pd
from lxml import etree

def to_urn(s: str):
    return f"{s.replace('.xml', '')}"

def get_files(dir):
    files = [
        (os.path.join(dir, f), to_urn(f))
        for f in os.listdir(dir)
        if os.path.isfile(os.path.join(dir, f))
    ]
    return files

def iter_lines(title, urn, tree, dir):
    rows = []

    for l in tree.iterfind(".//sentence"):
        words = []
        for element in l.findall(".//word"):
            if element.get("postag"): #filtering out weird xml issue here
                words.append(element.get("form"))

        row = {
            "label": dir,
            "urn": urn,
            "title": title,
            "text": " ".join(words), 
        }
        rows.append(row)

    return rows


def create_df(dir):
    data = []
    files = get_files("data/" + dir)

    for f, urn in files:
        tree = etree.parse(f)
        title = tree.xpath("//fileDesc/biblStruct/monogr/title/text()")[0]
        lines = iter_lines(title, urn, tree, dir)
        data += lines
    
    return pd.DataFrame(data)


df_prose = create_df("prose")
df_poetry = create_df("poetry")

df = pd.concat([df_prose, df_poetry], ignore_index=True)
print(df)
df.to_pickle('./corpus.pickle')

new_df = df[["label", "text"]]

new_df.to_pickle('./bert_corpus.pickle')


