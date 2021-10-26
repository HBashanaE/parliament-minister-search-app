from elasticsearch import Elasticsearch

es = Elasticsearch()

def simple_tokenizer(query):
    return query.split()

def tokenize(query, tokenizer):
    return tokenizer(query)

def classify_intent(query):
    ministries = ["අමාත්‍යතුමා", "අමාත්‍යතුමිිය", "අමාත්‍ය", "අමාත්‍යාංශය", "මන්ත්‍රීවරු", "අමාත්‍යවරු", "ඇමතිතුමා", "ඇමතිතුමිය", "ඇමතිවරු", "මන්ත්‍රීතුමා", "මන්ත්‍රීතුමිය", "මන්ත්‍රී"]
    provinces = ["අනුරාධපුර", "යාපනය", "ගාල්ල", "මඩකලපුව", "ජාතික ලැයිස්තුව", 
    "මාතර", "කළුතර", "රත්නපුර", "ගම්පහ", "කෑගල්ල", "වන්නි", "දිගාමඩුල්ල", "පුත්තලම",
    "පොළොන්නරුව", "මොණරාගල", "ත්‍රිකුණාමලය", "හම්බන්තොට", "මහනුවර", "මාතලේ",
    "බදුල්ල", "කොළඹ", "නුවරඑළිය", "කුරුණෑගල", "දිස්ත්‍රික්කය", "දිස්ත්‍රික්ක", "දිස්ත්‍රික්කයේ", "දිස්ත්‍රික්කයට"]
    parties = ["පෙරමුණ", "පෙරමුණේ", "සන්ධානය", "සන්ධානයේ  ", "බලවේගය", "බලවේගයේ", "පක්ෂය", "පක්ෂයේ", "කොංග්‍රස්", "කොංග්‍රසය", "කොන්ග්‍රස්", "කොන්ග්‍රසය", "කොංග්‍රසයේ", "කොන්ග්‍රසයේ",
     "කුට්ටනි", "කච්චි", "විඩුදලෛප්"]
    tokenized_query = tokenize(query, simple_tokenizer)
    intents = set()
    for token in tokenized_query:
        if(token in ministries):
            intents.add('ministry')
        if(token in provinces):
            intents.add('province')
        if(token in parties):
            intents.add('party')
        else:
            intents.add('misc')
    if(len(intents) > 1):
        intents.discard('misc')
    return intents

def search_index(query, intents):
    if('misc' in intents):
        print('misc query')
    else:
        print(intents)



query = 'මහින්ද රා'
body = {
            "query": {
                "match":{
                    "name": query
                }
            }
        }

# res = es.search(index="test", body=body)
# print(res)

intents = classify_intent(query)
search_index(query, intents)