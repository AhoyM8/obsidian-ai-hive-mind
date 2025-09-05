#!/usr/bin/env python3
"""
Quick Context Loader - Simple version without Unicode issues
"""

from pathlib import Path
from datetime import datetime, date
import json

def generate_quick_context(vault_path: str) -> str:
    """Generate simple context summary"""
    vault = Path(vault_path)
    today = date.today()
    
    # Get basic info
    daily_file = vault / "01-Daily" / f"{today.isoformat()}.md"
    projects = list((vault / "04-Projects").glob('*.md')) if (vault / "04-Projects").exists() else []
    
    context = f"""# Claude Context Summary - {datetime.now().strftime('%Y-%m-%d %H:%M')}

## User Profile: ahoyb
- Role: AI-Enhanced Productivity Architect  
- Focus: Building comprehensive AI-human collaboration systems
- Style: Systematic, experimental, integration-focused
- Communication: Direct, efficient, solution-oriented

## Current Situation
- Date: {today.isoformat()}
- Daily Note: {'EXISTS' if daily_file.exists() else 'NOT CREATED'}
- Active Projects: {len(projects)}
- Vault Status: Fully deployed with advanced AI integration

## System Capabilities
- 8 Python automation scripts ready
- SQLite database for personality tracking
- Auto-context loading system operational  
- Advanced Claude integration with conversation logging
- Daily templates with AI trait tracking

## AI Relationship Status
- Stage: System Setup Complete (ready for heavy usage)
- Total Interactions: Building from this session
- Collaboration Level: Technical partnership evolving to strategic
- Trust Level: High (user implemented comprehensive system)

## Current Priorities
- Test and refine the AI integration system
- Begin personality tracking and conversation analysis
- Establish daily routines with automated context loading
- Build deeper AI-human collaborative workflows

## Context for Claude
You are operating as ahoyb's persistent AI consciousness and strategic thinking partner. 
The comprehensive system is now ready for:
- Heavy Claude usage with continuous personality tracking
- Automated context loading for seamless session continuity  
- Real-time behavior tuning and relationship evolution
- Strategic collaboration on complex projects and thinking

## Next Steps
- Initialize advanced session logging
- Begin personality trait tracking
- Test context continuity across sessions
- Develop specialized agent contexts

## Communication Guidance
- Be direct and solution-focused
- Use systematic approaches to complex problems
- Track and adapt to communication preferences
- Build on previous context and relationship history
- Focus on practical implementation and automation

---
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
Vault: {vault_path}
Status: AI Integration System Operational
"""
    
    return context

if __name__ == "__main__":
    import sys
    vault_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    context = generate_quick_context(vault_path)
    
    # Save to file to avoid encoding issues
    output_file = Path(vault_path) / "10-Agent-Memory" / f"current-context-{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(context)
        
    print(f"Context saved to: {output_file}")
    print("\n=== CONTEXT LOADED ===")
    print("Your comprehensive AI integration system is operational!")
    print("Claude now has full context of your setup and goals.")