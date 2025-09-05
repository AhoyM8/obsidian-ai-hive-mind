# Week {{date:YYYY-[W]WW}} - {{date:MMMM DD, YYYY}}

## 📈 Weekly Overview
**Period:** {{monday:YYYY-MM-DD}} to {{sunday:YYYY-MM-DD}}

### Key Metrics
```dataview
TABLE sum(words-written) as "Words", sum(commits) as "Commits", sum(deep-work-hours) as "Deep Work"
FROM "01-Daily"
WHERE file.cday >= date("{{monday:YYYY-MM-DD}}") AND file.cday <= date("{{sunday:YYYY-MM-DD}}")
```

## 🎯 Goals Review
### Weekly Objectives Status
- [ ] Goal 1: 
  - Progress: /100%
  - Blockers:
  - Next steps:
- [ ] Goal 2:
  - Progress: /100%
  - Blockers:
  - Next steps:

### Project Advancement
```dataview
TABLE status, progress, next-milestone
FROM "04-Projects"
WHERE last-updated >= date("{{monday:YYYY-MM-DD}}")
```

## 🧠 Claude Code Integration Insights
### Most Productive Sessions
- 

### Pattern Recognition
- Common request types:
- Workflow optimizations discovered:
- Agent utilization patterns:

### Knowledge Expansion
- New concepts learned:
- Skills developed:
- Tools discovered:

## 💡 Idea Evolution
### Ideas Generated This Week
```dataview
LIST
FROM "05-Ideas"
WHERE file.cday >= date("{{monday:YYYY-MM-DD}}")
SORT file.cday DESC
```

### Ideas Developed/Implemented
- 

## 📊 Process Analysis
### What Worked Well
- 

### Areas for Improvement
- 

### Systems & Workflows
- New processes implemented:
- Existing processes optimized:
- Deprecated practices:

## 🔮 Next Week Planning
### Primary Focus Areas
- [ ] 
- [ ] 
- [ ] 

### Resource Allocation
- Deep work blocks planned:
- Learning time allocated:
- Creative time scheduled:

### Agent & Memory Setup
- Context updates needed:
- New agent roles to configure:
- Memory consolidation tasks:

## 🌟 Highlights & Wins
- 

## 🤔 Challenges & Learnings
- 

## 🔗 Connected Knowledge
### Key Connections Made
- 

### Cross-Domain Insights
- 

---
**Tags:** #weekly #review #{{date:YYYY}} #{{date:MMMM}} #planning
**Created:** {{date:YYYY-MM-DD HH:mm}}
**Next Review:** {{date+7d:YYYY-MM-DD}}
**Agent Memory Update:** [[Agent-Memory-Week-{{date:YYYY-[W]WW}}]]