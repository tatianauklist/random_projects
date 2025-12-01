# Compliance Checker 🔍⚖️

*Because "trust me, it's fine" isn't a legal strategy.*

A Python-based document analyzer that hunts down risky language, overreaching claims, and compliance red flags in your text before they become expensive problems.

## What It Does

Scans documents for problematic language patterns based on configurable rule sets. Think of it as a paranoid lawyer in CLI form - it flags things like "guaranteed returns," "under any circumstances," "waive all rights," and other phrases that make compliance officers nervous.

**Originally started as a plothole detector for fiction.** Turns out the same tech that catches "character had blue eyes in chapter 2, brown eyes in chapter 7" is really good at catching "we guarantee no risk" followed by "you assume all liability."

## Features

- **YAML-based rule sets** - Easy to customize for different domains (legal, medical, financial, marketing)
- **Severity & category tracking** - Know what's critical vs. what's just questionable
- **Progressive disclosure** - Summary first, drill down if you want details
- **Actually readable output** - No raw JSON dumps, just clean formatted results

## Quick Start

**Install dependencies:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install pyyaml
```

**Run it:**
```bash
python3 compliance_checker.py
```

Point it at a document, pick a rule set, get violations. Simple.

## Rule Sets

Currently includes:
- **rules.yaml** - General compliance (financial claims, medical statements, urgency tactics)
- **legal_rules.yaml** - Contract red flags (unconscionable terms, rights waivers, IP overreach)

Add your own by creating a YAML file with this structure:
```yaml
exclusions:
  - word: "your problematic phrase"
    severity: critical  # critical, high, or medium
    category: your_category
```

## Example Output
```
23 potential issues found.

By Severity:
critical: 7
high: 14
medium: 2

By Category:
absolute_claim: 3
unfair_practice: 3
unconscionable: 2
...
```

Then drill into specifics if you want to see exactly where each violation appears.

## Use Cases

- **Legal teams** - Catch problematic contract language before it ships
- **Compliance officers** - Scan marketing copy, terms of service, privacy policies
- **Content reviewers** - Flag risky claims in product descriptions or promotional materials
- **QA for knowledge bases** - Find outdated or contradictory documentation

## Why This Exists

Sometimes you need to check if your TOS accidentally claims users "forfeit all rights under any circumstances" or if your marketing copy promises "guaranteed results with zero risk." This tool finds that stuff fast.

## Tech Stack

Python, regex, YAML, and a healthy distrust of absolute claims.

## Future Ideas

- Export reports to PDF/CSV
- Multi-document batch processing
- Custom severity thresholds
- Integration with document management systems
- Web interface (maybe)

## Contributing

Found a category of problematic language that should be flagged? Add it to a rule set and submit a PR. This tool gets better the more real-world compliance knowledge goes into it.

---

**Built because "I should check this for compliance issues" and "I will actually check this for compliance issues" are very different things.**
