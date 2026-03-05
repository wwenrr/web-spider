# Modern Minimal Sidebar Research (Reference)

## Goal
Create a sidebar that feels modern, clean, and task-focused while keeping cognitive load low.

## Core Principles
1. Prioritize primary actions and reduce visible choices.
2. Keep hierarchy obvious with clear section grouping.
3. Use restrained visual styling (subtle borders, soft backgrounds, minimal decoration).
4. Preserve consistency in spacing, typography, and states.
5. Make navigation predictable and scannable.

## Sidebar Structure Standard
1. Header zone:
   - Brand mark/logo.
   - Product/context label.
   - One primary CTA (for the highest-value action).
2. Navigation zone:
   - Group items by purpose (e.g., Overview, Operations, Integrations).
   - Show only active/usable destinations as clickable links.
   - Keep not-yet-ready features non-clickable and clearly labeled (e.g., "Soon").
3. Footer zone:
   - User identity/profile shortcut.
   - Account actions (role badge, logout, etc.).

## Visual Rules
1. Keep a white base with neutral grays + one green accent (follow `.agents/ui-rule.md` tokens).
2. Use clear active state:
   - Stronger text weight.
   - Soft accent background.
   - Accent indicator (left border or equivalent).
3. Use subtle icon containers (small neutral background) for easier scanning.
4. Use one divider between major groups; avoid heavy separators.
5. Avoid decorative noise, gradients, or extra badges unless they communicate status.

## UX Behavior Rules
1. Primary CTA appears once, near the top.
2. Navigation labels should be short and action-oriented.
3. Disabled destinations:
   - Not clickable.
   - Lower contrast.
   - Optional small status tag ("Soon").
4. Hover transitions must be quick and subtle (about 150-200ms).
5. Maintain keyboard accessibility and visible focus states.

## Spacing & Sizing Baseline
1. Sidebar width: 240-280px desktop.
2. Section label spacing: compact but readable.
3. Item height: touch-friendly (about 40-44px minimum).
4. Use 8px spacing rhythm across paddings/margins.

## Implementation Checklist (Before Merge)
1. Does the sidebar have one clear primary CTA?
2. Are menu items grouped into logical sections?
3. Is active state immediately recognizable?
4. Are disabled/future items non-clickable and clearly marked?
5. Is visual noise reduced compared to previous version?
6. Does mobile layout still work without overlap or clipped content?
7. Does style remain compliant with `.agents/ui-rule.md`?

## Sources
- Nielsen Norman Group, Minimalist Design:
  https://www.nngroup.com/articles/minimalist-design/
- Material Design Navigation Patterns:
  https://m1.material.io/patterns/navigation.html
- Laws of UX, Hick’s Law:
  https://lawsofux.com/hicks-law/
