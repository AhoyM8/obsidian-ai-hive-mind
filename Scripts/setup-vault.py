#!/usr/bin/env python3
"""
Comprehensive Vault Setup and Automation
Sets up automated workflows, templates, and integrations for the Obsidian vault
"""

import os
import json
from pathlib import Path
from datetime import datetime, date
import shutil

class VaultSetup:
    """Complete vault setup and automation configuration"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.scripts_path = self.vault_path / "Scripts"
        
    def setup_automated_workflows(self):
        """Set up all automated workflows and schedules"""
        print("Setting up automated workflows...")
        
        # Create workflow automation script
        automation_script = self.scripts_path / "vault-automation.py"
        script_content = f"""#!/usr/bin/env python3
\"\"\"
Daily Vault Automation
Runs automated tasks for vault maintenance and optimization
\"\"\"

import sys
import os
from pathlib import Path
from datetime import datetime, date
import schedule
import time

sys.path.append(r'{self.scripts_path}')

try:
    from claude_integration import ObsidianClaudeIntegration
    from auto_organize import VaultOrganizer
except ImportError as e:
    print(f"Import error: {{e}}")
    print("Make sure all required scripts are in the Scripts folder")
    sys.exit(1)

class VaultAutomation:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.integration = ObsidianClaudeIntegration(vault_path)
        self.organizer = VaultOrganizer(vault_path)
        
    def daily_tasks(self):
        \"\"\"Run daily automation tasks\"\"\"
        print(f"Running daily tasks at {{datetime.now()}}")
        
        try:
            # Create daily note if it doesn't exist
            daily_file = self.integration.create_daily_note()
            print(f"Daily note ready: {{daily_file.name}}")
            
            # Organize inbox files
            results = self.organizer.organize_inbox(dry_run=False)
            if results:
                print(f"Organized {{len(results)}} files from inbox")
                
                # Create organization report
                report = self.organizer.create_organization_report(results)
                report_path = self.vault_path / "11-Analytics" / f"organization-{{date.today()}}.md"
                report_path.parent.mkdir(exist_ok=True)
                
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                    
            # Generate insights if it's Sunday
            if datetime.now().weekday() == 6:  # Sunday
                self.integration.generate_insights_report()
                print("Generated weekly insights report")
                
        except Exception as e:
            print(f"Error in daily tasks: {{e}}")
            
    def weekly_tasks(self):
        \"\"\"Run weekly automation tasks\"\"\"
        print(f"Running weekly tasks at {{datetime.now()}}")
        
        try:
            # Generate comprehensive insights
            self.integration.generate_insights_report()
            
            # Archive old session logs (older than 30 days)
            self.archive_old_files()
            
        except Exception as e:
            print(f"Error in weekly tasks: {{e}}")
            
    def archive_old_files(self):
        \"\"\"Archive files older than 30 days\"\"\"
        cutoff_date = datetime.now().timestamp() - (30 * 24 * 60 * 60)  # 30 days
        archived_count = 0
        
        # Archive old session logs
        claude_folder = self.vault_path / "09-Claude-Integration"
        archive_folder = self.vault_path / "07-Archives" / "Sessions"
        archive_folder.mkdir(parents=True, exist_ok=True)
        
        if claude_folder.exists():
            for file in claude_folder.glob("*.md"):
                if file.stat().st_mtime < cutoff_date:
                    shutil.move(str(file), str(archive_folder / file.name))
                    archived_count += 1
                    
        if archived_count > 0:
            print(f"Archived {{archived_count}} old session files")
            
    def run_scheduled_tasks(self):
        \"\"\"Set up and run scheduled tasks\"\"\"
        # Schedule daily tasks for 9 AM
        schedule.every().day.at("09:00").do(self.daily_tasks)
        
        # Schedule weekly tasks for Sunday at 10 AM  
        schedule.every().sunday.at("10:00").do(self.weekly_tasks)
        
        print("Vault automation scheduled. Press Ctrl+C to stop.")
        print("Daily tasks: 9:00 AM")
        print("Weekly tasks: Sunday 10:00 AM")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\\nVault automation stopped.")

def main():
    vault_path = r'{self.vault_path}'
    automation = VaultAutomation(vault_path)
    
    import argparse
    parser = argparse.ArgumentParser(description="Vault Automation")
    parser.add_argument('--run-now', action='store_true', help='Run daily tasks immediately')
    parser.add_argument('--schedule', action='store_true', help='Run scheduled automation')
    
    args = parser.parse_args()
    
    if args.run_now:
        automation.daily_tasks()
    elif args.schedule:
        automation.run_scheduled_tasks()
    else:
        print("Use --run-now for immediate execution or --schedule for automated scheduling")

if __name__ == "__main__":
    main()
"""
        
        with open(automation_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
            
        print(f"Created automation script: {automation_script}")
        
    def create_quick_commands(self):
        """Create quick command scripts for common tasks"""
        print("Creating quick command scripts...")
        
        # Quick daily note creation
        daily_script = self.scripts_path / "quick-daily.py"
        with open(daily_script, 'w', encoding='utf-8') as f:
            f.write(f"""#!/usr/bin/env python3
import sys
sys.path.append(r'{self.scripts_path}')
from claude_integration import ObsidianClaudeIntegration

integration = ObsidianClaudeIntegration(r'{self.vault_path}')
daily_file = integration.create_daily_note()
print(f"Daily note created: {{daily_file}}")
""")
        
        # Quick session start
        session_script = self.scripts_path / "quick-session.py"
        with open(session_script, 'w', encoding='utf-8') as f:
            f.write(f"""#!/usr/bin/env python3
import sys
import argparse
sys.path.append(r'{self.scripts_path}')
from claude_integration import ObsidianClaudeIntegration

parser = argparse.ArgumentParser(description="Start Claude session")
parser.add_argument('--type', default='general', help='Session type')
parser.add_argument('--project', default='', help='Project name') 
parser.add_argument('--goal', default='', help='Session goal')

args = parser.parse_args()

integration = ObsidianClaudeIntegration(r'{self.vault_path}')
session_file = integration.create_session_log(args.type, args.project, args.goal)
print(f"Session started: {{session_file}}")
""")
        
        # Quick insights
        insights_script = self.scripts_path / "quick-insights.py"
        with open(insights_script, 'w', encoding='utf-8') as f:
            f.write(f"""#!/usr/bin/env python3
import sys
sys.path.append(r'{self.scripts_path}')
from claude_integration import ObsidianClaudeIntegration

integration = ObsidianClaudeIntegration(r'{self.vault_path}')
report = integration.generate_insights_report()
print("Insights report generated!")
""")
        
        # Quick organization
        organize_script = self.scripts_path / "quick-organize.py"
        with open(organize_script, 'w', encoding='utf-8') as f:
            f.write(f"""#!/usr/bin/env python3
import sys
sys.path.append(r'{self.scripts_path}')
from auto_organize import VaultOrganizer

organizer = VaultOrganizer(r'{self.vault_path}')

# Show what would be organized
print("=== Files to organize ===")
results = organizer.organize_inbox(dry_run=True)

if results:
    confirm = input(f"\\nOrganize {{len(results)}} files? (y/N): ")
    if confirm.lower() == 'y':
        results = organizer.organize_inbox(dry_run=False)
        report = organizer.create_organization_report(results)
        print("\\n" + report)
else:
    print("No files to organize.")
""")
        
        print("Created quick command scripts:")
        print(f"  - {daily_script.name}: Create daily note")
        print(f"  - {session_script.name}: Start Claude session")
        print(f"  - {insights_script.name}: Generate insights")
        print(f"  - {organize_script.name}: Organize files")
        
    def setup_obsidian_plugins_config(self):
        """Configure recommended Obsidian plugins and settings"""
        print("Setting up Obsidian plugin configurations...")
        
        obsidian_folder = self.vault_path / ".obsidian"
        
        # Core plugins configuration
        core_plugins = {
            "file-explorer": True,
            "global-search": True,
            "switcher": True,
            "graph": True,
            "backlink": True,
            "outgoing-link": True,
            "tag-pane": True,
            "page-preview": True,
            "daily-notes": True,
            "templates": True,
            "note-composer": True,
            "command-palette": True,
            "markdown-importer": True,
            "word-count": True,
            "open-with-default-app": True,
            "file-recovery": True
        }
        
        with open(obsidian_folder / "core-plugins.json", 'w') as f:
            json.dump(core_plugins, f, indent=2)
            
        # Daily notes plugin configuration
        daily_notes_config = {
            "folder": "01-Daily",
            "format": "YYYY-MM-DD", 
            "template": "08-Templates/Daily Journal.md"
        }
        
        with open(obsidian_folder / "daily-notes.json", 'w') as f:
            json.dump(daily_notes_config, f, indent=2)
            
        # Templates plugin configuration
        templates_config = {
            "folder": "08-Templates"
        }
        
        with open(obsidian_folder / "templates.json", 'w') as f:
            json.dump(templates_config, f, indent=2)
            
        print("Obsidian plugin configurations created")
        
    def create_readme_and_guides(self):
        """Create comprehensive documentation"""
        print("Creating documentation and guides...")
        
        # Main README
        readme_content = f"""# AI-Enhanced Obsidian Vault

A comprehensive personal knowledge management and productivity system integrating Obsidian with Claude Code for AI-assisted workflows.

## 🏗️ Vault Structure

```
{self.vault_path.name}/
├── 00-Inbox/           # Capture zone for new notes
├── 01-Daily/           # Daily journal entries  
├── 02-Weekly/          # Weekly reviews and planning
├── 03-Monthly/         # Monthly retrospectives
├── 04-Projects/        # Project documentation and tracking
├── 05-Ideas/           # Idea capture and development
├── 06-Knowledge/       # Structured knowledge notes
├── 07-Archives/        # Archived and deprecated content
├── 08-Templates/       # Note templates for consistency
├── 09-Claude-Integration/ # Claude session logs and workflows
├── 10-Agent-Memory/    # AI agent context and memory
├── 11-Analytics/       # Insights and metrics reports
├── Assets/             # Images, files, and media
└── Scripts/            # Automation and integration scripts
```

## 🤖 Claude Code Integration

### Quick Commands
```bash
# Create daily note
python Scripts/quick-daily.py

# Start Claude session  
python Scripts/quick-session.py --type development --project "vault-setup"

# Generate insights
python Scripts/quick-insights.py

# Organize inbox files
python Scripts/quick-organize.py
```

### Automation
```bash
# Run daily automation tasks
python Scripts/vault-automation.py --run-now

# Set up scheduled automation
python Scripts/vault-automation.py --schedule
```

## 📝 Templates

### Core Templates
- **Daily Journal**: Structured daily reflection and planning
- **Weekly Review**: Comprehensive weekly analysis and planning  
- **Monthly Retrospective**: Deep monthly reflection and goal setting
- **Project Charter**: Project planning and tracking
- **Claude Session Log**: AI interaction documentation
- **Idea Capture**: Systematic idea development
- **Knowledge Note**: Structured learning documentation

## 🔄 Workflows

### Daily Workflow
1. Open daily note (auto-created at 9 AM)
2. Set intentions and priorities
3. Log Claude sessions for tasks
4. Capture ideas and insights throughout day
5. Evening reflection and next-day preparation

### Weekly Workflow  
1. Review week's daily notes
2. Analyze productivity metrics
3. Update project statuses
4. Plan next week's focus areas
5. Generate insights report

### Monthly Workflow
1. Comprehensive retrospective
2. Goal alignment and adjustment
3. Knowledge synthesis
4. System optimization
5. Strategic planning

## 🧠 Agent Memory System

The vault maintains persistent context and memory for AI agents:

- **Master Memory**: Core user profile and preferences
- **Context Switching**: Protocols for maintaining context across sessions
- **Pattern Library**: Documented successful approaches and solutions
- **Decision History**: Record of choices and their outcomes

## 📊 Analytics & Insights

Automated analysis provides insights on:
- Productivity patterns and trends
- Knowledge graph evolution  
- Idea development pipeline
- Session effectiveness metrics
- Goal achievement tracking

## 🛠️ Setup Instructions

### Initial Setup
1. Install Python dependencies: `pip install schedule frontmatter`
2. Configure Obsidian plugins (see `.obsidian/` folder)
3. Run initial automation setup
4. Customize templates for your needs

### Daily Usage
1. Start with daily note creation
2. Log Claude sessions as you work
3. Capture ideas in inbox
4. Run organization script end of day

## 🎯 Optimization Tips

- Use templates consistently for better analytics
- Tag notes appropriately for organization
- Regular inbox processing prevents clutter
- Review agent memory weekly for accuracy
- Customize automation schedules to your rhythm

---

**Created:** {datetime.now().strftime('%Y-%m-%d')}
**Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
**Version:** 1.0
"""

        with open(self.vault_path / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        # Quick start guide
        quickstart_content = """# Quick Start Guide

## First Time Setup (5 minutes)

1. **Open Obsidian and point to this vault folder**
2. **Install recommended plugins** (prompts will appear)
3. **Create your first daily note:**
   ```bash
   python Scripts/quick-daily.py
   ```
4. **Start a Claude session:**
   ```bash
   python Scripts/quick-session.py --goal "Learn the vault system"
   ```

## Daily Routine (2 minutes)

### Morning (1 minute)
- Open daily note (automatically created at 9 AM)
- Set your top 3 priorities
- Review yesterday's outcomes

### Throughout Day
- Log Claude sessions in real-time
- Capture ideas immediately in inbox
- Use templates for consistency

### Evening (1 minute) 
- Complete reflection section
- Run quick organization: `python Scripts/quick-organize.py`
- Set tomorrow's context

## Weekly Routine (15 minutes)

### Sunday Planning
- Generate insights: `python Scripts/quick-insights.py`
- Review weekly template
- Set next week's goals
- Update project statuses

## Troubleshooting

### Common Issues
- **Can't find Python scripts**: Ensure you're in the vault root directory
- **Import errors**: Install dependencies: `pip install schedule frontmatter`
- **Permission errors**: Make sure scripts have execute permissions

### Getting Help
- Check the documentation in each folder
- Review agent memory files for context
- Look at session logs for patterns

---
**Next:** Explore the Templates folder to understand the structure
"""

        with open(self.vault_path / "Quick-Start.md", 'w', encoding='utf-8') as f:
            f.write(quickstart_content)
            
        print("Documentation created:")
        print(f"  - README.md: Complete system overview")
        print(f"  - Quick-Start.md: Getting started guide")
        
    def create_batch_files(self):
        """Create Windows batch files for easy command access"""
        print("Creating Windows batch files...")
        
        # Daily note batch file
        daily_bat = self.vault_path / "daily.bat"
        with open(daily_bat, 'w') as f:
            f.write(f"""@echo off
cd /d "{self.vault_path}"
python Scripts/quick-daily.py
pause
""")
        
        # Session start batch file  
        session_bat = self.vault_path / "session.bat"
        with open(session_bat, 'w') as f:
            f.write(f"""@echo off
cd /d "{self.vault_path}"
set /p project="Project name (optional): "
set /p goal="Session goal (optional): "
python Scripts/quick-session.py --project "%project%" --goal "%goal%"
pause
""")
        
        # Organize batch file
        organize_bat = self.vault_path / "organize.bat"
        with open(organize_bat, 'w') as f:
            f.write(f"""@echo off
cd /d "{self.vault_path}"
python Scripts/quick-organize.py
""")
        
        # Insights batch file
        insights_bat = self.vault_path / "insights.bat"
        with open(insights_bat, 'w') as f:
            f.write(f"""@echo off  
cd /d "{self.vault_path}"
python Scripts/quick-insights.py
pause
""")
        
        print("Created batch files for Windows:")
        print(f"  - daily.bat: Create daily note")
        print(f"  - session.bat: Start Claude session") 
        print(f"  - organize.bat: Organize files")
        print(f"  - insights.bat: Generate insights")

def main():
    """Main setup execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Vault Setup and Configuration")
    parser.add_argument('--vault', default='.', help='Path to Obsidian vault')
    parser.add_argument('--full-setup', action='store_true', help='Run complete setup')
    
    args = parser.parse_args()
    
    setup = VaultSetup(args.vault)
    
    if args.full_setup:
        print("Running complete vault setup...")
        setup.setup_automated_workflows()
        setup.create_quick_commands()
        setup.setup_obsidian_plugins_config()
        setup.create_readme_and_guides()
        setup.create_batch_files()
        print("\\n✅ Vault setup complete!")
        print("\\nNext steps:")
        print("1. Open Obsidian and point to this vault")
        print("2. Install recommended plugins when prompted")
        print("3. Run 'python Scripts/quick-daily.py' to start")
        print("4. Double-click 'daily.bat' for easy daily note creation")
    else:
        print("Use --full-setup to run complete vault configuration")

if __name__ == "__main__":
    main()