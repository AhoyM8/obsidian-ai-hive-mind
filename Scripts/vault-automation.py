#!/usr/bin/env python3
"""
Daily Vault Automation
Runs automated tasks for vault maintenance and optimization
"""

import sys
import os
from pathlib import Path
from datetime import datetime, date
import schedule
import time

sys.path.append(r'Scripts')

try:
    from claude_integration import ObsidianClaudeIntegration
    from auto_organize import VaultOrganizer
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all required scripts are in the Scripts folder")
    sys.exit(1)

class VaultAutomation:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.integration = ObsidianClaudeIntegration(vault_path)
        self.organizer = VaultOrganizer(vault_path)
        
    def daily_tasks(self):
        """Run daily automation tasks"""
        print(f"Running daily tasks at {datetime.now()}")
        
        try:
            # Create daily note if it doesn't exist
            daily_file = self.integration.create_daily_note()
            print(f"Daily note ready: {daily_file.name}")
            
            # Organize inbox files
            results = self.organizer.organize_inbox(dry_run=False)
            if results:
                print(f"Organized {len(results)} files from inbox")
                
                # Create organization report
                report = self.organizer.create_organization_report(results)
                report_path = self.vault_path / "11-Analytics" / f"organization-{date.today()}.md"
                report_path.parent.mkdir(exist_ok=True)
                
                with open(report_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                    
            # Generate insights if it's Sunday
            if datetime.now().weekday() == 6:  # Sunday
                self.integration.generate_insights_report()
                print("Generated weekly insights report")
                
        except Exception as e:
            print(f"Error in daily tasks: {e}")
            
    def weekly_tasks(self):
        """Run weekly automation tasks"""
        print(f"Running weekly tasks at {datetime.now()}")
        
        try:
            # Generate comprehensive insights
            self.integration.generate_insights_report()
            
            # Archive old session logs (older than 30 days)
            self.archive_old_files()
            
        except Exception as e:
            print(f"Error in weekly tasks: {e}")
            
    def archive_old_files(self):
        """Archive files older than 30 days"""
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
            print(f"Archived {archived_count} old session files")
            
    def run_scheduled_tasks(self):
        """Set up and run scheduled tasks"""
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
            print("\nVault automation stopped.")

def main():
    vault_path = r'.'
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
