# Pre-Flight Checker

Stop last-minute launch scrambles. Know exactly what's blocking your event before it's too late.

## The Problem

You're two days from launch. Someone asks "Are we ready?" You scramble through Slack threads, spreadsheets, and tickets trying to piece together status. Database migration done? Security review complete? Feature flags configured? By the time you have an answer, you've lost an hour and discovered a critical blocker too late to fix.

**Pre-Flight Checker** gives you instant visibility into launch readiness—whether you're shipping software, running events, or deploying infrastructure.

## What It Does

- **Instant status**: See completion % across all launch categories in seconds
- **Clear blockers**: Know exactly what's preventing launch and which team owns it
- **No guesswork**: ✅/❌ status on every checklist item
- **Future**: Update checklists interactively or automate periodic checks

## Quick Start

```bash
pip install pyyaml
python main.py
```

**Output:**
```
security: 66.67%
- Penetration_test: ✅
- Security_review: ❌ <- blocker
- Secrets_rotated: ✅
------------------------
BLOCKERS:
- cdn_configured (infrastructure
- security_review (security)
- rollback_plan (readiness)
------------------------
```

## Your Checklist (YAML)

**Event Launch:**
```yaml
projectName: "security-workshop"
owner:
  name: John Doe
  email: john@example.com

participants:
  invites_sent: true
  flights_booked: false
  hotel_booked: true

program:
  scope: true
  speakers: true
  targets_acquired: false
```

**Software Deployment:**
```yaml
projectName: "v2.0-release"
owner:
  name: Jane Smith
  email: jane@example.com

infrastructure:
  database_migration: true
  cdn_configured: false
  monitoring_alerts: true

security:
  penetration_test: true
  security_review: false
  secrets_rotated: true

readiness:
  feature_flags_set: true
  rollback_plan: false
  load_testing: true
```

Adapt the categories to whatever you're launching. The tool is flexible.

## How It Helps

**Before any launch:**
- "Are we ready?" → Run the checker, get instant answer
- "What's blocking us?" → Clear list with ownership
- "Who do I need to chase?" → Category tells you which team

**During planning:**
- Track progress as items get completed (migrations, bookings, reviews)
- Share reports with stakeholders
- No more "where are we?" status meetings

**In production (coming soon):**
- Automated daily checks with Slack alerts
- Block deployments/events if checklist incomplete
- Team dashboard for distributed planning

## Roadmap

**✅ Phase 1: Core Reporting** (Complete)  
Clear status reports with blocker identification

**🚧 Phase 2: Interactive Updates** (Complete)  
Toggle checklist items and save changes from the CLI

**📋 Phase 3: Automation**  
Deploy to Cloud Run, run on schedule, weekly reports based on stakeholder type

## Why This Architecture

Built for both local use AND cloud automation from day one:

**Local:** Run the script, get instant feedback, update checklists  
**Cloud:** Scheduled checks, automated alerts, team dashboards

Same core logic, different interfaces. No rewrite needed when you're ready to automate.

---

**Built for:** Teams launching anything—software, events, infrastructure, products  
**Tech:** Python, PyYAML  
**Status:** Working CLI tool, cloud deployment in progress