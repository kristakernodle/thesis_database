from thesis_database.tools import Cursor
import thesis_database.models as models
import thesis_database.tools.queries.select_queries as queries


def list_reviewer_ids():
    with Cursor() as cursor:
        return queries.list_all_reviewer_ids(cursor)


def list_experiment_ids():
    with Cursor() as cursor:
        return queries.list_all_experiment_ids(cursor)


def list_trial_ids_for_folder(folder):
    with Cursor() as cursor:
        return queries.list_trial_ids_for_folder(cursor, folder.folder_id)


def list_all_blind_names():
    with Cursor() as cursor:
        return queries.list_all_blind_names(cursor)


def list_blind_folder_id(reviewer, folder):
    with Cursor() as cursor:
        return queries.list_blind_folder_id(cursor, reviewer.reviewer_id, folder.folder_id)


def list_folder_ids_for_experiment(experiment):
    with Cursor() as cursor:
        return queries.list_all_folder_ids_for_experiment(cursor, experiment.experiment_id)


def list_folder_ids_from_blind_folders(experiment):
    with Cursor() as cursor:
        return queries.list_all_folder_ids_for_blind_folders_of_experiment(cursor, experiment.experiment_id)


def list_all_folders(experiment):
    all_folders = list()
    for folder_id in list_folder_ids_for_experiment(experiment):
        all_folders.append(models.Folder.from_db(folder_id=folder_id))
    return all_folders


def list_all_blinded_folders(experiment):
    all_blinded_folders = list()
    for folder_id in list_folder_ids_from_blind_folders(experiment):
        all_blinded_folders.append(models.Folder.from_db(folder_id=folder_id))
    return all_blinded_folders


def list_all_not_blind_folders(experiment):
    all_folders = list_all_folders(experiment)
    all_masked_folders = list_all_blinded_folders(experiment)
    not_blind_folders = [folder for folder in all_folders if folder not in all_masked_folders]
    return not_blind_folders


def list_all_session_dir(experiment, mouse):
    with Cursor() as cursor:
        return queries.list_all_session_dirs_for_mouse(cursor, mouse.mouse_id, experiment.experiment_id)


def list_all_folder_dir(experiment):
    with Cursor() as cursor:
        return queries.list_all_folder_dirs_for_experiment(cursor, experiment.experiment_id)


def list_all_trial_dir(experiment):
    with Cursor() as cursor:
        return queries.list_all_trial_dirs_for_experiment(cursor, experiment.experiment_id)


def list_all_blind_folder_ids(experiment):
    with Cursor() as cursor:
        return queries.list_all_blind_folder_ids(cursor, experiment.experiment_id)


def list_all_blind_names_for_reviewer_experiment(reviewer, experiment):
    with Cursor() as cursor:
        return queries.list_all_blind_names_for_reviewer_experiment(cursor, reviewer.reviewer_id,
                                                                    experiment.experiment_id)


def list_all_blinded_trial_full_paths_for_reviewer_experiment(reviewer, experiment):
    with Cursor() as cursor:
        return queries.list_all_blind_trials_full_paths_for_reviewer_experiment(cursor, reviewer.reviewer_id,
                                                                                experiment.experiment_id)
