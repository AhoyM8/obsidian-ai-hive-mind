#!/usr/bin/env python3
import sys
sys.path.append(r'Scripts')
from claude_integration import ObsidianClaudeIntegration

integration = ObsidianClaudeIntegration(r'.')
daily_file = integration.create_daily_note()
print(f"Daily note created: {daily_file}")
