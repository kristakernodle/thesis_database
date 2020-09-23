from pathlib import Path
import thesis_database_pkg


def initialize_database(database_name):
    db_details, _, main_user, _ = thesis_database_pkg.utilities.read_config(
        Path(thesis_database_pkg.__file__).parent.joinpath('dbConfig').joinpath(
            f'{database_name}_database_config.yaml'))
    thesis_database_pkg.Database.initialize(database=db_details['database'],
                                            host=db_details['host'],
                                            port=5432,
                                            user=main_user['user'],
                                            password=main_user['password'])
