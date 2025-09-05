#!/usr/bin/env python3
"""
Claude Code Integration Script for Obsidian Vault
Automates session logging, memory management, and workflow optimization
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import hashlib

class ObsidianClaudeIntegration:
    """Main integration class for Claude Code and Obsidian"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.claude_folder = self.vault_path / "09-Claude-Integration"
        self.memory_folder = self.vault_path / "10-Agent-Memory"
        self.templates_folder = self.vault_path / "08-Templates"
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        for folder in [self.claude_folder, self.memory_folder]:
            folder.mkdir(exist_ok=True)
            
    def create_session_log(self, session_type: str = "general", project: str = "", goal: str = ""):
        """Create a new Claude session log from template"""
        timestamp = datetime.datetime.now()
        session_id = timestamp.strftime("%Y-%m-%d-%H%M")
        
        template_path = self.templates_folder / "Claude Session Log.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
            
        # Read template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        # Replace placeholders
        replacements = {
            "{{date:YYYY-MM-DD-HHmm}}": session_id,
            "{{date:YYYY-MM-DD}}": timestamp.strftime("%Y-%m-%d"),
            "{{date:HH:mm}}": timestamp.strftime("%H:%M"),
            "{{type}}": session_type,
            "{{project}}": project
        }
        
        content = template_content
        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)
            
        # Add goal if provided
        if goal:
            content = content.replace("**Primary Goal:** ", f"**Primary Goal:** {goal}")
            
        # Create session file
        session_file = self.claude_folder / f"{session_id}-{session_type}-session.md"
        with open(session_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Created session log: {session_file}")
        return session_file
        
    def update_agent_memory(self, context_data: Dict, memory_type: str = "general"):
        """Update agent memory with new context and patterns"""
        timestamp = datetime.datetime.now()
        memory_file = self.memory_folder / f"Agent-Memory-{memory_type}-{timestamp.strftime('%Y-%m-%d')}.md"
        
        # Create or update memory file
        if memory_file.exists():
            with open(memory_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        else:
            existing_content = self._create_memory_template(memory_type)
            
        # Add new context entry
        context_entry = f"""
## Context Update: {timestamp.strftime('%H:%M')}
### New Information
{context_data.get('info', '')}

### Patterns Observed
{context_data.get('patterns', '')}

### Decisions Made
{context_data.get('decisions', '')}

### Next Session Context
{context_data.get('next_context', '')}

---
"""
        
        # Insert at appropriate location
        updated_content = existing_content.replace(
            "## Context History", 
            f"## Context History{context_entry}"
        )
        
        with open(memory_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"Updated agent memory: {memory_file}")
        return memory_file
        
    def _create_memory_template(self, memory_type: str) -> str:
        """Create a new agent memory template"""
        timestamp = datetime.datetime.now()
        return f"""# Agent Memory: {memory_type.title()}

**Created:** {timestamp.strftime('%Y-%m-%d %H:%M')}
**Type:** #agent-memory #{memory_type}
**Status:** #status/active

## Core Context
### Project Overview
- **Current Focus:** 
- **Active Projects:** 
- **Key Goals:** 

### User Preferences
- **Communication Style:** 
- **Work Patterns:** 
- **Tool Preferences:** 

## Context History

## Pattern Library
### Common Workflows
- 

### Problem-Solution Patterns
- 

### Optimization Opportunities
- 

## Knowledge Graph
### Key Concepts
- 

### Domain Expertise
- 

### Cross-Connections
- 

---
**Tags:** #agent-memory #{memory_type} #status/active
**Last Updated:** {timestamp.strftime('%Y-%m-%d %H:%M')}
"""

    def create_daily_note(self):
        """Create daily note from template with current date"""
        today = datetime.date.today()
        daily_folder = self.vault_path / "01-Daily"
        daily_folder.mkdir(exist_ok=True)
        
        daily_file = daily_folder / f"{today.strftime('%Y-%m-%d')}.md"
        
        if daily_file.exists():
            print(f"Daily note already exists: {daily_file}")
            return daily_file
            
        template_path = self.templates_folder / "Daily Journal.md"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found: {template_path}")
            
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
            
        # Basic date replacements (Obsidian templates handle more complex ones)
        content = template_content.replace("{{date:YYYY-MM-DD}}", today.strftime('%Y-%m-%d'))
        content = content.replace("{{date:dddd}}", today.strftime('%A'))
        
        with open(daily_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Created daily note: {daily_file}")
        return daily_file
        
    def analyze_vault_metrics(self) -> Dict:
        """Analyze vault for productivity metrics"""
        metrics = {
            'total_files': 0,
            'daily_notes': 0,
            'claude_sessions': 0,
            'projects': 0,
            'ideas': 0,
            'knowledge_notes': 0,
            'recent_activity': []
        }
        
        for folder in self.vault_path.iterdir():
            if folder.is_dir() and not folder.name.startswith('.'):
                files = list(folder.glob('*.md'))
                metrics['total_files'] += len(files)
                
                if folder.name == "01-Daily":
                    metrics['daily_notes'] = len(files)
                elif folder.name == "04-Projects":
                    metrics['projects'] = len(files)
                elif folder.name == "05-Ideas":
                    metrics['ideas'] = len(files)
                elif folder.name == "06-Knowledge":
                    metrics['knowledge_notes'] = len(files)
                elif folder.name == "09-Claude-Integration":
                    metrics['claude_sessions'] = len(files)
                    
                # Track recent files
                for file in files:
                    if file.stat().st_mtime > (datetime.datetime.now() - datetime.timedelta(days=7)).timestamp():
                        metrics['recent_activity'].append({
                            'file': str(file),
                            'modified': datetime.datetime.fromtimestamp(file.stat().st_mtime).isoformat()
                        })
                        
        return metrics
        
    def generate_insights_report(self) -> str:
        """Generate insights about vault usage and patterns"""
        metrics = self.analyze_vault_metrics()
        
        report = f"""# Vault Analytics Report
**Generated:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}

## Overview Metrics
- **Total Files:** {metrics['total_files']}
- **Daily Notes:** {metrics['daily_notes']}
- **Claude Sessions:** {metrics['claude_sessions']}
- **Active Projects:** {metrics['projects']}
- **Ideas Captured:** {metrics['ideas']}
- **Knowledge Notes:** {metrics['knowledge_notes']}

## Recent Activity
**Files Modified in Last 7 Days:** {len(metrics['recent_activity'])}

## Productivity Insights
- **Daily Note Consistency:** {self._calculate_daily_consistency()}%
- **Session Frequency:** {metrics['claude_sessions'] / max(metrics['daily_notes'], 1):.1f} sessions per day
- **Idea Generation Rate:** {metrics['ideas'] / max(metrics['daily_notes'], 1):.1f} ideas per day

## Recommendations
{self._generate_recommendations(metrics)}

---
**Tags:** #analytics #insights #productivity
**Next Report:** {(datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')}
"""
        
        analytics_file = self.vault_path / "11-Analytics" / f"insights-{datetime.date.today()}.md"
        analytics_file.parent.mkdir(exist_ok=True)
        
        with open(analytics_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"Generated insights report: {analytics_file}")
        return report
        
    def _calculate_daily_consistency(self) -> float:
        """Calculate daily note consistency percentage"""
        daily_folder = self.vault_path / "01-Daily"
        if not daily_folder.exists():
            return 0.0
            
        daily_files = list(daily_folder.glob('*.md'))
        if not daily_files:
            return 0.0
            
        # Count days in the last 30 days
        thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
        recent_files = 0
        
        for file in daily_files:
            try:
                file_date = datetime.datetime.strptime(file.stem, '%Y-%m-%d').date()
                if file_date >= thirty_days_ago:
                    recent_files += 1
            except ValueError:
                continue
                
        return (recent_files / 30) * 100
        
    def _generate_recommendations(self, metrics: Dict) -> str:
        """Generate recommendations based on metrics"""
        recommendations = []
        
        if metrics['daily_notes'] == 0:
            recommendations.append("- Start daily journaling to track progress and insights")
            
        if metrics['claude_sessions'] / max(metrics['daily_notes'], 1) < 0.5:
            recommendations.append("- Increase Claude Code integration for enhanced productivity")
            
        if metrics['ideas'] / max(metrics['daily_notes'], 1) < 1:
            recommendations.append("- Focus on capturing more ideas during daily sessions")
            
        if len(metrics['recent_activity']) / metrics['total_files'] < 0.1:
            recommendations.append("- Review and update existing notes to maintain knowledge freshness")
            
        if not recommendations:
            recommendations.append("- Great consistency! Continue current practices and explore advanced workflows")
            
        return "\n".join(recommendations)

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Claude Code Obsidian Integration")
    parser.add_argument('--vault', default='.', help='Path to Obsidian vault')
    parser.add_argument('--action', required=True, 
                       choices=['session', 'daily', 'memory', 'insights'],
                       help='Action to perform')
    parser.add_argument('--type', default='general', help='Session or memory type')
    parser.add_argument('--project', default='', help='Project name')
    parser.add_argument('--goal', default='', help='Session goal')
    
    args = parser.parse_args()
    
    integration = ObsidianClaudeIntegration(args.vault)
    
    if args.action == 'session':
        integration.create_session_log(args.type, args.project, args.goal)
    elif args.action == 'daily':
        integration.create_daily_note()
    elif args.action == 'memory':
        # Example memory update
        context_data = {
            'info': 'New session started',
            'patterns': 'User prefers structured templates',
            'decisions': 'Using Python for automation',
            'next_context': 'Continue with workflow optimization'
        }
        integration.update_agent_memory(context_data, args.type)
    elif args.action == 'insights':
        integration.generate_insights_report()

if __name__ == "__main__":
    main()
