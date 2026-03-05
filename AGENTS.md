# Agent Rules

## UI Rule Compliance
- For any UI-related change, strictly follow `/home/mk/Documents/Github/Dogo-Corp/web-spider/.agents/ui-rule.md`.
- For UI improvements, also apply `/home/mk/Documents/Github/Dogo-Corp/web-spider/.agents/ui-modern-minimalism-sidebar.md`.
- Scope of mandatory application:
  - `**/*.html`
  - `**/*.erb`
  - `**/*.css`
  - `**/*.scss`
  - `**/*.js`
  - `**/*.ts`
  - `**/*.tsx`
  - `**/*.jsx`
  - `**/*.rb`
- If a request conflicts with the UI rule, prioritize the UI rule unless the user explicitly asks to override it.

## Plan Request Rule
- Trigger: when the user explicitly asks to "plan" (e.g. "plan", "hãy plan", "lập plan").
- Required behavior:
  1. Create a concrete execution plan before implementing changes.
  2. Save that plan to the `plans/` directory in this repository.

## Plan Output Format
- File location: `plans/`
- Filename format: `plan-YYYYMMDD-HHMMSS.md` (local time)
- Minimum sections:
  - `# Goal`
  - `# Assumptions`
  - `# Steps`
  - `# Validation`

## Function Ordering Rule
- Place helper functions below the main function that calls them.
- Example: if function `a()` calls function `b()`, then define `b()` below `a()`.

## Verification Rule
- After any code or configuration change, always run `poetry run lint` to verify before reporting completion.

## NiceGUI Native Elements Rule
- For UI work in this repository, prefer native DOM composition with `ui.element(...)` and CSS.
- Avoid NiceGUI Quasar convenience components for new UI (`ui.input`, `ui.button`, `ui.table`, `ui.dialog`, etc.) unless the user explicitly asks to use them.
- When a screen already exists with Quasar components and needs restyling, prioritize replacing those controls with native elements in the touched scope.
