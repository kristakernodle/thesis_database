import csv
from pathlib import Path
from .. import utilities as util, models
from thesis_database_pkg.tools import Database


def read_back_up_csv(full_path):
    with open(full_path) as f:
        csv_reader = csv.reader(f)
        next(csv_reader)
        return list(csv_reader)


def get_reviewer_from_old_id(reviewer_id, back_up_reviewers_full_path):
    all_reviewers = read_back_up_csv(back_up_reviewers_full_path)
    for reviewer_data in all_reviewers:
        if reviewer_data[0] == reviewer_id:
            return models.Reviewer.from_db(scored_dir=reviewer_data[-1])


def get_experiment_from_old_id(experiment_id, back_up_experiments_full_path):
    all_experiments = read_back_up_csv(back_up_experiments_full_path)
    for experiment_data in all_experiments:
        if experiment_data[0] == experiment_id:
            return models.Experiment.from_db(experiment_name=experiment_data[2])


def get_mouse_from_old_id(mouse_id, back_up_mouse_full_path):
    all_mice = read_back_up_csv(back_up_mouse_full_path)
    for mouse_data in all_mice:
        if mouse_data[0] == mouse_id:
            return models.Mouse.from_db(eartag=mouse_data[1])


def get_session_from_old_id(session_id, back_up_sessions_full_path):
    all_sessions = read_back_up_csv(back_up_sessions_full_path)
    for session_data in all_sessions:
        if session_data[0] == session_id:
            return models.Session.from_db(session_dir=session_data[-1])


def get_folder_from_old_id(folder_id, back_up_folders_full_path):
    all_folders = read_back_up_csv(back_up_folders_full_path)
    for folder_data in all_folders:
        if folder_data[0] == folder_id:
            return models.Folder.from_db(folder_dir=folder_data[-1])


def get_trial_from_old_id(trial_id, back_up_trials_full_path):
    all_trials = read_back_up_csv(back_up_trials_full_path)
    for trial_data in all_trials:
        if trial_data[0] == trial_id:
            return models.Trial.from_db(trial_dir=trial_data[-2])


def decode_exp_spec_details(exp_spec_details, experiment_name):
    if experiment_name == 'skilled-reaching':
        paw_preference = None
        reaching_box = None
        if 'right' in exp_spec_details:
            paw_preference = 'right'
        elif 'left' in exp_spec_details:
            paw_preference = 'left'
        if '1' in exp_spec_details:
            reaching_box = 1
        elif '2' in exp_spec_details:
            reaching_box = 2
        if paw_preference is None or reaching_box is None:
            print('Something decoded incorrectly')
            print(f'paw preference: {paw_preference}')
            print(f'reaching box: {reaching_box}')
            print(f'exp_spec_details: {exp_spec_details}')
        decoded_details = dict()
        decoded_details["paw preference"] = paw_preference
        decoded_details["reaching box"] = reaching_box
        return decoded_details
    else:
        return None


def populate_reviewers(back_up_reviewers_full_path):
    for reviewer_data in read_back_up_csv(back_up_reviewers_full_path):
        _, first_name, last_name, to_score_dir, scored_dir = reviewer_data
        models.Reviewer(first_name, last_name, to_score_dir, scored_dir).save_to_db()


def populate_experiments(back_up_experiments_full_path):
    for exp_data in read_back_up_csv(back_up_experiments_full_path):
        _, exp_dir, exp_name = exp_data
        models.Experiment(exp_name, exp_dir).save_to_db()


def populate_mouse(back_up_mouse_full_path):
    for mouse_data in read_back_up_csv(back_up_mouse_full_path):
        _, eartag, birthdate, encoded_genotype, sex = mouse_data
        models.Mouse(int(eartag), int(''.join(birthdate.split('-'))),
                     util.decode_genotype(encoded_genotype), sex).save_to_db()


def populate_participant_details(back_up_mouse_full_path, back_up_experiments_full_path,
                                 back_up_participant_details_full_path):
    for participant_detail in read_back_up_csv(back_up_participant_details_full_path):
        _, mouse_id, experiment_id, start_date, end_date, _, _ = participant_detail
        participant_dir = participant_detail[-1]
        mouse = get_mouse_from_old_id(mouse_id, back_up_mouse_full_path)
        experiment = get_experiment_from_old_id(experiment_id, back_up_experiments_full_path)
        exp_spec_details = decode_exp_spec_details(''.join(participant_detail[5:-1]), experiment.experiment_name)
        if start_date is not None and start_date is not '':
            start_date = int(''.join(start_date.split('-')))
        else:
            start_date = None
        if end_date is not None and end_date is not '':
            end_date = int(''.join(end_date.split('-')))
        else:
            end_date = None
        models.ParticipantDetails(mouse, experiment, participant_dir, start_date,
                                  end_date, exp_spec_details).save_to_db()


def populate_sessions(back_up_mouse_full_path, back_up_experiments_full_path, back_up_sessions_full_path):
    for session_data in read_back_up_csv(back_up_sessions_full_path):
        _, mouse_id, experiment_id, session_date, session_dir = session_data
        mouse = get_mouse_from_old_id(mouse_id, back_up_mouse_full_path)
        experiment = get_experiment_from_old_id(experiment_id, back_up_experiments_full_path)
        models.Session(mouse.mouse_id, experiment.experiment_id, session_dir,
                       int(''.join(session_date.split('-')))).save_to_db()


def populate_folders(back_up_sessions_full_path, back_up_folders_full_path):
    for folder_data in read_back_up_csv(back_up_folders_full_path):
        _, session_id, folder_dir = folder_data
        session = get_session_from_old_id(session_id, back_up_sessions_full_path)
        models.Folder(session.session_id, folder_dir).save_to_db()


def populate_trials(back_up_experiments_full_path, back_up_folders_full_path, back_up_trials_full_path):
    for trial_data in read_back_up_csv(back_up_trials_full_path):
        _, experiment_id, folder_id, trial_dir, trial_date = trial_data
        experiment = get_experiment_from_old_id(experiment_id, back_up_experiments_full_path)
        folder = get_folder_from_old_id(folder_id, back_up_folders_full_path)
        models.Trial(experiment.experiment_id, folder.folder_id, trial_dir,
                     int(''.join(trial_date.split('-')))).save_to_db()


def populate_blind_folders(back_up_reviewers_full_path, back_up_folders_full_path, back_up_blind_folders_full_path):
    for blind_folder_data in read_back_up_csv(back_up_blind_folders_full_path):
        _, folder_id, reviewer_id, blind_name = blind_folder_data
        folder = get_folder_from_old_id(folder_id, back_up_folders_full_path)
        reviewer = get_reviewer_from_old_id(reviewer_id, back_up_reviewers_full_path)
        models.BlindFolder(folder.folder_id, reviewer.reviewer_id, blind_name).save_to_db()


def populate_blind_trials(back_up_folders_full_path, back_up_trials_full_path, back_up_blind_trials_full_path):
    for blind_trial_data in read_back_up_csv(back_up_blind_trials_full_path):
        _, trial_id, folder_id, full_path = blind_trial_data
        trial = get_trial_from_old_id(trial_id, back_up_trials_full_path)
        folder = get_folder_from_old_id(folder_id, back_up_folders_full_path)
        models.BlindTrial(trial.trial_id, folder.folder_id, full_path).save_to_db()


def populate_db_from_back_up_csv(db_details, main_user):
    all_tables = ['reviewers',
                  'mouse',
                  'experiments',
                  'participant_details',
                  'sessions',
                  'folders',
                  'trials',
                  'blind_folders',
                  'blind_trials']
    dir_all_back_up_csv = db_details["backupDir"]
    path_all_back_up_csv = Path(dir_all_back_up_csv)
    if not all([path_all_back_up_csv.joinpath(table+'.csv').exists() for table in all_tables]):
        print('Some back up files do not exist')
        return False

    reviewer_csv = path_all_back_up_csv.joinpath('reviewers.csv')
    mouse_csv = path_all_back_up_csv.joinpath('mouse.csv')
    experiments_csv = path_all_back_up_csv.joinpath('experiments.csv')
    sessions_csv = path_all_back_up_csv.joinpath('sessions.csv')
    folders_csv = path_all_back_up_csv.joinpath('folders.csv')
    trials_csv = path_all_back_up_csv.joinpath('trials.csv')

    Database.initialize(database=db_details['database'],
                        host=db_details['host'],
                        port=5432,
                        user=main_user['user'],
                        password=main_user['password'])

    populate_reviewers(reviewer_csv)
    populate_experiments(experiments_csv)
    populate_mouse(mouse_csv)
    populate_participant_details(mouse_csv, experiments_csv, path_all_back_up_csv.joinpath('participant_details.csv'))
    populate_sessions(mouse_csv, experiments_csv, sessions_csv)
    populate_folders(sessions_csv, folders_csv)
    populate_trials(experiments_csv, folders_csv, trials_csv)
    populate_blind_folders(reviewer_csv, folders_csv, path_all_back_up_csv.joinpath('blind_folders.csv'))
    populate_blind_trials(folders_csv, trials_csv, path_all_back_up_csv.joinpath('blind_trials.csv'))
