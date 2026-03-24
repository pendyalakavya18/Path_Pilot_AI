import json
import os
from datetime import datetime

class DataStore:
    """
    Production data store that supports both file-based and in-memory storage.
    - For local development: uses file-based storage (data/ folder)
    - For production (Render): uses in-memory storage with session-based user IDs
    """
    
    def __init__(self, store_type='file', data_dir='data'):
        self.store_type = store_type
        self.data_dir = data_dir
        
        if store_type == 'file':
            os.makedirs(data_dir, exist_ok=True)
            self.users_file = os.path.join(data_dir, 'users.json')
            self.roadmaps_file = os.path.join(data_dir, 'roadmaps.json')
            self.tests_file = os.path.join(data_dir, 'tests.json')
            self.interviews_file = os.path.join(data_dir, 'interviews.json')
            self.progress_file = os.path.join(data_dir, 'progress.json')
            self._init_files()
        else:
            # In-memory storage for production
            self.users = {}
            self.roadmaps = {}
            self.tests = {}
            self.interviews = {}
            self.progress = {}
    
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
    
    # --- User Methods ---
    
    def save_user(self, user_id, user_data):
        if self.store_type == 'file':
            users = self._read_file(self.users_file)
            users[user_id] = user_data
            users[user_id]['updated_at'] = datetime.now().isoformat()
            self._write_file(self.users_file, users)
        else:
            self.users[user_id] = user_data
            self.users[user_id]['updated_at'] = datetime.now().isoformat()
    
    def get_user(self, user_id):
        if self.store_type == 'file':
            users = self._read_file(self.users_file)
            return users.get(user_id)
        else:
            return self.users.get(user_id)
    
    # --- Roadmap Methods ---
    
    def save_roadmap(self, user_id, roadmap_data):
        if self.store_type == 'file':
            roadmaps = self._read_file(self.roadmaps_file)
            roadmaps[user_id] = roadmap_data
            roadmaps[user_id]['created_at'] = datetime.now().isoformat()
            self._write_file(self.roadmaps_file, roadmaps)
        else:
            self.roadmaps[user_id] = roadmap_data
            self.roadmaps[user_id]['created_at'] = datetime.now().isoformat()
    
    def get_roadmap(self, user_id):
        if self.store_type == 'file':
            roadmaps = self._read_file(self.roadmaps_file)
            return roadmaps.get(user_id)
        else:
            return self.roadmaps.get(user_id)
    
    # --- Test Results Methods ---
    
    def save_test_result(self, user_id, test_data):
        if self.store_type == 'file':
            tests = self._read_file(self.tests_file)
            if user_id not in tests:
                tests[user_id] = []
            test_data['timestamp'] = datetime.now().isoformat()
            tests[user_id].append(test_data)
            self._write_file(self.tests_file, tests)
        else:
            if user_id not in self.tests:
                self.tests[user_id] = []
            test_data['timestamp'] = datetime.now().isoformat()
            self.tests[user_id].append(test_data)
    
    def get_test_results(self, user_id):
        if self.store_type == 'file':
            tests = self._read_file(self.tests_file)
            return tests.get(user_id, [])
        else:
            return self.tests.get(user_id, [])
    
    # --- Interview Methods ---
    
    def save_interview(self, user_id, interview_data):
        if self.store_type == 'file':
            interviews = self._read_file(self.interviews_file)
            if user_id not in interviews:
                interviews[user_id] = []
            interview_data['timestamp'] = datetime.now().isoformat()
            interviews[user_id].append(interview_data)
            self._write_file(self.interviews_file, interviews)
        else:
            if user_id not in self.interviews:
                self.interviews[user_id] = []
            interview_data['timestamp'] = datetime.now().isoformat()
            self.interviews[user_id].append(interview_data)
    
    def get_interviews(self, user_id):
        if self.store_type == 'file':
            interviews = self._read_file(self.interviews_file)
            return interviews.get(user_id, [])
        else:
            return self.interviews.get(user_id, [])
    
    # --- Progress Methods ---
    
    def save_progress(self, user_id, progress_data):
        if self.store_type == 'file':
            progress = self._read_file(self.progress_file)
            progress[user_id] = progress_data
            progress[user_id]['updated_at'] = datetime.now().isoformat()
            self._write_file(self.progress_file, progress)
        else:
            self.progress[user_id] = progress_data
            self.progress[user_id]['updated_at'] = datetime.now().isoformat()
    
    def get_progress(self, user_id):
        if self.store_type == 'file':
            progress = self._read_file(self.progress_file)
            return progress.get(user_id, {})
        else:
            return self.progress.get(user_id, {})

