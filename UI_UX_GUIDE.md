# UI/UX Guide

## Theme: Modern Minimal SaaS

**Feeling:**
- Clean, Minimal, Modern, Professional, Student-Friendly
- High-contrast, SaaS dashboard feel
- White background with soft gray sections
- Clean and mobile-first

### Colors

```css
:root {
  --background: #FFFFFF;
  --surface: #FFFFFF;
  --surface-soft: #F8FAFC;
  --text: #0F172A;
  --muted: #64748B;
  --border: #E2E8F0;
  --primary: #2563EB; /* primary blue */
  --primary-dark: #1D4ED8; /* dark blue */
  --accent: #3B82F6; /* vibrant blue */
  --success: #16A34A;
  --danger: #DC2626;
  --warning: #F59E0B;
  --ai-accent: #6D28D9;
}
```

### Typography

```css
body, h1, h2, h3, h4, h5, h6 {
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: var(--text);
}

body {
  background-color: var(--background);
}

h1, h2, h3, h4, h5, h6 {
  font-weight: 700;
}
```

### Design Principles

1. **Mobile-First Layout:** 
   - Cards stack vertically on mobile (specifically using grid breakpoint triggers to switch from 2-column or 1.5-column layouts to single-column layouts).
   - Use bottom navigation for students on mobile with clear icons (📊, 📚, 📝, ❓) and text labels, while automatically hiding redundant top-header navigation links.
   - Pad the body bottom (`padding-bottom: 80px`) to prevent bottom navigation overlaps with footer or content blocks.
   - Offset the fixed quiz submission footer above the bottom navigation bar (`bottom: 60px`) on mobile viewports.
   - Stack button groups vertically on screens under 480px wide to provide full-width, easy-to-tap touch targets.
   - Use a sidebar for admin interfaces on desktop (collapsible on mobile).
2. **Component Aesthetics:**
   - Use crisp, clean borders (`--border`).
   - Cards should have a white background (`--surface`) with subtle rounded corners, clean 1px borders, and extremely soft shadows.
   - Buttons should be rounded (6px border-radius) and use primary blue, white outline, or borderless styles.
   - Form fields should be styled with thin borders, clean backgrounds, and a subtle blue glow shadow when focused.
3. **Impersonation Banner:**
   - Must be prominent at the top of every page during an active impersonation session.
5. **Information Architecture (Academic Hierarchy):**
   - Structure follows: `Subject` &rarr; `Unit / Chapter` &rarr; `Resource` (Study Material, PYQ, Quiz).
   - Subject-level resources are those created without a specific unit link (`unit_id` is null). They appear directly on the Subject details view.
   - Unit-level resources are those created with a unit link (`unit_id` is defined). They appear exclusively on the Unit details page.
   - The primary flow for admins and students traces: Dashboard &rarr; Subject Details &rarr; Unit Details.
   - Consistent academic breadcrumbs must be visible at the top of Subject and Unit detail layouts.
6. **Interactive Quiz Attempts**: Student quiz attempt layout renders all questions. A live, client-side toggle switcher allows switching modes at any time. Learning Mode provides check-buttons next to options for checking explanations immediately, using light red and green styling to guide correctness visually without cluttering.
7. **Card Interactivity**: Subject cards on the student dashboard use soft blue highlights and scale slightly on hover (`.card-clickable`) to make the interface feel alive. They also present quantitative summaries (units, quizzes, resources count) to avoid dead layouts.
8. **Context-Rich Available Items**: All listed items (such as quizzes) must describe their placement in the Subject/Unit structure.
9. **Real-Time Instant Filters**: List structures (subjects directory) are equipped with real-time text input matching name, code, semester, and description with immediate empty-state warnings.
10. **Notifications UI & Subscription States**: The notification bell displays a small numeric badge (`--danger`) when unread items exist. Notification card elements share the soft borders (`--border`) and clean card shapes of the standard dashboard layout. Subject subscription buttons change dynamically from "🔔 Subscribe" (outlined blue) to "🔕 Unsubscribe" (solid blue/filled) to ensure immediate visual feedback of subscription status.
11. **Community Library**: Clean card layout displaying material titles, subject names, description previews, material types, and optional college tag labels. Dynamic filtering options include search keywords, material types, college tag filters, and sorting parameters (latest, views, likes, and rating). Soft, rounded badges are used to represent tags. Empty states provide feedback when no results match the filter criteria. Shared upload forms are clean, outlining file limits (5MB maximum, PDF only) and offering dual-method inputs (PDF upload or external URL) inside a clear dashed container.

### Avoid:
- Bakery/cafe styling, cream backgrounds, and brown colors.
- Decorative Roman/serif heading fonts (like Cormorant Garamond).
- Heavy gradients, neon colors, and cluttered layouts.
