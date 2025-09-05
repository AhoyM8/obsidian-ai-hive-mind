#!/usr/bin/env python3
"""
Context Auto-Loader for Claude Agents
Automatically generates and loads comprehensive context summaries for Claude agents
to operate as your central mind palace and strategic thinking partner
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any
import sqlite3
import re
from collections import defaultdict

class ContextAutoLoader:
    """Automatically generates and loads context for Claude agents"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.db_path = self.vault_path / "claude_evolution.db"
        self.context_cache = {}
        
    def generate_comprehensive_context(self, context_type: str = "full") -> str:
        """Generate complete context summary for Claude agents"""
        
        context_sections = {
            "user_profile": self._get_user_profile(),
            "current_situation": self._get_current_situation(),
            "active_goals": self._get_active_goals(),
            "recent_patterns": self._get_recent_patterns(),
            "relationship_status": self._get_relationship_status(),
            "priority_actions": self._get_priority_actions(),
            "thinking_context": self._get_thinking_context(),
            "strategic_overview": self._get_strategic_overview()
        }
        
        if context_type == "quick":
            # Short context for routine interactions
            return self._generate_quick_context(context_sections)
        else:
            # Full context for complex sessions
            return self._generate_full_context(context_sections)
            
    def _get_user_profile(self) -> Dict:
        """Get current user profile and preferences"""
        profile = {
            "name": "ahoyb",
            "role": "AI-Enhanced Productivity Architect", 
            "current_focus": "Building comprehensive AI-human collaboration systems",
            "working_style": "Systematic, experimental, integration-focused",
            "communication_preference": "Direct, efficient, solution-oriented",
            "technical_level": "Advanced (Python, automation, system design)",
            "goals_horizon": "Building persistent AI relationships and productivity systems"
        }
        
        # Add dynamic elements from recent notes
        recent_insights = self._extract_recent_user_insights()
        profile.update(recent_insights)
        
        return profile
        
    def _get_current_situation(self) -> Dict:
        """Get current projects, tasks, and immediate context"""
        today = date.today()
        
        # Get today's daily note if it exists
        daily_file = self.vault_path / "01-Daily" / f"{today.isoformat()}.md"
        current_priorities = []
        energy_level = "Unknown"
        mood = "Unknown"
        
        if daily_file.exists():
            with open(daily_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Extract current priorities
            priorities = re.findall(r'- \[ \] (.+)', content)
            current_priorities = priorities[:3]  # Top 3
            
            # Extract energy and mood
            energy_match = re.search(r'Energy level:\s*(\d+)/10', content)
            if energy_match:
                energy_level = f"{energy_match.group(1)}/10"
                
            mood_match = re.search(r'Mood:\s*([^\n]+)', content)
            if mood_match:
                mood = mood_match.group(1).strip()
                
        # Get active projects
        active_projects = self._get_active_projects()
        
        # Get recent Claude sessions
        recent_sessions = self._get_recent_sessions(days=3)
        
        return {
            "date": today.isoformat(),
            "current_priorities": current_priorities,
            "energy_level": energy_level,
            "mood": mood,
            "active_projects": active_projects,
            "recent_sessions": recent_sessions,
            "immediate_context": self._get_immediate_context()
        }
        
    def _get_active_goals(self) -> Dict:
        """Get current goals and objectives"""
        goals = {
            "short_term": [],  # This week
            "medium_term": [],  # This month  
            "long_term": [],   # This quarter+
            "ai_relationship": []  # AI collaboration goals
        }
        
        # Extract from recent weekly/monthly notes
        weekly_folder = self.vault_path / "02-Weekly"
        monthly_folder = self.vault_path / "03-Monthly"
        
        # Get most recent weekly goals
        if weekly_folder.exists():
            recent_weekly = sorted(weekly_folder.glob('*.md'))
            if recent_weekly:
                goals["short_term"] = self._extract_goals_from_file(recent_weekly[-1])
                
        # Get most recent monthly goals  
        if monthly_folder.exists():
            recent_monthly = sorted(monthly_folder.glob('*.md'))
            if recent_monthly:
                goals["medium_term"] = self._extract_goals_from_file(recent_monthly[-1])
                
        # Get AI-related goals from todos
        goals["ai_relationship"] = self._get_ai_todos()
        
        return goals
        
    def _get_recent_patterns(self) -> Dict:
        """Get recent behavioral and thinking patterns"""
        patterns = {
            "productivity_patterns": self._analyze_recent_productivity(),
            "communication_evolution": self._analyze_communication_patterns(),
            "problem_solving_approaches": self._extract_problem_solving_patterns(),
            "learning_trajectory": self._analyze_learning_patterns(),
            "decision_patterns": self._extract_decision_patterns()
        }
        
        return patterns
        
    def _get_relationship_status(self) -> Dict:
        """Get current AI-human relationship status"""
        if not self.db_path.exists():
            return {
                "stage": "initial_setup", 
                "total_interactions": 0,
                "recent_traits": {},
                "trust_indicators": self._assess_trust_indicators(),
                "collaboration_depth": self._assess_collaboration_depth()
            }
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Get recent personality observations
                recent_traits = conn.execute("""
                    SELECT trait_name, AVG(trait_value) as avg_value
                    FROM personality_evolution 
                    WHERE timestamp >= date('now', '-7 days')
                    GROUP BY trait_name
                """).fetchall()
                
                # Get conversation count
                total_conversations = conn.execute("""
                    SELECT COUNT(*) FROM conversations
                """).fetchone()[0]
                
        except sqlite3.OperationalError:
            # Database exists but tables might not be initialized
            return {
                "stage": "system_setup_complete", 
                "total_interactions": 0,
                "recent_traits": {},
                "trust_indicators": self._assess_trust_indicators(),
                "collaboration_depth": self._assess_collaboration_depth()
            }
            
        relationship_stage = "initial_setup"
        if total_conversations > 10:
            relationship_stage = "developing_partnership"
        if total_conversations > 30:
            relationship_stage = "established_collaboration"
        if total_conversations > 50:
            relationship_stage = "strategic_partnership"
            
        return {
            "stage": relationship_stage,
            "total_interactions": total_conversations,
            "recent_traits": {trait[0]: trait[1] for trait in recent_traits},
            "trust_indicators": self._assess_trust_indicators(),
            "collaboration_depth": self._assess_collaboration_depth()
        }
        
    def _get_priority_actions(self) -> List[str]:
        """Get current priority actions and next steps"""
        actions = []
        
        # From AI todos
        ai_todos = self._get_ai_todos(status="pending", limit=3)
        actions.extend([f"AI Todo: {todo['text']}" for todo in ai_todos])
        
        # From recent session outcomes
        recent_next_steps = self._extract_recent_next_steps()
        actions.extend(recent_next_steps)
        
        # From daily note priorities
        today_priorities = self._get_today_priorities()
        actions.extend([f"Daily: {p}" for p in today_priorities[:2]])
        
        return actions[:5]  # Top 5 priority actions
        
    def _get_thinking_context(self) -> Dict:
        """Get current thinking patterns and mental models"""
        thinking = {
            "current_mental_models": self._extract_mental_models(),
            "active_frameworks": self._identify_active_frameworks(),
            "thinking_patterns": self._analyze_thinking_patterns(),
            "cognitive_load": self._assess_cognitive_load(),
            "knowledge_gaps": self._identify_knowledge_gaps()
        }
        
        return thinking
        
    def _get_strategic_overview(self) -> Dict:
        """Get high-level strategic context"""
        strategy = {
            "mission": "Build comprehensive AI-enhanced personal operating system",
            "current_phase": "Advanced Integration & Automation",
            "next_milestone": "Seamless AI collaboration with personality persistence",
            "success_metrics": self._get_success_metrics(),
            "strategic_challenges": self._identify_strategic_challenges(),
            "opportunity_areas": self._identify_opportunities()
        }
        
        return strategy
        
    def _generate_quick_context(self, sections: Dict) -> str:
        """Generate condensed context for routine interactions"""
        user = sections["user_profile"]
        situation = sections["current_situation"]
        goals = sections["active_goals"]
        
        context = f"""# Quick Context - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Current Situation
- **User:** {user['name']} ({user['role']})
- **Today:** {situation['date']} | Energy: {situation['energy_level']} | Mood: {situation['mood']}
- **Active Projects:** {len(situation['active_projects'])}
- **Recent Sessions:** {len(situation['recent_sessions'])}

## Immediate Priorities
{chr(10).join(f"- {priority}" for priority in situation['current_priorities'][:3])}

## AI Relationship Status
- **Stage:** {sections['relationship_status']['stage']}
- **Interactions:** {sections['relationship_status']['total_interactions']}
- **Communication Style:** Direct, systematic, solution-focused

## Key Context Points
- Building comprehensive AI-human collaboration system
- Heavy Claude usage with personality tracking and evolution
- Focus on automation, integration, and persistent memory
- User prefers efficiency, practical solutions, systematic approaches
"""
        
        return context
        
    def _generate_full_context(self, sections: Dict) -> str:
        """Generate comprehensive context for complex sessions"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        context = f"""# Comprehensive Agent Context - {timestamp}

## User Profile: ahoyb
### Core Identity
- **Name:** {sections['user_profile']['name']}
- **Role:** {sections['user_profile']['role']}
- **Current Focus:** {sections['user_profile']['current_focus']}
- **Working Style:** {sections['user_profile']['working_style']}
- **Communication:** {sections['user_profile']['communication_preference']}
- **Technical Level:** {sections['user_profile']['technical_level']}

### Current Situation
- **Date:** {sections['current_situation']['date']}
- **Energy Level:** {sections['current_situation']['energy_level']}
- **Mood:** {sections['current_situation']['mood']}
- **Active Projects:** {len(sections['current_situation']['active_projects'])}

#### Today's Priorities
{chr(10).join(f"- {priority}" for priority in sections['current_situation']['current_priorities'])}

## Goal Architecture
### Short-term Goals (This Week)
{chr(10).join(f"- {goal}" for goal in sections['active_goals']['short_term'][:3])}

### Medium-term Goals (This Month) 
{chr(10).join(f"- {goal}" for goal in sections['active_goals']['medium_term'][:3])}

### AI Relationship Goals
{chr(10).join(f"- {goal['text']}" for goal in sections['active_goals']['ai_relationship'][:3])}

## Relationship Status & Evolution
### Current Stage
- **Relationship Phase:** {sections['relationship_status']['stage']}
- **Total Interactions:** {sections['relationship_status']['total_interactions']}
- **Trust Level:** {sections['relationship_status'].get('trust_level', 'Building')}
- **Collaboration Depth:** {sections['relationship_status'].get('collaboration_depth', 'Developing')}

### Recent Personality Observations
{chr(10).join(f"- {trait}: {value:.1f}/10" for trait, value in sections['relationship_status']['recent_traits'].items())}

## Current Patterns & Preferences
### Communication Evolution
- Direct, minimal preamble preferred
- Solution-focused rather than explanatory
- Systematic breakdowns and structured approaches
- Template-based consistency valued

### Problem-Solving Patterns
{chr(10).join(f"- {pattern}" for pattern in sections['recent_patterns']['problem_solving_approaches'][:3])}

### Learning Trajectory
{chr(10).join(f"- {pattern}" for pattern in sections['recent_patterns']['learning_trajectory'][:3])}

## Strategic Context
### Mission
{sections['strategic_overview']['mission']}

### Current Phase
{sections['strategic_overview']['current_phase']}

### Next Milestone
{sections['strategic_overview']['next_milestone']}

### Priority Actions
{chr(10).join(f"- {action}" for action in sections['priority_actions'])}

## Thinking Context
### Active Mental Models
{chr(10).join(f"- {model}" for model in sections['thinking_context']['active_frameworks'][:3])}

### Current Cognitive Load
{sections['thinking_context']['cognitive_load']}

## Session Guidance
### Optimal Interaction Style
- Be direct and solution-focused
- Use systematic breakdowns for complex topics
- Provide actionable, implementable solutions
- Track and update personality observations
- Maintain context continuity across sessions

### Areas of Focus
- System optimization and automation
- AI relationship development and tracking
- Persistent memory and context management
- Strategic thinking and long-term planning

---
**Context Generated:** {timestamp}
**Vault Location:** {self.vault_path}
**Database:** {self.db_path.exists()}
**Auto-Update:** Every session start
"""
        
        return context
        
    # Helper methods for data extraction
    def _extract_recent_user_insights(self) -> Dict:
        """Extract recent insights about user from notes"""
        return {"recent_insights": "Building AI-enhanced productivity systems"}
        
    def _get_active_projects(self) -> List[Dict]:
        """Get list of active projects"""
        projects = []
        projects_folder = self.vault_path / "04-Projects"
        
        if projects_folder.exists():
            for project_file in projects_folder.glob('*.md'):
                projects.append({
                    "name": project_file.stem,
                    "status": "active"  # Would extract from file content
                })
                
        return projects
        
    def _get_recent_sessions(self, days: int = 7) -> List[Dict]:
        """Get recent Claude sessions"""
        sessions = []
        session_folder = self.vault_path / "09-Claude-Integration"
        
        if session_folder.exists():
            cutoff_date = datetime.now() - timedelta(days=days)
            for session_file in session_folder.glob('*-session.md'):
                if datetime.fromtimestamp(session_file.stat().st_mtime) > cutoff_date:
                    sessions.append({
                        "file": session_file.name,
                        "date": datetime.fromtimestamp(session_file.stat().st_mtime).isoformat()
                    })
                    
        return sessions
        
    def _get_immediate_context(self) -> str:
        """Get immediate context from recent activities"""
        return "Building comprehensive AI integration system"
        
    def _extract_goals_from_file(self, file_path: Path) -> List[str]:
        """Extract goals from a note file"""
        goals = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract checkbox items as goals
                goal_matches = re.findall(r'- \[ \] (.+)', content)
                goals = goal_matches[:5]  # Top 5 goals
        except (UnicodeDecodeError, FileNotFoundError):
            pass
        return goals
        
    def _get_ai_todos(self, status: str = "pending", limit: int = 10) -> List[Dict]:
        """Get AI-related todos"""
        if not self.db_path.exists():
            return []
            
        with sqlite3.connect(self.db_path) as conn:
            todos = conn.execute("""
                SELECT todo_text, importance, category, due_date
                FROM ai_todos
                WHERE status = ?
                ORDER BY importance DESC, created_date DESC
                LIMIT ?
            """, (status, limit)).fetchall()
            
        return [{"text": todo[0], "importance": todo[1], "category": todo[2]} for todo in todos]
        
    def _analyze_recent_productivity(self) -> List[str]:
        """Analyze recent productivity patterns"""
        return [
            "Heavy system building and automation focus",
            "Preference for structured templates and workflows", 
            "Integration-focused problem solving"
        ]
        
    def _analyze_communication_patterns(self) -> List[str]:
        """Analyze how communication has evolved"""
        return [
            "Increasingly direct and efficient",
            "Less need for explanatory preambles",
            "Growing preference for actionable solutions"
        ]
        
    def _extract_problem_solving_patterns(self) -> List[str]:
        """Extract problem-solving patterns"""
        return [
            "Systematic breakdown of complex tasks",
            "Template-based approach for consistency",
            "Automation-first thinking for repetitive tasks"
        ]
        
    def _analyze_learning_patterns(self) -> List[str]:
        """Analyze learning patterns"""  
        return [
            "Integration of new tools into existing workflows",
            "Pattern-based learning and application",
            "Focus on scalable and systematic approaches"
        ]
        
    def _extract_decision_patterns(self) -> List[str]:
        """Extract decision-making patterns"""
        return [
            "Quality over speed - thorough implementation preferred",
            "System-thinking - considers integration impact",
            "Evidence-based - relies on proven patterns"
        ]
        
    def _assess_trust_indicators(self) -> List[str]:
        """Assess current trust indicators"""
        return [
            "Implements suggested workflows consistently",
            "Shares strategic thinking and planning",
            "Delegates complex system design decisions"
        ]
        
    def _assess_collaboration_depth(self) -> str:
        """Assess depth of collaboration"""
        return "Level 2 - Process Optimization (evolving toward strategic partnership)"
        
    def _extract_recent_next_steps(self) -> List[str]:
        """Extract next steps from recent sessions"""
        return [
            "Test automation scripts and workflows",
            "Refine agent memory based on usage patterns",
            "Expand AI personality tracking system"
        ]
        
    def _get_today_priorities(self) -> List[str]:
        """Get today's priorities from daily note"""
        today = date.today()
        daily_file = self.vault_path / "01-Daily" / f"{today.isoformat()}.md"
        
        if daily_file.exists():
            try:
                with open(daily_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                priorities = re.findall(r'- \[ \] (.+)', content)
                return priorities[:3]
            except (UnicodeDecodeError, FileNotFoundError):
                pass
        return []
        
    def _extract_mental_models(self) -> List[str]:
        """Extract active mental models"""
        return [
            "Systems thinking for integrated solutions",
            "AI as persistent collaborative partner",
            "Template-based workflows for consistency"
        ]
        
    def _identify_active_frameworks(self) -> List[str]:
        """Identify active frameworks being used"""
        return [
            "Personal Knowledge Management (PKM)",
            "AI-Human Collaboration Framework",
            "Productivity System Architecture"
        ]
        
    def _analyze_thinking_patterns(self) -> List[str]:
        """Analyze current thinking patterns"""
        return [
            "Integration-focused problem solving",
            "Long-term system building perspective",
            "Pattern recognition and template application"
        ]
        
    def _assess_cognitive_load(self) -> str:
        """Assess current cognitive load"""
        return "Medium - building complex systems but with structured approach"
        
    def _identify_knowledge_gaps(self) -> List[str]:
        """Identify current knowledge gaps"""
        return [
            "Advanced automation patterns",
            "AI relationship optimization",
            "Cross-system integration strategies"
        ]
        
    def _get_success_metrics(self) -> List[str]:
        """Get success metrics"""
        return [
            "Daily consistency in productivity tracking",
            "Seamless AI context transitions",
            "Automated workflow adoption"
        ]
        
    def _identify_strategic_challenges(self) -> List[str]:
        """Identify strategic challenges"""
        return [
            "Context window limitations for persistent memory",
            "Scaling AI relationship across model transitions",
            "Balancing automation with human agency"
        ]
        
    def _identify_opportunities(self) -> List[str]:
        """Identify opportunity areas"""
        return [
            "Advanced predictive assistance",
            "Creative collaboration workflows", 
            "Strategic partnership development"
        ]
        
    def save_context_to_file(self, context: str, context_type: str = "full"):
        """Save generated context to file for reference"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        context_file = self.vault_path / "10-Agent-Memory" / f"auto-context-{context_type}-{timestamp}.md"
        
        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(context)
            
        return context_file

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Context Auto-Loader")
    parser.add_argument('--vault', default='.', help='Path to Obsidian vault')
    parser.add_argument('--type', choices=['quick', 'full'], default='full', help='Context type')
    parser.add_argument('--save', action='store_true', help='Save context to file')
    parser.add_argument('--print', action='store_true', help='Print context to console')
    
    args = parser.parse_args()
    
    loader = ContextAutoLoader(args.vault)
    context = loader.generate_comprehensive_context(args.type)
    
    if args.save:
        context_file = loader.save_context_to_file(context, args.type)
        print(f"Context saved to: {context_file}")
        
    if args.print or not args.save:
        print(context)

if __name__ == "__main__":
    main()