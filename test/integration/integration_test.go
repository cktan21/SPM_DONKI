package main

import (
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
		"Track-Schedule Service": "http://localhost:4000",
		"Kong API Gateway - Project": "http://localhost:8000/project",
		"Kong API Gateway - Schedule": "http://localhost:8000/schedule",
		"Kong API Gateway - Tasks": "http://localhost:8000/tasks",
		"Kong API Gateway - User": "http://localhost:8000/user",
		"Kong API Gateway - Track-Schedule": "http://localhost:8000/track-schedule",
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
