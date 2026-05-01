# TSK-0411: CSS Variables for Theming
**Story:** STY-0404 | **Sprint:** - | **Status:** Done
**Assignee:** {CoderAgent} | **Estimate:** {hours}

## Description
Add CSS custom properties (variables) for theming and implement dark mode styles. Update styles.css to:
- Define color variables for both light and dark themes
- Add smooth transition (0.3s) for theme changes
- Prevent FOUC (Flash of Unstyled Content) on initial load
- Apply dark theme styles when [data-theme="dark"] is set on html/body

## Acceptance Criteria
- [ ] CSS variables defined for: background, text, border, accent, etc.
- [ ] Light theme (default) colors defined
- [ ] Dark theme colors defined under [data-theme="dark"]
- [ ] Smooth transition (0.3s) on color properties
- [ ] No FOUC - theme applied before paint (inline script in index.html)
- [ ] All existing components use CSS variables

## Dependencies
- None (can be done in parallel with TSK-0410)

## Execution Log
- *[2026-05-01]* Picked up by CoderAgent
- *[2026-05-01]* Completed — CSS variables for light/dark themes, smooth transitions, FOUC prevention script added