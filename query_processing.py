from elasticsearch import Elasticsearch
from sinling import word_splitter

es = Elasticsearch()

def simple_tokenizer(query):
    return query.split()

def tokenize(query, tokenizer):
    return tokenizer(query)

def classify_intent(query):
    ministries = ["අමාත්‍යතුමා", "අමාත්‍යතුමිිය", "අමාත්‍ය", "ඇමති", "අමාත්‍යාංශය", "මන්ත්‍රීවරු", "අමාත්‍යවරු", "ඇමතිතුමා", "ඇමතිතුමිය", "ඇමතිවරු", "මන්ත්‍රීතුමා", "මන්ත්‍රීතුමිය", "මන්ත්‍රී"]
    provinces = ["අනුරාධපුර", "අනුරාධපුරයේ", "යාපනය", "යාපනයේ", "ගාල්ල", "ගාල්ලේ", "මඩකලපුව", "මඩකලපුවේ",  "ලැයිස්තුව", "ජාතික", "ලැයිස්තුවෙන්",
    "මාතර", "කළුතර", "රත්නපුර", "රත්නපුරේ", "ගම්පහ", "කෑගල්ල", "කෑගල්ලේ", "වන්නි", "වන්නියේ", "දිගාමඩුල්ල", "දිගාමඩුල්ලේ", "පුත්තලම", "පුත්තලමේ"
    "පොළොන්නරුව", "පොළොන්නරුවේ", "මොණරාගල", "ත්‍රිකුණාමලය", "ත්‍රිකුණාමලයේ", "හම්බන්තොට", "මහනුවර", "නුවර", "මාතලේ",
    "බදුල්ල", "බදුල්ලේ","කොළඹ", "නුවරඑළිය", "නුවරඑළියේ", "කුරුණෑගල", "දිස්ත්‍රික්කය", "දිස්ත්‍රික්ක", "දිස්ත්‍රික්කයේ", "දිස්ත්‍රික්කයට"]
    parties = ["පෙරමුණ", "පෙරමුණේ", "සන්ධානය", "සන්ධානයේ  ", "බලවේගය", "බලවේගයේ", "පක්ෂය", "පක්ෂයේ", "කොංග්‍රස්", "කොංග්‍රසය", "කොන්ග්‍රස්", "කොන්ග්‍රසය", "කොංග්‍රසයේ", "කොන්ග්‍රසයේ",
     "කුට්ටනි", "කච්චි", "විඩුදලෛප්"]
    age = ["වයස", "අවුරුදු", "පරිණත", "ළාබාල", "ලාබාල", "තරුණ", "වයෝවෘධ"]
    civil_status = ["විවාහක", "අවිවාහක", "විවාහ"]

    tokenized_query = tokenize(query, simple_tokenizer)
    intents = set()
    for i, token in enumerate(tokenized_query):
        if(token in ministries):
            intents.add('ministry')
        if(token in provinces):
            split_base = word_splitter.split(token)['base']
            query = query + split_base
            intents.add('province')
        if(token in parties):
            split_base = word_splitter.split(token)['base']
            query = query + split_base
            intents.add('party')
        if(token in age):
            intents.add('age')
        if(token in civil_status):
            intents.add('civil_status')
        else:
            intents.add('misc')

    if(len(intents) > 1):
        intents.discard('misc')

    return intents, tokenized_query, query

def build_query(query, tokenized_query, intents):
    search_fields = []

    if('misc' in intents):
        body = {
                "size": 300,
                "query":{
                    "multi_match" : {
                            "query": query,
                            "fields": ["name", "committees_currently_in", "committees_was_in", "political_party", "electoral_district", "profession"]
                        }
                }
    }
    else:
        if('ministry' in intents):
            search_fields.append('position')
        if('province' in intents):
            search_fields.append('electoral_district')
        if('party' in intents):
            search_fields.append('political_party')
        if('civil_status' in intents):
            search_fields.append('civil_status')
        if('age' in intents):
            return build_age_query(query, tokenized_query)

        if(len(intents) > 1):
            body = {
                    "size": 300,
                    "query":{
                        "multi_match" : {
                            "query": query,
                            "fields": search_fields
                        }
                    }
            } 
        else:
            body = {
                    "size": 300,
                    "query":{
                        "match" : {
                            search_fields[0]: query
                        }
                    }
            }
    return body


def build_age_query(query, tokenized_query):
    ## TODO: Sort age
    
    young_identifiers = ["තරුණ", "ළාබාල", "ලාබාල"]

    mx_range_identifiers = ["වැඩි", "වඩා" ]
    mn_range_identifiers = ["අඩු"]

    upper_age = 80
    lower_age = 18
    age = 0
    range = -1
    order = 'asc'

    for token in tokenized_query:
        split_base = word_splitter.split(token)['base']
        if(token.isnumeric() and 18 < int(token) < 100):
            age = int(token)
        elif( split_base.isnumeric() and 18 < int(split_base) < 100 ):
            age = int(split_base)
        elif(token in mn_range_identifiers):
            range = 1
        elif(token in mx_range_identifiers):
            range = 0
        
        if(age > 0 and range != -1):
            if(range == 1):
                lower_age = 18
                upper_age = age
                order = 'desc'
            else:
                lower_age = age
                upper_age = 80
                order = 'asc'
            break
    else:
        if(any(identifier in tokenized_query for identifier in young_identifiers)):
            lower_age = 18
            upper_age = 35
            order = 'desc'
        else:
            lower_age = 35
            upper_age = 80
            order = 'asc'

    body = {
        "size": 300,
        "sort" : { 
                "date_of_birth" : {"order" : order, "format": "strict_date_optional_time_nanos"}
                },
        "query": {
            "range": {
            "date_of_birth": {
                "gte": f"now-{upper_age}y/d",
                "lte": f"now-{lower_age}y/d"
            }
            }
        }
        }
    return body


