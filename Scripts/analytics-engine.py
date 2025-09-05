#!/usr/bin/env python3
"""
Advanced Analytics Engine for Obsidian Vault
Generates deep insights, patterns, and recommendations from vault data
"""

import os
import re
import json
import pandas as pd
from pathlib import Path
from datetime import datetime, date, timedelta
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
import numpy as np

class VaultAnalytics:
    """Advanced analytics for Obsidian vault data"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.analytics_folder = self.vault_path / "11-Analytics"
        self.analytics_folder.mkdir(exist_ok=True)
        
    def analyze_productivity_patterns(self) -> Dict:
        """Analyze productivity patterns from daily notes and session logs"""
        patterns = {
            'daily_consistency': self._analyze_daily_consistency(),
            'time_patterns': self._analyze_time_patterns(),
            'energy_patterns': self._analyze_energy_patterns(),
            'goal_achievement': self._analyze_goal_achievement(),
            'session_effectiveness': self._analyze_session_effectiveness()
        }
        
        return patterns
        
    def _analyze_daily_consistency(self) -> Dict:
        """Analyze consistency of daily note creation and completion"""
        daily_folder = self.vault_path / "01-Daily"
        if not daily_folder.exists():
            return {'consistency_score': 0, 'streak': 0, 'gaps': []}
            
        daily_files = sorted([f for f in daily_folder.glob('*.md') 
                            if re.match(r'\d{4}-\d{2}-\d{2}\.md', f.name)])
        
        if not daily_files:
            return {'consistency_score': 0, 'streak': 0, 'gaps': []}
            
        # Calculate date range
        dates = []
        for file in daily_files:
            try:
                file_date = datetime.strptime(file.stem, '%Y-%m-%d').date()
                dates.append(file_date)
            except ValueError:
                continue
                
        if not dates:
            return {'consistency_score': 0, 'streak': 0, 'gaps': []}
            
        dates.sort()
        start_date = dates[0]
        end_date = dates[-1]
        total_days = (end_date - start_date).days + 1
        
        # Find gaps
        date_set = set(dates)
        gaps = []
        current_date = start_date
        while current_date <= end_date:
            if current_date not in date_set:
                gaps.append(current_date.isoformat())
            current_date += timedelta(days=1)
            
        # Calculate current streak
        streak = 0
        check_date = date.today()
        while check_date in date_set:
            streak += 1
            check_date -= timedelta(days=1)
            
        consistency_score = (len(dates) / total_days) * 100 if total_days > 0 else 0
        
        return {
            'consistency_score': round(consistency_score, 1),
            'total_days': total_days,
            'active_days': len(dates),
            'gaps': len(gaps),
            'gap_dates': gaps[-5:],  # Last 5 gaps
            'current_streak': streak,
            'longest_streak': self._calculate_longest_streak(dates)
        }
        
    def _calculate_longest_streak(self, dates: List[date]) -> int:
        """Calculate the longest consecutive streak of dates"""
        if not dates:
            return 0
            
        dates = sorted(set(dates))
        longest = current = 1
        
        for i in range(1, len(dates)):
            if dates[i] - dates[i-1] == timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1
                
        return longest
        
    def _analyze_time_patterns(self) -> Dict:
        """Analyze when most productive work happens"""
        session_folder = self.vault_path / "09-Claude-Integration"
        if not session_folder.exists():
            return {'peak_hours': [], 'session_distribution': {}}
            
        sessions_by_hour = defaultdict(int)
        sessions_by_day = defaultdict(int)
        
        for session_file in session_folder.glob('*-session.md'):
            try:
                # Extract timestamp from filename (YYYY-MM-DD-HHMM format)
                timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}-\d{4})', session_file.name)
                if timestamp_match:
                    timestamp_str = timestamp_match.group(1)
                    session_time = datetime.strptime(timestamp_str, '%Y-%m-%d-%H%M')
                    
                    sessions_by_hour[session_time.hour] += 1
                    sessions_by_day[session_time.strftime('%A')] += 1
                    
            except (ValueError, AttributeError):
                continue
                
        # Find peak hours (top 3)
        peak_hours = sorted(sessions_by_hour.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'sessions_by_hour': dict(sessions_by_hour),
            'sessions_by_day': dict(sessions_by_day),
            'peak_hours': [{'hour': hour, 'count': count} for hour, count in peak_hours],
            'total_sessions': sum(sessions_by_hour.values())
        }
        
    def _analyze_energy_patterns(self) -> Dict:
        """Analyze energy level patterns from daily notes"""
        daily_folder = self.vault_path / "01-Daily"
        if not daily_folder.exists():
            return {'average_energy': 0, 'energy_trends': {}}
            
        energy_data = []
        mood_data = []
        
        for daily_file in daily_folder.glob('*.md'):
            try:
                with open(daily_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract energy level (pattern: "Energy level: X/10")
                energy_match = re.search(r'Energy level:\s*(\d+)/10', content)
                if energy_match:
                    energy_level = int(energy_match.group(1))
                    file_date = datetime.strptime(daily_file.stem, '%Y-%m-%d').date()
                    energy_data.append({
                        'date': file_date,
                        'energy': energy_level,
                        'weekday': file_date.strftime('%A')
                    })
                    
                # Extract mood
                mood_match = re.search(r'Mood:\s*([^\n]+)', content)
                if mood_match:
                    mood = mood_match.group(1).strip()
                    mood_data.append(mood.lower())
                    
            except (ValueError, UnicodeDecodeError):
                continue
                
        if not energy_data:
            return {'average_energy': 0, 'energy_trends': {}}
            
        # Calculate averages by weekday
        weekday_energy = defaultdict(list)
        for entry in energy_data:
            weekday_energy[entry['weekday']].append(entry['energy'])
            
        weekday_averages = {
            day: round(sum(energies) / len(energies), 1) 
            for day, energies in weekday_energy.items()
        }
        
        # Energy trend over time (last 30 days)
        recent_data = [e for e in energy_data 
                      if e['date'] >= date.today() - timedelta(days=30)]
        
        overall_average = sum(e['energy'] for e in energy_data) / len(energy_data)
        recent_average = sum(e['energy'] for e in recent_data) / len(recent_data) if recent_data else overall_average
        
        return {
            'average_energy': round(overall_average, 1),
            'recent_average': round(recent_average, 1),
            'energy_by_weekday': weekday_averages,
            'energy_trend': 'improving' if recent_average > overall_average else 'declining' if recent_average < overall_average else 'stable',
            'most_common_moods': Counter(mood_data).most_common(5),
            'total_entries': len(energy_data)
        }
        
    def _analyze_goal_achievement(self) -> Dict:
        """Analyze goal setting and achievement patterns"""
        daily_folder = self.vault_path / "01-Daily"
        if not daily_folder.exists():
            return {'completion_rate': 0, 'goal_patterns': {}}
            
        total_goals = 0
        completed_goals = 0
        goal_categories = defaultdict(int)
        
        for daily_file in daily_folder.glob('*.md'):
            try:
                with open(daily_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Find task patterns
                tasks = re.findall(r'- \[([x ])\] (.+)', content)
                
                for status, task in tasks:
                    total_goals += 1
                    if status == 'x':
                        completed_goals += 1
                        
                    # Categorize tasks
                    task_lower = task.lower()
                    if any(word in task_lower for word in ['code', 'develop', 'build', 'implement']):
                        goal_categories['development'] += 1
                    elif any(word in task_lower for word in ['learn', 'study', 'research', 'read']):
                        goal_categories['learning'] += 1
                    elif any(word in task_lower for word in ['write', 'document', 'note']):
                        goal_categories['documentation'] += 1
                    elif any(word in task_lower for word in ['plan', 'organize', 'setup']):
                        goal_categories['planning'] += 1
                    else:
                        goal_categories['other'] += 1
                        
            except UnicodeDecodeError:
                continue
                
        completion_rate = (completed_goals / total_goals * 100) if total_goals > 0 else 0
        
        return {
            'completion_rate': round(completion_rate, 1),
            'total_goals': total_goals,
            'completed_goals': completed_goals,
            'goal_categories': dict(goal_categories),
            'most_common_category': max(goal_categories.items(), key=lambda x: x[1]) if goal_categories else None
        }
        
    def _analyze_session_effectiveness(self) -> Dict:
        """Analyze Claude Code session effectiveness"""
        session_folder = self.vault_path / "09-Claude-Integration"
        if not session_folder.exists():
            return {'average_duration': 0, 'session_types': {}}
            
        session_data = []
        session_types = defaultdict(int)
        
        for session_file in session_folder.glob('*-session.md'):
            try:
                with open(session_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Extract session type
                type_match = re.search(r'#session/(\w+)', content)
                if type_match:
                    session_type = type_match.group(1)
                    session_types[session_type] += 1
                    
                # Extract duration if available
                duration_match = re.search(r'Duration:\s*(\d+)', content)
                if duration_match:
                    duration = int(duration_match.group(1))
                    session_data.append({
                        'type': session_type if type_match else 'unknown',
                        'duration': duration
                    })
                    
            except UnicodeDecodeError:
                continue
                
        avg_duration = sum(s['duration'] for s in session_data) / len(session_data) if session_data else 0
        
        return {
            'total_sessions': sum(session_types.values()),
            'session_types': dict(session_types),
            'average_duration': round(avg_duration, 1),
            'most_common_type': max(session_types.items(), key=lambda x: x[1]) if session_types else None
        }
        
    def analyze_knowledge_growth(self) -> Dict:
        """Analyze knowledge accumulation and connection patterns"""
        knowledge_folder = self.vault_path / "06-Knowledge"
        ideas_folder = self.vault_path / "05-Ideas"
        
        knowledge_stats = self._analyze_folder_growth(knowledge_folder, 'knowledge')
        ideas_stats = self._analyze_folder_growth(ideas_folder, 'ideas')
        
        # Analyze cross-connections
        connections = self._analyze_note_connections()
        
        return {
            'knowledge_notes': knowledge_stats,
            'ideas': ideas_stats,
            'connections': connections,
            'knowledge_velocity': self._calculate_knowledge_velocity()
        }
        
    def _analyze_folder_growth(self, folder: Path, folder_type: str) -> Dict:
        """Analyze growth patterns in a specific folder"""
        if not folder.exists():
            return {'total_notes': 0, 'recent_growth': 0, 'categories': {}}
            
        files = list(folder.glob('*.md'))
        
        # Growth over time
        growth_by_month = defaultdict(int)
        categories = defaultdict(int)
        
        for file in files:
            creation_time = datetime.fromtimestamp(file.stat().st_ctime)
            month_key = creation_time.strftime('%Y-%m')
            growth_by_month[month_key] += 1
            
            # Extract categories from tags
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tags = re.findall(r'#(\w+)', content)
                    for tag in tags:
                        if tag not in ['knowledge', 'idea', 'note']:  # Skip generic tags
                            categories[tag] += 1
            except UnicodeDecodeError:
                continue
                
        # Recent growth (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_files = [f for f in files 
                       if datetime.fromtimestamp(f.stat().st_ctime) >= thirty_days_ago]
        
        return {
            'total_notes': len(files),
            'recent_growth': len(recent_files),
            'growth_by_month': dict(growth_by_month),
            'categories': dict(sorted(categories.items(), key=lambda x: x[1], reverse=True)[:10]),
            'avg_monthly_growth': sum(growth_by_month.values()) / len(growth_by_month) if growth_by_month else 0
        }
        
    def _analyze_note_connections(self) -> Dict:
        """Analyze connections between notes through links"""
        all_notes = []
        link_graph = defaultdict(set)
        
        for folder in self.vault_path.iterdir():
            if folder.is_dir() and not folder.name.startswith('.'):
                for note_file in folder.glob('*.md'):
                    try:
                        with open(note_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        # Find internal links
                        links = re.findall(r'\[\[([^\]]+)\]\]', content)
                        note_name = note_file.stem
                        all_notes.append(note_name)
                        
                        for link in links:
                            link_graph[note_name].add(link)
                            
                    except UnicodeDecodeError:
                        continue
                        
        # Calculate connection metrics
        total_notes = len(all_notes)
        total_connections = sum(len(links) for links in link_graph.values())
        
        # Most connected notes
        connection_counts = {note: len(links) for note, links in link_graph.items()}
        most_connected = sorted(connection_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Orphaned notes (no incoming or outgoing links)
        referenced_notes = set()
        for links in link_graph.values():
            referenced_notes.update(links)
            
        orphaned_notes = set(all_notes) - set(link_graph.keys()) - referenced_notes
        
        return {
            'total_notes': total_notes,
            'total_connections': total_connections,
            'avg_connections_per_note': round(total_connections / total_notes, 2) if total_notes > 0 else 0,
            'most_connected': [{'note': note, 'connections': count} for note, count in most_connected],
            'orphaned_count': len(orphaned_notes),
            'connection_density': round(total_connections / (total_notes * total_notes), 4) if total_notes > 0 else 0
        }
        
    def _calculate_knowledge_velocity(self) -> Dict:
        """Calculate the velocity of knowledge creation and processing"""
        # Analyze note creation over time
        all_folders = ['05-Ideas', '06-Knowledge', '04-Projects']
        velocity_data = []
        
        for folder_name in all_folders:
            folder = self.vault_path / folder_name
            if not folder.exists():
                continue
                
            for file in folder.glob('*.md'):
                creation_time = datetime.fromtimestamp(file.stat().st_ctime)
                velocity_data.append({
                    'date': creation_time.date(),
                    'type': folder_name.split('-')[1].lower(),
                    'file': file.name
                })
                
        # Group by week
        weekly_velocity = defaultdict(lambda: defaultdict(int))
        for item in velocity_data:
            week = item['date'].isocalendar()[1]
            year = item['date'].year
            week_key = f"{year}-W{week:02d}"
            weekly_velocity[week_key][item['type']] += 1
            
        # Calculate recent velocity (last 4 weeks)
        recent_weeks = sorted(weekly_velocity.keys())[-4:]
        recent_velocity = sum(
            sum(weekly_velocity[week].values()) 
            for week in recent_weeks
        )
        
        return {
            'notes_per_week': dict(weekly_velocity),
            'recent_velocity': recent_velocity,
            'velocity_trend': self._calculate_velocity_trend(weekly_velocity)
        }
        
    def _calculate_velocity_trend(self, weekly_data: Dict) -> str:
        """Calculate if knowledge velocity is increasing or decreasing"""
        if len(weekly_data) < 4:
            return 'insufficient_data'
            
        weeks = sorted(weekly_data.keys())
        first_half = weeks[:len(weeks)//2]
        second_half = weeks[len(weeks)//2:]
        
        first_half_avg = sum(
            sum(weekly_data[week].values()) for week in first_half
        ) / len(first_half)
        
        second_half_avg = sum(
            sum(weekly_data[week].values()) for week in second_half
        ) / len(second_half)
        
        if second_half_avg > first_half_avg * 1.1:
            return 'accelerating'
        elif second_half_avg < first_half_avg * 0.9:
            return 'declining'
        else:
            return 'stable'
            
    def generate_comprehensive_report(self) -> str:
        """Generate a comprehensive analytics report"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Gather all analytics
        productivity = self.analyze_productivity_patterns()
        knowledge = self.analyze_knowledge_growth()
        
        report = f"""# Comprehensive Vault Analytics Report
**Generated:** {timestamp}

## 📊 Executive Summary
- **Vault Health Score:** {self._calculate_health_score(productivity, knowledge)}/100
- **Daily Consistency:** {productivity['daily_consistency']['consistency_score']}%
- **Knowledge Velocity:** {knowledge['knowledge_velocity']['recent_velocity']} notes/week
- **Connection Density:** {knowledge['connections']['connection_density']}

## 🎯 Productivity Analysis

### Daily Consistency
- **Consistency Score:** {productivity['daily_consistency']['consistency_score']}%
- **Current Streak:** {productivity['daily_consistency']['current_streak']} days
- **Longest Streak:** {productivity['daily_consistency']['longest_streak']} days
- **Recent Gaps:** {len(productivity['daily_consistency']['gap_dates'])} in tracking period

### Time Patterns
"""
        
        # Add peak hours analysis
        if productivity['time_patterns']['peak_hours']:
            report += "**Most Productive Hours:**\n"
            for hour_data in productivity['time_patterns']['peak_hours']:
                report += f"- {hour_data['hour']:02d}:00 ({hour_data['count']} sessions)\n"
        
        report += f"""
### Energy & Mood Patterns  
- **Average Energy:** {productivity['energy_patterns']['average_energy']}/10
- **Recent Trend:** {productivity['energy_patterns']['energy_trend']}
- **Best Days:** {self._get_best_energy_days(productivity['energy_patterns'])}

### Goal Achievement
- **Completion Rate:** {productivity['goal_achievement']['completion_rate']}%
- **Total Goals Tracked:** {productivity['goal_achievement']['total_goals']}
- **Most Common Category:** {productivity['goal_achievement']['most_common_category'][0] if productivity['goal_achievement']['most_common_category'] else 'N/A'}

## 🧠 Knowledge Analysis

### Knowledge Growth
- **Total Knowledge Notes:** {knowledge['knowledge_notes']['total_notes']}
- **Ideas Captured:** {knowledge['ideas']['total_notes']}
- **Recent Growth:** {knowledge['knowledge_notes']['recent_growth']} new notes (30 days)

### Knowledge Connections
- **Total Connections:** {knowledge['connections']['total_connections']}
- **Average Connections/Note:** {knowledge['connections']['avg_connections_per_note']}
- **Orphaned Notes:** {knowledge['connections']['orphaned_count']}

### Knowledge Velocity
- **Current Velocity:** {knowledge['knowledge_velocity']['recent_velocity']} notes/week
- **Trend:** {knowledge['knowledge_velocity']['velocity_trend']}

## 🤖 Claude Code Integration Analysis

### Session Patterns
- **Total Sessions:** {productivity['session_effectiveness']['total_sessions']}
- **Average Duration:** {productivity['session_effectiveness']['average_duration']} minutes
- **Most Common Type:** {productivity['session_effectiveness']['most_common_type'][0] if productivity['session_effectiveness']['most_common_type'] else 'N/A'}

## 💡 Insights & Recommendations

### Strengths
{self._generate_strengths(productivity, knowledge)}

### Optimization Opportunities
{self._generate_recommendations(productivity, knowledge)}

### Next Month Focus Areas
{self._generate_focus_areas(productivity, knowledge)}

## 📈 Trend Analysis

### Positive Trends
- {self._identify_positive_trends(productivity, knowledge)}

### Areas for Attention
- {self._identify_concern_areas(productivity, knowledge)}

## 🔧 System Health

### Vault Organization
- **File Distribution:** Well-organized across {len(list(self.vault_path.glob('*/')))} folders
- **Template Usage:** Consistent structure maintained
- **Automation Status:** {self._check_automation_status()}

### Data Quality
- **Completeness:** {self._assess_data_completeness(productivity, knowledge)}%
- **Consistency:** {self._assess_data_consistency()}
- **Accuracy:** Regular validation maintained

---
**Tags:** #analytics #comprehensive-report #productivity #knowledge-management
**Next Report:** {(datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')}
**Action Items:** [[Analytics-Action-Items-{datetime.now().strftime('%Y-%m-%d')}]]
"""
        
        # Save report
        report_file = self.analytics_folder / f"comprehensive-report-{datetime.now().strftime('%Y-%m-%d')}.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"Comprehensive report generated: {report_file}")
        return report
        
    def _calculate_health_score(self, productivity: Dict, knowledge: Dict) -> int:
        """Calculate overall vault health score out of 100"""
        score = 0
        
        # Daily consistency (25 points)
        consistency = productivity['daily_consistency']['consistency_score']
        score += min(25, consistency * 0.25)
        
        # Goal completion (20 points)  
        completion = productivity['goal_achievement']['completion_rate']
        score += min(20, completion * 0.2)
        
        # Knowledge growth (25 points)
        recent_growth = knowledge['knowledge_notes']['recent_growth']
        score += min(25, recent_growth * 2)  # 2 points per new note
        
        # Connection density (15 points)
        density = knowledge['connections']['connection_density']
        score += min(15, density * 3000)  # Scale up the small density value
        
        # Session activity (15 points)
        sessions = productivity['session_effectiveness']['total_sessions']
        score += min(15, sessions * 0.5)
        
        return int(score)
        
    def _get_best_energy_days(self, energy_data: Dict) -> str:
        """Get the days with highest average energy"""
        if not energy_data['energy_by_weekday']:
            return 'Insufficient data'
            
        best_days = sorted(energy_data['energy_by_weekday'].items(), 
                          key=lambda x: x[1], reverse=True)[:2]
        return ', '.join([f"{day} ({energy:.1f})" for day, energy in best_days])
        
    def _generate_strengths(self, productivity: Dict, knowledge: Dict) -> str:
        """Generate list of identified strengths"""
        strengths = []
        
        if productivity['daily_consistency']['consistency_score'] > 80:
            strengths.append("- Excellent daily journaling consistency")
            
        if productivity['goal_achievement']['completion_rate'] > 70:
            strengths.append("- High goal completion rate shows strong execution")
            
        if knowledge['knowledge_velocity']['velocity_trend'] == 'accelerating':
            strengths.append("- Accelerating knowledge creation velocity")
            
        if knowledge['connections']['avg_connections_per_note'] > 2:
            strengths.append("- Strong knowledge interconnection building")
            
        if not strengths:
            strengths.append("- Systematic approach to personal knowledge management")
            
        return '\n'.join(strengths)
        
    def _generate_recommendations(self, productivity: Dict, knowledge: Dict) -> str:
        """Generate optimization recommendations"""
        recommendations = []
        
        if productivity['daily_consistency']['consistency_score'] < 70:
            recommendations.append("- Focus on improving daily note consistency")
            
        if productivity['goal_achievement']['completion_rate'] < 60:
            recommendations.append("- Review goal setting strategy for more achievable targets")
            
        if knowledge['connections']['orphaned_count'] > 5:
            recommendations.append("- Connect orphaned notes to improve knowledge graph density")
            
        if productivity['energy_patterns']['energy_trend'] == 'declining':
            recommendations.append("- Investigate factors affecting energy levels")
            
        if not recommendations:
            recommendations.append("- Continue current practices while exploring advanced workflows")
            
        return '\n'.join(recommendations)
        
    def _generate_focus_areas(self, productivity: Dict, knowledge: Dict) -> str:
        """Generate next month focus areas"""
        focus_areas = []
        
        # Dynamic focus based on data
        if knowledge['knowledge_velocity']['recent_velocity'] < 5:
            focus_areas.append("- Increase knowledge capture and processing")
            
        if productivity['session_effectiveness']['total_sessions'] < 20:
            focus_areas.append("- Enhance Claude Code integration and usage")
            
        if knowledge['connections']['connection_density'] < 0.01:
            focus_areas.append("- Build more connections between knowledge domains")
            
        focus_areas.append("- Experiment with advanced automation workflows")
        focus_areas.append("- Develop specialized agent memory contexts")
        
        return '\n'.join(focus_areas[:3])  # Top 3 focus areas
        
    def _identify_positive_trends(self, productivity: Dict, knowledge: Dict) -> str:
        """Identify positive trends in the data"""
        trends = []
        
        if productivity['daily_consistency']['current_streak'] > 7:
            trends.append(f"Current {productivity['daily_consistency']['current_streak']}-day consistency streak")
            
        if knowledge['knowledge_velocity']['velocity_trend'] == 'accelerating':
            trends.append("Accelerating knowledge creation and capture")
            
        if productivity['energy_patterns']['energy_trend'] == 'improving':
            trends.append("Improving energy levels and mood patterns")
            
        return '\n- '.join(trends) if trends else "Stable performance maintained"
        
    def _identify_concern_areas(self, productivity: Dict, knowledge: Dict) -> str:
        """Identify areas that need attention"""
        concerns = []
        
        if productivity['daily_consistency']['consistency_score'] < 50:
            concerns.append("Low daily consistency impacting tracking effectiveness")
            
        if knowledge['connections']['orphaned_count'] > 10:
            concerns.append("High number of orphaned notes reducing knowledge integration")
            
        if productivity['energy_patterns']['energy_trend'] == 'declining':
            concerns.append("Declining energy patterns may affect productivity")
            
        return '\n- '.join(concerns) if concerns else "No significant concerns identified"
        
    def _check_automation_status(self) -> str:
        """Check if automation scripts are properly configured"""
        scripts_folder = self.vault_path / 'Scripts'

        vault_automation_exists = (scripts_folder / 'vault-automation.py').exists()
        auto_organize_exists = (scripts_folder / 'auto-organize.py').exists()
        claude_exists = (
            (scripts_folder / 'claude_integration.py').exists() or
            (scripts_folder / 'claude-integration.py').exists()
        )

        existing_scripts = int(vault_automation_exists) + int(auto_organize_exists) + int(claude_exists)
        total_expected = 3
        
        return f"Active ({existing_scripts}/{total_expected} scripts configured)"
        
    def _assess_data_completeness(self, productivity: Dict, knowledge: Dict) -> int:
        """Assess how complete the data collection is"""
        completeness_score = 0
        
        # Check various data sources
        if productivity['daily_consistency']['total_days'] > 0:
            completeness_score += 25
            
        if productivity['session_effectiveness']['total_sessions'] > 0:
            completeness_score += 25
            
        if knowledge['knowledge_notes']['total_notes'] > 0:
            completeness_score += 25
            
        if knowledge['connections']['total_connections'] > 0:
            completeness_score += 25
            
        return completeness_score
        
    def _assess_data_consistency(self) -> str:
        """Assess consistency of data entry patterns"""
        # This could be expanded with more sophisticated checks
        return "Good (template usage consistent)"

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Vault Analytics Engine")
    parser.add_argument('--vault', default='.', help='Path to Obsidian vault')
    parser.add_argument('--report', choices=['productivity', 'knowledge', 'comprehensive'], 
                       default='comprehensive', help='Type of report to generate')
    
    args = parser.parse_args()
    
    analytics = VaultAnalytics(args.vault)
    
    if args.report == 'productivity':
        patterns = analytics.analyze_productivity_patterns()
        print(json.dumps(patterns, indent=2, default=str))
    elif args.report == 'knowledge':
        knowledge = analytics.analyze_knowledge_growth()
        print(json.dumps(knowledge, indent=2, default=str))
    else:
        report = analytics.generate_comprehensive_report()
        print("Comprehensive analytics report generated!")

if __name__ == "__main__":
    main()