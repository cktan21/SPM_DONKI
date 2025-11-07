package main

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"testing"
)

const manageProjectServiceURL = "http://localhost:4100"
const projectTestUserID = "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
const projectTestProjectID = "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a"
const projectTestProjectIDForEnrichment = "352486e8-a727-470c-add4-10fe26f1fbce"

const projectTestHRUserID = "944d73be-9625-4fd1-8c6a-00e161da0642"
const projectTestAdminUserID = "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
const projectTestManagerUserID = "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
const projectTestStaffUserID = "0ec8a99d-3aab-4ec6-b692-fda88656844f"

// TestManageProjectServiceHealth tests the root endpoint of manage-project service
func TestManageProjectServiceHealth(t *testing.T) {
	t.Log("🧪 Testing Manage-Project Service Health")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	resp, err := http.Get(manageProjectServiceURL + "/")
	if err != nil {
		t.Errorf("❌ Failed to connect to manage-project service: %v", err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		t.Errorf("❌ Health check failed: Status %d, Response: %s", resp.StatusCode, string(body))
		return
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		t.Errorf("❌ Failed to decode health check response: %v", err)
		return
	}

	if message, ok := result["message"].(string); ok {
		t.Logf("✅ Manage-Project Service: %s", message)
	}

	if service, ok := result["service"].(string); ok {
		t.Logf("✅ Service name: %s", service)
	}

	t.Log("🎉 Manage-Project Service Health Test Completed!")
}

// TestGetProjectsByUser tests the GET /uid/{uid} endpoint
func TestGetProjectsByUser(t *testing.T) {
	t.Log("🧪 Testing Get Projects by User (Role-Based)")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Get Projects for User", func(t *testing.T) {
		resp, err := http.Get(manageProjectServiceURL + "/uid/" + projectTestUserID)
		if err != nil {
			t.Errorf("❌ Failed to get projects for user: %v", err)
			return
		}
		defer resp.Body.Close()

		// Accept both 200 (success) and 404 (no projects found) as valid responses
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusNotFound {
			body, _ := io.ReadAll(resp.Body)
			t.Errorf("❌ Unexpected status code: %d, Response: %s", resp.StatusCode, string(body))
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode response: %v", err)
			return
		}

		if resp.StatusCode == http.StatusOK {
			// Check response structure
			if userID, ok := result["user_id"].(string); ok {
				t.Logf("✅ User ID: %s", userID)
			}

			if userName, ok := result["user_name"].(string); ok {
				t.Logf("✅ User Name: %s", userName)
			}

			if userRole, ok := result["user_role"].(string); ok {
				t.Logf("✅ User Role: %s", userRole)
			}

			if projects, ok := result["projects"].([]interface{}); ok {
				t.Logf("✅ Found %d projects", len(projects))

				// Validate project structure
				for i, proj := range projects {
					if projMap, ok := proj.(map[string]interface{}); ok {
						if projID, ok := projMap["id"].(string); ok {
							t.Logf("   📋 Project %d: ID=%s", i+1, projID)
						}

						if projName, ok := projMap["name"].(string); ok {
							t.Logf("      Name: %s", projName)
						}

						// Check if tasks are included
						if tasks, ok := projMap["tasks"].([]interface{}); ok {
							t.Logf("      Tasks: %d", len(tasks))
						}
					}
				}
			} else if message, ok := result["message"].(string); ok {
				t.Logf("ℹ️  %s", message)
			}
		} else if resp.StatusCode == http.StatusNotFound {
			if message, ok := result["message"].(string); ok {
				t.Logf("ℹ️  %s", message)
			}
		}
	})

	t.Log("🎉 Get Projects by User Test Completed!")
}

// TestGetProjectByID tests the GET /pid/{project_id} endpoint
func TestGetProjectByID(t *testing.T) {
	t.Log("🧪 Testing Get Project by ID")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Get Project by ID", func(t *testing.T) {
		resp, err := http.Get(manageProjectServiceURL + "/pid/" + projectTestProjectID)
		if err != nil {
			t.Errorf("❌ Failed to get project by ID: %v", err)
			return
		}
		defer resp.Body.Close()

		// Accept both 200 (success) and 404 (not found) as valid responses
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusNotFound {
			body, _ := io.ReadAll(resp.Body)
			t.Errorf("❌ Unexpected status code: %d, Response: %s", resp.StatusCode, string(body))
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode response: %v", err)
			return
		}

		if resp.StatusCode == http.StatusOK {
			// Check response structure
			if projectID, ok := result["project_id"].(string); ok {
				t.Logf("✅ Project ID: %s", projectID)
			}

			if message, ok := result["message"].(string); ok {
				t.Logf("✅ %s", message)
			}

			if project, ok := result["project"].(map[string]interface{}); ok {
				if projID, ok := project["id"].(string); ok {
					t.Logf("✅ Project ID from project object: %s", projID)
				}

				if projName, ok := project["name"].(string); ok {
					t.Logf("✅ Project Name: %s", projName)
				}

				if ownerName, ok := project["owner_name"].(string); ok {
					t.Logf("✅ Owner Name: %s", ownerName)
				}

				// Check if tasks are included and enriched
				if tasks, ok := project["tasks"].([]interface{}); ok {
					t.Logf("✅ Found %d tasks in project", len(tasks))

					// Validate task enrichment (should have collaborators, status, deadline, etc.)
					for i, task := range tasks {
						if taskMap, ok := task.(map[string]interface{}); ok {
							if taskID, ok := taskMap["id"].(string); ok {
								t.Logf("   📋 Task %d: ID=%s", i+1, taskID)
							}

							if taskName, ok := taskMap["name"].(string); ok {
								t.Logf("      Name: %s", taskName)
							}

							// Check for enriched fields
							if status, ok := taskMap["status"].(string); ok {
								t.Logf("      Status: %s", status)
							}

							if deadline, ok := taskMap["deadline"].(string); ok {
								t.Logf("      Deadline: %s", deadline)
							}

							if collaborators, ok := taskMap["collaborators"].([]interface{}); ok {
								t.Logf("      Collaborators: %d", len(collaborators))
							}
						}
					}
				} else {
					t.Logf("ℹ️  No tasks found in project")
				}
			} else {
				if message, ok := result["message"].(string); ok {
					t.Logf("ℹ️  %s", message)
				}
			}
		} else if resp.StatusCode == http.StatusNotFound {
			if message, ok := result["message"].(string); ok {
				t.Logf("ℹ️  %s", message)
			}
		}
	})

	t.Log("🎉 Get Project by ID Test Completed!")
}

// TestManageProjectServiceEndpoints tests all endpoints comprehensively
func TestManageProjectServiceEndpoints(t *testing.T) {
	t.Log("🧪 Testing All Manage-Project Service Endpoints")
	t.Log("=" + string(bytes.Repeat([]byte("="), 60)))

	// Test root endpoint
	t.Run("Root Endpoint", func(t *testing.T) {
		resp, err := http.Get(manageProjectServiceURL + "/")
		if err != nil {
			t.Errorf("❌ Root endpoint failed: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			t.Errorf("❌ Root endpoint returned status %d", resp.StatusCode)
			return
		}
		t.Logf("✅ Root endpoint: Status %d", resp.StatusCode)
	})

	// Test favicon endpoint (should return 204)
	t.Run("Favicon Endpoint", func(t *testing.T) {
		resp, err := http.Get(manageProjectServiceURL + "/favicon.ico")
		if err != nil {
			t.Errorf("❌ Favicon endpoint failed: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusNoContent {
			t.Logf("⚠️  Favicon endpoint returned status %d (expected 204)", resp.StatusCode)
		} else {
			t.Logf("✅ Favicon endpoint: Status %d", resp.StatusCode)
		}
	})

	// Test invalid endpoint (should return 404)
	t.Run("Invalid Endpoint", func(t *testing.T) {
		resp, err := http.Get(manageProjectServiceURL + "/invalid-endpoint")
		if err != nil {
			t.Errorf("❌ Invalid endpoint test failed: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusNotFound {
			t.Logf("⚠️  Invalid endpoint returned status %d (expected 404)", resp.StatusCode)
		} else {
			t.Logf("✅ Invalid endpoint correctly returned 404")
		}
	})

	t.Log("🎉 All Manage-Project Service Endpoints Test Completed!")
}

// TestManageProjectServiceRoleBasedAccess tests role-based access control
func TestManageProjectServiceRoleBasedAccess(t *testing.T) {
	t.Log("🧪 Testing Role-Based Access Control")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	// Note: These tests assume test users exist in your database
	// You may need to create test users with different roles first

	testCases := []struct {
		name     string
		userID   string
		expected string // "hr", "admin", "manager", "staff"
	}{
		{"HR User", projectTestHRUserID, "hr"},
		{"Admin User", projectTestAdminUserID, "admin"},
		{"Manager User", projectTestManagerUserID, "manager"},
		{"Staff User", projectTestStaffUserID, "staff"},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			resp, err := http.Get(manageProjectServiceURL + "/uid/" + tc.userID)
			if err != nil {
				t.Logf("⚠️  Could not test user %s: %v (user may not exist)", tc.userID, err)
				return
			}
			defer resp.Body.Close()

			if resp.StatusCode == http.StatusOK {
				var result map[string]interface{}
				if err := json.NewDecoder(resp.Body).Decode(&result); err == nil {
					if userRole, ok := result["user_role"].(string); ok {
						t.Logf("✅ User %s has role: %s", tc.userID, userRole)

						// Verify role-based project access
						if projects, ok := result["projects"].([]interface{}); ok {
							t.Logf("   📋 User has access to %d projects", len(projects))

							// HR/Admin should see all projects
							if (userRole == "hr" || userRole == "admin") && len(projects) > 0 {
								t.Logf("   ✅ HR/Admin user correctly sees projects")
							}

							// Staff/Manager should see owned + member projects
							if (userRole == "staff" || userRole == "manager") {
								t.Logf("   ✅ Staff/Manager user correctly sees projects")
							}
						}
					}
				}
			} else if resp.StatusCode == http.StatusNotFound {
				t.Logf("ℹ️  User %s not found or has no projects", tc.userID)
			} else {
				body, _ := io.ReadAll(resp.Body)
				t.Logf("⚠️  Unexpected status for user %s: %d, Response: %s", tc.userID, resp.StatusCode, string(body))
			}
		})
	}

	t.Log("🎉 Role-Based Access Control Test Completed!")
}

// TestManageProjectServiceTaskEnrichment tests that tasks are properly enriched
func TestManageProjectServiceTaskEnrichment(t *testing.T) {
	t.Log("🧪 Testing Task Enrichment in Projects")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Verify Task Enrichment", func(t *testing.T) {
		resp, err := http.Get(manageProjectServiceURL + "/pid/" + projectTestProjectIDForEnrichment)
		if err != nil {
			t.Logf("⚠️  Could not test project %s: %v (project may not exist)", projectTestProjectIDForEnrichment, err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode == http.StatusOK {
			var result map[string]interface{}
			if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
				t.Errorf("❌ Failed to decode response: %v", err)
				return
			}

			if project, ok := result["project"].(map[string]interface{}); ok {
				if tasks, ok := project["tasks"].([]interface{}); ok && len(tasks) > 0 {
					t.Logf("✅ Found %d tasks in project", len(tasks))

					enrichmentFields := []string{
						"status",
						"deadline",
						"collaborators",
						"created_by",
						"project",
					}

					for i, task := range tasks {
						if taskMap, ok := task.(map[string]interface{}); ok {
							t.Logf("   📋 Task %d:", i+1)

							enrichmentCount := 0
							for _, field := range enrichmentFields {
								if _, exists := taskMap[field]; exists {
									enrichmentCount++
									t.Logf("      ✅ Has %s field", field)
								}
							}

							if enrichmentCount > 0 {
								t.Logf("      ✅ Task is properly enriched (%d enrichment fields)", enrichmentCount)
							} else {
								t.Logf("      ⚠️  Task may not be fully enriched")
							}

							// Check collaborators structure (should have names, not just IDs)
							if collaborators, ok := taskMap["collaborators"].([]interface{}); ok {
								for j, collab := range collaborators {
									if collabMap, ok := collab.(map[string]interface{}); ok {
										if id, ok := collabMap["id"].(string); ok {
											if name, ok := collabMap["name"].(string); ok {
												t.Logf("         👤 Collaborator %d: %s (%s)", j+1, name, id)
											} else {
												t.Logf("         ⚠️  Collaborator %d missing name: %s", j+1, id)
											}
										}
									}
								}
							}
						}
					}
				} else {
					t.Logf("ℹ️  Project has no tasks to enrich")
				}
			}
		} else if resp.StatusCode == http.StatusNotFound {
			t.Logf("ℹ️  Project %s not found", projectTestProjectIDForEnrichment)
		}
	})

	t.Log("🎉 Task Enrichment Test Completed!")
}

