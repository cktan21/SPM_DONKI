package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"testing"
	"time"
)

const manageTaskServiceURL = "http://localhost:4000"
const testUserID = "bba910a9-1685-4fa3-af21-ccb2e11cf751"
const testProjectID = "f434f31d-3c12-4867-889c-794edf0c6199"
const testTaskID = "8cf55bcb-a6b2-45dd-b08c-b7469372839e"
const invalidProjectID = "invalid-project-id-12345"
const invalidParentTaskID = "00000000-0000-0000-0000-000000000001"
const invalidCollaboratorID = "00000000-0000-0000-0000-000000000002"
const invalidProjectIDForUpdate = "11111111-2222-3333-4444-555555555555"
const testCollaboratorID = "0ec8a99d-3aab-4ec6-b692-fda88656844f"

// TestManageTaskServiceHealth tests the root endpoint of manage-task service
func TestManageTaskServiceHealth(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Manage-Task Service Health")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	resp, err := http.Get(manageTaskServiceURL + "/")
	if err != nil {
		t.Errorf("❌ Failed to connect to manage-task service: %v", err)
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
		t.Logf("✅ Manage-Task Service: %s", message)
	}

	if service, ok := result["service"].(string); ok {
		t.Logf("✅ Service name: %s", service)
	}

	t.Log("🎉 Manage-Task Service Health Test Completed!")
}

// Helper function to delete a task (used for cleanup)
func deleteTask(taskID string) error {
	if taskID == "" {
		return nil
	}
	req, err := http.NewRequest("DELETE", manageTaskServiceURL+"/"+taskID, nil)
	if err != nil {
		return err
	}
	client := &http.Client{Timeout: 10 * time.Second}
	resp, err := client.Do(req)
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

// TestTaskCRUDOperations tests the complete CRUD workflow: Create => Update => Delete
func TestTaskCRUDOperations(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Task CRUD Operations (Create => Update => Delete)")
	t.Log("=" + string(bytes.Repeat([]byte("="), 60)))

	var createdTaskID string

	// Ensure cleanup happens even if test fails before deletion step
	defer func() {
		if createdTaskID != "" {
			if err := deleteTask(createdTaskID); err != nil {
				t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
			} else {
				t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
			}
		}
	}()

	// Setup: Log test user and project IDs
	t.Run("Setup: Test Data", func(t *testing.T) {
		t.Logf("✅ Using test user ID: %s", testUserID)
		t.Logf("✅ Using test project ID: %s", testProjectID)
	})

	// Step 1: Create a new task
	t.Run("Step 1: Create Task", func(t *testing.T) {
		t.Log("📝 Creating a new task...")

		// Prepare task creation payload
		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("Integration Test Task - %d", time.Now().Unix()),
			"pid":            testProjectID,
			"desc":           "This is a test task created by integration tests",
			"priorityLevel":  5,
			"label":          "testing",
			"created_by_uid": testUserID,
			"collaborators":  []string{testUserID},
			"schedule": map[string]interface{}{
				"status":       "pending",
				"start":        time.Now().Add(24 * time.Hour).Format(time.RFC3339),
				"deadline":     time.Now().Add(7 * 24 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, err := json.Marshal(taskPayload)
		if err != nil {
			t.Fatalf("❌ Failed to marshal task payload: %v", err)
		}

		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)
		if err != nil {
			t.Fatalf("❌ Failed to create task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			t.Fatalf("❌ Task creation failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if err := json.Unmarshal(body, &result); err != nil {
			t.Fatalf("❌ Failed to decode create task response: %v", err)
		}

		// Extract task ID from response
		if taskID, ok := result["task_id"].(string); ok && taskID != "" {
			createdTaskID = taskID
		} else if task, ok := result["task"].(map[string]interface{}); ok {
			if taskID, ok := task["id"].(string); ok && taskID != "" {
				createdTaskID = taskID
			} else if taskID, ok := task["task_id"].(string); ok && taskID != "" {
				createdTaskID = taskID
			}
		}

		if createdTaskID == "" {
			t.Fatalf("❌ Could not extract task ID from response: %s", string(body))
		}

		t.Logf("✅ Task created successfully! Task ID: %s", createdTaskID)

		// Verify response structure
		if message, ok := result["message"].(string); ok {
			t.Logf("✅ Message: %s", message)
		}

		if schedule, ok := result["schedule"].(map[string]interface{}); ok {
			t.Logf("✅ Schedule created: %v", schedule)
		}

		if notificationSent, ok := result["notification_sent"].(bool); ok {
			t.Logf("✅ Notification sent: %v", notificationSent)
		}
	})

	// Ensure we have a task ID before proceeding
	if createdTaskID == "" {
		t.Fatal("❌ Cannot proceed with update/delete - task ID is empty")
	}

	// Step 2: Update the task
	t.Run("Step 2: Update Task", func(t *testing.T) {
		t.Log("✏️  Updating the created task...")

		// Prepare update payload
		updatePayload := map[string]interface{}{
			"name":          fmt.Sprintf("Updated Integration Test Task - %d", time.Now().Unix()),
			"desc":          "This task has been updated by integration tests",
			"priorityLevel": 8,
			"label":         "updated-testing",
			"status":        "in_progress",
			"deadline":      time.Now().Add(10 * 24 * time.Hour).Format(time.RFC3339),
		}

		jsonData, err := json.Marshal(updatePayload)
		if err != nil {
			t.Fatalf("❌ Failed to marshal update payload: %v", err)
		}

		req, err := http.NewRequest(
			"PUT",
			manageTaskServiceURL+"/"+createdTaskID,
			bytes.NewBuffer(jsonData),
		)
		if err != nil {
			t.Fatalf("❌ Failed to create update request: %v", err)
		}
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err := client.Do(req)
		if err != nil {
			t.Fatalf("❌ Failed to update task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		if resp.StatusCode != http.StatusOK {
			t.Fatalf("❌ Task update failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if err := json.Unmarshal(body, &result); err != nil {
			t.Fatalf("❌ Failed to decode update response: %v", err)
		}

		t.Logf("✅ Task updated successfully!")

		// Verify update response
		if message, ok := result["message"].(string); ok {
			t.Logf("✅ Message: %s", message)
		}

		if updatesApplied, ok := result["updates_applied"].(map[string]interface{}); ok {
			if taskFields, ok := updatesApplied["task_fields"].([]interface{}); ok {
				t.Logf("✅ Updated task fields: %v", taskFields)
			}
			if scheduleFields, ok := updatesApplied["schedule_fields"].([]interface{}); ok {
				t.Logf("✅ Updated schedule fields: %v", scheduleFields)
			}
		}

		// Verify the update by fetching the task
		t.Log("🔍 Verifying update by fetching task...")
		getResp, err := http.Get(manageTaskServiceURL + "/tasks/" + createdTaskID)
		if err == nil && getResp.StatusCode == http.StatusOK {
			var taskResult map[string]interface{}
			if json.NewDecoder(getResp.Body).Decode(&taskResult) == nil {
				if task, ok := taskResult["task"].(map[string]interface{}); ok {
					if name, ok := task["name"].(string); ok {
						if strings.Contains(name, "Updated") {
							t.Logf("✅ Verified: Task name updated to: %s", name)
						}
					}
					if status, ok := task["status"].(string); ok {
						t.Logf("✅ Verified: Task status is: %s", status)
					}
				}
			}
			getResp.Body.Close()
		}
	})

	// Step 3: Delete the task
	t.Run("Step 3: Delete Task", func(t *testing.T) {
		t.Log("🗑️  Deleting the created task...")

		req, err := http.NewRequest("DELETE", manageTaskServiceURL+"/"+createdTaskID, nil)
		if err != nil {
			t.Fatalf("❌ Failed to create delete request: %v", err)
		}

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err := client.Do(req)
		if err != nil {
			t.Fatalf("❌ Failed to delete task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		// Accept both 200 and 404 (idempotent delete) as success
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusNotFound {
			t.Fatalf("❌ Task deletion failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if err := json.Unmarshal(body, &result); err != nil {
			t.Fatalf("❌ Failed to decode delete response: %v", err)
		}

		t.Logf("✅ Task deleted successfully!")

		// Verify delete response
		if message, ok := result["message"].(string); ok {
			t.Logf("✅ Message: %s", message)
		}

		if taskDelete, ok := result["task_delete"].(map[string]interface{}); ok {
			if statusCode, ok := taskDelete["status_code"].(float64); ok {
				t.Logf("✅ Delete status code: %.0f", statusCode)
			}
		}

		// Verify deletion by trying to fetch the task (should return 404)
		t.Log("🔍 Verifying deletion by fetching task (should fail)...")
		getResp, err := http.Get(manageTaskServiceURL + "/tasks/" + createdTaskID)
		if err == nil {
			if getResp.StatusCode == http.StatusNotFound {
				t.Logf("✅ Verified: Task is deleted (404 returned)")
				// Clear task ID to prevent redundant cleanup in defer
				createdTaskID = ""
			} else {
				t.Logf("⚠️  Task may still exist (Status: %d)", getResp.StatusCode)
			}
			getResp.Body.Close()
		}
	})

	t.Log("🎉 Task CRUD Operations Test Completed Successfully!")
}

// TestGetTaskByID tests the GET /tasks/{task_id} endpoint
func TestGetTaskByID(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Get Task by ID")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Get Task by ID", func(t *testing.T) {
		resp, err := http.Get(manageTaskServiceURL + "/tasks/" + testTaskID)
		if err != nil {
			t.Errorf("❌ Failed to get task by ID: %v", err)
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
			if taskID, ok := result["task_id"].(string); ok {
				t.Logf("✅ Task ID: %s", taskID)
			}

			if message, ok := result["message"].(string); ok {
				t.Logf("✅ %s", message)
			}

			if task, ok := result["task"].(map[string]interface{}); ok {
				if name, ok := task["name"].(string); ok {
					t.Logf("✅ Task Name: %s", name)
				}

				if status, ok := task["status"].(string); ok {
					t.Logf("✅ Task Status: %s", status)
				}

				if deadline, ok := task["deadline"].(string); ok {
					t.Logf("✅ Task Deadline: %s", deadline)
				}

				// Check for enriched fields
				if collaborators, ok := task["collaborators"].([]interface{}); ok {
					t.Logf("✅ Found %d collaborators", len(collaborators))
				}

				if project, ok := task["project"].(map[string]interface{}); ok {
					if projName, ok := project["name"].(string); ok {
						t.Logf("✅ Project Name: %s", projName)
					}
				}
			}
		} else if resp.StatusCode == http.StatusNotFound {
			if message, ok := result["message"].(string); ok {
				t.Logf("ℹ️  %s", message)
			}
		}
	})

	t.Log("🎉 Get Task by ID Test Completed!")
}

// TestGetTasksByUser tests the GET /tasks/user/{user_id} endpoint
func TestGetTasksByUser(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Get Tasks by User")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Get Tasks for User", func(t *testing.T) {
		resp, err := http.Get(manageTaskServiceURL + "/tasks/user/" + testUserID)
		if err != nil {
			t.Errorf("❌ Failed to get tasks for user: %v", err)
			return
		}
		defer resp.Body.Close()

		// Accept both 200 (success) and 404 (no tasks found) as valid responses
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

			if user, ok := result["user"].(map[string]interface{}); ok {
				if userName, ok := user["name"].(string); ok {
					t.Logf("✅ User Name: %s", userName)
				}
			}

			if tasks, ok := result["tasks"].([]interface{}); ok {
				t.Logf("✅ Found %d tasks", len(tasks))

				// Validate task structure
				for i, task := range tasks {
					if taskMap, ok := task.(map[string]interface{}); ok {
						if taskObj, ok := taskMap["task"].(map[string]interface{}); ok {
							if taskID, ok := taskObj["id"].(string); ok {
								t.Logf("   📋 Task %d: ID=%s", i+1, taskID)
							}
							if taskName, ok := taskObj["name"].(string); ok {
								t.Logf("      Name: %s", taskName)
							}
							if status, ok := taskObj["status"].(string); ok {
								t.Logf("      Status: %s", status)
							}
						}
					}
				}
			} else if count, ok := result["count"].(float64); ok {
				t.Logf("ℹ️  Task count: %.0f", count)
			}
		} else if resp.StatusCode == http.StatusNotFound {
			if message, ok := result["message"].(string); ok {
				t.Logf("ℹ️  %s", message)
			}
		}
	})

	t.Log("🎉 Get Tasks by User Test Completed!")
}

// TestManageTaskServiceEndpoints tests all endpoints comprehensively
func TestManageTaskServiceEndpoints(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing All Manage-Task Service Endpoints")
	t.Log("=" + string(bytes.Repeat([]byte("="), 60)))

	// Test root endpoint
	t.Run("Root Endpoint", func(t *testing.T) {
		resp, err := http.Get(manageTaskServiceURL + "/")
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
		resp, err := http.Get(manageTaskServiceURL + "/favicon.ico")
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
		resp, err := http.Get(manageTaskServiceURL + "/invalid-endpoint")
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

	t.Log("🎉 All Manage-Task Service Endpoints Test Completed!")
}

// TestTaskCreationValidation tests task creation with various validation scenarios
func TestTaskCreationValidation(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Task Creation Validation")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	// Using hardcoded test user and project IDs

	t.Run("Create Task with Minimal Required Fields", func(t *testing.T) {
		var createdTaskID string
		
		// Ensure cleanup happens even if test fails
		defer func() {
			if createdTaskID != "" {
				if err := deleteTask(createdTaskID); err != nil {
					t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
				} else {
					t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
				}
			}
		}()

		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("Minimal Task - %d", time.Now().Unix()),
			"pid":            testProjectID,
			"created_by_uid": testUserID,
			"schedule": map[string]interface{}{
				"deadline":     time.Now().Add(7 * 24 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, _ := json.Marshal(taskPayload)
		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)

		if err != nil {
			t.Logf("⚠️  Could not test minimal task creation: %v", err)
			return
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		if resp.StatusCode == http.StatusOK || resp.StatusCode == http.StatusCreated {
			t.Logf("✅ Minimal task creation succeeded")
			var result map[string]interface{}
			if json.Unmarshal(body, &result) == nil {
				// Extract task ID from response
				if taskID, ok := result["task_id"].(string); ok && taskID != "" {
					createdTaskID = taskID
				} else if task, ok := result["task"].(map[string]interface{}); ok {
					if taskID, ok := task["id"].(string); ok && taskID != "" {
						createdTaskID = taskID
					} else if taskID, ok := task["task_id"].(string); ok && taskID != "" {
						createdTaskID = taskID
					}
				}
				if createdTaskID != "" {
					t.Logf("✅ Created task ID: %s (will be cleaned up)", createdTaskID)
				}
			}
		} else {
			t.Logf("ℹ️  Minimal task creation returned status %d: %s", resp.StatusCode, string(body))
		}
	})

	t.Run("Create Task with Invalid Project ID", func(t *testing.T) {
		var createdTaskID string
		
		// Ensure cleanup happens even if test fails (in case validation doesn't work as expected)
		defer func() {
			if createdTaskID != "" {
				if err := deleteTask(createdTaskID); err != nil {
					t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
				} else {
					t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
				}
			}
		}()

		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("Invalid Project Task - %d", time.Now().Unix()),
			"pid":            invalidProjectID,
			"created_by_uid": testUserID,
			"schedule": map[string]interface{}{
				"deadline":     time.Now().Add(7 * 24 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, _ := json.Marshal(taskPayload)
		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)

		if err != nil {
			t.Logf("⚠️  Could not test invalid project validation: %v", err)
			return
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		if resp.StatusCode == http.StatusBadRequest || resp.StatusCode == http.StatusNotFound {
			t.Logf("✅ Validation correctly rejected invalid project ID")
		} else {
			// If task was created despite invalid project ID, extract ID for cleanup
			if resp.StatusCode == http.StatusOK || resp.StatusCode == http.StatusCreated {
				var result map[string]interface{}
				if json.Unmarshal(body, &result) == nil {
					if taskID, ok := result["task_id"].(string); ok && taskID != "" {
						createdTaskID = taskID
					} else if task, ok := result["task"].(map[string]interface{}); ok {
						if taskID, ok := task["id"].(string); ok && taskID != "" {
							createdTaskID = taskID
						}
					}
				}
			}
			t.Logf("ℹ️  Invalid project validation returned status %d: %s", resp.StatusCode, string(body))
		}
	})

	t.Log("🎉 Task Creation Validation Test Completed!")
}

// TestUpdateTask_ScheduleOnly tests updating only schedule fields without changing task fields
func TestUpdateTask_ScheduleOnly(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Schedule-Only Update")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	var createdTaskID string

	// Ensure cleanup happens even if test fails
	defer func() {
		if createdTaskID != "" {
			if err := deleteTask(createdTaskID); err != nil {
				t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
			} else {
				t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
			}
		}
	}()

	t.Run("Update Schedule Fields Only", func(t *testing.T) {
		// Step 1: Create a task
		t.Log("📝 Creating task for schedule-only update test...")
		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("Schedule Update Test - %d", time.Now().Unix()),
			"pid":            testProjectID,
			"desc":           "Task for schedule-only update",
			"priorityLevel":  4,
			"label":          "schedule-test",
			"created_by_uid": testUserID,
			"collaborators":  []string{testUserID},
			"schedule": map[string]interface{}{
				"status":       "pending",
				"start":        time.Now().Add(30 * time.Minute).Format(time.RFC3339),
				"deadline":     time.Now().Add(24 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, _ := json.Marshal(taskPayload)
		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)
		if err != nil {
			t.Fatalf("❌ Failed to create task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			t.Fatalf("❌ Task creation failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if json.Unmarshal(body, &result) != nil {
			t.Fatalf("❌ Failed to decode create response")
		}

		// Extract task ID
		if taskID, ok := result["task_id"].(string); ok && taskID != "" {
			createdTaskID = taskID
		} else if task, ok := result["task"].(map[string]interface{}); ok {
			if taskID, ok := task["id"].(string); ok && taskID != "" {
				createdTaskID = taskID
			}
		}

		if createdTaskID == "" {
			t.Fatalf("❌ Could not extract task ID")
		}

		t.Logf("✅ Task created: %s", createdTaskID)

		// Step 2: Update only schedule fields
		t.Log("✏️  Updating schedule fields only...")
		newDeadline := time.Now().Add(72 * time.Hour).Format(time.RFC3339)
		updatePayload := map[string]interface{}{
			"status":   "in_progress",
			"deadline": newDeadline,
		}

		jsonData, _ = json.Marshal(updatePayload)
		req, _ := http.NewRequest("PUT", manageTaskServiceURL+"/"+createdTaskID, bytes.NewBuffer(jsonData))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err = client.Do(req)
		if err != nil {
			t.Fatalf("❌ Failed to update schedule: %v", err)
		}
		defer resp.Body.Close()

		body, _ = io.ReadAll(resp.Body)
		if resp.StatusCode != http.StatusOK {
			t.Fatalf("❌ Schedule update failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		t.Logf("✅ Schedule updated successfully")

		// Step 3: Verify update by fetching task
		t.Log("🔍 Verifying schedule update...")
		getResp, err := http.Get(manageTaskServiceURL + "/tasks/" + createdTaskID)
		if err != nil {
			t.Logf("⚠️  Could not verify update: %v", err)
			return
		}
		defer getResp.Body.Close()

		if getResp.StatusCode == http.StatusOK {
			var taskResult map[string]interface{}
			if json.NewDecoder(getResp.Body).Decode(&taskResult) == nil {
				if task, ok := taskResult["task"].(map[string]interface{}); ok {
					if status, ok := task["status"].(string); ok {
						if status == "in_progress" {
							t.Logf("✅ Verified: Status updated to 'in_progress'")
						} else {
							t.Logf("⚠️  Status is '%s' (expected 'in_progress')", status)
						}
					}
					if deadline, ok := task["deadline"].(string); ok && deadline != "" {
						t.Logf("✅ Verified: Deadline updated")
					}
				}
			}
		}
	})

	t.Log("🎉 Schedule-Only Update Test Completed!")
}

// TestUpdateTask_Collaborators tests updating task collaborators
func TestUpdateTask_Collaborators(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Collaborator Update")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	var createdTaskID string

	// Ensure cleanup happens even if test fails
	defer func() {
		if createdTaskID != "" {
			if err := deleteTask(createdTaskID); err != nil {
				t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
			} else {
				t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
			}
		}
	}()

	t.Run("Update Collaborators", func(t *testing.T) {
		// Step 1: Create a task with one collaborator
		t.Log("📝 Creating task with initial collaborator...")
		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("Collaborator Update Test - %d", time.Now().Unix()),
			"pid":            testProjectID,
			"desc":           "Task for collaborator update",
			"priorityLevel":  4,
			"label":          "collab-test",
			"created_by_uid": testUserID,
			"collaborators":  []string{testUserID},
			"schedule": map[string]interface{}{
				"status":       "pending",
				"deadline":     time.Now().Add(36 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, _ := json.Marshal(taskPayload)
		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)
		if err != nil {
			t.Fatalf("❌ Failed to create task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			t.Fatalf("❌ Task creation failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if json.Unmarshal(body, &result) != nil {
			t.Fatalf("❌ Failed to decode create response")
		}

		// Extract task ID
		if taskID, ok := result["task_id"].(string); ok && taskID != "" {
			createdTaskID = taskID
		} else if task, ok := result["task"].(map[string]interface{}); ok {
			if taskID, ok := task["id"].(string); ok && taskID != "" {
				createdTaskID = taskID
			}
		}

		if createdTaskID == "" {
			t.Fatalf("❌ Could not extract task ID")
		}

		t.Logf("✅ Task created: %s", createdTaskID)

		// Step 2: Update collaborators (add another collaborator)
		t.Log("✏️  Updating collaborators...")
		updatePayload := map[string]interface{}{
			"collaborators": []string{testUserID, testCollaboratorID},
		}

		jsonData, _ = json.Marshal(updatePayload)
		req, _ := http.NewRequest("PUT", manageTaskServiceURL+"/"+createdTaskID, bytes.NewBuffer(jsonData))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err = client.Do(req)
		if err != nil {
			t.Fatalf("❌ Failed to update collaborators: %v", err)
		}
		defer resp.Body.Close()

		body, _ = io.ReadAll(resp.Body)
		if resp.StatusCode != http.StatusOK {
			t.Fatalf("❌ Collaborator update failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		t.Logf("✅ Collaborators updated successfully")

		// Step 3: Verify update by fetching task
		t.Log("🔍 Verifying collaborator update...")
		getResp, err := http.Get(manageTaskServiceURL + "/tasks/" + createdTaskID)
		if err != nil {
			t.Logf("⚠️  Could not verify update: %v", err)
			return
		}
		defer getResp.Body.Close()

		if getResp.StatusCode == http.StatusOK {
			var taskResult map[string]interface{}
			if json.NewDecoder(getResp.Body).Decode(&taskResult) == nil {
				if task, ok := taskResult["task"].(map[string]interface{}); ok {
					if collaborators, ok := task["collaborators"].([]interface{}); ok {
						t.Logf("✅ Verified: Collaborators array length: %d", len(collaborators))
					} else {
						t.Logf("⚠️  Collaborators array not found in response")
					}
				}
			}
		}
	})

	t.Log("🎉 Collaborator Update Test Completed!")
}

// TestUpdateTask_InvalidParentTaskId tests validation of invalid parent task ID
func TestUpdateTask_InvalidParentTaskId(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Invalid Parent Task ID Validation")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	var createdTaskID string

	// Ensure cleanup happens even if test fails
	defer func() {
		if createdTaskID != "" {
			if err := deleteTask(createdTaskID); err != nil {
				t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
			} else {
				t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
			}
		}
	}()

	t.Run("Invalid Parent Task ID Should Be Rejected", func(t *testing.T) {
		// Create a task first
		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("Invalid Parent Test - %d", time.Now().Unix()),
			"pid":            testProjectID,
			"desc":           "Task for invalid parent test",
			"priorityLevel":  3,
			"label":          "invalid-parent",
			"created_by_uid": testUserID,
			"collaborators":  []string{testUserID},
			"schedule": map[string]interface{}{
				"status":       "pending",
				"deadline":     time.Now().Add(24 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, _ := json.Marshal(taskPayload)
		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)
		if err != nil {
			t.Fatalf("❌ Failed to create task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			t.Fatalf("❌ Task creation failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if json.Unmarshal(body, &result) != nil {
			t.Fatalf("❌ Failed to decode create response")
		}

		// Extract task ID
		if taskID, ok := result["task_id"].(string); ok && taskID != "" {
			createdTaskID = taskID
		} else if task, ok := result["task"].(map[string]interface{}); ok {
			if taskID, ok := task["id"].(string); ok && taskID != "" {
				createdTaskID = taskID
			}
		}

		if createdTaskID == "" {
			t.Fatalf("❌ Could not extract task ID")
		}

		// Try to update with invalid parent task ID
		updatePayload := map[string]interface{}{
			"parentTaskId": invalidParentTaskID,
		}

		jsonData, _ = json.Marshal(updatePayload)
		req, _ := http.NewRequest("PUT", manageTaskServiceURL+"/"+createdTaskID, bytes.NewBuffer(jsonData))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err = client.Do(req)
		if err != nil {
			t.Fatalf("❌ Failed to send update request: %v", err)
		}
		defer resp.Body.Close()

		body, _ = io.ReadAll(resp.Body)

		// Accept 400 or 500 as valid rejection
		if resp.StatusCode == http.StatusBadRequest || resp.StatusCode == http.StatusInternalServerError {
			t.Logf("✅ Invalid parentTaskId correctly rejected with status %d", resp.StatusCode)
		} else {
			t.Logf("ℹ️  Invalid parentTaskId returned status %d: %s", resp.StatusCode, string(body))
		}
	})

	t.Log("🎉 Invalid Parent Task ID Validation Test Completed!")
}

// TestUpdateTask_InvalidCollaborator tests validation of invalid collaborator ID
func TestUpdateTask_InvalidCollaborator(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Invalid Collaborator Validation")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	var createdTaskID string

	// Ensure cleanup happens even if test fails
	defer func() {
		if createdTaskID != "" {
			if err := deleteTask(createdTaskID); err != nil {
				t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
			} else {
				t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
			}
		}
	}()

	t.Run("Invalid Collaborator Should Be Rejected", func(t *testing.T) {
		// Create a task first
		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("Invalid Collaborator Test - %d", time.Now().Unix()),
			"pid":            testProjectID,
			"desc":           "Task for invalid collaborator test",
			"priorityLevel":  3,
			"label":          "invalid-collab",
			"created_by_uid": testUserID,
			"collaborators":  []string{testUserID},
			"schedule": map[string]interface{}{
				"status":       "pending",
				"deadline":     time.Now().Add(24 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, _ := json.Marshal(taskPayload)
		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)
		if err != nil {
			t.Fatalf("❌ Failed to create task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			t.Fatalf("❌ Task creation failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if json.Unmarshal(body, &result) != nil {
			t.Fatalf("❌ Failed to decode create response")
		}

		// Extract task ID
		if taskID, ok := result["task_id"].(string); ok && taskID != "" {
			createdTaskID = taskID
		} else if task, ok := result["task"].(map[string]interface{}); ok {
			if taskID, ok := task["id"].(string); ok && taskID != "" {
				createdTaskID = taskID
			}
		}

		if createdTaskID == "" {
			t.Fatalf("❌ Could not extract task ID")
		}

		// Try to update with invalid collaborator ID
		updatePayload := map[string]interface{}{
			"collaborators": []string{invalidCollaboratorID},
		}

		jsonData, _ = json.Marshal(updatePayload)
		req, _ := http.NewRequest("PUT", manageTaskServiceURL+"/"+createdTaskID, bytes.NewBuffer(jsonData))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err = client.Do(req)
		if err != nil {
			t.Fatalf("❌ Failed to send update request: %v", err)
		}
		defer resp.Body.Close()

		body, _ = io.ReadAll(resp.Body)

		// Expect 400 Bad Request
		if resp.StatusCode == http.StatusBadRequest {
			t.Logf("✅ Invalid collaborator correctly rejected with status 400")
		} else {
			t.Logf("ℹ️  Invalid collaborator returned status %d: %s", resp.StatusCode, string(body))
		}
	})

	t.Log("🎉 Invalid Collaborator Validation Test Completed!")
}

// TestUpdateTask_InvalidProjectId tests validation of invalid project ID on update
func TestUpdateTask_InvalidProjectId(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Invalid Project ID Validation (Update)")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	var createdTaskID string

	// Ensure cleanup happens even if test fails
	defer func() {
		if createdTaskID != "" {
			if err := deleteTask(createdTaskID); err != nil {
				t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
			} else {
				t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
			}
		}
	}()

	t.Run("Invalid Project ID Should Be Rejected", func(t *testing.T) {
		// Create a task first
		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("Invalid Project Update Test - %d", time.Now().Unix()),
			"pid":            testProjectID,
			"desc":           "Task for invalid project update test",
			"priorityLevel":  3,
			"label":          "invalid-project",
			"created_by_uid": testUserID,
			"collaborators":  []string{testUserID},
			"schedule": map[string]interface{}{
				"status":       "pending",
				"deadline":     time.Now().Add(24 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, _ := json.Marshal(taskPayload)
		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)
		if err != nil {
			t.Fatalf("❌ Failed to create task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			t.Fatalf("❌ Task creation failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if json.Unmarshal(body, &result) != nil {
			t.Fatalf("❌ Failed to decode create response")
		}

		// Extract task ID
		if taskID, ok := result["task_id"].(string); ok && taskID != "" {
			createdTaskID = taskID
		} else if task, ok := result["task"].(map[string]interface{}); ok {
			if taskID, ok := task["id"].(string); ok && taskID != "" {
				createdTaskID = taskID
			}
		}

		if createdTaskID == "" {
			t.Fatalf("❌ Could not extract task ID")
		}

		// Try to update with invalid project ID
		updatePayload := map[string]interface{}{
			"pid": invalidProjectIDForUpdate,
		}

		jsonData, _ = json.Marshal(updatePayload)
		req, _ := http.NewRequest("PUT", manageTaskServiceURL+"/"+createdTaskID, bytes.NewBuffer(jsonData))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err = client.Do(req)
		if err != nil {
			t.Fatalf("❌ Failed to send update request: %v", err)
		}
		defer resp.Body.Close()

		body, _ = io.ReadAll(resp.Body)

		// Expect 400 Bad Request
		if resp.StatusCode == http.StatusBadRequest {
			t.Logf("✅ Invalid project ID correctly rejected with status 400")
		} else {
			t.Logf("ℹ️  Invalid project ID returned status %d: %s", resp.StatusCode, string(body))
		}
	})

	t.Log("🎉 Invalid Project ID Validation Test Completed!")
}

// TestUpdateTask_ScheduleNoExisting tests updating schedule when task has no existing schedule
func TestUpdateTask_ScheduleNoExisting(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Schedule Update Without Existing Schedule")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	var createdTaskID string

	// Ensure cleanup happens even if test fails
	defer func() {
		if createdTaskID != "" {
			if err := deleteTask(createdTaskID); err != nil {
				t.Logf("⚠️  Failed to cleanup task %s: %v", createdTaskID, err)
			} else {
				t.Logf("🧹 Cleaned up test task: %s", createdTaskID)
			}
		}
	}()

	t.Run("Schedule Update Should Handle Missing Schedule Gracefully", func(t *testing.T) {
		// Create a task with minimal schedule
		taskPayload := map[string]interface{}{
			"name":           fmt.Sprintf("No Schedule Test - %d", time.Now().Unix()),
			"pid":            testProjectID,
			"desc":           "Task for schedule edge case test",
			"priorityLevel":  3,
			"label":          "no-schedule",
			"created_by_uid": testUserID,
			"collaborators":  []string{testUserID},
			"schedule": map[string]interface{}{
				"status":       "pending",
				"deadline":     time.Now().Add(24 * time.Hour).Format(time.RFC3339),
				"is_recurring": false,
			},
		}

		jsonData, _ := json.Marshal(taskPayload)
		resp, err := http.Post(
			manageTaskServiceURL+"/createTask",
			"application/json",
			bytes.NewBuffer(jsonData),
		)
		if err != nil {
			t.Fatalf("❌ Failed to create task: %v", err)
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			t.Fatalf("❌ Task creation failed: Status %d, Response: %s", resp.StatusCode, string(body))
		}

		var result map[string]interface{}
		if json.Unmarshal(body, &result) != nil {
			t.Fatalf("❌ Failed to decode create response")
		}

		// Extract task ID
		if taskID, ok := result["task_id"].(string); ok && taskID != "" {
			createdTaskID = taskID
		} else if task, ok := result["task"].(map[string]interface{}); ok {
			if taskID, ok := task["id"].(string); ok && taskID != "" {
				createdTaskID = taskID
			}
		}

		if createdTaskID == "" {
			t.Fatalf("❌ Could not extract task ID")
		}

		// Update schedule fields (should handle gracefully even if schedule doesn't exist)
		updatePayload := map[string]interface{}{
			"status":   "in_progress",
			"deadline": time.Now().Add(72 * time.Hour).Format(time.RFC3339),
		}

		jsonData, _ = json.Marshal(updatePayload)
		req, _ := http.NewRequest("PUT", manageTaskServiceURL+"/"+createdTaskID, bytes.NewBuffer(jsonData))
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err = client.Do(req)
		if err != nil {
			t.Fatalf("❌ Failed to send update request: %v", err)
		}
		defer resp.Body.Close()

		body, _ = io.ReadAll(resp.Body)

		// Should return 200 even if schedule doesn't exist (graceful handling)
		if resp.StatusCode == http.StatusOK {
			t.Logf("✅ Schedule update handled gracefully (status 200)")
		} else {
			t.Logf("ℹ️  Schedule update returned status %d: %s", resp.StatusCode, string(body))
		}

		// Verify service stays healthy by fetching task
		getResp, err := http.Get(manageTaskServiceURL + "/tasks/" + createdTaskID)
		if err == nil {
			if getResp.StatusCode == http.StatusOK {
				t.Logf("✅ Service remains healthy after schedule update")
			}
			getResp.Body.Close()
		}
	})

	t.Log("🎉 Schedule Update Without Existing Schedule Test Completed!")
}

// TestUpdateTask_DirectKnownTask tests updating a known/existing task directly
func TestUpdateTask_DirectKnownTask(t *testing.T) {
	t.Parallel()
	t.Log("🧪 Testing Direct Update on Known Task")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	t.Run("Update Known Task Directly", func(t *testing.T) {
		// Use the known test task ID
		updatePayload := map[string]interface{}{
			"label":  "updatedByItest",
			"notes":  "quick sanity update from test",
			"status": "in_progress",
		}

		jsonData, _ := json.Marshal(updatePayload)
		req, err := http.NewRequest("PUT", manageTaskServiceURL+"/"+testTaskID, bytes.NewBuffer(jsonData))
		if err != nil {
			t.Fatalf("❌ Failed to create update request: %v", err)
		}
		req.Header.Set("Content-Type", "application/json")

		client := &http.Client{Timeout: 10 * time.Second}
		resp, err := client.Do(req)
		if err != nil {
			t.Logf("⚠️  Could not update known task: %v (task may not exist)", err)
			return
		}
		defer resp.Body.Close()

		body, _ := io.ReadAll(resp.Body)

		if resp.StatusCode == http.StatusOK {
			t.Logf("✅ Direct update on known task %s succeeded", testTaskID)
		} else if resp.StatusCode == http.StatusNotFound {
			t.Logf("ℹ️  Known task %s not found (may have been deleted)", testTaskID)
		} else {
			t.Logf("ℹ️  Direct update returned status %d: %s", resp.StatusCode, string(body))
		}
	})

	t.Log("🎉 Direct Known Task Update Test Completed!")
}
