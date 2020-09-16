from pathlib import Path
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import dbMaintenance
from utilities import read_config, write_config


def setup_database(dbName):
    dbConfig_path = Path.cwd().joinpath('dbConfig').joinpath(f'{dbName}_database_config.yaml')

    # Get or generate the configuration settings for the database to access
    if dbConfig_path.exists():
        # Database config already exists
        dbDetails, superUser, mainUser = read_config(dbConfig_path)
    else:
        # Database config does not already exist, starting from default
        default_dbConfig_path = Path.cwd().joinpath('dbConfig').joinpath('default_database_config.yaml')
        dbDetails, superUser, mainUser = read_config(default_dbConfig_path)

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
    databaseExists = cursor.fetchall()[0][0]

    if not databaseExists:

        createDatabase_command = f"CREATE DATABASE {dbDetails['database']};"
        # createUser_command = f"CREATE USER {mainUser['user']} WITH ENCRYPTED PASSWORD '{mainUser['password']}';"
        # grantPrivileges_command = f"GRANT ALL PRIVILEGES ON DATABASE {dbDetails['database']} TO {mainUser['user']};"

        cursor.execute(createDatabase_command)
        # cursor.execute(createUser_command)
        # cursor.execute(grantPrivileges_command)

        # Close this connection to the database
        con.close()

        # Create the tables and views as the mainUser
        dbMaintenance.create_all_tables(dbDetails, mainUser)
        dbMaintenance.create_all_views(dbDetails, mainUser)

    else:
        print("Database already exists!")
        drop_db = input('Do you want to drop this database? [y/N]: ')
        if drop_db.lower() in ['y', 'yes', '1']:
            dropDatabase_command = f"DROP DATABASE {dbDetails['database']};"
            cursor.execute(dropDatabase_command)
        con.close()
