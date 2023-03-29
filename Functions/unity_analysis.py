""" 
    Set of funcitons to do the analysis on the Unity stream markers
"""

# Import libraries
import numpy as np
import pandas as pd

def total_metrics(unity_stream):
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
        str_events = stream["Event"].to_list()
        events_code = [event.split(',')[0] for event in stream["Event"].tolist()]

        # Look the index of the last "Starting experiment" str found. In case experiment was started
        # multiple times in the same recording
        experiment_start = [1 if "Starting Experiment" in event else 0 for event in events_code]

        # Determine number of pipelines in stream        
        n_pipelines = np.sum([1 if (event==1) and not (experiment_start[i+1]) else 0 for (i,event) in enumerate(experiment_start[:-1])])
        pipeline = -1                                   # Initialize pipeline index
        total_selections[s] = np.zeros((n_pipelines, 2))  # Initialize array for [pipeline, [correct, incorrect]]

        for (i,val) in enumerate(experiment_start[:-1]):
            # If the experiment start index is the one selected
            if (val==1) and (experiment_start[i+1]==0):
                pipeline += 1
            # If experiment has started, consecutive 0's will be inside one run
            elif (val == 0):
                # Check if the time stamp of the current and previous event are the same
                if (str_events[i].split(" ")[-1] == str_events[i-1].split(" ")[-1]):
                        continue
                else:
                    if ("41" in events_code[i]) and not ("1041" in events_code[i]): total_selections[s][pipeline, 0] += 1
                    elif "42" in events_code[i]: total_selections[s][pipeline, 1] += 1    

        ## Implement
        # - Change the code above for
        # -- For loop that trims the experiment to the indices of a single pipeline
        # -- Call the "count_events" function to return right and wrong answers

    return total_selections

def ball_dropped(unity_stream):
    """
    """
    # Missing implementation
    # - Similar to total_metrics, but just look for the 1041, when they drop the ball
    # - Return a list of len(nsubjects) with each item being an np.array of len(npipelines)

    return None

def count_events(event_list, event, not_event=None):
    """ Returns the number of times that a certain event is found

        Parameters
        ----------
            events_list: list[str]
                List of events to look into
            event: str
                Event to count
            not_event: str
                If different from `None`, do not consider this types of events
        
        Returns
        -------
            event_count: int
                Number of times the event was found
    """
    event_count = 0
    for val in event_list:
        if (not_event != None):
            if(event in val) and not (not_event in val):
                event_count += 1
        else: 
            if (event in val):
                event_count += 1
    
    return event_count  

def itr(unity_stream):
    # Missing information transfer rate implementation
    a = 0
    
