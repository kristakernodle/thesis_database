from pathlib import Path

import psycopg2
import yaml
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import dbMaintenance.create_all_tables
import dbMaintenance.create_all_views


def read_config(yaml_full_path):
    with open(yaml_full_path) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data['dbDetails'], data['superUser'], data['mainUser']


def write_config(db_details, super_user, main_user, yaml_full_path):
    data = {'dbDetails': db_details,
            'superUser': super_user,
            'mainUser': main_user
            }
    with open(yaml_full_path, 'w+') as f:
        yaml.dump(data, f)


if __name__ == '__main__':
    dbName = input('Enter Database Name (no spaces or special characters): ').lower()
    dbConfig_path = Path.cwd().joinpath('dbConfig').joinpath(f'{dbName}_database_config.yaml')

    # Get or generate the configuration settings for the database to access
    if dbConfig_path.exists():
        # Database config already exists
        dbDetails, superUser, mainUser = read_config(dbConfig_path)
    else:
        # Database config does not already exist, starting from default
        default_dbConfig_path = Path.cwd().joinpath('dbConfig').joinpath('default_database_config.yaml')
        dbDetails, superUser, mainUser = read_config(dbConfig_path)

        dbDetails['database'] = dbName
        dbDetails['host'] = input('Host (not sure? use localhost): ')
        dbDetails['backupDir'] = input('Enter the directory where all back-up files should be saved: ')
        superUser['password'] = input('Super user password: ')
        mainUser['user'] = input('Main user: ')
        mainUser['password'] = input('Main user password: ')
        write_config(dbDetails, superUser, mainUser,
                     Path.cwd().joinpath('dbConfig').joinpath(f'{dbName}_database_config.yaml'))

    # Connect to PostgreSQL DBMS
    con = psycopg2.connect(**superUser)
    con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = con.cursor()
    databaseExists_command = f"SELECT EXISTS( SELECT datname FROM pg_catalog.pg_database WHERE datname = '{dbName}');"
    cursor.execute(databaseExists_command)
    databaseExists = cursor.fetchone()[0]

    if ~databaseExists:

        createDatabase_command = f"CREATE DATABASE {dbDetails['database']};"
        createUser_command = f"CREATE USER {mainUser['user']} WITH ENCRYPTED PASSWORD '{mainUser['password']}';"
        grantPrivileges_command = f"GRANT ALL PRIVILEGES ON DATABASE {dbDetails['database']} TO {mainUser['user']};"

        cursor.execute(createDatabase_command)
        cursor.execute(createUser_command)
        cursor.execute(grantPrivileges_command)

        # Close this connection to the database
        con.close()

        # Create the tables and views as the mainUser
        dbMaintenance.create_all_tables.create_all_tables_main(dbDetails, mainUser)
        dbMaintenance.create_all_views.create_views_main(dbDetails, mainUser)

    else:
        print("Database already exists!")
        con.close()
