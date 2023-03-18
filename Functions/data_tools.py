"""
    Set of functions to work with the Boccia software pilot data
"""

# Import libraries
import os
import mne
import pyxdf
import numpy as np
import pandas as pd
import scipy.signal as signal

def import_data(xdf_file:str) -> tuple[mne.io.fiff.raw.Raw, pd.DataFrame, pd.DataFrame]:
    """
        Imports xdf file and returns the EEG stream, Python response, and Unity stream

        Parameters
        ----------
            xdf_file: str

        Returns
        -------
            eeg_mne: mne.io.fiff.raw.RAW
                EEG data in an MNE format
            python_stream: pd.DataFrame
                DataFrame with the stream of events sent from the BCI-essentials-python backend
            unity_stream: pd.DataFrame
                DataFrame with the stream of events sent from the BCI-essentials-unity frontend        
    """

    [xdf_file, _] = pyxdf.load_xdf(xdf_file)

    # First, determine first sample that needs to be subtracted from all streams
    for i in range(len(xdf_file)):
        stream_name = xdf_file[i]["info"]["name"][0]
        if (stream_name == "DSI24") | (stream_name == "DSI7"):
            first_sample = float(xdf_file[i]["footer"]["info"]["first_timestamp"][0])

    # Second, separate all streams and save data
    for i in range(len(xdf_file)):
        stream_name = xdf_file[i]["info"]["name"][0]

        # Data stream
        if (stream_name == "DSI24") | (stream_name == "DSI7"):
            eeg_np = xdf_file[i]["time_series"].T
            srate = float(xdf_file[i]["info"]["nominal_srate"][0])
            n_chans = len(xdf_file[i]['info']['desc'][0]['channels'][0]['channel'])
            ch_names = [xdf_file[i]['info']['desc'][0]['channels'][0]['channel'][c]['label'][0] for c in range(n_chans)]
            ch_types = "eeg"
            
            # Drop trigger channel
            eeg_np = eeg_np[:-1, :]
            ch_names = ch_names[:-1]
                        
            # Create MNE object
            info = mne.create_info(ch_names, srate, ch_types)
            eeg_mne = mne.io.RawArray(eeg_np, info)

        # Unity stream
        if (stream_name == "PythonResponse"):
            python_series = xdf_file[i]["time_series"]
            python_time_stamps = xdf_file[i]["time_stamps"]

            dict_python = {
                "Time stamps": np.array(python_time_stamps) - first_sample,
                "Signal value": np.zeros(len(python_time_stamps)),
                "Event": [event[0] for event in python_series]
                }
            
            python_stream = pd.DataFrame(dict_python)            

        # Unity events
        if (stream_name == "UnityEvents"):
            unity_series = xdf_file[i]["time_series"]
            unity_time_stamps = xdf_file[i]["time_stamps"]

            dict_unity = {
                "Time stamps": np.array(unity_time_stamps) - first_sample,
                "Signal value": np.zeros(len(unity_time_stamps)),
                "Event": [event[0] for event in unity_series]
            }

            unity_stream = pd.DataFrame(dict_unity)
    
    return (eeg_mne, python_stream, unity_stream)