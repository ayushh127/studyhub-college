# StudyHub College - Mobile PWA Installation Guide

This guide explains how to install **StudyHub College** as a Progressive Web App (PWA) on your mobile device. Because it is a PWA, you do not need to download a bulky `.apk` or register on app stores to use it.

---

## How to Install the App

### On Android (Chrome)
1. Open **Google Chrome** on your mobile phone.
2. Navigate to your deployed website URL (e.g. `http://<your-username>.pythonanywhere.com`).
3. You may see a pop-up banner at the bottom saying **"Add StudyHub to Home Screen"**. Tap it.
4. If the banner does not appear:
   * Tap the **three-dot menu** in the top right corner of Chrome.
   * Select **"Add to Home screen"** or **"Install app"**.
5. Confirm by tapping **"Install"**. The app icon will now appear on your home screen and in your app drawer.

### On iOS (Safari)
1. Open **Safari** on your iPhone.
2. Navigate to your deployed website URL.
3. Tap the **Share** button (the square icon with an arrow pointing up) at the bottom navigation bar.
4. Scroll down and select **"Add to Home Screen"**.
5. Tap **"Add"** in the top-right corner. The app will now be available on your home screen.

---

## PWA Behavior & Features

Once installed and launched from the home screen, StudyHub College behaves like a native app:
* **Standalone Window**: The browser address bar and navigation controls are hidden, maximizing screen space for reading materials and taking quizzes.
* **Classical Minimal Academic Theme Integration**: The top system status bar automatically matches the warm dark brown theme color (`#3C2A21`), and the viewport background uses the cream/ivory color scheme (`#FDFBF7`).
* **Persistent Bottom Nav**: A dedicated bottom navigation bar stays locked at the bottom of the screen on mobile, providing immediate one-tap access to the Student Dashboard, Subjects, Alerts, PYQs, and Quizzes.

---

## PWA vs. Native APK: Comparison

| Feature | PWA (Current Stage) | Native APK |
| :--- | :--- | :--- |
| **App Store Approval** | Not needed. Install instantly from any web link. | Required for Google Play or sideloaded. |
| **Updates** | **Instant**. Every time the code is updated on the server, all clients get the updates automatically. | Users must download and reinstall new APK updates. |
| **Download Size** | **Almost Zero**. Installs in under 1 second. | Ranges from 15MB to 50MB. |
| **Device Security Block** | **None**. Runs in the secure browser sandbox. | Android blocks by default ("Block by Play Protect" or "Unknown Sources"). |
| **Cross-Platform** | Works on both Android and iOS devices. | Requires separate builds for Android (APK) and iOS (IPA). |

### Why PWA is Better for the MVP Pilot
For our small pilot (10 students and 2 teachers), the PWA approach is superior to building a native APK because:
1. **Instant Deployments**: If you find a bug during the pilot, you can fix it locally, push to GitHub, pull on PythonAnywhere, and the students will get the bug fix instantly the next time they open the app.
2. **Frictionless Onboarding**: Students do not need to toggle advanced developer settings on their phones to sideload unverified APKs. They simply browse the link and tap install.
3. **Storage Efficiency**: It uses virtually no disk space on the students' phones.
