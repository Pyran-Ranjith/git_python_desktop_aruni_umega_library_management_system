# Desktop Library Management System
- Project folder: git_desktop_aruni_umega_library_management_system
- Folder structure:
git_desktop_aruni_umega_library_management_system/
├── public/           # Your frontend files
│   ├── index.html
│   ├── script.js
│   └── styles.css
├── assets/           # Optional - for Nativefier icons
│   └── icon.png
├── server.js         # Your backend
├── package.json      # Clean version
├── sql.sql           # Database script
└── README.md

## Installation and Build Instructions:
- cd git_desktop_aruni_umega_library_management_system
- npm install
- npm install -g nativefier
## Your Daily Workflow:
- Terminal 1 (Development):
    - npm run dev
↑ Run this once and keep it running ↑

- Terminal 2 (Desktop App):
    - nativefier --name "Library Management" http://localhost:3000

    - Just double-click your existing Library Management.exe file

    - No commands needed in Terminal 2 for daily use

### When to Rebuild Desktop App:
- Only run npm run build-desktop again when:

1. You add new features and want them in the desktop app

2. You change the app name or icon

3. You want to create a new version for distribution

4. After major UI/UX changes

### Summary:
* npm run dev → Run daily (auto-restarts)

* npm run build-desktop → Run only when you need to update the desktop app

So for normal development, you only need Terminal 1 running npm run dev! The desktop app you already built will automatically connect to your updated server. 