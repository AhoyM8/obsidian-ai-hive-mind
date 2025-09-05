#!/usr/bin/env python3
import sys
import argparse
sys.path.append(r'Scripts')
from claude_integration import ObsidianClaudeIntegration

parser = argparse.ArgumentParser(description="Start Claude session")
parser.add_argument('--type', default='general', help='Session type')
parser.add_argument('--project', default='', help='Project name') 
parser.add_argument('--goal', default='', help='Session goal')

args = parser.parse_args()

integration = ObsidianClaudeIntegration(r'.')
session_file = integration.create_session_log(args.type, args.project, args.goal)
print(f"Session started: {session_file}")
