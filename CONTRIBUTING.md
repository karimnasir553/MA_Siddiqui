# Supervisor Collaboration Guide

This document explains how **Prof. Dr.-Ing. habil. Philipp Beckerle** and other supervisors can give feedback, track progress, and ask questions — entirely through the GitHub web interface, with no Git knowledge required.

---

## Giving Feedback via Issues

Every piece of feedback, question, or task lives as a **GitHub Issue**. This keeps everything searchable, traceable, and linked to the relevant code.

### How to Open an Issue

1. Go to the repository on GitHub
2. Click the **"Issues"** tab at the top
3. Click the green **"New issue"** button
4. Choose a template (see below) and fill in the fields
5. Click **"Submit new issue"**

That's it. The student will be notified automatically.

---

## Issue Templates

### Feedback
Use this when you have comments on a chapter, figure, or piece of code.

**Fields:**
- Section/Chapter affected
- Type: Writing / Code / Results / General
- Description of feedback
- Priority: High / Medium / Low

### Task
Use this to assign a specific piece of work.

**Fields:**
- Task description
- Related project phase
- Deadline
- Done when... (acceptance criteria)

### Question
Use this when you need clarification on something.

**Fields:**
- Your question
- Context (what you were looking at)
- Needed by (date)

---

## Leaving Comments on Code

1. Go to the **"Pull Requests"** tab
2. Open any open PR
3. Click the **"Files changed"** tab
4. Click the **+** icon next to any line to leave an inline comment
5. Click **"Start a review"** or **"Add single comment"**

---

## Milestone Structure

Progress is tracked across five milestones:

| Milestone | Target Date | Scope |
|-----------|-------------|-------|
| 1 — Literature Review & Setup | ~1 July 2025 | Background reading, repo set up, SQL pipeline running |
| 2 — SQL Pipeline & Benchmark | ~22 July 2025 | SQL data processed, LSTM trained, KernelSHAP baseline done |
| 3 — All Robot Data Collected | ~19 August 2025 | ROS2 data collected for all three failure scenarios |
| 4 — Full SHAP Analysis | ~16 September 2025 | TimeSHAP + WinIT complete, all comparison figures generated |
| 5 — Thesis Submitted | ~21 October 2025 | Final PDF submitted |

---

## Labels

| Label | Meaning |
|-------|---------|
| `feedback` | General supervisor comment |
| `writing` | Concerns the thesis text |
| `code` | Concerns the code or experiments |
| `question` | A question that needs an answer |
| `urgent` | Needs attention before the next meeting |
| `discussion` | Agenda item for the next meeting |

---

## No Git Required

You never need to use the command line. Everything described above works entirely through the GitHub website at `github.com/<repo>`.
