/// <reference types="cypress" />
// chat test
Cypress.on("uncaught:exception", () => false);

Cypress.config("defaultCommandTimeout", 120000);
Cypress.config("pageLoadTimeout", 120000);

const PROJECT_ID = "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a";
const EXISTING_TASK = "CHAT TESTING DONOT DELETE CY";

describe("Manager flow: send and delete message", () => {
  beforeEach(() => {
    cy.visit("/auth/login", { timeout: 120000 });
  });

  it("sends a message with mention and deletes it", () => {
    // --- LOGIN ---
    cy.get("#email").should("be.visible").type("testmanager@example.com");
    cy.get("#password").should("be.visible").type("managerpassword");
    cy.contains("button", "Login").click();

    // --- DASHBOARD ---
    cy.url().should("include", "/dashboard");
    cy.contains("Dashboard", { timeout: 60000 }).should("be.visible");
    cy.wait(1000);

    // --- OPEN PROJECT ---
    cy.contains("TESTING JW CY DONT AMEND", { timeout: 120000 })
      .scrollIntoView()
      .should("be.visible")
      .click({ force: true });

    cy.url().should("eq", `http://localhost:3000/project/${PROJECT_ID}`);
    cy.contains("Project Dashboard", { timeout: 60000 }).should("be.visible");
    cy.wait(2000);

    // --- FIND & CLICK EXISTING TASK IN TABLE ---
    cy.log(`🔍 Searching for existing task: "${EXISTING_TASK}"`);
    cy.get("table", { timeout: 20000 })
      .should("exist")
      .within(() => {
        cy.contains("td", EXISTING_TASK, { timeout: 15000 })
          .scrollIntoView()
          .should("be.visible")
          .click({ force: true });
      });

    // --- VERIFY TASK PAGE LOADED ---
    cy.url({ timeout: 60000 }).should("include", "/task/");
    cy.contains(EXISTING_TASK, { timeout: 20000 }).should("be.visible");

    cy.log("✅ Successfully opened the task page!");

    // --- CHAT MESSAGE FLOW ---
    cy.get('input[placeholder*="Type a message"]', { timeout: 20000 })
      .should("be.visible")
      .as("chatInput");

    // Type '@' to trigger mention dropdown
    cy.get("@chatInput").type("@");
    cy.wait(1000); // wait for mention dropdown

    // Select 'test staff' from dropdown
    cy.contains("button", "test staff", { timeout: 10000 })
      .should("be.visible")
      .click({ force: true });

    // Add rest of message
    cy.get("@chatInput").type(" when will this be done?");

    // Click Send button
    cy.get(
      'button.h-10.w-10.bg-blue-600.hover\\:bg-blue-700.text-white.shadow-sm.disabled\\:opacity-50',
      { timeout: 10000 }
    )
      .should("be.visible")
      .click({ force: true });

    // Verify message appears
    cy.contains("@test staff when will this be done?", { timeout: 20000 })
      .scrollIntoView()
      .should("be.visible");

    cy.log("✅ Message sent successfully!");

    // --- DELETE THE SENT MESSAGE ---
    cy.log("🗑 Attempting to delete the sent message...");

    cy.contains("@test staff when will this be done?", { timeout: 20000 })
      .closest("div.rounded-2xl") // the message bubble wrapper
      .within(() => {
        cy.get('button.h-5.w-5.text-blue-100.hover\\:bg-blue-700')
          .should("exist")
          .last() // pick the Trash2 (delete) one, after Edit2
          .click({ force: true });
      });

    // Confirm deletion
    cy.on("window:confirm", () => true);
    cy.wait(2000);

    // Verify it’s gone
    cy.contains("@test staff when will this be done?").should("not.exist");
    cy.log("✅ Message deleted successfully!");
  });
});
