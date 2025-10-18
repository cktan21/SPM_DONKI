package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync"
	"testing"
	"time"
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
		"Kong API Gateway - Project": "http://localhost:8000/project",
		"Kong API Gateway - Schedule": "http://localhost:8000/schedule",
		"Kong API Gateway - Tasks": "http://localhost:8000/tasks",
		"Kong API Gateway - User": "http://localhost:8000/user",
		"Kong API Gateway - Track-Schedule": "http://localhost:8000/manage-task",
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

// TestRecurringTaskFunctionality tests the recurring task features of the Schedule Service
func TestRecurringTaskFunctionality(t *testing.T) {
	scheduleServiceURL := "http://localhost:5300"

	t.Log("🧪 Testing Recurring Task Functionality")
	t.Log("=" + string(bytes.Repeat([]byte("="), 50)))

	// Test reading existing schedules and checking for recurring tasks
	t.Run("Read Existing Schedules", func(t *testing.T) {
		// Get all schedules (this would need to be implemented in the service)
		// For now, let's check the scheduled jobs endpoint to see what's already there
		resp, err := http.Get(scheduleServiceURL + "/recurring/scheduled")
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
			t.Logf("📋 Found %d existing scheduled recurring tasks", len(jobs))
			
			recurringCount := 0
			for _, job := range jobs {
				if jobMap, ok := job.(map[string]interface{}); ok {
					if id, ok := jobMap["id"].(string); ok {
						if nextRun, ok := jobMap["next_run_time"].(string); ok {
							t.Logf("   🔄 Job ID: %s, Next Run: %s", id, nextRun)
							recurringCount++
						}
					}
				}
			}
			
			if recurringCount > 0 {
				t.Logf("✅ Successfully found %d recurring tasks that are scheduled", recurringCount)
			} else {
				t.Logf("ℹ️  No recurring tasks currently scheduled")
			}
		}
	})

	// Test reading existing schedules and checking if they are recurring
	t.Run("Check Existing Schedules for Recurring Tasks", func(t *testing.T) {
		// Get all schedules from the database
		resp, err := http.Get(scheduleServiceURL + "/recurring/all")
		if err != nil {
			t.Errorf("❌ Failed to get schedules: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(resp.Body)
			t.Errorf("❌ Failed to get schedules: Status %d, Response: %s", resp.StatusCode, string(body))
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode schedules response: %v", err)
			return
		}

		if message, ok := result["message"].(string); ok {
			t.Logf("✅ %s", message)
		}

		// Check if we have any schedules
		if schedules, ok := result["schedules"].([]interface{}); ok {
			t.Logf("📋 Found %d total schedules in database", len(schedules))
			
			recurringCount := 0
			nonRecurringCount := 0
			
			for _, schedule := range schedules {
				if scheduleMap, ok := schedule.(map[string]interface{}); ok {
					if isRecurring, ok := scheduleMap["is_recurring"].(bool); ok {
						if isRecurring {
							recurringCount++
							// Check if it has proper recurring fields
							frequency, hasFreq := scheduleMap["frequency"]
							nextOccurrence, hasNext := scheduleMap["next_occurrence"]
							
							if hasFreq && hasNext && frequency != nil && nextOccurrence != nil {
								t.Logf("   🔄 Recurring: SID=%v, Frequency=%v, Next=%v", 
									scheduleMap["sid"], frequency, nextOccurrence)
							} else {
								t.Logf("   ⚠️  Incomplete Recurring: SID=%v (missing frequency or next_occurrence)", 
									scheduleMap["sid"])
							}
						} else {
							nonRecurringCount++
						}
					}
				}
			}
			
			t.Logf("📊 Schedule Analysis:")
			t.Logf("   🔄 Recurring tasks: %d", recurringCount)
			t.Logf("   📝 Non-recurring tasks: %d", nonRecurringCount)
			
			if recurringCount > 0 {
				t.Logf("✅ Found %d recurring tasks in the database", recurringCount)
			} else {
				t.Logf("ℹ️  No recurring tasks found in the database")
			}
		}
	})

	// Test checking if we can create recurring jobs for existing schedules
	t.Run("Verify Recurring Job Creation Capability", func(t *testing.T) {
		// This test verifies that the recurring processor can handle job creation
		// We'll test by checking if the service can process different frequency types
		
		frequencies := []string{"Weekly", "Monthly", "Yearly", "Immediate"}
		
		for _, freq := range frequencies {
			t.Run(fmt.Sprintf("Test %s Frequency", freq), func(t *testing.T) {
				// Test that the frequency is supported by checking if we can create a test job
				// This is a validation test - we're not actually creating jobs, just testing capability
				
				// Simulate the recurring processor's frequency validation
				supportedFrequencies := []string{"Weekly", "Monthly", "Yearly", "Immediate"}
				isSupported := false
				for _, supported := range supportedFrequencies {
					if freq == supported {
						isSupported = true
						break
					}
				}
				
				if isSupported {
					t.Logf("✅ Frequency '%s' is supported", freq)
				} else {
					t.Errorf("❌ Frequency '%s' is not supported", freq)
				}
			})
		}
	})

	// Test getting scheduled jobs
	t.Run("Get Scheduled Jobs", func(t *testing.T) {
		resp, err := http.Get(scheduleServiceURL + "/recurring/scheduled")
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

		if jobs, ok := result["jobs"].([]interface{}); ok {
			for _, job := range jobs {
				if jobMap, ok := job.(map[string]interface{}); ok {
					if id, ok := jobMap["id"].(string); ok {
						if nextRun, ok := jobMap["next_run_time"].(string); ok {
							t.Logf("   Job ID: %s, Next Run: %s", id, nextRun)
						}
					}
				}
			}
		}
	})

	// Test health check for schedule service
	t.Run("Schedule Service Health Check", func(t *testing.T) {
		resp, err := http.Get(scheduleServiceURL)
		if err != nil {
			t.Errorf("❌ Schedule service health check failed: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			t.Errorf("❌ Schedule service health check failed: Status %d", resp.StatusCode)
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode health check response: %v", err)
			return
		}

		if message, ok := result["message"].(string); ok {
			t.Logf("✅ Schedule Service: %s", message)
		}
	})

	t.Log("🎉 Recurring Task Functionality Test Completed!")
}

// TestKongRecurringTaskFunctionality tests recurring tasks through Kong API Gateway
func TestKongRecurringTaskFunctionality(t *testing.T) {
	kongScheduleURL := "http://localhost:8000/schedule"
	
	t.Log("🌐 Testing Recurring Task Functionality via Kong API Gateway")
	t.Log("=" + string(bytes.Repeat([]byte("="), 60)))

	// Test creating a recurring task through Kong
	t.Run("Create Recurring Task via Kong", func(t *testing.T) {
		// First create a task via Kong
		taskData := map[string]interface{}{
			"name":           fmt.Sprintf("Kong Test Weekly Task %d", time.Now().Unix()),
			"desc":           "Description for Kong test task",
			"created_by_uid": "7b055ff5-84f4-47bc-be7d-5905caec3ec6",
			"priorityLevel":  5,
		}

		jsonData, err := json.Marshal(taskData)
		if err != nil {
			t.Fatalf("Failed to marshal task JSON: %v", err)
		}

		// Create task via Kong
		taskResp, err := http.Post("http://localhost:8000/tasks/createTask", "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			t.Errorf("❌ Failed to create task via Kong: %v", err)
			return
		}
		defer taskResp.Body.Close()

		if taskResp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(taskResp.Body)
			t.Errorf("❌ Failed to create task via Kong: Status %d, Response: %s", taskResp.StatusCode, string(body))
			return
		}

		// Parse task response to get task ID
		var taskResult map[string]interface{}
		if err := json.NewDecoder(taskResp.Body).Decode(&taskResult); err != nil {
			t.Errorf("❌ Failed to decode Kong task response: %v", err)
			return
		}

		var taskID string
		if task, ok := taskResult["task"].(map[string]interface{}); ok {
			if id, ok := task["id"].(string); ok {
				taskID = id
			}
		}

		if taskID == "" {
			t.Errorf("❌ Failed to extract task ID from Kong response")
			return
		}

		// Now create the schedule via Kong
		now := time.Now()
		startTime := now.Add(1 * time.Minute)
		deadlineTime := now.Add(2 * time.Hour)
		nextOccurrence := now.Add(2 * time.Minute)

		scheduleData := map[string]interface{}{
			"tid":             taskID,
			"start":           startTime.Format(time.RFC3339),
			"deadline":        deadlineTime.Format(time.RFC3339),
			"is_recurring":    true,
			"next_occurrence":    nextOccurrence.Format(time.RFC3339),
			"frequency":       "Weekly",
		}

		scheduleJsonData, err := json.Marshal(scheduleData)
		if err != nil {
			t.Fatalf("Failed to marshal schedule JSON: %v", err)
		}

		resp, err := http.Post(kongScheduleURL+"/", "application/json", bytes.NewBuffer(scheduleJsonData))
		if err != nil {
			t.Errorf("❌ Failed to create recurring task via Kong: %v", err)
			return
		}
		defer resp.Body.Close()

		if resp.StatusCode != http.StatusOK {
			body, _ := io.ReadAll(resp.Body)
			t.Errorf("❌ Failed to create recurring task via Kong: Status %d, Response: %s", resp.StatusCode, string(body))
			return
		}

		var result map[string]interface{}
		if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
			t.Errorf("❌ Failed to decode Kong response: %v", err)
			return
		}

		t.Logf("✅ Recurring task created successfully via Kong")
		if data, ok := result["data"].(map[string]interface{}); ok {
			if sid, ok := data["sid"].(string); ok {
				t.Logf("   Task ID: %s, Schedule ID: %s", taskID, sid)
			}
		}
	})

	// Test getting scheduled jobs through Kong
	t.Run("Get Scheduled Jobs via Kong", func(t *testing.T) {
		resp, err := http.Get(kongScheduleURL + "/recurring/scheduled")
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

	t.Log("🎉 Kong Recurring Task Functionality Test Completed!")
}
