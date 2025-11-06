Cypress.on('uncaught:exception', () => false);

// Global patience settings
Cypress.config('defaultCommandTimeout', 120000);
Cypress.config('pageLoadTimeout', 120000);

before(() => {
  cy.task('clearDownloads', Cypress.config('downloadsFolder'));
});

describe('Manager flow: login → wait for dashboard → open report page → generate report', () => {
  beforeEach(() => {
    // Login page + hydration buffer
    cy.visit('/auth/login', { timeout: 120000 });
    cy.wait(5000); // allow Vite/Nuxt warmup
  });

  it('logs in, waits for dashboard projects, then generates report', () => {
    // --- LOGIN ---
    cy.get('#email', { timeout: 90000 }).should('be.visible').type('testmanager@example.com');
    cy.get('#password', { timeout: 90000 }).should('be.visible').type('managerpassword');
    cy.contains('button', 'Login', { timeout: 90000 }).should('be.visible').click();

    // --- DASHBOARD ---
    cy.url({ timeout: 120000 }).should('include', '/dashboard');
    cy.contains('Dashboard', { timeout: 120000 }).should('be.visible');

    // 🕐 Wait until project cards are rendered (DashboardCards)
    // adjust selector depending on how your cards look — they usually contain project names or have a "Showing X projects" text
    cy.contains('Showing', { timeout: 180000 })
      .should('be.visible'); // this line waits until the "Showing X projects" text is visible

    // give a bit more breathing room after data appears
    cy.wait(8000);

    // --- OPEN REPORT DROPDOWN ---
    cy.contains('Report', { timeout: 120000 })
      .should('be.visible')
      .click({ force: true });

    cy.wait(5000); // sidebar animation/opening buffer

    // --- CLICK "Generate Report" ---
    cy.contains('Generate Report', { timeout: 120000 })
      .should('be.visible')
      .click({ force: true });

    // --- WAIT FOR REPORT PAGE ---
    cy.url({ timeout: 120000 }).should('include', '/generatereport');
    cy.wait(15000); // allow large page + module imports
    cy.contains('Report Generator', { timeout: 120000 }).should('be.visible');

    // --- SET FILTER TYPE = "Project" ---
    cy.get('button[role="combobox"]', { timeout: 60000 })
      .first()
      .should('be.visible')
      .click({ force: true });

    cy.contains('Project', { timeout: 60000 })
      .should('be.visible')
      .click({ force: true });

    cy.wait(5000); // allow re-render

    // --- SELECT PROJECT "TESTING PLS DONT AMEND T^T" ---
    cy.contains('Select Project', { timeout: 60000 }).should('be.visible');
    cy.get('.h-11').contains('Choose a project').click({ force: true });
    cy.wait(4000);
    cy.contains('Delete this project', { timeout: 90000 })
      .scrollIntoView()
      .should('be.visible')
      .click({ force: true });

    cy.wait(8000); // let selection propagate

    // --- CLICK "Generate Report" BUTTON ---
    cy.contains('button', 'Generate Report', { timeout: 90000 })
      .should('be.enabled')
      .click({ force: true });

    // --- VERIFY REPORT RENDERED ---
    // --- VERIFY REPORT RENDERED ---
    // Wait for the report header first
    cy.contains('Report #', { timeout: 180000 }).should('be.visible');

    // 🧠 Wait until all 5 stat cards are rendered ("Completed", "In Progress", "To Do", "Overdue", "Total Hours")
    const stats = ['Completed', 'In Progress', 'To Do', 'Overdue', 'Total Hours'];
    stats.forEach(label => {
    cy.contains(label, { timeout: 180000 }).should('be.visible');
    });

    // small buffer after cards finish rendering
    cy.wait(5000);

    // --- Now verify Task Details (if it exists)
    cy.get('body').then($body => {
    if ($body.text().includes('Task Details')) {
        cy.contains('Task Details', { timeout: 180000 }).should('be.visible');
    } else {
        cy.log('⚠️ No Task Details found, skipping table check');
    }
    });

    // --- Verify export buttons exist
    cy.contains('Export PDF', { timeout: 60000 }).should('exist');
    cy.contains('Export Excel', { timeout: 60000 }).should('exist');

    // --- VERIFY EXPORT DOWNLOADS ---
    const downloadsFolder = Cypress.config('downloadsFolder');

    // PDF download
    cy.contains('Export PDF', { timeout: 60000 })
    .should('be.visible')
    .click({ force: true });

    cy.wait(8000); // wait for file save
    cy.task('findDownloadedFile', { dir: downloadsFolder, ext: '.pdf' })
    .should('not.be.null')
    .then((pdfPath) => {
        cy.log(`✅ PDF downloaded: ${pdfPath}`);
    });

    // Excel download
    cy.contains('Export Excel', { timeout: 60000 })
    .should('be.visible')
    .click({ force: true });

    cy.wait(8000);
    cy.task('findDownloadedFile', { dir: downloadsFolder, ext: '.xlsx' })
    .should('not.be.null')
    .then((xlsPath) => {
        cy.log(`✅ Excel downloaded: ${xlsPath}`);
    });

  });
});
