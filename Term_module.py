# 10월_ 엑셀파일 전부 합치기

import pandas as pd
import os

class Intergration :
    def __init__(self,folder_path): 
        self.folder_path = folder_path
        self.combined_df = pd.DataFrame()
    
    def read_combine_file(self):
        
        excel_files = [f for f in os.listdir(self.folder_path) if f.endswith('.xlsx')]
        
        for file in sorted(excel_files, key=lambda x: int(x.split('.')[0])):
            file_path = os.path.join(self.folder_path, file)
            df = pd.read_excel(file_path, engine='openpyxl')
            file_number = int(file.split('.')[0])
            df['10월'] = file_number
            self.combined_df = pd.concat([self.combined_df, df], ignore_index=True)
        
        cols = ['10월'] + [col for col in self.combined_df if col != '10월']
        self.combined_df = self.combined_df[cols]
    
    def save_combined_file(self, save_path):
        self.combined_df.to_excel(save_path, index = False)
        return self.combined_df

# 10월 상행 하행 영동선(서창JC~신갈JC)구간만 포함하기 

class Post_Process :
    def __init__ (self, relative_file_path):
        self.relative_file_path = relative_file_path
        self.UpDownWard_file = pd.DataFrame()
    
    def delete_row(self, start, end) :
        UpDownWard = pd.read_excel(self.relative_file_path, engine= 'openpyxl')
        
        for day in range(1,32):
            day_df = UpDownWard[UpDownWard['10월'] == day].iloc[start:end]
            self.UpDownWard_file = pd.concat([self.UpDownWard_file,day_df])
    
    def delete_col(self) :
        self.UpDownWard_file = self.UpDownWard_file.drop(columns = ['연장'])

    def save_processed_file(self, save_path) :
        self.UpDownWard_file.to_excel(save_path, index= False)
        return self.UpDownWard_file

# <확인점1,2> 상행 하행 가장 차 막히는 구간 찾기

class Section :
    def __init__(self, file_path):
        self.file_path = file_path
        self.sections = []
        self.df = pd.DataFrame()
        self.sections_df = pd.DataFrame()
    
    def get_avgSpeed(self) :
        self.df = pd.read_excel(self.file_path)
        self.df['평균속도'] = self.df.mean(axis=1, numeric_only= True)
    def get_day_min_avgspeed_section(self) :
        for day in range(1, 32):
            day_section = self.df.loc[self.df['10월'] == day]
            day_min_Avg = day_section.loc[day_section['평균속도'].idxmin()]
            section = day_min_Avg['구간']
            self.sections.append(section)
        self.sections_df = pd.DataFrame({
        '10월': range(1, 32),  
        '가장 막힌 구간': self.sections  
        })
    def find_most_frequent_section(self):
        most_frequent_section = self.sections_df['가장 막힌 구간'].value_counts().idxmax()
        return most_frequent_section
    def save_day_confused_file(self, save_path):
        self.sections_df.to_excel(save_path)

# <확인점3,4> 상행 하행 가장 차가 막히는 시간대 찾기

class Time :
    def __init__(self, file_path):
        self.file_path = file_path
        self.time_means = []
        self.df_time_means = pd.DataFrame()
        self.Min_AvgSpeed = None
    
    def get_avgspeed(self):
        df = pd.read_excel(self.file_path)
        time = df.iloc[:,2:27]
        self.time_means = time.mean()
        return self.time_means

    def get_day_min_avgspeed_time(self):
        self.df_time_means = pd.DataFrame(self.time_means).reset_index()
        self.df_time_means.columns = ['시간', '평균속도']
        self.Min_AvgSpeed = self.df_time_means['평균속도'].min()
        return self.Min_AvgSpeed

    def find_buisiest_time(self):
        Busiest_time = self.df_time_means[self.df_time_means['평균속도'] == self.Min_AvgSpeed]['시간'].iloc[0]
        return Busiest_time

    def save_confused_time_file(self, save_path):
        self.df_time_means.to_excel(save_path)
        return self.df_time_means

# <명제1,2,3> 하행 출근시간대(06-09)는 월요일, 
# 상행 퇴근시간대(16-19)는 금요일이 가장 차가 막힐 것이다.

class Busyday :
    def __init__(self,file_path):
        self.file_path = file_path
        self.df = pd.read_excel(self.file_path)
        self.df_day_means = pd.DataFrame()
        self.day_means = {}
        self.day_dates_dict = {
        "Monday": [7, 14, 21, 28],
        "Tuesday": [1, 8, 15, 22, 29],
        "Wednesday": [2, 9, 16, 23, 30],
        "Thursday": [3, 10, 17, 24, 31],
        "Friday": [4, 11, 18, 25],
        "Saturday": [5, 12, 19, 26],
        "Sunday": [6, 13, 20, 27]
        }
        self.weekend_dates = [5,6,12,13,19,20,26,27]
        self.holiday_dates = [1,3,9]

        self.day_dates_dict2 = {
        "Weekend" : self.weekend_dates,
        "Holiday" : self.holiday_dates,
        "Weekdays" : [day for day in range(1, 32) if day not in self.weekend_dates and day not in self.holiday_dates]
        }
    
    def get_day_avgspeed (self, start, end, day_dates, day_name):
        GoWork_GoHome_Time = self.df.iloc[:, start:end]
        dates = GoWork_GoHome_Time[self.df['10월'].isin(day_dates)].copy()
        dates.loc[:, '날짜'] = self.df['10월'][self.df['10월'].isin(day_dates)]
        dates = dates[['날짜'] + [col for col in dates.columns if col != '날짜']]
        day_Mean = dates.iloc[:, 1:].mean()
        total_mean = day_Mean.mean()
        self.day_means[day_name] = total_mean
        return self.day_means

    def combine_day_avgspeed(self):
        self.df_day_means = pd.DataFrame(
        {"요일": list(self.day_means.keys()), "평균속도": list(self.day_means.values())}
        )
    
    def save_confused_GoWork_GoHome_Time(self, save_path):
        self.df_day_means.to_excel(save_path)
        return self.df_day_means