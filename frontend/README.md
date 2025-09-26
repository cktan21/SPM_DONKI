# README: Frontend Project (Nuxt 4 + Tailwind CSS + shadcn-vue)

This project uses Nuxt 4, Tailwind CSS v4, and shadcn-vue components. Follow these instructions to get started and handle common issues.

Documentation for Nuxt: https://nuxt.com/docs/4.x/getting-started/introduction

<!-- NOTE: Search for shadcn-vue not shadcn. shadcn is for Next.js  -->

Components for Shadcn-vue: https://www.shadcn-vue.com/docs/components/accordion.html

You can also look at their `Home` or `Themes` page for some prebuilt pages or templates:

Themes: https://www.shadcn-vue.com
Blocks: https://www.shadcn-vue.com/blocks.html

Some of the stuff such as the templates in `Themes` may not have the source code on shadcn-vue website. You can look for it at their github repo

Shadcn-vue github: https://github.com/unovue/shadcn-vue

---

1️⃣ Setup

Navigate to your frontend project folder:

cd frontend

Install dependencies:

# bun
bun install

---

2️⃣ shadcn-vue Components

All UI components live in app/components/ui/ (*** For this specific project only, read below to find out more)
**Important:** Commit this folder to Git so team members don’t need to regenerate components.

If you need a component that is not inside [app/component/ui], you can add them by running the command below:

npx shadcn-vue@latest add <component-name>

Example:

npx shadcn-vue@latest add button

By default, after you run the code above, newly added components will appear under [components/ui/<component-name>/]. 
Note this is aother component ui folder that is created outside of the app directory. This is technically the default way. 

However, due to some importing problems which is not so simple to fix, i've added another component/ui inside the app directory, so 
its alot easier to import. You find them at [app/components/ui]

So if you happen to add any component using npx ```shadcn-vue@latest add <component-name>```, it will be in the [component/ui] folder outside the app 
directory. You should move the newly added component into the [app/component/ui]

---

3️⃣ Required: Create lib/utils.ts inside app/

<!-- I've forced commit this util.ts, so its unlikely you will need to manually add this file anymore. 
But in any cases you need, follow the steps below -->

shadcn-vue components rely on a helper cn in lib/utils.ts.  
You **must create this folder and file under `app/`**:

1. Create folder:

frontend/app/lib/

2. Create file utils.ts and copy & paste the code below:


export function cn(...classes: (string | boolean | undefined)[]) {
  return classes.filter(Boolean).join(' ')
}


3. Components can now import it:

import { cn } from "@/lib/utils"


<!-- Side Note: -->

In Nuxt 4, `@/` points to the `app/` folder by default.

---

4️⃣ Running the Development Server

Start the development server at http://localhost:3000:

Routing is based on the folder structure under app/pages. Each .vue file automatically becomes a route.

Examples:

- app/pages/index.vue               → http://localhost:3000/
- app/pages/abc.vue                 → http://localhost:3000/abc
- app/pages/auth/login.vue          → http://localhost:3000/auth/login
- app/pages/dashboard/settings.vue  → http://localhost:3000/dashboard/settings

Notes:
1. A file named index.vue inside a folder maps to the folder route.
   Example: app/pages/auth/index.vue → /auth

2. Dynamic routes can be created using square brackets in filenames.
   Example: app/pages/user/[id].vue → /user/:id

This means you can organize pages in nested folders, and the URL will follow the folder structure automatically.

# dev

# bun
bun run dev

---

5️⃣ Production

Build for production:

# bun
bun run build

Preview production build locally:

# bun
bun run preview

Check Nuxt 4 deployment docs: https://nuxt.com/docs/getting-started/deployment

---

6️⃣ Troubleshooting Common Issues

Issue: `npm install ... failed` / `BuildMessage {}`

CLI may fail to auto-install dependencies.

Solution:

# Bun
bun add tw-animate-css class-variance-authority lucide-vue-next clsx tailwind-merge reka-ui

# OR npm
npm install tw-animate-css class-variance-authority lucide-vue-next clsx tailwind-merge reka-ui

Re-run the add command if needed:

npx shadcn-vue@latest add button

---

Issue: `component.json already exists`

* Happens if CLI partially generated components before.  
* **Do not delete** `components/ui/` — it is needed.  
* Only delete `.shadcn/` or `components.json` if restarting shadcn-vue setup from scratch.

If you face the `component.json already exists` problem, try running `bun run dev` now, it should work

---

Issue: Team members cannot run the project

Make sure they:

1. Navigate to the frontend folder.  
2. Install dependencies (`bun install`, `npm install`, etc.).  
3. Keep `app/components/ui/` present.  
4. Ensure `app/lib/utils.ts` exists for `cn` helper.

---

7️⃣ Notes

* shadcn-vue uses a registry JSON (`app.json`) to generate components.  
* Default theme/style is new-york-v4. No need to modify unless customizing.  
* Always keep `app/components/ui/` and `tailwind.config.js` committed.  
* `.shadcn/` is optional, can be ignored in Git.

---

8️⃣ Optional: Adding All Components at Once 

*** You should not need to run this step at all, since everything is inside [app/components/ui] already.

However if you like to proceed and add all components at once, you can use the code below

No official `*` shortcut exists. To add multiple components:

npx shadcn-vue@latest add accordion alert alert-dialog avatar badge button calendar card checkbox dialog drawer dropdown-menu form hover-card input label menubar navigation-menu popover progress radio-group scroll-area select separator sheet skeleton slider switch table tabs textarea toast toggle tooltip

Note: This populates all standard components under [components/ui/] outside of the app directory. After populating, you should move all the individual
components into [app/components/ui]

---

9️⃣ Useful Links

* [Nuxt 4 Documentation](https://nuxt.com/docs)  
* [Tailwind CSS v4](https://tailwindcss.com/docs)  
* [shadcn-vue Documentation](https://shadcn-vue.com/docs)

---

🔟 Recommended Project Folder Structure

frontend/
├─ app/
|  ├─ app.vue
│  ├─ assets/
│  ├─ components/
│  │  └─ ui/
│  │     ├─ button/
│  │     ├─ card/
│  │     └─ ... other shadcn components
│  ├─ lib/
│  │  └─ utils.ts       # cn helper
│  ├─ pages/
│  │  ├─ index.vue         # Home page
│  │  ├─ about.vue         # About page
│  │  └─ auth/
│  │     ├─ login.vue      # Login page
│  │     └─ register.vue   # Register page
│  ├─ plugins/
│  └─ ... other Nuxt folders
├─ .nuxt/
├─ node_modules/
├─ public/
├─ .gitignore
├─ bun.lockb
├─ components.json
├─ nuxt.config.ts
├─ package-lock.json
├─ package.json
├─ README.txt         # This file
└─ tsconfig.json

> All team members should maintain this structure.  
> `components/ui/` and `app/lib/utils.ts` **must exist** for shadcn-vue components to work.

---

With this setup, all team members can run the frontend, add new components safely, and troubleshoot Bun/npm issues.
