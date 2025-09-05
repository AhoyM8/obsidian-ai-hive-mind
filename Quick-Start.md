# Quick Start Guide

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
