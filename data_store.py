import json
import os
from datetime import datetime

class DataStore:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.users_file = os.path.join(data_dir, 'users.json')
        self.roadmaps_file = os.path.join(data_dir, 'roadmaps.json')
        self.tests_file = os.path.join(data_dir, 'tests.json')
        self.interviews_file = os.path.join(data_dir, 'interviews.json')
        self.progress_file = os.path.join(data_dir, 'progress.json')
        
        self._init_files()
    
    def _init_files(self):
        for file_path in [self.users_file, self.roadmaps_file, self.tests_file, 
                          self.interviews_file, self.progress_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump({}, f)
    
    def _read_file(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def _write_file(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def save_user(self, user_id, user_data):
        users = self._read_file(self.users_file)
        users[user_id] = user_data
        users[user_id]['updated_at'] = datetime.now().isoformat()
        self._write_file(self.users_file, users)
    
    def get_user(self, user_id):
        users = self._read_file(self.users_file)
        return users.get(user_id)
    
    def save_roadmap(self, user_id, roadmap_data):
        roadmaps = self._read_file(self.roadmaps_file)
        roadmaps[user_id] = roadmap_data
        roadmaps[user_id]['created_at'] = datetime.now().isoformat()
        self._write_file(self.roadmaps_file, roadmaps)
    
    def get_roadmap(self, user_id):
        roadmaps = self._read_file(self.roadmaps_file)
        return roadmaps.get(user_id)
    
    def save_test_result(self, user_id, test_data):
        tests = self._read_file(self.tests_file)
        if user_id not in tests:
            tests[user_id] = []
        test_data['timestamp'] = datetime.now().isoformat()
        tests[user_id].append(test_data)
        self._write_file(self.tests_file, tests)
    
    def get_test_results(self, user_id):
        tests = self._read_file(self.tests_file)
        return tests.get(user_id, [])
    
    def save_interview(self, user_id, interview_data):
        interviews = self._read_file(self.interviews_file)
        if user_id not in interviews:
            interviews[user_id] = []
        interview_data['timestamp'] = datetime.now().isoformat()
        interviews[user_id].append(interview_data)
        self._write_file(self.interviews_file, interviews)
    
    def get_interviews(self, user_id):
        interviews = self._read_file(self.interviews_file)
        return interviews.get(user_id, [])
    
    def save_progress(self, user_id, progress_data):
        progress = self._read_file(self.progress_file)
        progress[user_id] = progress_data
        progress[user_id]['updated_at'] = datetime.now().isoformat()
        self._write_file(self.progress_file, progress)
    
    def get_progress(self, user_id):
        progress = self._read_file(self.progress_file)
        return progress.get(user_id, {})
