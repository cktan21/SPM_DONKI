describe('Login Page', () => {
  beforeEach(() => {
    // Visit the login page
    cy.visit('/auth/login');
  });

  it('loads successfully', () => {
    cy.wait(10000)
    cy.contains('Login').should('be.visible');
    cy.get('input#email').should('be.visible');
    cy.get('input#password').should('be.visible');
    cy.contains('button', 'Login').should('be.visible');
    cy.wait(3000)
  });

  it('shows error if both fields are empty', () => {
    cy.contains('button', 'Login').click();
    cy.contains('Please enter your email and password').should('be.visible');
    cy.wait(3000)
  });

  it('shows error if only email is filled', () => {
  cy.visit('/auth/login');
  cy.get('#email', { timeout: 10000 }).should('be.visible').type('testmanager@example.com');
  cy.contains('button', 'Login').click();
  cy.contains('Please enter your password').should('be.visible');
  cy.wait(3000)
  });

  it('shows error if invalid email format', () => {
    cy.get('#email').type('invalidemail');
    cy.get('#password').type('managerpassword');
    cy.contains('button', 'Login').click();
    cy.contains('Please enter a valid email address').should('be.visible');
    cy.wait(3000)
  });

  // optional: only works if backend is running and you have a test account
  it('logs in successfully', () => {
    cy.get('#email').type('testmanager@example.com');
    cy.get('#password').type('managerpassword');
    cy.contains('button', 'Login').click();
    cy.url({ timeout: 25000 }).should('include', '/dashboard');
    cy.wait(3000)
  });
});
