#!/usr/bin/env python3
import sys
sys.path.append(r'Scripts')
from claude_integration import ObsidianClaudeIntegration

integration = ObsidianClaudeIntegration(r'.')
report = integration.generate_insights_report()
print("Insights report generated!")
