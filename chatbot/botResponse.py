from string import punctuation
from dataLoad import data_surah, data_tafsir, labels, model, nama_surah, vocab
import pickle
import json
import pandas as pd
import numpy as np
import re
import random
from sklearn.feature_extraction.text import TfidfVectorizer


def preprocess_string(string):
    string = string.lower()
    exclude = set(punctuation)
    string = "".join(ch for ch in string if ch not in exclude)
    return string


def tfidf(text):
    fit = False
    vec = ""
    if fit != True:
        vec = TfidfVectorizer(vocabulary=vocab, norm=None)
        fit = True
    tfidf = vec.fit_transform([text])
    return tfidf


def prediction(fitur):
    prd = model.predict_proba(fitur)  # Do Predict
    tag = labels.classes_[np.argmax(prd)]  # Get the predicted label

    # Get the content of response by tag that predicted before then return it
    for tg in data_surah["intents"]:
        if tg["tag"] == tag:
            responses = tg["responses"]
            return responses

    for tg2 in data_tafsir["intents"]:
        if tg2["tag"] == tag:
            responses = tg2["responses"]
            return responses


def bot_response(text):
    text = preprocess_string(text)  # Clean the question
    matriks_tfidf = tfidf(text)  # Get the TFIDF of the question

    responses = prediction(matriks_tfidf) # do predict

    if "teks_ayat" in responses[0]:
        if text.find("ayat") != -1:  # If user ask spesific ayat
            # print(" ada keyword ayat")
            rgx = re.search("(?<=ayat\s)\d+", text)  # Check if there is a number right after word "ayat"
            # print(rgx)

            if rgx != None: # if there is a number
                ayat = text[rgx.start() : rgx.end()]  # Get the number, error if there is not any number
                for rp in responses:
                    if len(responses) < int(ayat):  # Check if user input bigger than total ayat in responses(surat)
                        return f"Surat {nama_surah[rp['no_surah'] - 1]} hanya memiliki {responses[len(responses)-1]['no_ayat']} ayat"
                    elif rp["no_ayat"] == int(ayat):  # Check if ayat equal with requested ayat
                        return f"Surah {nama_surah[rp['no_surah'] - 1]}({rp['no_surah']}) Ayat {rp['no_ayat']}: \n \n{rp['teks_ayat']}({rp['no_ayat']}) \n \n{rp['teks_terjemah']}({rp['no_ayat']}) \n[QS. {rp['no_surah']}:{rp['no_ayat']}]"
            elif rgx == None:  # Or use  else keyword instead
                return f"Harap sertakan nomor ayatnya \ncontoh: \nsurat alfatihah ayat 2 \nsurat albaqarah ayat 110"

    elif "teks_tafsir" in responses[0]:
        if text.find("tafsir") != -1:  # If user ask spesific ayat or tafsir
            # print(" ada keyword tafsir")
            rgx = re.search(
                "(?<=ayat\s)\d+", text
            )  # Check if there is a number right after word "ayat" (eg: tafsir surat almaun ayat 23)

            if rgx != None: # if there is a number
                ayat = text[
                    rgx.start() : rgx.end()
                ]  # Get the number, error if there is not any number
                for rp in responses:
                    if len(responses) < int(
                        ayat
                    ):  # Check if user input bigger than total ayat in responses(surat)
                        return f"Surat {nama_surah[rp['surah_id'] - 1]} hanya memiliki {responses[len(responses)-1]['no_ayat']} ayat"
                    elif rp["no_ayat"] == int(
                        ayat
                    ):  # Check if ayat number equal with requested ayat
                        return f"Tafsir surah {nama_surah[rp['surah_id'] - 1]}({rp['surah_id']}) Ayat {rp['no_ayat']}: \n \n{rp['teks_tafsir']}({rp['no_ayat']}) \n[QS. {rp['surah_id']}:{rp['no_ayat']}]"
            elif rgx == None:  # Or use  else keyword instead
                return f"Harap sertakan nomor ayatnya \ncontoh: \ntafsir surat alfatihah ayat 2 \ntafsir yunus ayat 50"

    elif "surat_name" in responses[0]:
        # print("ini info surat")
        rp = responses[0]
        return f"Surah {rp['surat_name']}({rp['surat_text']} ) merupakan surat ke {rp['id']} dalam Al-Qur'an yang memiliki arti '{rp['surat_terjemahan']}' dan ayat berjumlah {rp['count_ayat']}. Surat ini termasuk golongan {rp['golongan_surah']}"

    elif type(responses[0]) == str:
        # print("Ini random choice")
        return random.choice(responses)
