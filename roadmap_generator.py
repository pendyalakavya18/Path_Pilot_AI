from ai_engine import OllamaEngine
from rag_system import RAGSystem
from knowledge_base import get_learning_resources

class RoadmapGenerator:
    def __init__(self):
        self.ai_engine = OllamaEngine()
        self.rag_system = RAGSystem()
    
    def create_roadmap(self, role, company, weeks, current_skills=None):
        roadmap = self.ai_engine.generate_roadmap(role, company, weeks, current_skills)
        
        if 'weekly_plan' in roadmap:
            for week in roadmap['weekly_plan']:
                week['resources'] = []
                for topic in week.get('topics', []):
                    resources = self.rag_system.get_resources_for_skill(topic, top_k=2)
                    week['resources'].extend(resources)
        
        return roadmap
    
    def get_weekly_details(self, roadmap, week_number):
        if 'weekly_plan' not in roadmap:
            return None
        
        weekly_plan = roadmap['weekly_plan']
        
        # Try matching by the 'week' field first
        for week in weekly_plan:
            week_val = week.get('week')
            if week_val == week_number or str(week_val) == str(week_number):
                return week
        
        # Fallback: use index (week_number is 1-indexed)
        idx = week_number - 1
        if 0 <= idx < len(weekly_plan):
            return weekly_plan[idx]
        
        return None
    
    def adapt_roadmap(self, roadmap, completed_weeks, performance_scores):
        if not performance_scores:
            return roadmap
        
        avg_score = sum(performance_scores) / len(performance_scores)
        
        remaining_weeks = roadmap.get('weekly_plan', [])[completed_weeks:]
        
        for week in remaining_weeks:
            base_hours = week.get('hours_per_day', 2)
            adjustment_factor = 1 + (1 - avg_score / 10) * 0.3
            week['hours_per_day'] = round(base_hours * adjustment_factor, 1)
        
        return roadmap
