#!/usr/bin/env python3
import sys
sys.path.append(r'Scripts')
from auto_organize import VaultOrganizer

organizer = VaultOrganizer(r'.')

# Show what would be organized
print("=== Files to organize ===")
results = organizer.organize_inbox(dry_run=True)

if results:
    confirm = input(f"\nOrganize {len(results)} files? (y/N): ")
    if confirm.lower() == 'y':
        results = organizer.organize_inbox(dry_run=False)
        report = organizer.create_organization_report(results)
        print("\n" + report)
else:
    print("No files to organize.")
