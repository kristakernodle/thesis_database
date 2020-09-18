from pathlib import Path
from thesis_database_pkg import models, tools


def update_experiment_from_data_dirs(experiment):
    if not Path(experiment.experiment_dir).exists():
        print(f'Experiment directory, {experiment.experiment_dir}, does not exist.')

    all_participant_dirs = list(Path(experiment.experiment_dir).glob('et*/'))

    for participant_dir in all_participant_dirs:

        eartag_num = int(participant_dir.name.strip('et'))
        mouse = models.Mouse.from_db(eartag_num)

        if mouse is None:
            continue

        mouse_details = models.ParticipantDetails.from_db(eartag_num, experiment.experiment_name)

        if mouse_details is None:
            continue

        if experiment.experiment_name == 'skilled-reaching':
            training_dir = Path(mouse_details.participant_dir).joinpath('Training')
            all_session_dirs = training_dir.glob(f'et{eartag_num}_*_*T*/')
        elif experiment.experiment_name == 'grooming':
            training_dir = Path(mouse_details.participant_dir)
            all_session_dirs = training_dir.glob(f'et{eartag_num}_*_*G*/')
        else:
            all_session_dirs = None
            print('Need information about training and session directories for this experiment')

        for session_dir in all_session_dirs:
            session_date = int(session_dir.name.split('_')[1])
            session = models.Session(mouse.mouse_id, experiment.experiment_id,
                                     str(session_dir), session_date).save_to_db()

            if experiment.experiment_name == 'skilled-reaching':
                all_folder_dirs = session_dir.glob('Reaches*')
            elif experiment.experiment_name == 'grooming':
                print('Need information about how to input grooming experiment from data dirs')
                continue
            else:
                all_folder_dirs = None
                print('Need information about folder and trial directories for this experiment')

            for folder_dir in all_folder_dirs:
                folder = models.Folder(session.session_id, str(folder_dir)).save_to_db()
                all_trial_dirs = folder_dir.glob('*R*.mp4')

                if len(list(all_trial_dirs)) == 0:
                    all_trial_dirs = folder_dir.glob('*R*.MP4')

                for trial_dir in all_trial_dirs:
                    models.Trial(experiment.experiment_id,
                                 folder.folder_id,
                                 str(trial_dir),
                                 session.session_date).save_to_db()


def update_from_data_dirs(db_details, main_user):
    tools.Database.initialize(database=db_details['database'],
                              host=db_details['host'],
                              port=5432,
                              user=main_user['user'],
                              password=main_user['password'])
    with tools.Cursor() as cursor:
        all_experiment_names = tools.list_all_experiment_names(cursor)

    for experiment_name in all_experiment_names:
        update_experiment_from_data_dirs(experiment_name)
