from bids.layout import BIDSLayout
import pandas as pd
import numpy as np
import os

__all__ = ['get_timing','bunch_timing' ]
__author__ = ["Shawn Rhoads"]

class events_class(object):

    def __init__(self, base_dir, task_id, sub_ids=None, verbose=True):
        assert type(base_dir) == str, "base_dir should be type(str)"
        assert type(task_id) == str, "task_id should be type(str)"


        self.base_dir = base_dir
        self.layout = BIDSLayout(base_dir)
        self.task_id = task_id

        if sub_ids == None:
            self.sub_ids = self.layout.get_subjects(task=task_id)
        else:
            assert type(sub_ids) == list, "sub_ids should be type(list)"
            for i in sub_ids:
                assert type(i) == str, "elements in sub_ids should be type(str)"
                assert any(i==j for j in self.layout.get_subjects(task=task_id)), f"cannot find sub_ids with {task} task data"

        if verbose:
            print(f'{len(self.sub_ids)} subjects in {self.task_id} task')

    def get_timing(self, trial_type_cols=[], trimTRby=10, software='AFNI', write=True):
        '''
        Throws timing information for each subject into dictionary
        '''
        assert (software == 'AFNI' or software == 'SPM'), "software should be AFNI or SPM"

        self.events_dict = {}

        self.events_dict[self.task_id] = {}

        for sub_identifier in self.sub_ids:

            self.events_dict[self.task_id][sub_identifier] = {}

            run_ids = self.layout.get_runs(subject=sub_identifier, task=self.task_id)

            for run_identifier in run_ids:
                __eventFile__ = self.layout.get(suffix='events',
                                                 task=self.task_id,
                                                  run=run_identifier,
                                                  extension='tsv',
                                                  return_type='file')

                # get df of events information
                __trialInfo__ = pd.read_table(__eventFile__[0])

                if run_identifier == 1:
                    onsets = {}
                    durations = {}

                if trial_type_cols == []: #if no columns for trial_types specified

                    for column in __trialInfo__.columns[2:]:

                        __conditions__ = sorted(list(set(__trialInfo__[column])))

                        # extracting onset and duration information for task, subject, run, trial_type
                        if run_identifier == 1:
                            onsets[column] = {}
                            durations[column] = {}

                        for itrial in __conditions__:
                            if run_identifier == 1:
                                onsets[column][itrial] = {}
                                durations[column][itrial] = {}
                            try:
                                onsets[column][itrial][run_identifier] = (list(__trialInfo__[__trialInfo__[column]==itrial].onset-trimTRby)) # subtracting trimTRby due to remove dummy scans
                                durations[column][itrial][run_identifier] = (list(__trialInfo__[__trialInfo__[column]==itrial].duration))
                            except KeyError:
                                onsets[column][itrial] = {}
                                durations[column][itrial] = {}

                                onsets[column][itrial][run_identifier] = (list(__trialInfo__[__trialInfo__[column]==itrial].onset-trimTRby)) # subtracting trimTRby due to remove dummy scans
                                durations[column][itrial][run_identifier] = (list(__trialInfo__[__trialInfo__[column]==itrial].duration))
                else:
                    for t1 in trial_type_cols:
                        assert any(t1==t2 for t2 in __trialInfo__.columns), f"{t1} info is not in *events.tsv"

                    for column in trial_type_cols:

                        __conditions__ = sorted(list(set(__trialInfo__[column])))

                        # extracting onset and duration information for task, subject, run, trial_type
                        if run_identifier == 1:
                            onsets[column] = {}
                            durations[column] = {}

                        for itrial in __conditions__:
                            if run_identifier == 1:
                                onsets[column][itrial] = {}
                                durations[column][itrial] = {}

                            try:
                                onsets[column][itrial][run_identifier] = (list(__trialInfo__[__trialInfo__[column]==itrial].onset-trimTRby)) # subtracting trimTRby due to remove dummy scans
                                durations[column][itrial][run_identifier] = (list(__trialInfo__[__trialInfo__[column]==itrial].duration))
                            except KeyError:
                                onsets[column][itrial] = {}
                                durations[column][itrial] = {}

                                onsets[column][itrial][run_identifier] = (list(__trialInfo__[__trialInfo__[column]==itrial].onset-trimTRby)) # subtracting trimTRby due to remove dummy scans
                                durations[column][itrial][run_identifier] = (list(__trialInfo__[__trialInfo__[column]==itrial].duration))

            self.events_dict[self.task_id][sub_identifier]['onsets'] = onsets
            self.events_dict[self.task_id][sub_identifier]['durations'] = durations

            if write == True:

                if trial_type_cols == []: #if no columns for trial_types specified

                    for column in __trialInfo__.columns[2:]:
                        if column == 'response_time': #cannot handle response_times yet
                            continue

                        writeToPath = os.path.join(self.base_dir,'derivatives','timing',f'sub-{sub_identifier}',column)

                        if not os.path.exists(writeToPath):
                            os.makedirs(writeToPath)

                        for (onset_key, onset_val), (dur_key, dur_val) in zip(onsets[column].items(), durations[column].items()):
                            assert (onset_key==dur_key), "onset conditions and duration conditions do not match!"

                            with open(f'{writeToPath}/sub-{sub_identifier}_task-{self.task_id}_timing-{onset_key}.txt', 'w') as filehandle:

                                for (run_onsets, run_durs) in zip(onset_val.values(), dur_val.values()):


                                    filehandle.writelines("%f:%f\t" % (onset_time, dur_time) for (onset_time, dur_time) in zip(run_onsets, run_durs))
                                    filehandle.write("\n")
                else:

                    for column in trial_type_cols:
                        if column == 'response_time': #cannot handle response_times yet
                            continue

                        writeToPath = os.path.join(self.base_dir,'derivatives','timing',f'sub-{sub_identifier}',column)

                        if not os.path.exists(writeToPath):
                            os.makedirs(writeToPath)

                        for (onset_key, onset_val), (dur_key, dur_val) in zip(onsets[column].items(), durations[column].items()):
                            assert (onset_key==dur_key), "onset conditions and duration conditions do not match!"

                            with open(f'{writeToPath}/sub-{sub_identifier}_task-{self.task_id}_timing-{onset_key}.txt', 'w') as filehandle:

                                for (run_onsets, run_durs) in zip(onset_val.values(), dur_val.values()):

                                    filehandle.writelines("%f:%f\t" % (onset_time, dur_time) for (onset_time, dur_time) in zip(run_onsets, run_durs))
                                    filehandle.write("\n")

    # def bunch_timing(self, trial_type):
        
    #     subject_info = {}

    #     for sub_id in self.events_dict[self.task_id].keys(): #loop over subjects
    #         subject_info[sub_id] = {}

    #         conditions = [i for i in self.events_dict[self.task_id][sub_id]['onsets'][trial_type].keys()]

    #         for cond in conditions:
    #             onsets = [i for i in self.events_dict[self.task_id][sub_id]['onsets'][trial_type][cond].values()]
    #             durations = [i for i in self.events_dict[self.task_id][sub_id]['durations'][trial_type][cond].values()]

    #             subject_info[sub_id][trial_type] = [Bunch(conditions=conditions,
    #                                                       onsets=onsets,
    #                                                       durations=durations)]
    #     return subject_info
