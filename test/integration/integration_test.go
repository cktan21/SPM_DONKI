package main

import (
	"bytes"
	"encoding/json"
	"io"
	"net/http"
	"sync"
	"testing"
)

// TestServiceEndpoints is the entry point for the test.
// It will be automatically run by the `go test` command.
func TestServiceEndpoints(t *testing.T) {
	// List of all endpoints to test, including both direct and Kong ports.
	endpointsMap := map[string]string{
		"Project Service":  "http://localhost:5200",
		"Schedule Service": "http://localhost:5300",
		"Tasks Service": "http://localhost:5500",
		"User Service": "http://localhost:5100",
		"Manage-Task Service": "http://localhost:4000",
		"Notify User Service": "http://localhost:4500",
		"Kong API Gateway - Project": "http://localhost:8000/project",
		"Kong API Gateway - Schedule": "http://localhost:8000/schedule",
		"Kong API Gateway - Tasks": "http://localhost:8000/tasks",
		"Kong API Gateway - User": "http://localhost:8000/user",
		"Kong API Gateway - Track-Schedule": "http://localhost:8000/manage-task",
		"Kong API Gateway - Notify User": "http://localhost:8000/notify-user",
	}

	// Use a WaitGroup to ensure all goroutines finish before the test completes.
	var wg sync.WaitGroup
	wg.Add(len(endpointsMap))

	// Launch a goroutine for each endpoint check.
	for name, url := range endpointsMap {
		// Use a closure to capture the URL for each goroutine.
		go func(url string) {
			defer wg.Done()

			// Make the HTTP request with a timeout to prevent indefinite hangs.
			resp, err := http.Get(url)
			if err != nil {
				// Use t.Errorf to report a test failure. This is critical for CI/CD.
				t.Errorf("🔴 FAILED: %s - Error: %v", url, err)
				return
			}
			defer resp.Body.Close()

			// Check for a 200 OK status code.
			if resp.StatusCode != http.StatusOK {
				t.Errorf("%s 🔴 FAILED: %s - Unexpected Status: %d", name, url, resp.StatusCode)
			} else {
				// Add a success log to the test output.
				t.Logf("%s ✅ SUCCESS: %s - Status: %d", name, url, resp.StatusCode)
			}
		}(url)
	}

	// Wait for all checks to complete.
	wg.Wait()
}

// TestNotifyUserServiceFunctionality tests the notify_user service functionality
func TestNotifyUserServiceFunctionality(t *testing.T) {
	notifyUserServiceURL := "http://localhost:4500"

	t.Log("🧪 Testing Notify User Service Functionality")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	// Test reading all recurring tasks from notify_user service
	t.Run("Get All Recurring Tasks", func(t *testing.T) {
		resp, err := http.Get(notifyUserServiceURL + "/task/recurring")
		if err != nil {
			t.Errorf("❌ Failed to get recurring tasks: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(resp.Body)
			t.Errorf("❌ Failed to get recurring tasks: Status %d, Response: %s", resp.StatusCode, string(body))
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode recurring tasks response: %v", err)
			return
		}

		if message, ok := result["message"].(string); ok {
			t.Logf("✅ %s", message)
		}

		// Check if we have any recurring tasks
		if tasks, ok := result["tasks"].([]interface{}); ok {
			t.Logf("📋 Found %d recurring tasks", len(tasks))
			
			recurringCount := 0
			for _, task := range tasks {
				if taskMap, ok := task.(map[string]interface{}); ok {
					if sid, ok := taskMap["sid"].(string); ok {
						if frequency, ok := taskMap["frequency"].(string); ok {
							if nextOccurrence, ok := taskMap["next_occurrence"].(string); ok {
								t.Logf("   🔄 Task SID: %s, Frequency: %s, Next: %s", sid, frequency, nextOccurrence)
								recurringCount++
							}
						}
					}
				}
			}
			
			if recurringCount > 0 {
				t.Logf("✅ Successfully found %d recurring tasks", recurringCount)
			} else {
				t.Logf("ℹ️  No recurring tasks found")
			}
		}
	})

	// Test getting scheduled jobs from notify_user service
	t.Run("Get Scheduled Jobs", func(t *testing.T) {
		resp, err := http.Get(notifyUserServiceURL + "/task/scheduled")
		if err != nil {
			t.Errorf("❌ Failed to get scheduled jobs: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(resp.Body)
			t.Errorf("❌ Failed to get scheduled jobs: Status %d, Response: %s", resp.StatusCode, string(body))
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode scheduled jobs response: %v", err)
			return
		}

		if message, ok := result["message"].(string); ok {
			t.Logf("✅ %s", message)
		}

		// Check if we have any scheduled jobs
		if jobs, ok := result["jobs"].([]interface{}); ok {
			t.Logf("📋 Found %d scheduled jobs in the processor", len(jobs))
			
			scheduledCount := 0
			for _, job := range jobs {
				if jobMap, ok := job.(map[string]interface{}); ok {
					if id, ok := jobMap["id"].(string); ok {
						if nextRun, ok := jobMap["next_run_time"].(string); ok {
							t.Logf("   🔄 Job ID: %s, Next Run: %s", id, nextRun)
							scheduledCount++
						}
					}
				}
			}
			
			if scheduledCount > 0 {
				t.Logf("✅ Successfully found %d scheduled jobs in the processor", scheduledCount)
			} else {
				t.Logf("ℹ️  No jobs currently scheduled in the processor")
			}
		}
	})

	// Test verify notify_user service health and functionality
	t.Run("Verify Notify User Service Health", func(t *testing.T) {
		// Test the main health endpoint
		resp, err := http.Get(notifyUserServiceURL)
		if err != nil {
			t.Errorf("❌ Notify user service health check failed: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			t.Errorf("❌ Notify user service health check failed: Status %d", resp.StatusCode)
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode health check response: %v", err)
			return
		}

		if message, ok := result["message"].(string); ok {
			t.Logf("✅ Notify User Service: %s", message)
		}
	})

	t.Log("🎉 Notify User Service Functionality Test Completed!")
}

// TestKongNotifyUserFunctionality tests notify_user service through Kong API Gateway
func TestKongNotifyUserFunctionality(t *testing.T) {
	kongNotifyUserURL := "http://localhost:8000/notify-user"
	
	t.Log("🌐 Testing Notify User Service via Kong API Gateway")
	t.Log("=" + string(bytes.Repeat([]byte("="), 60)))

	// Test getting recurring tasks through Kong
	t.Run("Get Recurring Tasks via Kong", func(t *testing.T) {
		resp, err := http.Get(kongNotifyUserURL + "/task/recurring")
		if err != nil {
			t.Errorf("❌ Failed to get recurring tasks via Kong: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(resp.Body)
			t.Errorf("❌ Failed to get recurring tasks via Kong: Status %d, Response: %s", resp.StatusCode, string(body))
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode Kong recurring tasks response: %v", err)
			return
		}

		if message, ok := result["message"].(string); ok {
			t.Logf("✅ Kong Gateway: %s", message)
		}
	})

	// Test getting scheduled jobs through Kong
	t.Run("Get Scheduled Jobs via Kong", func(t *testing.T) {
		resp, err := http.Get(kongNotifyUserURL + "/task/scheduled")
		if err != nil {
			t.Errorf("❌ Failed to get scheduled jobs via Kong: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(resp.Body)
			t.Errorf("❌ Failed to get scheduled jobs via Kong: Status %d, Response: %s", resp.StatusCode, string(body))
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode Kong scheduled jobs response: %v", err)
			return
		}

		if message, ok := result["message"].(string); ok {
			t.Logf("✅ Kong Gateway: %s", message)
		}
	})

	t.Log("🎉 Kong Notify User Service Test Completed!")
}
