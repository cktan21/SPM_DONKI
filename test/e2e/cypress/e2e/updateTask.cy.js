describe('updateTask', () => {

  beforeEach(() => {
    cy.visit('http://localhost:3000/auth/login')
  });

  it('staff task CRUD', () => {
    // login w staff acc
    // contains loop in case of error 500
    function Login_staff(){
      cy.get('[type="email"]').clear()
      cy.get('[type="email"]').type("teststaff@example.com")
      cy.get('[type="password"]').clear()
      cy.get('[type="password"]').type("staffpassword")
      cy.contains('button','Login').click()

      cy.wait(2500)
      cy.url().then((url)=>{
        if(url.includes('/login'))
          Login_staff()
      })
    }
    Login_staff()

    //create new task
    cy.contains("TESTING JW CY DONT AMEND",{timeout:20000}).should('exist').click()
    cy.contains("Create New Task",{timeout:20000}).should('exist').click()
    cy.get('[id="task-name"]',{timeout:20000}).type("st1")
    cy.get('[id="task-description"]').type("sd")
    cy.get('[id="task-notes"]').type("sn")
    cy.get('[id="task-priority"]').type("5")
    cy.get('[id="task-label"]').click()
    cy.contains("Feature",{timeout:20000}).click({force: true})
    cy.get('[id="task-status"]').click()
    cy.contains("To-do",{timeout:20000}).click({force: true})
    cy.get('[id="task-start"]').click().wait(100)
    cy.contains('button',"10",{timeout:20000}).click({force: true})
    cy.get('[id="task-start-time"]').type("00:00",{force: true})
    cy.get('[id="task-deadline"]').click().wait(100)
    cy.contains('button',"12",{timeout:20000}).click({force: true})
    cy.get('[id="task-deadline-time"]').type("01:00",{force: true})
    cy.get('[id="task-recurring"]').click()
    cy.contains("No",{timeout:20000}).click({force: true})
    cy.contains('button',"Create Task").click()

    //delete new task
    // cy.contains('[data-slot="table-cell"]',"st1",{timeout:20000}).should('exist').click()
    // cy.contains('button',"Delete",{timeout:20000}).click().wait(1000)
    // cy.get('[role="alertdialog"]').contains('[type="button"]',"Delete").click({force: true})
  });

  it('manager task assignment', () => {
    // login w staff acc
    // contains loop in case of error 500
    function Login_manager(){
      cy.get('[type="email"]').clear()
      cy.get('[type="email"]').type("testmanager@example.com")
      cy.get('[type="password"]').clear()
      cy.get('[type="password"]').type("managerpassword")
      cy.contains('button','Login').click()

      cy.wait(2500)
      cy.url().then((url)=>{
        if(url.includes('/login'))
          Login_manager()
      })
    }
    Login_manager()

    //access newly created task
    cy.contains("TESTING JW CY DONT AMEND",{timeout:20000}).should('exist').click()
    cy.contains('[data-slot="table-cell"]',"st1",{timeout:20000}).should('exist').click()
    cy.contains('button',"Edit",{timeout:20000}).click().wait(1000)
    cy.contains("Search and select collaborators",{timeout:20000}).click()
    cy.contains("test staff",{timeout:20000}).click()
    cy.contains("Save Changes").click()
    cy.pause()

    //delete new task
    cy.contains('[data-slot="table-cell"]',"st1",{timeout:20000}).should('exist').click()
    cy.contains('button',"Delete",{timeout:20000}).click().wait(1000)
    cy.get('[role="alertdialog"]').contains('[type="button"]',"Delete").click({force: true})

    cy.on('uncaught:exception',(err, runnable)=>{return false})
  });
})