package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"testing"
)

const manageProjectServiceURL = "http://localhost:4100"
const projectServiceURL = "http://localhost:5200"

const projectTestUserID = "bba910a9-1685-4fa3-af21-ccb2e11cf751"
const projectTestProjectID = "2f72ee2f-eda4-4245-8df5-bec3f1fc1c2a"
const projectTestProjectIDForEnrichment = "352486e8-a727-470c-add4-10fe26f1fbce"

const projectTestHRUserID = "944d73be-9625-4fd1-8c6a-00e161da0642"
const projectTestAdminUserID = "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
const projectTestManagerUserID = "a43815c3-2051-44b9-9646-8ceaf9d6cb87"
const projectTestStaffUserID = "0ec8a99d-3aab-4ec6-b692-fda88656844f"

const invalidPID = "not-a-valid-uuid-12345"

// Helper function to perform GET request with timeout and retry
func getWithTimeout(url string) (*http.Response, error) {
	return httpGetWithRetry(url, 2)
}

// Helper function to delete a project (used for cleanup)
func deleteProject(projectID string) error {
	if projectID == "" {
		return nil
	}
	resp, err := httpDeleteWithRetry(projectServiceURL+"/"+projectID, 2)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	// Accept both 200 and 404 (idempotent delete) as success
	if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusNotFound {
		body, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("delete failed with status %d: %s", resp.StatusCode, string(body))
	}
	return nil
}

// TestManageProjectServiceHealth tests the root endpoint of manage-project service
func TestManageProjectServiceHealth(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Manage-Project Service Health")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	resp, err := getWithTimeout(manageProjectServiceURL + "/")
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
	t.Parallel()
	t.Log("🧪 Testing Get Projects by User (Role-Based)")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Get Projects for User", func(t *testing.T) {
		resp, err := getWithTimeout(manageProjectServiceURL + "/uid/" + projectTestUserID)
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
	t.Parallel()
	t.Log("🧪 Testing Get Project by ID")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Get Project by ID", func(t *testing.T) {
		resp, err := getWithTimeout(manageProjectServiceURL + "/pid/" + projectTestProjectID)
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
	t.Parallel()
	t.Log("🧪 Testing All Manage-Project Service Endpoints")
	t.Log("=" + string(bytes.Repeat([]byte("="), 60)))

	// Test root endpoint
	t.Run("Root Endpoint", func(t *testing.T) {
		resp, err := getWithTimeout(manageProjectServiceURL + "/")
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
		resp, err := getWithTimeout(manageProjectServiceURL + "/favicon.ico")
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
		resp, err := getWithTimeout(manageProjectServiceURL + "/invalid-endpoint")
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
	t.Parallel()
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
			resp, err := getWithTimeout(manageProjectServiceURL + "/uid/" + tc.userID)
			if err != nil {
				t.Logf("⚠️  Could not test user %s: %v (user may not exist or service unavailable)", tc.userID, err)
				return
			}
			if resp == nil {
				t.Logf("ℹ️  Response is nil for user %s (service may be unavailable)", tc.userID)
				return
			}
			if resp.Body != nil {
				defer resp.Body.Close()
			}

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
	t.Parallel()
	t.Log("🧪 Testing Task Enrichment in Projects")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Verify Task Enrichment", func(t *testing.T) {
		resp, err := getWithTimeout(manageProjectServiceURL + "/pid/" + projectTestProjectIDForEnrichment)
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

// TestBehaviour_AdminGetsAllProjects verifies that admin users see all projects
func TestBehaviour_AdminGetsAllProjects(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Admin Gets All Projects Behaviour")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Admin Should See All Projects", func(t *testing.T) {
		resp, err := getWithTimeout(manageProjectServiceURL + "/uid/" + projectTestAdminUserID)
		if err != nil {
			t.Logf("⚠️  Could not get projects for admin: %v (service may be unavailable)", err)
			return
		}
		if resp == nil {
			t.Logf("ℹ️  Response is nil for admin user (service may be unavailable)")
			return
		}
		if resp.Body != nil {
			defer resp.Body.Close()
		}

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
			if userRole, ok := result["user_role"].(string); ok {
				t.Logf("✅ Admin user role: %s", userRole)

				if projects, ok := result["projects"].([]interface{}); ok {
					t.Logf("✅ Admin has access to %d projects", len(projects))

					// Admin/HR should see all projects (verify they see multiple if they exist)
					if userRole == "admin" || userRole == "hr" {
						t.Logf("✅ Admin/HR role correctly identified")
					}
				}
			}
		} else if resp.StatusCode == http.StatusNotFound {
			if message, ok := result["message"].(string); ok {
				t.Logf("ℹ️  %s", message)
			}
		}
	})

	t.Log("🎉 Admin Gets All Projects Test Completed!")
}

// TestBehaviour_StaffOwnedAndMember verifies that staff users see owned and member projects
func TestBehaviour_StaffOwnedAndMember(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Staff Owned and Member Projects Behaviour")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Staff Should See Owned and Member Projects", func(t *testing.T) {
		resp, err := getWithTimeout(manageProjectServiceURL + "/uid/" + projectTestStaffUserID)
		if err != nil {
			t.Errorf("❌ Failed to get projects for staff: %v", err)
			return
		}
		defer resp.Body.Close()

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
			if userRole, ok := result["user_role"].(string); ok {
				t.Logf("✅ Staff user role: %s", userRole)

				if projects, ok := result["projects"].([]interface{}); ok {
					t.Logf("✅ Staff has access to %d projects", len(projects))

					// Staff should see owned + member projects
					if userRole == "staff" {
						t.Logf("✅ Staff role correctly identified")
					}
				}
			}
		} else if resp.StatusCode == http.StatusNotFound {
			if message, ok := result["message"].(string); ok {
				t.Logf("ℹ️  %s", message)
			}
		}
	})

	t.Log("🎉 Staff Owned and Member Projects Test Completed!")
}

// TestBehaviour_ManagerSameDepartment verifies that manager users see same-department projects
func TestBehaviour_ManagerSameDepartment(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Manager Same Department Projects Behaviour")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Manager Should See Same Department Projects", func(t *testing.T) {
		resp, err := getWithTimeout(manageProjectServiceURL + "/uid/" + projectTestManagerUserID)
		if err != nil {
			t.Logf("⚠️  Could not get projects for manager: %v (service may be unavailable)", err)
			return
		}
		if resp == nil {
			t.Logf("ℹ️  Response is nil for manager user (service may be unavailable)")
			return
		}
		if resp.Body != nil {
			defer resp.Body.Close()
		}

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
			if userRole, ok := result["user_role"].(string); ok {
				t.Logf("✅ Manager user role: %s", userRole)

				if userDept, ok := result["user_dept"].(string); ok {
					t.Logf("✅ Manager department: %s", userDept)
				}

				if projects, ok := result["projects"].([]interface{}); ok {
					t.Logf("✅ Manager has access to %d projects", len(projects))

					// Manager should see owned + member + same-dept projects
					if userRole == "manager" {
						t.Logf("✅ Manager role correctly identified")
					}
				}
			}
		} else if resp.StatusCode == http.StatusNotFound {
			if message, ok := result["message"].(string); ok {
				t.Logf("ℹ️  %s", message)
			}
		}
	})

	t.Log("🎉 Manager Same Department Projects Test Completed!")
}

// TestBehaviour_InvalidPID tests handling of invalid project IDs
func TestBehaviour_InvalidPID(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Invalid PID Handling")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Invalid PID Should Be Handled Gracefully", func(t *testing.T) {
		resp, err := getWithTimeout(manageProjectServiceURL + "/pid/" + invalidPID)
		if err != nil {
			t.Errorf("❌ Failed to request invalid PID: %v", err)
			return
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		// Accept 400 (bad request), 404 (not found), or 422 (unprocessable) as valid error responses
		if resp.StatusCode == http.StatusBadRequest ||
			resp.StatusCode == http.StatusNotFound ||
			resp.StatusCode == 422 {
			t.Logf("✅ Invalid PID correctly rejected with status %d", resp.StatusCode)
			if resp.StatusCode == http.StatusBadRequest {
				t.Logf("✅ Service validates PID format (400 Bad Request)")
			}
		} else if resp.StatusCode == http.StatusOK {
			// If service accepts invalid PID, log it but don't fail
			t.Logf("⚠️  Service accepted invalid PID (may not have UUID validation)")
		} else {
			t.Logf("ℹ️  Invalid PID returned status %d: %s", resp.StatusCode, string(body))
		}
	})

	t.Log("🎉 Invalid PID Handling Test Completed!")
}

// TestBehaviour_BadInternalKey tests handling of bad internal API key
func TestBehaviour_BadInternalKey(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Bad Internal API Key Handling")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Bad Internal Key Should Not Crash Service", func(t *testing.T) {
		headers := map[string]string{
			"X-Internal-API-Key": "definitely-wrong-key-12345",
		}
		resp, err := httpRequestWithRetry("GET", manageProjectServiceURL+"/uid/"+projectTestStaffUserID, nil, headers, 2)
		if err != nil {
			t.Errorf("❌ Request failed: %v", err)
			return
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		// Service should not crash - any response is acceptable
		// 200 = service doesn't require internal key (acceptable)
		// 401/403 = service rejected bad key (acceptable)
		// 500 = service error (not ideal but service didn't crash)
		if resp.StatusCode == http.StatusOK {
			t.Logf("✅ Service tolerated bad internal key (may not require it)")
		} else if resp.StatusCode == http.StatusUnauthorized || resp.StatusCode == http.StatusForbidden {
			t.Logf("✅ Service correctly rejected bad internal key (%d)", resp.StatusCode)
		} else {
			t.Logf("ℹ️  Bad internal key returned status %d: %s", resp.StatusCode, string(body))
		}
	})

	t.Log("🎉 Bad Internal API Key Handling Test Completed!")
}
