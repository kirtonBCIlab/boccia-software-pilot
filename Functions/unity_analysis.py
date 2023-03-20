""" 
    Set of funcitons to do the analysis on the Unity stream markers
"""

# Import libraries
import numpy as np
import pandas as pd

def total_metrics(unity_stream:list[pd.DataFrame]) -> list:
    """
        Returns the total correct and incorrect selections found in the `unity_stream`

        Parameters
        ----------
            unity_stream: list[pd.DataFrame]
                Unity streams to evaluate, must contain columns for `[Time stamps, Signal value, Event]`
            
        Returns
        -------
            total_selections: np.ndarray
                List with `len(subjects)` where each value has and array with the `[pipeline, [correct, incorrect]]` selections
    """
    # Preallocate and initiate variables
    total_selections = [None] * len(unity_stream)

    for s, stream in enumerate(unity_stream):
        str_events = [event.split(',')[0] for event in stream["Event"].tolist()]

        # Look the index of the last "Starting experiment" str found. In case experiment was started
        # multiple times in the same recording
        experiment_start = [1 if "Starting Experiment" in event else 0 for event in str_events]

        # Determine number of pipelines in stream        
        n_pipelines = np.sum([1 if (event==1) and (experiment_start[i+1]) else 0 for (i,event) in enumerate(experiment_start)])
        pipeline = -1                                   # Initialize pipeline index
        total_selections[s] = np.zeros((n_pipelines, 2))  # Initialize array for [pipeline, [correct, incorrectz]]

        for (i,val) in enumerate(experiment_start):
            # If the experiment start index is the one selected
            if (val==1) and (experiment_start[i+1]==0):
                pipeline += 1
            # If experiment has started, consecutive 0's will be inside one run
            elif (val == 0):
                if ("41" in str_events[i]) and not ("1041" in str_events[i]): total_selections[s][pipeline, 0] += 1
                elif "42" in str_events[i]: total_selections[s][pipeline, 1] += 1    

    return total_selections

def itr(unity_stream:list[pd.DataFrame]):
    # Missing information transfer rate implementation
    a = 0
    
