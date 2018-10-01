# -*- coding: utf-8 -*-
import argparse
import datetime
import json
import os
import sys
import time

from check_changes_utils import check_changes
from json_utils import write_json_data

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj

class DirecoryChecker:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument ('version', nargs='?')

        if sys.version_info.major == 3:
            self.python_version = 3
        elif sys.version_info.major == 2:
            reload(sys)
            sys.setdefaultencoding('utf8')
            self.python_version = 2
        
        if self.parser.parse_args(sys.argv[1:]).version == 'old' and self.python_version == 3:
            print('Use python v2')
            sys.exit(0)
        
        self._base_log_file_name = 'file_checker_base.json'
        self._base_dir = os.path.dirname(os.path.abspath(__file__))
        self._base_log_file_path = os.path.join(self._base_dir, self._base_log_file_name)

        self.get_or_create_base_log_file()

    def get_directory_path(self):
        message = 'Enter Directory path: '
        if self.python_version == 2:
            dir_path = raw_input(message)
        else:
            dir_path = input(message)
        if os.path.isdir(dir_path):
            return dir_path
        else:
            if dir_path.lower() == 'q':
                sys.exit(0)
            print('\n --- Wrong Directory path ---')
            print(' -- Enter correct path or enter q for exit--- \n')

    def get_files_from_directory(self, directory):
        files = os.listdir(directory)
        sorted_object_in_directory = {'files': [], 'subfolders': []}

        for file in files:
            file_path = os.path.join(directory, file)
            file_change_date = time.ctime(os.path.getmtime(file_path))
            if os.path.isfile(os.path.join(directory, file)):
                sorted_object_in_directory['files'].append({
                        'file_name': file,
                        'initial_date': file_change_date
                    })
            else:
                sorted_object_in_directory['subfolders'].append({
                        'folder_name': file,
                        'initial_date': file_change_date
                    })
        return sorted_object_in_directory
    
    def get_or_create_base_log_file(self):
        if os.path.isfile(self._base_log_file_path):
            message = 'Base Log file allready exist'
            print(message)
            print('-'*len(message))
        else:
            initial_data = { 'files_log': {} }
            write_json_data(self._base_log_file_path, initial_data)
            print('Json Log file was created')

    def check_dir_initial_recod(self, dir_path):
        with open(self._base_log_file_path, 'r') as f:
            log_data = json.load(f)
        return log_data.get('files_log').get(dir_path, None)

    def create_initial_records(self, dir_path):     
        with open(self._base_log_file_path, 'r') as f:
            log_data = json.load(f)
            date = datetime.datetime.now()
            files_and_folders = self.get_files_from_directory(dir_path)
            files = files_and_folders.get('files')
            subfolders = files_and_folders.get('subfolders')

            log_data.get('files_log').update({
                dir_path: {
                    'initial_state': {
                        'path': dir_path,
                        'date': date,
                        'files': files,
                        'subfolders': subfolders,
                    },
                    'actual_state': {
                        'date': date,
                        'files': files,
                        'subfolders': subfolders,
                    },
                    'history': []
                }
            })

        write_json_data(self._base_log_file_path, log_data, default_param=date_handler)
        print('Json Log file with initial record was created')

    def update_log_file(self, dir_log_data, dir_path):
        date = datetime.datetime.now()
        
        feed_data = dir_log_data.get('actual_state')              
        new_data = self.get_files_from_directory(dir_path)

        changed_data = check_changes(feed_data, new_data)
        if changed_data is not None:
            actual_state = {
                    'date': date,
                    'files': changed_data.get('files', None),
                    'subfolders': changed_data.get('subfolders', None),
                }
            action_story = {
                        'check_data': date,
                        'added': changed_data.get('added', None),
                        'deleted': changed_data.get('deleted', None)
                }

            with open(self._base_log_file_path, 'r') as f:
                log_data = json.load(f)

            log_data_history = log_data.get('files_log').get(dir_path).get('history')
            if log_data_history is not None:
                log_data_history.append(action_story)
                log_data.get('files_log').get(dir_path)['actual_state'] = actual_state
                write_json_data(self._base_log_file_path, log_data, default_param=date_handler)

            print('Log file was updated')
        else:
            print('No changes in this directory')


    def _get_history(self, feed_data):
        history = feed_data.get('history')
        if history:
            return history

    def run_checker(self):
        while True:
            dir_path = self.get_directory_path()
            if dir_path:
                break
        dir_log_data = self.check_dir_initial_recod(dir_path)
        if dir_log_data is None:
            self.create_initial_records(dir_path)
        else:
            self.update_log_file(dir_log_data, dir_path)

def main():
    dir_checker = DirecoryChecker()
    dir_checker.run_checker()

if __name__ == '__main__':
    main()
        