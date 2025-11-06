// --- 🧹 CLEAN UP EXISTING TASKS WITH SAME NAME ---
    // cy.log("🧹 Checking for existing tasks with same name...");
    // const deleteExistingTasks = () => {
    //   cy.get("body").then(($body) => {
    //     const hasTask = $body.find(`:contains("${TASK_NAME}")`).length > 0;
    //     if (hasTask) {
    //       cy.log("🗑 Found an existing test task — deleting...");
    //       cy.contains(TASK_NAME)
    //         .first()
    //         .scrollIntoView()
    //         .should("be.visible")
    //         .click({ force: true });

    //       // --- 1️⃣ Click first Delete button on the task page ---
    //       cy.contains("Delete", { timeout: 20000 })
    //         .should("be.visible")
    //         .click({ force: true });

    //       // --- 2️⃣ Wait for popup dialog ---
    //       cy.contains("Are you sure?", { timeout: 10000 }).should("be.visible");
    //       cy.contains(/This action cannot be undone/i, { timeout: 10000 }).should("be.visible");

    //       // --- 3️⃣ Click red Delete button in popup ---
    //       cy.wait(500); // dialog fade-in buffer
    //       cy.contains("button", /^Delete$/)
    //         .should("be.visible")
    //         .click({ force: true });

    //       // --- 4️⃣ Wait for redirect or re-navigate if stuck ---
    //       cy.url({ timeout: 60000 }).then((url) => {
    //         if (url.includes("/task/")) {
    //           cy.log("⏳ Still on task page after deletion, forcing navigation...");
    //           cy.wait(5000);
    //           cy.visit(`/project/${PROJECT_ID}`);
    //         }
    //       });

    //       cy.url({ timeout: 60000 })
    //     //   should("include", `/project/${PROJECT_ID}`);
    //       cy.contains("Project Dashboard", { timeout: 60000 }).should("be.visible");
    //       cy.wait(2000);

    //       // Recursively delete duplicates if any remain
    //       deleteExistingTasks();
    //     } else {
    //       cy.log("✅ No existing tasks found.");
    //     }
    //   });
    // };
    // deleteExistingTasks();


///
 <reference types="cypress" />

Cypress.on("uncaught:exception", () => false);

Cypress.config("defaultCommandTimeout", 120000);
Cypress.config("pageLoadTimeout", 120000);

const PROJECT_ID = "7f233f02-561e-4ada-9ecc-2f39320ee022";
const TASK_NAME = "Create Task Test Cy";

describe("Manager flow: create new task", () => {
  beforeEach(() => {
    cy.visit("/auth/login", { timeout: 120000 });
  });

  it("creates a new task successfully", () => {
    // --- LOGIN ---
    cy.get("#email").should("be.visible").type("testmanager@example.com");
    cy.get("#password").should("be.visible").type("managerpassword");
    cy.contains("button", "Login").click();

    // --- DASHBOARD ---
    cy.url().should("include", "/dashboard");
    cy.contains("Dashboard", { timeout: 60000 }).should("be.visible");
    cy.wait(1000);

    // --- OPEN PROJECT ---
    cy.contains("TESTING PLS DONT AMEND", { timeout: 120000 })
      .scrollIntoView()
      .should("be.visible")
      .click({ force: true });

    cy.url().should("eq", `http://localhost:3000/project/${PROJECT_ID}`);
    cy.contains("Project Dashboard", { timeout: 60000 }).should("be.visible");

    // --- OPEN CREATE TASK ---
    cy.contains("Create New Task", { timeout: 60000 })
      .scrollIntoView()
      .click({ force: true });

    cy.contains("Create New Task", { timeout: 60000 }).should("be.visible");

    // --- FILL FORM ---
    cy.get("#task-name").should("be.visible").clear().type(TASK_NAME);
    cy.get("#task-description").type("Automated E2E test task creation");

    // --- STATUS: Ongoing ---
    cy.get("#task-status").click({ force: true });
    cy.get("body").contains(/^Ongoing$/).should("be.visible").click({ force: true });
    cy.wait(300);

    // --- PRIORITY ---
    cy.get("#task-priority").clear().type("7");

    // --- LABEL: Feature ---
    cy.get("#task-label").click({ force: true });
    cy.get("body").contains(/^Feature$/).should("be.visible").click({ force: true });
    cy.wait(300);

    // --- ADD COLLABORATORS ---
    cy.contains("Search and select collaborators").click({ force: true });
    cy.get('input[placeholder="Type to search..."]').type("test admin", { delay: 30 });
    cy.get("body").contains("test admin").click({ force: true });
    cy.wait(200);

    cy.contains("Search and select collaborators").click({ force: true });
    cy.get('input[placeholder="Type to search..."]').type("test staff", { delay: 30 });
    cy.get("body").contains("test staff").click({ force: true });
    cy.wait(500);

    // --- DATE HELPERS ---
    const navigateToMonth = (monthAbbr, year) => {
      cy.get("body").then(($body) => {
        const header = $body.text();
        if (!header.includes(monthAbbr) || !header.includes(year)) {
          cy.get('button[aria-label*="Next"], button[aria-label*="next month"]')
            .first()
            .click({ force: true });
          cy.wait(300);
          navigateToMonth(monthAbbr, year);
        }
      });
    };

    const pickDay = (day) => {
      cy.get("body")
        .find('[role="grid"] button')
        .not('[disabled]')
        .contains(new RegExp(`^${day}$`))
        .click({ force: true });
    };

    // --- START DATE: 31 Dec 2025 ---
    cy.get("#task-start").click({ force: true });
    cy.wait(500);
    navigateToMonth("Dec", "2025");
    pickDay(31);
    cy.get("body").click(0, 0);
    cy.wait(500);

    // --- DEADLINE: 16 Jan 2026 ---
    cy.get("#task-deadline").click({ force: true });
    cy.wait(500);
    navigateToMonth("Jan", "2026");
    pickDay(16);
    cy.get("body").click(0, 0);
    cy.wait(500);

    // --- NON-RECURRING ---
    cy.get("#task-recurring").click({ force: true });
    cy.get("body").contains(/No\s*\(One-time\)/i).click({ force: true });
    cy.wait(500);

    // --- SUBMIT ---
    cy.contains("button", /^Create Task$/).should("be.enabled").click({ force: true });

    // --- VERIFY ---
    cy.url({ timeout: 180000 }).should("include", `/project/${PROJECT_ID}`);
    cy.contains("Project Dashboard", { timeout: 60000 }).should("be.visible");
    cy.contains(TASK_NAME, { timeout: 120000 }).should("be.visible");
  });
});
