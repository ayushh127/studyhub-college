# AI Agent Guide (AGENTS.md)

This file serves as a reference for AI agents assisting with the development or maintenance of StudyHub College. 

## Project Context
- **Name:** StudyHub College
- **Goal:** Multi-college study platform for managing materials, PYQs, and quizzes.
- **Current State:** MVP Phase. No AI features, subscriptions, or native mobile apps are included in the MVP.
- **Tech Stack:** Python Flask, Flask-SQLAlchemy, SQLite, Jinja2, Vanilla CSS/JS.

## Rules for AI Agents
1. **Maintain Context:** Always read `PROJECT_PLAN.md`, `TASKS.md`, and `CHANGELOG.md` when resuming or starting a new task to understand the current progress.
2. **File Updates:** After completing any major implementation step, you MUST update:
   - `TASKS.md`
   - `CHANGELOG.md`
   - `PROJECT_PLAN.md`
3. **No Unprompted Creations:** Do not create random folders or placeholder logic outside the agreed scope. Follow the structure defined in `PROJECT_PLAN.md` and `ROUTES.md`.
4. **Theme Enforcement:** Adhere strictly to the "Classical Minimal Academic" theme as defined in `UI_UX_GUIDE.md`. Avoid generic SaaS styles, heavy gradients, or neon colors.
5. **Future Readiness:** Write clean, modular code so that features described in `FUTURE_AI_FEATURES.md` can be integrated later without massive refactoring.
