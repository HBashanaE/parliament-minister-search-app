import os
import json
from collections import defaultdict

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, '../data/data_essential_member_details.json')

with open(filepath, 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

preprocessed_data = []
for entry in data:
    member_details = {}

    name = entry['member_sname_sin']
    basic_details = defaultdict(lambda: None, entry['basic_details'])
    political_party = basic_details['දේශපාලන පක්ෂය']
    electoral_district = basic_details['මැතිවරණ දිස්ත්‍රික්කය / ජාතික ලැයිස්තුව']
    date_of_birth = basic_details['උපන් දිනය']
    civil_status = basic_details['සිවිල් තත්ත්වය']
    religion = basic_details['ආගම']
    position = basic_details['තනතුර']
    profession = basic_details['වෘත්තිය / රැකියාව']
    committees_currently_in = entry['commitees_current']
    committees_was_in = entry['commitees_old']

    for variable in ["name", "political_party", "electoral_district", "date_of_birth",
                     "civil_status", "religion", "position", "profession", "committees_currently_in", "committees_was_in"]:
        member_details[variable] = eval(variable)
    preprocessed_data.append(member_details)

filepath = os.path.join(dirname, '../data/preprocessed_member_details.json')

with open(filepath, 'w', encoding='utf-8') as json_file:
    data = json.dump(preprocessed_data, json_file, ensure_ascii=False)

