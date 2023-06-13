from pprint import pprint
import csv
import re
import operator
import itertools
import os


def read_to_dict(file_name):
    contacts_dict = []
    with open(file_name, encoding="utf8") as f:
        reader = csv.reader(f, delimiter=",")
        contacts_list = list(reader)

        keys = contacts_list[0]
        values = contacts_list[1:]
        for num, vals in enumerate(values):
            contacts_dict.append({})
            for key, val in zip(keys, vals):
                contacts_dict[num].update({key: val})

        return contacts_dict


def write_to_file(file_name, dicts):
    keys = list(dicts[0].keys())
    with open(file_name, "w", encoding="utf8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(keys)
        for d in dicts:
            datawriter.writerow(d.values())


def fix_phones(in_file, out_file):
    with open(in_file, encoding="utf8") as f:
        text = f.read()

    pattern_phone = r'(\+7|8)?\s*\(?(\d{3})\)?[\s*-]?(\d{3})[\s*-]?(\d{2})[\s*-]?(\d{2})(\s*)\(?(доб\.?)?\s*(\d*)?\)?'
    fixed_phones = re.sub(pattern_phone, r'+7(\2)\3-\4-\5\6\7\8', text)
    with open(out_file, 'w+', encoding="utf8") as f:
        text = f.write(fixed_phones)


def fix_names(in_file):
    contacts_dict = read_to_dict(in_file)
    for v in contacts_dict:
        splt = v['lastname'].split(' ')
        if len(splt) > 1:
            v['lastname'] = splt[0]
            v['firstname'] = splt[1]
            if len(splt) > 2:
                v['surname'] = splt[2]

        splt = v['firstname'].split(' ')
        if len(splt) > 1:
            v['firstname'] = splt[0]
            v['surname'] = splt[1]

    return contacts_dict


def merge_names(contacts):
    all_keys = set(contacts[0].keys())
    group_list = ['firstname', 'lastname']
    group = operator.itemgetter(*group_list)
    cols = operator.itemgetter(*(all_keys ^ set(group_list)))
    contacts.sort(key=group)
    grouped = itertools.groupby(contacts, group)

    merge_data = []
    for (firstname, lastname), g in grouped:
        merge_data.append({'lastname': lastname, 'firstname': firstname})
        for gr in g:
            d1 = merge_data[-1]
            for k, v in gr.items():
                if k not in d1 or d1[k] == '':
                    d1[k] = v

    return merge_data


def main():
    fix_phones(in_file="phonebook_raw.csv", out_file="fixed_phones.csv")

    fixed_names = fix_names(in_file="fixed_phones.csv")
    os.remove("fixed_phones.csv")

    merged_names = merge_names(fixed_names)

    write_to_file("phonebook.csv", merged_names)


if __name__ == "__main__":
    main()