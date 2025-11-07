package main

import (
	"io"
	"net"
	"net/http"
	"time"
)

// HTTP client configuration for CI/CD resilience
var httpClient = &http.Client{
	Timeout: 30 * time.Second, // Increased timeout for CI/CD (was 10s)
	Transport: &http.Transport{
		MaxIdleConns:        100,
		MaxIdleConnsPerHost: 10,
		IdleConnTimeout:     90 * time.Second,
	},
}

// Helper function to make HTTP requests with retry logic
func httpRequestWithRetry(method, url string, body io.Reader, headers map[string]string, maxRetries int) (*http.Response, error) {
	var resp *http.Response
	var err error
	
	for attempt := 0; attempt <= maxRetries; attempt++ {
		if attempt > 0 {
			// Exponential backoff: 1s, 2s, 4s
			backoff := time.Duration(1<<uint(attempt-1)) * time.Second
			time.Sleep(backoff)
		}
		
		req, err := http.NewRequest(method, url, body)
		if err != nil {
			return nil, err
		}
		
		// Set headers
		for k, v := range headers {
			req.Header.Set(k, v)
		}
		
		resp, err = httpClient.Do(req)
		if err == nil {
			return resp, nil
		}
		
		// Check if error is retryable (timeout or connection error)
		if netErr, ok := err.(net.Error); ok && netErr.Timeout() {
			continue // Retry on timeout
		}
		if attempt < maxRetries {
			continue // Retry on other errors
		}
	}
	
	return resp, err
}

// Convenience wrapper for GET requests with retry
func httpGetWithRetry(url string, maxRetries int) (*http.Response, error) {
	return httpRequestWithRetry("GET", url, nil, nil, maxRetries)
}

// Convenience wrapper for POST requests with retry
func httpPostWithRetry(url string, contentType string, body io.Reader, maxRetries int) (*http.Response, error) {
	headers := map[string]string{"Content-Type": contentType}
	return httpRequestWithRetry("POST", url, body, headers, maxRetries)
}

// Convenience wrapper for PUT requests with retry
func httpPutWithRetry(url string, contentType string, body io.Reader, maxRetries int) (*http.Response, error) {
	headers := map[string]string{"Content-Type": contentType}
	return httpRequestWithRetry("PUT", url, body, headers, maxRetries)
}

// Convenience wrapper for DELETE requests with retry
func httpDeleteWithRetry(url string, maxRetries int) (*http.Response, error) {
	return httpRequestWithRetry("DELETE", url, nil, nil, maxRetries)
}

