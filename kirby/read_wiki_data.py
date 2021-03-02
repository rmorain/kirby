# AUTOGENERATED! DO NOT EDIT! File to edit: 11_read_wiki_data.ipynb (unless otherwise specified).

__all__ = ['fix_label', 'write_to_file', 'write_to_database', 'read_wiki_data', 'main']

# Cell
from qwikidata.json_dump import WikidataJsonDump
import sqlite3
import pandas
import CreateDatabase
from .properties import properties

# Cell
# wjd = WikidataJsonDump('latest-all.json.bz2')


# Make sure all string with apostrophes have an scape character for sql


def fix_label(label):
    index = 0
    while index < len(label):
        if label[index] == '\'':
            label = label[:index] + '\'' + label[index:]
            index += 1
        index += 1
    return label


def write_to_file(conn, entities, properties, aliases):

    for idx, item in enumerate(entities):
        if idx % 1000 == 0:
            conn.write("\n\n\n\nINSERT INTO Entities\n (entity_id, label, description)\n VALUES\n")
        if (idx + 1) % 1000 == 0 or idx == len(entities) - 1:
            item = item[:-1] + ';'
        conn.write('{}\n'.format(item))

    for idx, item in enumerate(properties):
        if idx % 1000 == 0:
            conn.write(
                "\n\n\n\nINSERT INTO Properties_relations\n (entity_id, relations)\n VALUES\n")
        if (idx + 1) % 1000 == 0 or idx == len(properties) - 1:
            item = item[:-1] + ';'
        conn.write('{}\n'.format(item))

    for idx, item in enumerate(aliases):
        if idx % 1000 == 0:
            conn.write("\n\n\n\nINSERT INTO Aliases\n (entity_id, aliases)\n VALUES\n")

        if (idx + 1) % 1000 == 0 or idx == len(aliases) - 1:
            item = item[:-1] + ';'
        conn.write('{}\n'.format(item))


def write_to_database(conn, c, entities, properties, aliases):

    query = []
    for idx, item in enumerate(entities):
        if idx % 1000 == 0:
            query.append("INSERT INTO Entities\n (entity_id, label, description)\n VALUES")

        if (idx + 1) % 1000 == 0 or idx == len(entities) - 1:
            query.append(item[:-1] + ';')
            c.execute('\n'.join(query))
            query.clear()
        else:
            query.append(item)
    query.clear()
    for idx, item in enumerate(properties):
        if idx % 1000 == 0:
            query.append("INSERT INTO Properties_relations\n (entity_id, relations)\n VALUES")

        if (idx + 1) % 1000 == 0 or idx == len(properties) - 1:
            query.append(item[:-1] + ';')
            c.execute('\n'.join(query))
            query.clear()
        query.append(item)
    query.clear()

    for idx, item in enumerate(aliases):
        if idx % 1000 == 0:
            query.append("INSERT INTO Aliases\n (entity_id, aliases)\n VALUES")
        if (idx + 1) % 1000 == 0 or idx == len(aliases) - 1:
            query.append(item[:-1] + ';')
            # print(query)
            c.execute('\n'.join(query))
            query.clear()
        else:
            query.append(item)
    conn.commit()


def read_wiki_data(wjd, o_format, o_file):
    items_list = []  # This will hold the data for the items
    # items = {}  # Connected items go in the objects dictionary
    max_entities = 100  # Variable to stop the program during testing
    property_list = []  # List of all properties
    aliases = []  # List of all aliases
    conn = None
    c = None
    if o_format == 0:
        conn = open('{}.txt'.format(o_file), 'a', encoding="utf-8")
    else:
        # Create database
        CreateDatabase.create_database(o_file)
        # Connection to database
        conn = sqlite3.connect('{}.db'.format(o_file))
        c = conn.cursor()

    for ii, entity_dict in enumerate(wjd):

        if ii % 500 == 0 and ii != 0:
            if o_format == 0:
                write_to_file(conn, items_list, property_list, aliases)
            else:
                write_to_database(conn, c, items_list, property_list, aliases)

            aliases.clear()
            property_list.clear()
            items_list.clear()
        description = ''
        # Store the id of the entity
        entity_id = entity_dict['id']
        index = 0

        if 'descriptions' in entity_dict and 'en' in entity_dict['descriptions'] and 'value' in entity_dict['descriptions']['en']:
            description = entity_dict['descriptions']['en']['value']

        # Just keep the entities that have a name in English
        if 'labels' in entity_dict:
            if 'en' in entity_dict['labels']:
                # temp = fix_label(entity_dict['labels']['en']['value'])
                items_list.append('(\'{}\', \'{}\', \'{}\'),'.format(entity_id, fix_label(entity_dict['labels']['en']['value']),
                                                                     fix_label(description)))
            else:
                continue

        if 'aliases' in entity_dict:  # Create table
            entity_aliases = []
            if 'en-gb' in entity_dict['aliases']:
                for element in entity_dict['aliases']['en-gb']:
                    entity_aliases.append(fix_label(element['value']))
            if 'en' in entity_dict['aliases']:
                for element in entity_dict['aliases']['en']:
                    entity_aliases.append(fix_label(element['value']))
            if len(entity_aliases) > 0:
                aliases.append('(\'{}\', \'{}\'),'.format(entity_id, ','.join(entity_aliases)))

        if "claims" in entity_dict:
            entity_properties = []
            for inner_key in entity_dict["claims"].keys():
                if 'datavalue' in entity_dict["claims"][inner_key][0]['mainsnak'] \
                        and ('value' in entity_dict["claims"][inner_key][0]['mainsnak']['datavalue']) \
                        and isinstance(entity_dict["claims"][inner_key][0]['mainsnak']['datavalue']['value'], dict) \
                        and ('id' in entity_dict["claims"][inner_key][0]['mainsnak']['datavalue']['value']):
                    entity_properties.append('({}, {})'.format(inner_key, entity_dict["claims"][inner_key][0]['mainsnak']['datavalue']['value']['id']))
            property_list.append('(\'{}\', \'{}\'),'.format(entity_id, ','.join(entity_properties)))

# Cell
def main():
    wjd_name = input("Enter the JSON path: ")
    print(wjd_name)
    wiki_dump = WikidataJsonDump(wjd_name)
    print("What output file do you want? a database file or a text file with insert statements?",
          '\n0: text file\n1: database file')
    output_format = -1
    while not (output_format == 0 or output_format == 1):
        output_format = int(input('Please enter 0 or 1: '))
    if output_format == 0:
        output_file = input('Enter name of text file. Do not include .txt: ')
    else:
        output_file = input('Enter name of database file. Do not include .db: ')

    read_wiki_data(wiki_dump, output_format, output_file)


if __name__ == "__main__":
    main()