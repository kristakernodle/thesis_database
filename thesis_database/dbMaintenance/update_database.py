from pathlib import Path
import thesis_database.models as models
import thesis_database.tools as tools
from thesis_database.db_initialize import initialize_database


def update_experiment_from_data_dirs(a_experiment):
    if not Path(a_experiment.experiment_dir).exists():
        print(f'Experiment directory, {a_experiment.experiment_dir}, does not exist.')

    all_participant_dirs = list(Path(a_experiment.experiment_dir).glob('et*/'))

    for participant_dir in all_participant_dirs:

        eartag_num = int(participant_dir.name.strip('et'))
        mouse = models.Mouse.from_db(eartag_num)

        if mouse is None:
            print(f"Mouse not in database, eartag {eartag_num}")
            continue

        mouse_details = models.ParticipantDetails.from_db(eartag_num, a_experiment.experiment_name)

        if mouse_details is None:
            print(f"Mouse participant details not in database, eartag {eartag_num}")
            continue

        if a_experiment.experiment_name == 'skilled-reaching':
            training_dir = Path(mouse_details.participant_dir).joinpath('Training')
            all_session_dirs = training_dir.glob(f'et{eartag_num}_*_*T*/')
        elif a_experiment.experiment_name == 'grooming':
            training_dir = Path(mouse_details.participant_dir)
            all_session_dirs = training_dir.glob(f'et{eartag_num}_*_*G*/')
        else:
            all_session_dirs = None
            print('Need information about training and session directories for this experiment')

        # Get all session directories for sessions in database
        session_dir_in_db = tools.get.list_all_session_dir_for_mouse(a_experiment, mouse)

        use_all_session_dirs = list(all_session_dirs)
        for session_dir in use_all_session_dirs:
            if str(session_dir) in session_dir_in_db:
                continue
            session_dir_split = str(session_dir).split('T')
            if len(session_dir_split) > 3:
                session_num = session_dir_split[-2].split('-')[0]
            else:
                session_num = session_dir_split[-1]
            session_date = int(session_dir.name.split('_')[1])
            models.Session(mouse.mouse_id, a_experiment.experiment_id, str(session_dir), session_date,
                           session_num).save_to_db()

        session_dir_in_db = tools.get.list_all_session_dir_for_mouse(a_experiment, mouse)
        for session_dir in session_dir_in_db:
            session = models.Session.from_db(session_dir=session_dir)
            print(session_dir)

            # Define folder directory patterns TODO move this to an experiments configuration
            if a_experiment.experiment_name == 'skilled-reaching':
                all_folder_dirs = list(Path(session_dir).glob('Reaches*'))
            elif a_experiment.experiment_name == 'grooming':
                print('Need information about how to input grooming experiment from data dirs')
                continue
            else:
                all_folder_dirs = None
                print('Need information about folder and trial directories for this experiment')

            # Get all folder directories for folders in database
            folder_dir_in_db = tools.get.list_all_folder_dir(experiment)

            for folder_dir in all_folder_dirs:
                if folder_dir in folder_dir_in_db:
                    continue
                models.Folder(session.session_id, str(folder_dir)).save_to_db()

            for folder_dir in all_folder_dirs:
                folder = models.Folder.from_db(folder_dir=str(folder_dir))

                # Define trial directory patterns TODO same as session directory patterns
                all_trial_dirs = list(folder_dir.glob('*R*.mp4'))

                # TODO I don't think this will work for the grooming trials, so I need to build something in.
                # Related to previous to-do in doc
                if len(list(all_trial_dirs)) == 0:
                    all_trial_dirs = list(folder_dir.glob('*G*.MP4'))

                # Get all trial directories for trials in database
                trial_dir_in_db = tools.get.list_all_trial_dir(experiment)
                for trial_dir in all_trial_dirs:
                    if str(trial_dir) in trial_dir_in_db:
                        continue
                    models.Trial(experiment.experiment_id,
                                 folder.folder_id,
                                 str(trial_dir),
                                 session.session_date).save_to_db()


def update_from_data_dirs(db_details, main_user):
    with tools.Cursor() as cursor:
        all_experiment_names = tools.list_all_experiment_names(cursor)

    for experiment_name in all_experiment_names:
        if experiment_name in ['pasta-handling', 'grooming']:
            continue
        print(f"Beginning update: {experiment_name}")
        experiment = models.Experiment.from_db(experiment_name=experiment_name)
        update_experiment_from_data_dirs(experiment)


if __name__ == '__main__':
    project_name = 'hello'
    experiment_name = 'skilled-reaching'

    initialize_database(project_name)
    experiment = models.Experiment.from_db(experiment_name=experiment_name)
    update_experiment_from_data_dirs(experiment)
