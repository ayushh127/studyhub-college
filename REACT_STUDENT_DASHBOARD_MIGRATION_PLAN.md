# Migration Plan: React Student Dashboard (v2)

This document details the blueprint for migrating the student dashboard page from Flask-Jinja2 templates to a modern React frontend in **Version 2**. 

---

## 1. Directory Structure

To keep frontend development isolated and clean, we will house the React source files inside a root-level `/frontend` directory. The production build will output files directly to Flask's static folder for serving.

```
StudyHub/
├── app/
│   ├── static/
│   │   └── react/               # Built static React assets (JS, CSS, assets)
│   └── templates/
│       └── react/
│           └── dashboard_v2.html # Flask Jinja wrapper loading built React entrypoint
├── frontend/                     # React + Vite repository root
│   ├── public/                  # Public assets
│   ├── src/
│   │   ├── components/          # Reusable UI widgets (cards, sidebars, loaders)
│   │   ├── hooks/               # Custom react queries and hooks
│   │   ├── layouts/             # Dashboard shell layout
│   │   ├── pages/               # Page components (Dashboard.jsx)
│   │   ├── services/            # Axios API client handlers
│   │   ├── App.jsx              # Main App routing / context
│   │   ├── index.css            # Tailwind CSS directives
│   │   └── main.jsx             # React entrypoint
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
```

---

## 2. React Libraries
* **Framework:** React 18+ (bundled with Vite)
* **Styling:** Tailwind CSS (configured with academic harmonies: slates, indigo accents, and subtle borders)
* **Animations:** Framer Motion (for page transitions, tab switches, and hover micro-animations)
* **Icons:** Lucide React (clean, vector stroke icons)
* **HTTP Client:** Axios or native `fetch` (pre-configured with request interceptors to handle sessions)

---

## 3. Dashboard Visual Design

We will transition the "Classical Minimal Academic" theme into a premium **Glassmorphic Workspace** design:
* **Layout:** Fixed left sidebar navigation, top status header, and scrollable grid-based workspace.
* **Header:** Modern welcome banner featuring user name, selected college logo/initials avatar, and a compact notification bell with unread badge count.
* **Metrics Row:** Horizontal grid of micro-cards displaying quick stats:
  - Subscribed Subjects Count
  - Unattempted Quizzes Count
  - Unread Notifications Count
  - Shared Community Assets Count
* **Subjects Grid:** Cards representing followed subjects showing course codes, semester info, and progress status indicator bars.
* **Dual Workspace Panels:**
  - *Left Panel:* Recent quizzes (Subject tag, difficulty badge, timer info).
  - *Right Panel:* Community library updates and global notification cards preview.

---

## 4. API Endpoint Specification

To feed the React frontend, we will implement a read-only endpoint on the Flask backend:
* **Endpoint:** `GET /api/student/dashboard`
* **Security:** Checked by Flask authentication middleware (`login_required` + student role verification). Returns `401` or `403` JSON responses on unauthorized sessions.

### JSON Response Schema Example:
```json
{
  "success": true,
  "user": {
    "name": "Ayush Sharma",
    "email": "student@timing.com",
    "role": "student"
  },
  "college": {
    "id": 1,
    "name": "Test Timing College",
    "code": "TIME_COLL",
    "logo_url": "/files/college-logos/1",
    "initials": "TTC"
  },
  "stats": {
    "followed_subjects_count": 2,
    "unread_notifications_count": 0,
    "pending_quizzes_count": 3,
    "community_uploads_count": 1
  },
  "followed_subjects": [
    {
      "id": 1,
      "name": "Database Management Systems",
      "code": "DBMS101",
      "semester": 4,
      "units_count": 5,
      "quizzes_count": 3,
      "materials_count": 12
    }
  ],
  "recent_quizzes": [
    {
      "id": 4,
      "title": "DBMS Normalization Quiz",
      "subject_code": "DBMS101",
      "unit_number": 2,
      "difficulty": "medium",
      "duration_minutes": 15,
      "question_count": 10
    }
  ],
  "notifications_preview": [],
  "community_materials_preview": [
    {
      "id": 1,
      "title": "SQL Join Cheatsheet",
      "subject_name": "DBMS",
      "uploaded_by": "Timing Student",
      "likes_count": 5,
      "rating": 4.8,
      "created_at": "2026-06-08T04:23:28Z"
    }
  ]
}
```

---

## 5. Auth / Session Strategy
* **Cookie-Based Auth:** React client requests will rely on standard HTTP session cookies already set during Flask login. No manual JSON Web Token (JWT) storage is necessary.
* **Axios Interceptors:** Set `withCredentials: true` globally on Axios to ensure the browser forwards cookies on every API request.
* **Session Expiration:** If an API call returns `401 Unauthorized` or `403 Forbidden`, the React app will redirect the browser window directly to `/auth/login` to re-authenticate.

---

## 6. Rollout & Routing Strategy
To ensure zero disruption for production environments:
1. Keep the existing Jinja2-rendered dashboard route `/student/dashboard` untouched.
2. Register a new route **`GET /student/dashboard-v2`** in `app/routes/student.py`.
3. In local development:
   - Run Vite on port `5173` with proxy configuration forwarding `/api/` requests to the local Flask port `5000`.
4. In production/staging environments:
   - `/student/dashboard-v2` renders a Jinja template (`react/dashboard_v2.html`) containing the single built React root element:
     ```html
     <div id="react-root"></div>
     <script src="{{ url_for('static', filename='react/index.js') }}"></script>
     ```
5. Perform user testing. Once fully vetted and stable, modify `/student/dashboard` to serve the React wrapper.

---

## 7. Migration Risks & Mitigations
* **CSRF Protection:** Standard GET request does not require CSRF tokens. However, future POST actions (toggles, submissions) will need CSRF headers.
  - *Mitigation:* Deliver the CSRF token via a meta tag in the wrapper HTML (`react/dashboard_v2.html`) or fetch it from `/api/csrf-token`, then append it as a `X-CSRFToken` header in Axios requests.
* **Flicker on Load:** Fetching data on React mount can cause brief content layout shifts.
  - *Mitigation:* Build a CSS-only landing skeleton loader matching card shapes to prevent visual jumps.

---

## 8. Granular Implementation Steps

1. **Step 1: Frontend Setup**
   - Initialize `/frontend` folder with Vite React-TS or JS framework.
   - Configure `tailwind.config.js` and input directives.
2. **Step 2: Flask Endpoint Integration**
   - Implement `/api/student/dashboard` route returning structured JSON data.
3. **Step 3: Flask Route Wrapper**
   - Add `/student/dashboard-v2` route and create Jinja template pointing to Vite's local dev assets or built files.
4. **Step 4: Layouts & Components**
   - Construct sidebars, headers, status cards, and metric rows in React.
5. **Step 5: API Integration & Data Binding**
   - Integrate Axios fetch client and bind backend values to cards.
6. **Step 6: Polish & Animations**
   - Apply Framer Motion transitions and verify performance.
7. **Step 7: Verification**
   - Execute QA tests on `/student/dashboard-v2` to verify session persistence, error redirects, and loading states.
