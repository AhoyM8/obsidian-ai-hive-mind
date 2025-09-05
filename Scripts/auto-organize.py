#!/usr/bin/env python3
"""
Automated File Organization for Obsidian Vault
Intelligently moves files to appropriate folders based on content and metadata
"""

import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
import frontmatter

class VaultOrganizer:
    """Automated file organization for Obsidian vault"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.inbox_folder = self.vault_path / "00-Inbox"
        self.rules = self._load_organization_rules()
        
    def _load_organization_rules(self) -> Dict:
        """Load file organization rules"""
        return {
            'patterns': {
                # Date-based patterns
                r'^\d{4}-\d{2}-\d{2}(?!-)': '01-Daily',
                r'(?i)week\s*\d+|weekly': '02-Weekly', 
                r'(?i)month|monthly': '03-Monthly',
                
                # Content-based patterns
                r'(?i)project|charter|roadmap': '04-Projects',
                r'(?i)idea|concept|innovation': '05-Ideas',
                r'(?i)knowledge|learning|notes': '06-Knowledge',
                r'(?i)claude|session|agent': '09-Claude-Integration',
                r'(?i)memory|context|agent-memory': '10-Agent-Memory',
                r'(?i)template': '08-Templates',
                r'(?i)archive|old|deprecated': '07-Archives'
            },
            'tags': {
                '#daily': '01-Daily',
                '#weekly': '02-Weekly',
                '#monthly': '03-Monthly',
                '#project': '04-Projects',
                '#idea': '05-Ideas',
                '#knowledge': '06-Knowledge',
                '#claude-session': '09-Claude-Integration',
                '#agent-memory': '10-Agent-Memory',
                '#template': '08-Templates',
                '#archive': '07-Archives'
            },
            'frontmatter': {
                'type': {
                    'daily': '01-Daily',
                    'weekly': '02-Weekly', 
                    'monthly': '03-Monthly',
                    'project': '04-Projects',
                    'idea': '05-Ideas',
                    'knowledge': '06-Knowledge',
                    'session': '09-Claude-Integration',
                    'memory': '10-Agent-Memory',
                    'template': '08-Templates'
                },
                'status': {
                    'archive': '07-Archives',
                    'deprecated': '07-Archives'
                }
            }
        }
    
    def organize_inbox(self, dry_run: bool = False) -> List[Dict]:
        """Organize all files in the inbox"""
        if not self.inbox_folder.exists():
            print("Inbox folder doesn't exist")
            return []
            
        results = []
        for file_path in self.inbox_folder.glob('*.md'):
            result = self._organize_file(file_path, dry_run)
            if result:
                results.append(result)
                
        return results
    
    def _organize_file(self, file_path: Path, dry_run: bool = False) -> Optional[Dict]:
        """Organize a single file based on content analysis"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse frontmatter if present
            try:
                post = frontmatter.loads(content)
                metadata = post.metadata
                content_only = post.content
            except:
                metadata = {}
                content_only = content
                
            # Determine target folder
            target_folder = self._determine_target_folder(
                file_path.name, content_only, metadata
            )
            
            if not target_folder:
                return None
                
            # Create target path
            target_dir = self.vault_path / target_folder
            target_dir.mkdir(exist_ok=True)
            target_path = target_dir / file_path.name
            
            # Handle name conflicts
            if target_path.exists():
                target_path = self._resolve_name_conflict(target_path)
                
            result = {
                'source': str(file_path),
                'target': str(target_path),
                'folder': target_folder,
                'reason': self._get_organization_reason(file_path.name, content_only, metadata)
            }
            
            if not dry_run:
                shutil.move(str(file_path), str(target_path))
                print(f"Moved: {file_path.name} -> {target_folder}/")
            else:
                print(f"Would move: {file_path.name} -> {target_folder}/")
                
            return result
            
        except Exception as e:
            print(f"Error organizing {file_path}: {e}")
            return None
    
    def _determine_target_folder(self, filename: str, content: str, metadata: Dict) -> Optional[str]:
        """Determine the target folder for a file"""
        # 1. Check frontmatter metadata
        if metadata:
            for key, value_map in self.rules['frontmatter'].items():
                if key in metadata:
                    value = str(metadata[key]).lower()
                    if value in value_map:
                        return value_map[value]
        
        # 2. Check for tags in content
        tags = re.findall(r'#[\w-]+', content)
        for tag in tags:
            if tag in self.rules['tags']:
                return self.rules['tags'][tag]
                
        # 3. Check filename patterns
        for pattern, folder in self.rules['patterns'].items():
            if re.search(pattern, filename):
                return folder
                
        # 4. Check content patterns
        for pattern, folder in self.rules['patterns'].items():
            if re.search(pattern, content[:1000]):  # Check first 1000 chars
                return folder
                
        # 5. Special date detection
        if self._is_daily_note(filename, content):
            return '01-Daily'
            
        return None
    
    def _is_daily_note(self, filename: str, content: str) -> bool:
        """Check if file appears to be a daily note"""
        # Check for date in filename
        if re.match(r'^\d{4}-\d{2}-\d{2}', filename):
            return True
            
        # Check for daily note content patterns
        daily_patterns = [
            r'(?i)morning\s+intentions?',
            r'(?i)daily\s+tasks?',
            r'(?i)evening\s+reflection',
            r'(?i)gratitude',
            r'(?i)today(?:\s|\')?s?\s+(?:goals?|priorities?|focus)'
        ]
        
        return any(re.search(pattern, content) for pattern in daily_patterns)
    
    def _get_organization_reason(self, filename: str, content: str, metadata: Dict) -> str:
        """Get the reason why file was organized to specific folder"""
        # Check metadata first
        if metadata:
            for key, value_map in self.rules['frontmatter'].items():
                if key in metadata:
                    value = str(metadata[key]).lower()
                    if value in value_map:
                        return f"Frontmatter {key}: {value}"
        
        # Check tags
        tags = re.findall(r'#[\w-]+', content)
        for tag in tags:
            if tag in self.rules['tags']:
                return f"Tag: {tag}"
                
        # Check patterns
        for pattern, folder in self.rules['patterns'].items():
            if re.search(pattern, filename):
                return f"Filename pattern: {pattern}"
            if re.search(pattern, content[:1000]):
                return f"Content pattern: {pattern}"
                
        return "Manual classification"
    
    def _resolve_name_conflict(self, target_path: Path) -> Path:
        """Resolve naming conflicts by adding timestamp"""
        timestamp = datetime.now().strftime("%H%M%S")
        stem = target_path.stem
        suffix = target_path.suffix
        
        new_name = f"{stem}-{timestamp}{suffix}"
        return target_path.parent / new_name
    
    def create_organization_report(self, results: List[Dict]) -> str:
        """Create a report of organization actions"""
        if not results:
            return "No files were organized."
            
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        report = f"""# File Organization Report
**Generated:** {timestamp}
**Files Processed:** {len(results)}

## Organization Summary
"""
        
        # Group by folder
        folder_counts = {}
        for result in results:
            folder = result['folder']
            folder_counts[folder] = folder_counts.get(folder, 0) + 1
            
        for folder, count in sorted(folder_counts.items()):
            report += f"- **{folder}:** {count} files\n"
            
        report += "\n## Detailed Actions\n"
        
        for result in results:
            filename = Path(result['source']).name
            report += f"- `{filename}` → **{result['folder']}** ({result['reason']})\n"
            
        report += f"""
## Organization Rules Applied
### Frontmatter Rules
- `type: daily` → 01-Daily
- `type: project` → 04-Projects  
- `type: idea` → 05-Ideas
- `status: archive` → 07-Archives

### Tag-based Rules
- `#daily` → 01-Daily
- `#project` → 04-Projects
- `#idea` → 05-Ideas
- `#claude-session` → 09-Claude-Integration

### Pattern-based Rules
- Date format (YYYY-MM-DD) → 01-Daily
- "project", "charter" → 04-Projects
- "idea", "concept" → 05-Ideas
- "claude", "session" → 09-Claude-Integration

---
**Tags:** #organization #automation #vault-maintenance
**Next Organization:** {(datetime.now().strftime('%Y-%m-%d'))}
"""
        
        return report
    
    def setup_auto_organization(self) -> None:
        """Set up automatic organization rules and scripts"""
        # Create organization config
        config_path = self.vault_path / ".obsidian" / "organization-config.json"
        config = {
            "auto_organize": True,
            "watch_folders": ["00-Inbox"],
            "organization_rules": self.rules,
            "schedule": {
                "frequency": "daily",
                "time": "09:00"
            },
            "notifications": True,
            "dry_run_first": True
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
            
        print(f"Created organization config: {config_path}")
        
        # Create automation script
        automation_script = self.vault_path / "Scripts" / "daily-organization.py"
        script_content = f"""#!/usr/bin/env python3
import sys
import os
sys.path.append('{self.vault_path / "Scripts"}')

from auto_organize import VaultOrganizer

def main():
    organizer = VaultOrganizer(r'{self.vault_path}')
    
    # Run dry run first
    print("=== DRY RUN ===")
    results = organizer.organize_inbox(dry_run=True)
    
    if results:
        confirm = input(f"Organize {{len(results)}} files? (y/N): ")
        if confirm.lower() == 'y':
            print("=== ACTUAL RUN ===")
            results = organizer.organize_inbox(dry_run=False)
            
            # Create report
            report = organizer.create_organization_report(results)
            report_path = r'{self.vault_path}' + "/11-Analytics/organization-" + str(datetime.date.today()) + ".md"
            
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(report)
                
            print(f"Organization complete! Report saved to {{report_path}}")
    else:
        print("No files to organize.")

if __name__ == "__main__":
    main()
"""
        
        with open(automation_script, 'w', encoding='utf-8') as f:
            f.write(script_content)
            
        print(f"Created automation script: {automation_script}")

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Vault File Organization")
    parser.add_argument('--vault', default='.', help='Path to Obsidian vault')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be moved without moving')
    parser.add_argument('--setup', action='store_true', help='Set up auto-organization')
    
    args = parser.parse_args()
    
    organizer = VaultOrganizer(args.vault)
    
    if args.setup:
        organizer.setup_auto_organization()
    else:
        results = organizer.organize_inbox(dry_run=args.dry_run)
        
        if results:
            report = organizer.create_organization_report(results)
            print("\n" + "="*50)
            print(report)
        else:
            print("No files found to organize.")

if __name__ == "__main__":
    main()