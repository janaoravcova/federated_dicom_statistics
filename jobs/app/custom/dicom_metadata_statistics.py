import argparse
import os
from typing import Dict, List

from nvflare.apis.fl_context import FLContext
from nvflare.app_common.abstract.statistics_spec import Statistics, Histogram, Feature
import pandas as pd
import pydicom
from dicom_tag import DicomTag
from pathlib import Path

class DicomMetadataStatistics(Statistics):

    def __init__(self, data_dir="D:\dfslocal\ChestAI_USB2967"):
        super().__init__()
        self.data_dir = data_dir
        self.data = []

    def initialize(self, fl_ctx: FLContext = None):
        self.data = self.load_distinct_patients(fl_ctx)
        print(self.data)

    def load_distinct_patients(self, fl_ctx: FLContext = None) -> Dict[str, pd.DataFrame]:
        for file in self.get_files_in_directory():
            dicom_file = pydicom.dcmread(file, specific_tags=[DicomTag.PatientSex.value, DicomTag.StudyInstanceUID.value])
            print("Dicom file: " + file)
            print(dicom_file[DicomTag.StudyInstanceUID.value])
            matching_study_list = [d for d in self.data if
                                   d[DicomTag.StudyInstanceUID.value] == dicom_file.StudyInstanceUID]
            if len(matching_study_list) == 0:
                self.data.append(dicom_file)

    def get_files_in_directory(self):
        file_list = []
        print("Getting all files in: " + self.data_dir)
        print("Path is valid: " + str(os.path.exists(self.data_dir)))
        for dir_path, dir_names, file_names in os.walk(self.data_dir):
            for filename in file_names:
                file_list.append(os.path.join(dir_path, filename))

        return file_list

    def features(self) -> Dict[str, List[Feature]]:
        pass

    def count(self, dataset_name: str, feature_name: str) -> int:
        pass

    def sum(self, dataset_name: str, feature_name: str) -> float:
        pass

    def mean(self, dataset_name: str, feature_name: str) -> float:
        pass

    def stddev(self, dataset_name: str, feature_name: str) -> float:
        pass

    def variance_with_mean(self, dataset_name: str, feature_name: str, global_mean: float,
                           global_count: float) -> float:
        pass

    def histogram(self, dataset_name: str, feature_name: str, num_of_bins: int, global_min_value: float,
                  global_max_value: float) -> Histogram:
        pass

    def max_value(self, dataset_name: str, feature_name: str) -> float:
        pass

    def min_value(self, dataset_name: str, feature_name: str) -> float:
        pass

parser = argparse.ArgumentParser(description='Process input parameters')
parser.add_argument('--datadir', required=False, help='Path to directory with datasets'
                                                      ' (if single folder with data needs to be analyzed)')

args = parser.parse_args()
print("File      Path:", Path(__file__).absolute())
print("Directory Path:", Path().absolute())
stats = DicomMetadataStatistics(args.datadir)
stats.initialize()
