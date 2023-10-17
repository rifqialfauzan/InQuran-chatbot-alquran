import pickle
import json

with open("model/tfidf.pkl", "rb") as f:
    vocab = pickle.load(f)

with open("model/model_mlp.pickle", "rb") as f:
    model = pickle.load(f)

with open("model/label_mlp.pickle", "rb") as f:
    labels = pickle.load(f)

with open("data\data_SurahAyat.json", encoding="utf8") as f:
    data_surah = json.load(f)

with open("data\data_tafsir.json", encoding="utf8") as f:
    data_tafsir = json.load(f)

with open("data\surahFile.txt", encoding="utf8") as f:
    nama_surah = f.read().splitlines()

with open("data\messages\listsurah.txt", encoding="utf8") as f:
    list_surah = f.read().splitlines()

with open("data\messages\greeting.txt", encoding="utf8") as f:
    greeting_msg = f.read()

