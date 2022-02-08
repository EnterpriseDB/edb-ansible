import os
import json

if __name__ == '__main__':
    a_file = open("vars.json", "r")
    json_object = json.load(a_file)

    if os.getenv('EDB_PG_TYPE') == 'EPAS':
        json_object['pg_databases'][0]['owner'] = 'enterprisedb'
        json_object['pg_grant_roles'][0]['user'] = 'enterprisedb'
    else:
        json_object['pg_databases'][0]['owner'] = 'postgres'
        json_object['pg_grant_roles'][0]['user'] = 'postgres'
    a_file = open("vars.json", "w")
    json.dump(json_object, a_file, indent=1)
    a_file.close()