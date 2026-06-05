# UI/UX Guide

## Theme: Classical Minimal Academic

**Feeling:**
- Minimal, Premium, Calm, Academic
- Modern Roman library feel
- Old parchment/study desk inspiration
- Clean and mobile-first

### Colors

```css
:root {
  --background: #FAF7F0; /* warm cream */
  --surface: #FFFFFF; /* white */
  --surface-soft: #F3EBDD; /* parchment/ivory */
  --primary: #8B5E34; /* classical brown/walnut */
  --primary-dark: #5C3A21;
  --accent: #FFB340; /* light golden-orange */
  --text: #1F1A17; /* warm charcoal */
  --muted: #7A6F64; /* brown-gray */
  --border: #E5D6C3;
  --success: #2F855A;
  --danger: #B42318;
  --warning: #B7791F;
  --ai-accent: #6D28D9; /* royal purple, for future use only */
}
```

### Typography

```css
body {
  font-family: 'Inter', system-ui, sans-serif;
  color: var(--text);
  background-color: var(--background);
}

h1, h2, h3 {
  font-family: 'Cormorant Garamond', serif;
  color: var(--primary-dark);
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
   - Use soft, warm borders (`--border`).
   - Cards should have a white background (`--surface`) with subtle rounded corners and very soft shadows.
   - Buttons should be touch-friendly (min 44px height on mobile).
3. **Impersonation Banner:**
   - Must be prominent at the top of every page during an active impersonation session.
5. **Information Architecture (Academic Hierarchy):**
   - Structure follows: `Subject` &rarr; `Unit / Chapter` &rarr; `Resource` (Study Material, PYQ, Quiz).
   - Subject-level resources are those created without a specific unit link (`unit_id` is null). They appear directly on the Subject details view.
   - Unit-level resources are those created with a unit link (`unit_id` is defined). They appear exclusively on the Unit details page.
   - The primary flow for admins and students traces: Dashboard &rarr; Subject Details &rarr; Unit Details.
   - Consistent academic breadcrumbs must be visible at the top of Subject and Unit detail layouts.
- **Interactive Quiz Attempts**: Student quiz attempt layout renders all questions. A live, client-side toggle switcher allows switching modes at any time. Learning Mode provides check-buttons next to options for checking explanations immediately, using light red and green styling to guide correctness visually without cluttering.
- **Card Interactivity**: Subject cards on the student dashboard use soft parchment/brown highlights and scale slightly on hover (`.card-clickable`) to make the interface feel alive. They also present quantitative summaries (units, quizzes, resources count) to avoid dead layouts.
- **Context-Rich Available Items**: All listed items (such as quizzes) must describe their placement in the Subject/Unit structure.
- **Real-Time Instant Filters**: List structures (subjects directory) are equipped with real-time text input matching name, code, semester, and description with immediate empty-state warnings.
- **Notifications UI & Subscription States**: The notification bell should display a small numeric badge (`--danger`) when unread items exist. Notification card elements should share the soft borders (`--border`) and clean card shapes of the standard dashboard layout. Subject subscription buttons must change dynamically from "🔔 Subscribe" (outlined) to "🔕 Unsubscribe" (solid brown/filled) to ensure immediate visual feedback of subscription status.

### Avoid:
- Generic blue SaaS themes.
- Neon colors.
- Heavy gradients.
- Cluttered UIs.
