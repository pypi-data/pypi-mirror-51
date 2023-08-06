#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from collections import defaultdict

import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

DEFAULT_HPO_SYN_MAP_FILE = os.path.join(os.path.dirname(__file__), "data/hpo_synonyms.txt")
#assert os.path.isfile(DEFAULT_HPO_SYN_MAP_FILE), "Cannot find HPO syn file (have you run GET_STARTED?): {}".format(DEFAULT_HPO_SYN_MAP_FILE)
HPO_SYN_MAP_FILE = DEFAULT_HPO_SYN_MAP_FILE
#MAX_PHENOS = 4

PHENOTYPIC_ABNORMALITY_ID = "HP:0000118"

def lemmatize(word):
  word = re.sub('[^0-9a-zA-Z]+', '', word)
  word = word.lower()
  return WordNetLemmatizer().lemmatize(word)

#Returns a map from an HPO ID to the full list of its synonymous names
def load_all_hpo_synonyms(filename=HPO_SYN_MAP_FILE):
  returnMap = defaultdict(set)
  for line in open(filename):
    lineData = line.strip().split("\t")
    hpo = lineData[0]
    syn = lineData[1]
    returnMap[hpo].add(syn)
  return returnMap

#Does the given word imply that, as far as we are concerned, the sentence is over?
#point_enders = [".", ":"]
point_enders = [".", u'•', '•', ";", "\t"]
def end_of_point(word):
  #for char in point_enders:
  #  if char in word: return True
  if word[-1] in point_enders: return True
  if word == "but": return True
  if word == "except": return True
  if word == "however": return True
  if word == "though": return True
  return False

#Parses the medical record into a list of sentences.
subpoint_enders = [",", ":"]
def end_of_subpoint(word):
  if word[-1] in subpoint_enders: return True
  if word == "and": return True
  return False

def string_to_record_linewise(medical_record):
  return medical_record.split("\n")

def load_medical_record_linewise(medical_record):
  recordFile = string_to_record_linewise(medical_record)
  sentences = []
  for line in recordFile:
    if ":" not in line: continue
    curSentence = []
    for word in line.strip().split(" "):
      word = word.lower()
      if len(word) < 1: continue
      curSentence.append(word)
      if end_of_point(word):
        sentences.append(" ".join(curSentence))
        curSentence = []
    if len(curSentence) > 0: sentences.append(" ".join(curSentence))
  subsentence_sets = []
  for sent in sentences:
    subsents = []
    curSubsent = []
    for word in sent.split(" "):
      word = word.lower()
      curSubsent.append(word)
      if end_of_subpoint(word):
        subsents.append(" ".join(curSubsent))
        curSubsent = []
    if len(curSubsent) > 0: subsents.append(" ".join(curSubsent))
    subsentence_sets.append(subsents)
  return subsentence_sets

def string_to_record_nonlinewise(medical_record):
  listForm = []
  for line in medical_record.split("\n"):
    if len(line) < 1: continue
    listForm.append(line)
  return " ".join(listForm).split(" ")

def load_medical_record_subsentences(medical_record):
  record = string_to_record_nonlinewise(medical_record)
  sentences = []
  curSentence = []
  for word in record:
    word = word.lower()
    if len(word) < 1: continue
    curSentence.append(word)
    if end_of_point(word):
      sentences.append(" ".join(curSentence))
      curSentence = []
  if len(curSentence) > 0: sentences.append(" ".join(curSentence))
  subsentence_sets = []
  for sent in sentences:
    subsents = []
    curSubsent = []
    for word in sent.split(" "):
      word = word.lower()
      curSubsent.append(word)
      if end_of_subpoint(word):
        subsents.append(" ".join(curSubsent))
        curSubsent = []
    if len(curSubsent) > 0: subsents.append(" ".join(curSubsent))
    subsentence_sets.append(subsents)
  return subsentence_sets + load_medical_record_linewise(medical_record)

def load_mr_map(parsed_record):
  returnMap = defaultdict(set)
  for i in range(len(parsed_record)):
    line = set(parsed_record[i])
    for word in line: returnMap[word].add(i)
  return returnMap

#Checks the given sentence for any flags from the lists you indicate.
negative_flags = ["no", "not", "none", "negative", "non", "never", "without", "denies"]
family_flags = ["cousin", "parent", "mom", "mother", "dad", "father", "grandmother", "grandfather", "grandparent", "family", "brother", "sister", "sibling", "uncle", "aunt", "nephew", "niece", "son", "daughter", "grandchild"]
healthy_flags = ["normal"]
disease_flags = ["associated", "gene", "recessive", "dominant", "variant", "cause", "literature", "individuals"]
treatment_flags = []
history_flags = []
mild_flags = []
uncertain_flags = []


low_synonyms = set(["low", "decreased", "decrease", "deficient", "deficiency", "deficit", "deficits", "reduce", "reduced", "lack", "lacking", "insufficient", "impairment", "impaired", "impair", "difficulty", "difficulties", "trouble"])
high_synonyms = set(["high", "increased", "increase", "elevated", "elevate", "elevation"])
abnormal_synonyms = set(["abnormal", "unusual", "atypical", "abnormality", "anomaly", "anomalies", "problem"])
common_synonyms = [
low_synonyms,
high_synonyms,
abnormal_synonyms
]

def synonym_lemmas(word):
  returnSet = set()
  for synSet in common_synonyms:
    if word in synSet: returnSet |= synSet
  return returnSet

def custom_lemmas(word):
  returnSet = set()
  if len(word) < 2: return returnSet
  if word[-1] == "s": returnSet.add(word[:-1])
  if word[-1] == "i": returnSet.add(word[:-1] + "us")
  if word [-1] == "a":
    returnSet.add(word[:-1] + "um")
    returnSet.add(word[:-1] + "on")
  if len(word) < 3: return returnSet
  if word[-2:] == "es":
    returnSet.add(word[:-2])
    returnSet.add(word[:-2] + "is")
  if word[-2:] == "ic":
    returnSet.add(word[:-2] + "ia")
    returnSet.add(word[:-2] + "y")
  if word[-2:] == "ly": returnSet.add(word[:-2])
  if word[-2:] == "ed": returnSet.add(word[:-2])
  if len(word) < 4: return returnSet
  if word[-3:] == "ata": returnSet.add(word[:-2])
  if word[-3:] == "ies": returnSet.add(word[:-3] + "y")
  if word[-3:] == "ble": returnSet.add(word[:-2] + "ility")
  if len(word) < 7: return returnSet
  if word[-6:] == "bility": returnSet.add(word[:-5] + "le")
  if len(word) < 8: return returnSet
  if word[-7:] == "ication":
    returnSet.add(word[:-7] + "y")
    returnSet.add(word[:-7] + "ied")
  return returnSet


def add_lemmas(wordSet):
  lemmas = set()
  for word in wordSet:
    lemma = lemmatize(word)
    if len(lemma) > 0: lemmas.add(lemma)
    lemmas |= synonym_lemmas(word)
    lemmas |= custom_lemmas(word)
  return wordSet | lemmas


def get_flags(line, *flagsets):
  line = add_lemmas(set(line))
  returnFlags = set()
  for flagset in flagsets:
    flagset = add_lemmas(set(flagset))
    for word in flagset:
      if word in line: returnFlags.add(word)
  return returnFlags

def alphanum_only(wordSet):
  returnSet = set()
  for word in wordSet:
    #returnSet |= set(word_tokenize(re.sub('[^0-9a-zA-Z]+', ' ', word)))
    returnSet |= set(re.sub('[^0-9a-zA-Z]+', ' ', word).split(" "))
  return returnSet

def sort_ids_by_occurrences_then_earliness(id_to_lines):
  listForm = []
  for hpoid in id_to_lines.keys(): listForm.append((hpoid, len(id_to_lines[hpoid]), min(id_to_lines[hpoid])))
  listForm.sort(key=lambda x: [-1*x[1], x[2], x[0]])
  returnList = list()
  for item in listForm: returnList.append(item[0])
  return returnList
  #returnSet = set()
  #for item in listForm[:MAX_PHENOS]: returnSet.add(item[0])
  #return returnSet

#Extracts what this algorithm believes is the best set of phenotypes for the patient, and prints them out, line by line, in the following format:
##HPO ID	Name	Number of sentences the ID was found in	example sentence where it was found
def extract_phenotypes(record, names, hpo_syn_file=HPO_SYN_MAP_FILE):
  safe_ID_to_lines = defaultdict(set)
  medical_record = load_medical_record_subsentences(record)
  medical_record_subsentences = []
  medical_record_words = []
  medical_record_flags = []
  subsent_to_sentence = []
  for subsents in medical_record:
    whole_sentence = ""
    for subsent in subsents: whole_sentence += subsent + " "
    whole_sentence = whole_sentence.strip()
    whole_sentence = re.sub('[^0-9a-zA-Z]+', ' ', whole_sentence)
    flags = get_flags(whole_sentence.split(" "), negative_flags, family_flags, healthy_flags, disease_flags, treatment_flags, history_flags, uncertain_flags, mild_flags)
    for subsent in subsents:
      medical_record_subsentences.append(subsent)
      subsent_to_sentence.append(whole_sentence)
      medical_record_words.append(add_lemmas(alphanum_only(set([subsent]))))
      medical_record_flags.append(flags)
  mr_map = load_mr_map(medical_record_words)
  syns = load_all_hpo_synonyms(hpo_syn_file)
  for hpoID in syns.keys():
    for syn in syns[hpoID]:
      syn = re.sub('[^0-9a-zA-Z]+', ' ', syn.lower())
      synTokens = alphanum_only(set([syn]))
      if len(synTokens) < 1: continue
      firstToken = list(synTokens)[0]
      lines = set(mr_map[firstToken])
      for token in synTokens:
        lines &= set(mr_map[token])
        if len(lines) < 1: break
      if len(lines) < 1: continue
      for i in lines:
        line = " ".join(medical_record_words[i])
        flagged = False
        for flag in medical_record_flags[i]:
          if flag not in synTokens:
            flagged = True
            break
        if flagged: continue
        safe_ID_to_lines[hpoID].add(i)
  safe_IDs = sort_ids_by_occurrences_then_earliness(safe_ID_to_lines)
  returnString = ["HPO ID\tPhenotype name\tNo. occurrences\tEarliness (lower = earlier)\tExample sentence"]
  #returnString = []
  for ID in safe_IDs: returnString.append("\t".join([ID, names[ID], str(len(safe_ID_to_lines[ID])), str(min(safe_ID_to_lines[ID])), subsent_to_sentence[safe_ID_to_lines[ID].pop()]]))
  return "\n".join(returnString)

def extract_phenotypes_custom_thesaurus(record, thesaurus, names):
  global HPO_SYN_MAP_FILE
  #HPO_SYN_MAP_FILE = thesaurus
  returnString = extract_phenotypes(record, names, hpo_syn_file=thesaurus)
  #HPO_SYN_MAP_FILE = DEFAULT_HPO_SYN_MAP_FILE
  return returnString

