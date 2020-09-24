from pathlib import Path
import thesis_database


def initialize_database(database_name):
    db_details, _, main_user, _ = thesis_database.utilities.read_config(
        Path('/Users/Krista/Documents/GitHub/thesis_database/thesis_database/').joinpath('dbConfig').joinpath(
            f'{database_name}_database_config.yaml'))
    thesis_database.Database.initialize(database=db_details['database'],
                                        host=db_details['host'],
                                        port=5432,
                                        user=main_user['user'],
                                        password=main_user['password'])
