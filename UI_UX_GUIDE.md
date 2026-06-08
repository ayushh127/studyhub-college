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
   - Use bottom navigation for students on mobile with clear icons (🏠 Home, 📚 Subjects, 🌐 Community, ❓ Quizzes, 👤 Profile) and text labels.
   - Hide student text navigation links from the top header on mobile viewports, keeping only App logo, mobile bell icon, and profile dropdown icon.
   - Collapse Community Library search filters on mobile viewports behind a toggle button while showing quick chips (Latest, Most Liked, Top Rated, PDFs, Links) directly.
   - Pad the body bottom (`padding-bottom: 80px`) to prevent bottom navigation overlaps with footer or content blocks.
   - Offset the fixed quiz submission footer above the bottom navigation bar (`bottom: 60px`) on mobile viewports.
   - Stack button groups, form inputs, search filters, and card containers vertically on screens under 768px wide to provide full-width, easy-to-tap touch targets.
   - Use a sidebar for admin interfaces on desktop (collapsible on mobile).
2. **Component Aesthetics:**
   - Use crisp, clean borders (`--border`).
   - Cards should have a white background (`--surface`) with subtle rounded corners, clean 1px borders, and extremely soft shadows.
   - Buttons should be rounded (6px border-radius) and use primary blue, white outline, or borderless styles.
   - Form fields and buttons should have a minimum height of 40px to ensure touch friendliness.
   - Unified Profile Dropdown provides a compact access point for user details (User Name, role badge) and options (View Profile, My Uploads, Logout), styled with simple borders, soft shadows, and clean hover states.
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
10. **Notifications UI & Subscription States**: The notification bell displays a small numeric badge (`--danger`) when unread items exist. Notification card elements share the soft borders (`--border`) and clean card shapes of the standard dashboard layout. Subject subscription buttons change dynamically from "🔔 Subscribe" (outlined blue) to "🔕 Unsubscribe" (solid blue/filled) to ensure immediate visual feedback of subscription status. Clicking "View Details" on a notification marks the notification as read automatically and redirects to the safe detail page or start page of the target item instead of triggering a direct file download.
11. **Community Library**: Clean card layout displaying material titles, subject names, description previews, material types, and optional college tag labels. Dynamic filtering options include search keywords, material types, college tag filters, and sorting parameters (latest, views, likes, and rating). Soft, rounded badges are used to represent tags. Empty states provide feedback when no results match the filter criteria. Shared upload forms are clean, outlining file limits (5MB maximum, PDF only) and offering dual-method inputs (PDF upload or external URL) inside a clear dashed container. Card titles are clickable links to details pages. Likes utilize an Instagram-style AJAX toggle button with heart icons (`♥` for liked, `♡` for unliked) that updates instantly without page reload. Notice banners are shown for non-public (hidden, under review, removed) materials visible only to uploaders. Uploader names are clickable links to public uploader profiles that showcase the student's active upload stats (total uploads, views, likes, average rating) and their shared materials. Includes uploader action buttons (Edit, Remove) for editing and soft-deleting active uploads directly from the details page and My Shared Materials listing, with clear pop-up confirmation dialogs.

12. **UI Redesign Overhaul Plan (Phase 13)**: The interface shifts to a professional product-level SaaS resource-library design. Uses pure white surfaces, light slate borders, charcoal text, and blue/purple accents. Implements lightweight interactions using Alpine.js and HTMX for smooth, fast, and responsive student layouts.
13. **College Logo & Onboarding Search**:
    - College Logo styling: Use aspect-ratio preservation (`object-fit: contain` or `object-fit: cover`) with defined maximum width/height constraints (e.g., standard height of 40px in tables, 80px on select college cards, 120px in detail views/dashboards).
    - Initials Avatar fallback: When a college logo is not uploaded, render a clean, high-contrast circular or rounded-rect initials avatar using the college name or code. Use a consistent background (such as soft blue/slate `var(--surface-soft)`) and bold text.
    - Client-side onboarding filter: On the college selection page, a real-time text input filters the listing of colleges matching name, code, city, or state. Shows a clean, styled empty state with helpful tips when no matching colleges are found.

14. **Student Onboarding & Subscription UI/UX**:
    - Multi-step wizard: Break onboarding into small progress-tracked steps. Display a clean top progress indicator (Step 1: College, Step 2: Subjects, Step 3: Done) that dynamically highlights completed, active, and pending steps.
    - College selection: Render active colleges as responsive cards containing logos or fallback initials, code, city, and state. Include real-time client-side text filtering and a clean empty search state.
    - Selected college view: Display selected colleges as a distinct card with a "Change College" toggle to show/hide the search selector.
    - Subject preview: Render subjects as a grid of clean cards with codes, unit counts, and subscription status badges to show students available courses.
    - Complete onboarding: Provide a clear finish action button that is active only when a college has been successfully linked.
    - Onboarding dashboard prompt: If onboarding is incomplete, display a prominent warning banner with a friendly message and a "Complete Setup" CTA button pointing to onboarding.
    - Selected College Dashboard Card: Render selected college metadata clearly on the dashboard with logo/initials, and an inline AJAX follow updates toggle button (changing status and style instantly).
    - Followed Subjects Filter: Display only followed subjects in the dashboard list. If no subjects are followed, show an empty state card with a "Browse All Subjects" button.
    - Quick Access Grid: Provide a responsive navigation row for quick access to Subjects, Quizzes, Community Library, and Notifications.

### Avoid:
- Bakery/cafe styling, cream backgrounds, and brown colors.
- Decorative Roman/serif heading fonts (like Cormorant Garamond).
- Heavy gradients, neon colors, and cluttered layouts.
