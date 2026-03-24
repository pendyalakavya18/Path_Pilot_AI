from datetime import datetime

class ProgressTracker:
    def __init__(self):
        pass
    
    def calculate_progress(self, roadmap, completed_modules):
        if not roadmap or 'weekly_plan' not in roadmap:
            return {
                'progress_percentage': 0,
                'completed_weeks': 0,
                'total_weeks': 0
            }
        
        total_weeks = len(roadmap['weekly_plan'])
        completed_weeks = len(completed_modules)
        
        progress_percentage = (completed_weeks / total_weeks * 100) if total_weeks > 0 else 0
        
        return {
            'progress_percentage': round(progress_percentage, 2),
            'completed_weeks': completed_weeks,
            'total_weeks': total_weeks,
            'remaining_weeks': total_weeks - completed_weeks
        }
    
    def track_test_performance(self, test_results):
        if not test_results:
            return {
                'average_score': 0,
                'total_tests': 0,
                'improvement_rate': 0
            }
        
        total_score = sum(test.get('score', 0) for test in test_results)
        avg_score = total_score / len(test_results)
        
        improvement_rate = 0
        if len(test_results) >= 2:
            recent_scores = [test.get('score', 0) for test in test_results[-3:]]
            older_scores = [test.get('score', 0) for test in test_results[:-3]] if len(test_results) > 3 else [test_results[0].get('score', 0)]
            
            recent_avg = sum(recent_scores) / len(recent_scores)
            older_avg = sum(older_scores) / len(older_scores)
            
            improvement_rate = recent_avg - older_avg
        
        return {
            'average_score': round(avg_score, 2),
            'total_tests': len(test_results),
            'improvement_rate': round(improvement_rate, 2),
            'latest_score': test_results[-1].get('score', 0) if test_results else 0
        }
    
    def track_interview_performance(self, interview_results):
        if not interview_results:
            return {
                'average_score': 0,
                'total_interviews': 0,
                'improvement_rate': 0
            }
        
        scores = []
        for interview in interview_results:
            if 'evaluations' in interview:
                avg_score = sum(e.get('overall_score', 0) for e in interview['evaluations']) / len(interview['evaluations']) if interview['evaluations'] else 0
                scores.append(avg_score)
        
        if not scores:
            return {
                'average_score': 0,
                'total_interviews': 0,
                'improvement_rate': 0
            }
        
        avg_score = sum(scores) / len(scores)
        
        improvement_rate = 0
        if len(scores) >= 2:
            improvement_rate = (scores[-1] - scores[0]) / len(scores)
        
        return {
            'average_score': round(avg_score, 2),
            'total_interviews': len(interview_results),
            'improvement_rate': round(improvement_rate, 2),
            'latest_score': scores[-1] if scores else 0
        }
    
    def calculate_overall_readiness(self, progress_data, test_performance, interview_performance):
        progress_score = progress_data.get('progress_percentage', 0) / 100 * 10
        test_score = test_performance.get('average_score', 0) / 10
        interview_score = interview_performance.get('average_score', 0)
        
        readiness_score = (progress_score * 0.3 + test_score * 0.3 + interview_score * 0.4)
        
        readiness_level = 'Not Ready'
        if readiness_score >= 8:
            readiness_level = 'Highly Ready'
        elif readiness_score >= 6:
            readiness_level = 'Ready'
        elif readiness_score >= 4:
            readiness_level = 'Moderately Ready'
        
        return {
            'readiness_score': round(readiness_score, 2),
            'readiness_level': readiness_level,
            'breakdown': {
                'progress': round(progress_score, 2),
                'tests': round(test_score, 2),
                'interviews': round(interview_score, 2)
            }
        }
    
    def get_learning_time_adjustment(self, performance_score, base_time=2):
        adjustment_factor = 1 + (1 - performance_score / 10) * 0.3
        adjusted_time = base_time * adjustment_factor
        return round(adjusted_time, 1)
