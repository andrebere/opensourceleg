import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.io import loadmat
from scipy.interpolate import interp1d


class ThermalTest:
    def __init__(self, trial, current_step_val, date, unit, fahrenheit_flag, interp_T):
        self.trial = trial
        self.current_step_val = current_step_val
        self.date = date
        self.unit = unit
        self.fahrenheit_flag = fahrenheit_flag
        self.interp_T = interp_T
        # we wanna -----
        self.T_active_csv = f"{self.trial}_{self.date}_{self.unit}__active.csv"
        self.T_inactive_csv = f"{self.trial}_{self.date}_{self.unit}__inactive.csv"
        self.T_frame_csv = None  # Example leaves this blank
        self.V_mat = f"{self.trial}_{self.date}.mat"

        # From the TM sw update we get a matrix 

    def compile_data(self):
        """
        this is needed only for the old logs. Now TC gave us a sw updates where we can get an nxm matrix where n are the numbers of points saved and m corresponds t:
        time siries, averaged Temp first point interest, averaged Temp second point interest, etc...
        """
        """
        temp = {}
        temp_lengths = []

        if self.T_active_csv:
            temp['active'] = self.format_ROIdata(self.T_active_csv)
            temp_lengths.append(len(temp['active']))

        if self.T_inactive_csv:
            temp['inactive'] = self.format_ROIdata(self.T_inactive_csv)
            temp_lengths.append(len(temp['inactive']))

        if self.T_frame_csv:
            temp['frame'] = self.format_ROIdata(self.T_frame_csv)
            temp_lengths.append(len(temp['frame']))

        if len(temp_lengths) > 1 and np.ptp(temp_lengths) != 0:
            raise ValueError("Temperature vectors must be of the same length")
        print('DAQ')
        # this file is missing, but it was used to extrapolated the time
        DAQ = loadmat(self.V_mat)['data']
        volt_label = DAQ.dtype.names[0]

        temp_fns = list(temp.keys())

        plt.figure()
        for fn in temp_fns:
            plt.plot(temp[fn], label=fn)
        plt.xlabel('Index')
        plt.ylabel('Temperature (°C)')
        plt.grid(True)
        plt.show()

        temp_idx_on, temp_idx_off = self.pick_bounds()

        plt.figure()
        plt.plot(DAQ['Time'].ravel(), DAQ[volt_label].ravel())
        plt.xlabel('Time (sec)')
        plt.ylabel('Voltage (V)')
        plt.grid(True)
        plt.show()

        DAQ_t_on, DAQ_t_off = self.pick_bounds()

        DAQ_t = DAQ['Time'].ravel()
        voltage_on_idcs = (DAQ_t >= DAQ_t_on) & (DAQ_t <= DAQ_t_off)
        voltage_on = DAQ[volt_label].ravel()[voltage_on_idcs]
        t_DAQ_on = DAQ_t[voltage_on_idcs]
        t_DAQ_on -= t_DAQ_on[0]

        T_temp = t_DAQ_on[-1] / (temp_idx_off - temp_idx_on + 1)

        temp_start = []
        for fn in temp_fns:
            temp_start.append(np.mean(temp[fn][:temp_idx_on]))
            temp[fn] = temp[fn][temp_idx_on:]
            if fn == temp_fns[0]:
                temp['t'] = np.arange(len(temp[fn])) * T_temp

        data = {
            'ambient': np.mean(temp_start),
            't': np.arange(0, temp['t'][-1], self.interp_T),
        }

        interp_method = 'pchip'
        for fn in temp_fns:
            f = interp1d(temp['t'], temp[fn], kind=interp_method)
            data[fn] = f(data['t'])

        f_voltage = interp1d(t_DAQ_on, voltage_on, kind=interp_method, fill_value=0, bounds_error=False)
        data['voltage'] = f_voltage(data['t'])
        data['resistance'] = data['voltage'] / self.current_step_val
        data['q'] = data['voltage'] * self.current_step_val

        return data
    """
        df = pd.read_csv(file_path)
        min_length = min([len(df[col]) for col in df.columns])
        df_cropped = df.iloc[:min_length]
        #print(df_cropped)
        return df_cropped

    def pick_bounds(self):
        input('Scale plot to start of rise. Press Enter to continue...')
        print('Select on point:')
        x_on = plt.ginput(1)[0][0]
        print(f"Time On: {x_on}")

        input('Scale plot to start of fall. Press Enter to continue...')
        print('Select off point:')
        y_off = plt.ginput(1)[0][0]
        print(f"Time Off: {y_off}")

        return round(x_on), round(y_off)

    def format_ROIdata(self, filename):
        rawdata = np.loadtxt(filename, delimiter=',')
        if self.fahrenheit_flag:
            rawdata = (rawdata - 32) * 5 / 9
        data_mat = rawdata.reshape(-1, 5, 5).mean(axis=(1, 2))
        return data_mat
    

    def normalize_time(self, data):
        """
        Normalize time column to milliseconds relative to the first timestamp.

        Parameters:
            data (pd.DataFrame): A DataFrame with a "Time" column in string format.

        Returns:
            pd.Series: A Series of time values normalized to milliseconds.
        """
        # Convert "Time" column to datetime with milliseconds
        data["Time"] = pd.to_datetime(data["Time"], format="%Y-%m-%d %H:%M:%S:%f")
        
        # Calculate the difference in time relative to the first timestamp
        time_deltas = data["Time"] - data["Time"].iloc[0]
        
        # Convert to milliseconds and return as a Series
        return time_deltas.dt.total_seconds() * 1000


#folder_path = r'C:\Users\bere2\OneDrive - Fondazione Istituto Italiano Tecnologia\Rehab\Umich\Benchmarking\postprocessing'
folder_path = r'C:\\Users\bere2\OneDrive - Fondazione Istituto Italiano Tecnologia\Rehab\Umich\\Matlab\\Thermal Skip\\Baseline Riley'
#trial = "\\skip_motorside_5A"
trial = '\\andrea_test.csv'

file_path = folder_path + trial
current_step_val = 5  # A
date = "20240313"
unit = "C"
F_flag = 0
interp_T = 0.01

thermal_test = ThermalTest(file_path, current_step_val, date, unit, F_flag, interp_T)
data = thermal_test.compile_data()

# extrapolate time
#print(data["Time"])
data["NormalizedTime"] = thermal_test.normalize_time(data)
print(data)