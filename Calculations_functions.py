import numpy as np
import yaml

def check_crossing(file_path,vector=any):
    """Check if the vector crosses a threshold within a specified time window."""
    cfg_dic = read_yaml_file(file_path)
    rms_vector = np.sqrt(np.mean(vector**2))
    threshold = rms_vector * cfg_dic['calculations']['threshold_scaling']
    stimulation_time = cfg_dic['stim_cfg']['time_before']
    time_window = [cfg_dic['time_window_settings']['start_time']+stimulation_time,cfg_dic['time_window_settings']['end_time']+stimulation_time]
    # crossing_events = np.where((vector[:1] < threshold) & (vector[1:] >= threshold))[0] + 1
    crossing_points = np.where((vector[:-1] < threshold) & (vector[1:] >= threshold))[0] + 1
    time_window_samples = np.array(time_window) * 30000
    time_window_samples = time_window_samples.astype(int)
    time_window_samples = np.linspace(time_window_samples[0], time_window_samples[1], time_window_samples[1] - time_window_samples[0]).astype(int)
    return np.intersect1d(crossing_points, time_window_samples).any()   


def read_yaml_file(file_path):
    """Read the contents of a yaml file."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data
    
