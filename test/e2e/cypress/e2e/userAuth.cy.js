describe('userAuth', () => {
  it('Visit login site', () => {
    cy.visit('http://localhost:3000/auth/login')

    cy.get('[type="email"]').type("teststaff@example.com")
    cy.get('[type="password"]').type("staffpassword")
    cy.contains('button','Login').click()
    cy.get('[data-slot="avatar"]',{timeout:10000}).should('exist').click()
    cy.contains('Log out').click()
    cy.wait(3000)
    
    cy.get('[type="email"]').type("testmanager@example.com")
    cy.get('[type="password"]').type("managerpassword")
    cy.contains('button','Login').click()
    cy.get('[data-slot="avatar"]',{timeout:10000}).should('exist').click()
    cy.contains('Log out').click()
    cy.wait(3000)
    
    cy.get('[type="email"]').type("testhr@example.com")
    cy.get('[type="password"]').type("hrpassword")
    cy.contains('button','Login').click()
    cy.get('[data-slot="avatar"]',{timeout:10000}).should('exist').click()
    cy.contains('Log out').click()
    cy.wait(3000)
    
    cy.get('[type="email"]').type("testadmin@example.com")
    cy.get('[type="password"]').type("adminpassword")
    cy.contains('button','Login').click()
    cy.get('[data-slot="avatar"]',{timeout:10000}).should('exist').click()
    cy.contains('Log out').click()
    cy.wait(3000)

    Cypress.on('uncaught:exception', (err, runnable) => {
    return false;
    });
  })
})