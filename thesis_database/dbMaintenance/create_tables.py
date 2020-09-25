from thesis_database.tools import Database
from thesis_database.tools import Cursor


# MOUSE TABLE
def create_mouse_table(a_cursor):
    a_cursor.execute("CREATE TABLE mouse("
                     "mouse_id uuid default uuid_generate_v4() constraint mouse_pkey primary key,"
                     "eartag smallint not null,"
                     "birthdate date not null,"
                     "genotype boolean not null,"
                     "sex varchar(6) not null);")
    a_cursor.execute("create unique index mouse_eartag_uindex on mouse (eartag);")


# EXPERIMENTS TABLE
def create_experiments_table(a_cursor):
    a_cursor.execute("CREATE TABLE experiments( "
                     "experiment_id uuid default uuid_generate_v4()  constraint experiments_pkey primary key,"
                     "experiment_dir varchar(255) not null,"
                     "experiment_name varchar(50) not null);")
    a_cursor.execute("create unique index experiments_experiment_dir_uindex on experiments (experiment_dir);")
    a_cursor.execute("create unique index experiments_experiment_name_uindex on experiments (experiment_name);")


# PARTICIPANT DETAILS TABLE
def create_participant_details_table(a_cursor):
    a_cursor.execute("CREATE TABLE participant_details( "
                     "detail_id uuid default uuid_generate_v4() constraint participant_details_pkey primary key,"
                     "mouse_id uuid references mouse not null,"
                     "experiment_id uuid references experiments not null,"
                     "start_date date,"
                     "end_date date,"
                     "exp_spec_details json,"
                     "participant_dir varchar(255));")
    a_cursor.execute("create unique index participant_dir_uindex on participant_details (participant_dir);")


# REVIEWERS TABLE
def create_reviewers_table(a_cursor):
    a_cursor.execute("CREATE TABLE reviewers("
                     "reviewer_id  uuid default uuid_generate_v4() constraint reviewers_pkey primary key,"
                     "first_name varchar(10) not null,"
                     "last_name varchar(10) not null,"
                     "toScore_dir varchar(255) not null,"
                     "scored_dir varchar(255) not null);")
    a_cursor.execute("create unique index reviewers_toScore_dir_uindex on reviewers (toScore_dir);")
    a_cursor.execute("create unique index reviewers_scored_dir_uindex on reviewers (scored_dir);")


# SESSIONS TABLE
def create_sessions_table(a_cursor):
    a_cursor.execute("CREATE TABLE sessions("
                     "session_id uuid default uuid_generate_v4() constraint session_pkey primary key,"
                     "mouse_id uuid references mouse not null,"
                     "experiment_id uuid references experiments not null,"
                     "session_date date not null,"
                     "session_dir varchar(255) not null,"
                     "session_num smallint);")
    a_cursor.execute("create unique index sessions_session_dir_uindex on sessions (session_dir);")


# FOLDERS TABLE
def create_folders_table(a_cursor):
    a_cursor.execute("CREATE TABLE folders("
                     "folder_id uuid default uuid_generate_v4() constraint folder_pkey primary key,"
                     "session_id uuid references sessions not null,"
                     "folder_dir varchar(255) not null);")
    a_cursor.execute("create unique index folders_folder_dir_uindex on folders (folder_dir);")


# BLIND FOLDERS TABLE
def create_blind_folders_table(a_cursor):
    a_cursor.execute("CREATE TABLE blind_folders("
                     "blind_folder_id uuid default uuid_generate_v4() constraint blind_folders_pkey primary key,"
                     "folder_id uuid references folders not null,"
                     "reviewer_id uuid references reviewers not null,"
                     "blind_name varchar(15) not null);")
    a_cursor.execute("create unique index blind_folders_blind_name_uindex on blind_folders (blind_name);")


# TRIALS TABLE
def create_trials_table(a_cursor):
    a_cursor.execute("CREATE TABLE trials("
                     "trial_id uuid default uuid_generate_v4() constraint trials_pkey primary key,"
                     "experiment_id uuid references experiments not null,"
                     "folder_id uuid references folders not null,"
                     "trial_dir varchar(255) not null,"
                     "trial_date date);")
    a_cursor.execute("create unique index trial_dir_uindex on trials (trial_dir);")


# BLIND TRIALS TABLE
def create_blind_trials_table(a_cursor):
    a_cursor.execute("CREATE TABLE blind_trials("
                     "blind_trial_id uuid default uuid_generate_v4() constraint blind_trial_pkey primary key,"
                     "trial_id uuid references trials not null,"
                     "folder_id  uuid references folders not null,"
                     "full_path varchar(255) not null);")
    a_cursor.execute("create unique index blind_trials_full_path_uindex on blind_trials (full_path);")


# TRIAL SCORE TABLE
def create_trial_score_table(a_cursor):
    a_cursor.execute("CREATE TABLE trial_scores("
                     "trial_score_id uuid default uuid_generate_v4() constraint trial_score_pkey primary key,"
                     "trial_id uuid references trials not null,"
                     "reviewer_id uuid references reviewers not null,"
                     "trial_num smallint not null,"
                     "reach_score smallint not null,"
                     "abnormal_movt_score bool not null,"
                     "grooming_score bool not null);")


# CREATE ALL TABLES
def create_all_tables_main(db_details, main_user):
    Database.initialize(database=db_details['database'],
                        host=db_details['host'],
                        port=5432,
                        user=main_user['user'],
                        password=main_user['password'])
    with Cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        create_mouse_table(cursor)
        create_experiments_table(cursor)
        create_participant_details_table(cursor)
        create_sessions_table(cursor)
        create_folders_table(cursor)
        create_trials_table(cursor)
        create_reviewers_table(cursor)
        create_blind_folders_table(cursor)
        create_blind_trials_table(cursor)
        create_trial_score_table(cursor)
