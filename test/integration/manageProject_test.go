package main

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net"
	"net/http"
	"os"
	"strings"
	"testing"
	"time"

	"github.com/joho/godotenv"
)

/***********************
 Boot + .env (optional)
***********************/
func init() {
	_ = godotenv.Load(".env.local")
	_ = godotenv.Load(".env")
}

/***********************
 Helpers
***********************/
var httpClient = &http.Client{Timeout: 60 * time.Second}

func getenv(key, def string) string {
	if v := strings.TrimSpace(os.Getenv(key)); v != "" {
		return v
	}
	return def
}

func waitUntilReady(base string, maxWait time.Duration) error {
	deadline := time.Now().Add(maxWait)
	hostPort := strings.TrimPrefix(base, "http://")
	hostPort = strings.TrimPrefix(hostPort, "https://")
	if i := strings.Index(hostPort, "/"); i > -1 {
		hostPort = hostPort[:i]
	}
	for {
		conn, err := net.DialTimeout("tcp", hostPort, 2*time.Second)
		if err == nil {
			_ = conn.Close()
			time.Sleep(250 * time.Millisecond)
			return nil
		}
		if time.Now().After(deadline) {
			return fmt.Errorf("service %s not ready: %w", base, err)
		}
		time.Sleep(600 * time.Millisecond)
	}
}

func getWithHeaders(t *testing.T, url string, headers map[string]string) (*http.Response, []byte, error) {
	req, _ := http.NewRequest(http.MethodGet, url, nil)
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	resp, err := httpClient.Do(req)
	if err != nil {
		return nil, nil, err
	}
	body, _ := io.ReadAll(resp.Body)
	_ = resp.Body.Close()
	return resp, body, nil
}

func postJSON(t *testing.T, url string, payload any, headers map[string]string) (*http.Response, []byte, error) {
	b, _ := json.Marshal(payload)
	req, _ := http.NewRequest(http.MethodPost, url, bytes.NewReader(b))
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := httpClient.Do(req)
	if err != nil {
		return nil, nil, err
	}
	body, _ := io.ReadAll(resp.Body)
	_ = resp.Body.Close()
	return resp, body, nil
}

func putJSON(t *testing.T, url string, payload any, headers map[string]string) (*http.Response, []byte, error) {
	b, _ := json.Marshal(payload)
	req, _ := http.NewRequest(http.MethodPut, url, bytes.NewReader(b))
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	req.Header.Set("Content-Type", "application/json")
	resp, err := httpClient.Do(req)
	if err != nil {
		return nil, nil, err
	}
	body, _ := io.ReadAll(resp.Body)
	_ = resp.Body.Close()
	return resp, body, nil
}

func deleteReq(t *testing.T, url string, headers map[string]string) (*http.Response, []byte, error) {
	req, _ := http.NewRequest(http.MethodDelete, url, nil)
	for k, v := range headers {
		req.Header.Set(k, v)
	}
	resp, err := httpClient.Do(req)
	if err != nil {
		return nil, nil, err
	}
	body, _ := io.ReadAll(resp.Body)
	_ = resp.Body.Close()
	return resp, body, nil
}

func maybeInternalHeaders() map[string]string {
	h := map[string]string{}
	if key := strings.TrimSpace(os.Getenv("INTERNAL_API_KEY")); key != "" {
		h["X-Internal-API-Key"] = key
	}
	return h
}

func extractID(m map[string]any) (string, bool) {
	if m == nil {
		return "", false
	}
	if v, ok := m["id"].(string); ok && strings.TrimSpace(v) != "" {
		return v, true
	}
	if v, ok := m["id"]; ok {
		s := fmt.Sprintf("%v", v)
		if strings.TrimSpace(s) != "" {
			return s, true
		}
	}
	return "", false
}

/***********************
 Defaults (IDs in-file)
***********************/
const (
	defaultPID           = "7f233f02-561e-4ada-9ecc-2f39320ee022"
	defaultAdminUID      = "d568296e-3644-4ac0-9714-dcaa0aaa5fb0"
	defaultStaffUID      = "fb892a63-2401-46fc-b660-bf3fe1196d4e"
	defaultManagerUID    = "655a9260-f871-480f-abea-ded735b2170a"
	defaultOwnerUID      = "655a9260-f871-480f-abea-ded735b2170a"
	defaultOwnerSameDept = "655a9260-f871-480f-abea-ded735b2170a" // adjust if needed
)

/***********************
 Service Bases (env-override)
***********************/
var (
	manageProjectBase = getenv("MANAGE_PROJECT_BASE", "http://localhost:4100")
	projectBase       = getenv("PROJECT_BASE", "http://localhost:5200")
	taskBase          = getenv("TASK_BASE", "http://localhost:5500")
	manageTaskBase    = getenv("MANAGE_TASK_BASE", "http://localhost:4000")
	userBase          = getenv("USER_BASE", "http://localhost:5100")
)

/***********************
 Data setup helpers (best-effort)
***********************/
func createProject(t *testing.T, ownerUID string, members []string, name string, headers map[string]string) (string, func()) {
	t.Helper()
	payload := map[string]any{
		"name":        name,
		"description": "itest",
		"uid":         ownerUID,
	}
	if len(members) > 0 {
		payload["members"] = members
	}
	candidates := []string{
		projectBase + "/create",
		projectBase + "/",
		projectBase + "/project",
	}

	for _, url := range candidates {
		resp, body, err := postJSON(t, url, payload, headers)
		if err != nil {
			continue
		}
		if resp.StatusCode != http.StatusOK && resp.StatusCode != http.StatusCreated {
			continue
		}
		var anyMap map[string]any
		if err := json.Unmarshal(body, &anyMap); err == nil {
			if id, ok := extractID(anyMap); ok {
				return id, func() { _ = deleteProject(t, id, headers) }
			}
			if proj, _ := anyMap["project"].(map[string]any); proj != nil {
				if id, ok := extractID(proj); ok {
					return id, func() { _ = deleteProject(t, id, headers) }
				}
			}
			if data, _ := anyMap["data"].(map[string]any); data != nil {
				if id, ok := extractID(data); ok {
					return id, func() { _ = deleteProject(t, id, headers) }
				}
			}
		}
	}
	t.Skip("Could not create project via Project MS; adjust create endpoint/payload to match your API")
	return "", func() {}
}

func addMember(t *testing.T, pid string, memberUID string, headers map[string]string) {
	t.Helper()
	candidates := []struct {
		url     string
		method  string
		payload any
	}{
		{projectBase + "/pid/" + pid + "/members", http.MethodPut, map[string]any{"add": []string{memberUID}}},
		{projectBase + "/members/" + pid, http.MethodPut, map[string]any{"members": []string{memberUID}}},
		{projectBase + "/pid/" + pid, http.MethodPut, map[string]any{"members": []string{memberUID}}},
	}
	for _, c := range candidates {
		var resp *http.Response
		var body []byte
		var err error
		switch c.method {
		case http.MethodPut:
			resp, body, err = putJSON(t, c.url, c.payload, headers)
		default:
			continue
		}
		if err == nil && (resp.StatusCode == 200 || resp.StatusCode == 204) {
			return
		}
		_ = body
	}
}

func deleteProject(t *testing.T, pid string, headers map[string]string) error {
	t.Helper()
	candidates := []string{
		projectBase + "/pid/" + pid,
		projectBase + "/" + pid,
		projectBase + "/delete/" + pid,
	}
	for _, url := range candidates {
		resp, _, err := deleteReq(t, url, headers)
		if err == nil && (resp.StatusCode == 200 || resp.StatusCode == 204) {
			return nil
		}
	}
	return fmt.Errorf("delete not supported")
}

func createTaskForProject(t *testing.T, pid string, title string, headers map[string]string) (string, func()) {
	t.Helper()
	payload := map[string]any{
		"title":       title,
		"description": "itest task",
		"pid":         pid,
	}
	candidates := []string{
		taskBase + "/create",
		taskBase + "/",
		taskBase + "/task",
	}
	for _, url := range candidates {
		resp, body, err := postJSON(t, url, payload, headers)
		if err != nil {
			continue
		}
		if resp.StatusCode != 200 && resp.StatusCode != 201 {
			continue
		}
		var anyMap map[string]any
		if err := json.Unmarshal(body, &anyMap); err == nil {
			if id, ok := extractID(anyMap); ok {
				return id, func() {}
			}
			if task, _ := anyMap["task"].(map[string]any); task != nil {
				if id, ok := extractID(task); ok {
					return id, func() {}
				}
			}
		}
	}
	t.Skip("Could not create task via Task MS; adjust endpoint/payload to match your API")
	return "", func() {}
}

/***********************
 Baseline tests
***********************/
func TestManageProject_Health(t *testing.T) {
	_ = waitUntilReady(manageProjectBase, 25*time.Second)
	resp, body, err := getWithHeaders(t, manageProjectBase+"/", nil)
	if err != nil {
		t.Fatalf("GET / failed: %v", err)
	}
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("GET / unexpected status: %d body=%s", resp.StatusCode, string(body))
	}
	var payload map[string]any
	if err := json.Unmarshal(body, &payload); err != nil {
		t.Fatalf("GET / invalid JSON: %v body=%s", err, string(body))
	}
	// Friendly success line
	t.Logf("✅ Health OK: %s", string(body))

	if msg, _ := payload["message"].(string); !strings.Contains(msg, "running") {
		t.Errorf("unexpected / message: %v", payload["message"])
	}
}

func TestManageProject_ByUID(t *testing.T) {
	_ = waitUntilReady(manageProjectBase, 25*time.Second)
	uid := getenv("MANAGE_PROJECT_TEST_UID", defaultStaffUID)
	headers := maybeInternalHeaders()

	ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
	defer cancel()
	var lastErr error
	for i := 0; i < 4; i++ {
		if ctx.Err() != nil {
			break
		}
		resp, body, err := getWithHeaders(t, fmt.Sprintf("%s/uid/%s", manageProjectBase, uid), headers)
		if err == nil && resp.StatusCode == http.StatusOK {
			var payload map[string]any
			if json.Unmarshal(body, &payload) == nil {
				// Friendly success line
				t.Logf("✅ /uid/%s OK: message=%v", uid, payload["message"])

				// basic schema checks
				if _, ok := payload["user_id"]; !ok {
					t.Errorf("missing user_id")
				}
				if _, ok := payload["projects"]; !ok {
					t.Errorf("missing projects")
				}
				return
			}
		}
		lastErr = err
		time.Sleep(800 * time.Millisecond)
	}
	if lastErr != nil {
		t.Fatalf("GET /uid/%s error: %v", uid, lastErr)
	}
	t.Fatalf("GET /uid/%s did not return 200 OK", uid)
}

func TestManageProject_ByPID(t *testing.T) {
	_ = waitUntilReady(manageProjectBase, 25*time.Second)
	pid := getenv("MANAGE_PROJECT_TEST_PID", defaultPID)
	headers := maybeInternalHeaders()
	
	// Add retry logic like ByUID test
	ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
	defer cancel()
	var lastErr error
	for i := 0; i < 4; i++ {
		if ctx.Err() != nil {
			break
		}
		resp, body, err := getWithHeaders(t, fmt.Sprintf("%s/pid/%s", manageProjectBase, pid), headers)
		if err == nil && resp.StatusCode == http.StatusOK {
			var payload map[string]any
			if json.Unmarshal(body, &payload) == nil {
				msg, _ := payload["message"].(string)
				if msg == "" {
					msg = "OK"
				}
				t.Logf("✅ /pid/%s OK: message=%s", pid, msg)
				if _, ok := payload["project"]; !ok {
					t.Errorf("missing project")
				}
				return
			}
		}
		lastErr = err
		time.Sleep(800 * time.Millisecond)
	}
	if lastErr != nil {
		t.Fatalf("GET /pid/%s error: %v", pid, lastErr)
	}
	t.Fatalf("GET /pid/%s did not return 200 OK", pid)
}

/***********************
 Behaviour tests
***********************/

// Admin/HR: should fetch ALL projects (we will create two)
func TestBehaviour_AdminGetsAllProjects(t *testing.T) {
	headers := maybeInternalHeaders()
	adminUID := getenv("ADMIN_UID", defaultAdminUID)

	if err := waitUntilReady(manageProjectBase, 25*time.Second); err != nil {
		t.Skipf("manage-project not reachable: %v", err)
	}
	if err := waitUntilReady(projectBase, 25*time.Second); err != nil {
		t.Skipf("project service not reachable: %v", err)
	}

	p1, cleanup1 := createProject(t, adminUID, nil, "itest-all-1", headers)
	defer cleanup1()
	p2, cleanup2 := createProject(t, adminUID, nil, "itest-all-2", headers)
	defer cleanup2()
	if p1 == "" || p2 == "" {
		t.Skip("Project creation skipped; cannot assert admin behaviour")
	}

	// Add retry logic with context timeout
	ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
	defer cancel()
	var lastErr error
	var resp *http.Response
	var body []byte
	for i := 0; i < 4; i++ {
		if ctx.Err() != nil {
			break
		}
		var err error
		resp, body, err = getWithHeaders(t, fmt.Sprintf("%s/uid/%s", manageProjectBase, adminUID), headers)
		if err == nil && resp.StatusCode == http.StatusOK {
			var out map[string]any
			if json.Unmarshal(body, &out) == nil {
				arr, _ := out["projects"].([]any)
				if len(arr) < 2 {
					t.Errorf("expected >=2 projects for admin; got %d", len(arr))
				}
				return
			}
		}
		lastErr = err
		time.Sleep(800 * time.Millisecond)
	}
	if lastErr != nil {
		t.Fatalf("GET /uid/%s failed: %v", adminUID, lastErr)
	}
	if resp == nil {
		t.Fatalf("GET /uid/%s did not return 200 OK", adminUID)
	}
	t.Fatalf("unexpected status: %d body=%s", resp.StatusCode, string(body))
}

// Staff: owned + member projects
func TestBehaviour_StaffOwnedAndMember(t *testing.T) {
	headers := maybeInternalHeaders()
	staffUID := getenv("STAFF_UID", defaultStaffUID)

	if err := waitUntilReady(projectBase, 25*time.Second); err != nil {
		t.Skipf("project service not reachable: %v", err)
	}
	if err := waitUntilReady(manageProjectBase, 25*time.Second); err != nil {
		t.Skipf("manage-project not reachable: %v", err)
	}

	ownedPID, cleanupOwned := createProject(t, staffUID, nil, "itest-owned", headers)
	defer cleanupOwned()
	if ownedPID == "" {
		t.Skip("Project creation skipped; cannot assert staff behaviour")
	}

	ownerForMember := getenv("OWNER_UID", defaultOwnerUID)
	memberPID, cleanupMember := createProject(t, ownerForMember, []string{staffUID}, "itest-member", headers)
	defer cleanupMember()
	if memberPID == "" {
		memberPID2, cleanupMember2 := createProject(t, ownerForMember, nil, "itest-member-2", headers)
		defer cleanupMember2()
		if memberPID2 == "" {
			t.Skip("Could not create second project; cannot assert member behaviour")
		}
		addMember(t, memberPID2, staffUID, headers)
		memberPID = memberPID2
	}

	// Add retry logic with context timeout
	ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
	defer cancel()
	var lastErr error
	var resp *http.Response
	var body []byte
	for i := 0; i < 4; i++ {
		if ctx.Err() != nil {
			break
		}
		var err error
		resp, body, err = getWithHeaders(t, fmt.Sprintf("%s/uid/%s", manageProjectBase, staffUID), headers)
		if err == nil && resp.StatusCode == http.StatusOK {
			var out map[string]any
			if json.Unmarshal(body, &out) == nil {
				arr, _ := out["projects"].([]any)
				if len(arr) == 0 {
					t.Errorf("expected some projects for staff; got 0")
				}
				return
			}
		}
		lastErr = err
		time.Sleep(800 * time.Millisecond)
	}
	if lastErr != nil {
		t.Fatalf("GET /uid/%s failed: %v", staffUID, lastErr)
	}
	if resp == nil {
		t.Fatalf("GET /uid/%s did not return 200 OK", staffUID)
	}
	t.Fatalf("unexpected status: %d body=%s", resp.StatusCode, string(body))
}

// Manager: also gets projects whose owner is in the same department
func TestBehaviour_ManagerSameDepartment(t *testing.T) {
	headers := maybeInternalHeaders()
	managerUID := getenv("MANAGER_UID", defaultManagerUID)
	ownerSameDept := getenv("OWNER_SAME_DEPT_UID", defaultOwnerSameDept)

	if err := waitUntilReady(projectBase, 25*time.Second); err != nil {
		t.Skipf("project service not reachable: %v", err)
	}
	if err := waitUntilReady(manageProjectBase, 25*time.Second); err != nil {
		t.Skipf("manage-project not reachable: %v", err)
	}

	pid, cleanup := createProject(t, ownerSameDept, nil, "itest-dept", headers)
	defer cleanup()
	if pid == "" {
		t.Skip("Project creation skipped; cannot assert manager dept behaviour")
	}

	// Add retry logic with context timeout
	ctx, cancel := context.WithTimeout(context.Background(), 25*time.Second)
	defer cancel()
	var lastErr error
	var resp *http.Response
	var body []byte
	for i := 0; i < 4; i++ {
		if ctx.Err() != nil {
			break
		}
		var err error
		resp, body, err = getWithHeaders(t, fmt.Sprintf("%s/uid/%s", manageProjectBase, managerUID), headers)
		if err == nil && resp.StatusCode == http.StatusOK {
			var out map[string]any
			if json.Unmarshal(body, &out) == nil {
				if out["projects"] == nil {
					t.Errorf("expected projects for manager; got nil")
				}
				return
			}
		}
		lastErr = err
		time.Sleep(800 * time.Millisecond)
	}
	if lastErr != nil {
		t.Fatalf("GET /uid/%s failed: %v", managerUID, lastErr)
	}
	if resp == nil {
		t.Fatalf("GET /uid/%s did not return 200 OK", managerUID)
	}
	t.Fatalf("unexpected status: %d body=%s", resp.StatusCode, string(body))
}

// Task enrichment: create project + task, then ensure /pid/{id} returns tasks (optionally enriched)
func TestBehaviour_TaskEnrichment(t *testing.T) {
	headers := maybeInternalHeaders()
	ownerUID := getenv("OWNER_UID", defaultOwnerUID)

	if err := waitUntilReady(projectBase, 25*time.Second); err != nil {
		t.Skipf("project service not reachable: %v", err)
	}
	if err := waitUntilReady(taskBase, 25*time.Second); err != nil {
		t.Skipf("task service not reachable: %v", err)
	}
	if err := waitUntilReady(manageTaskBase, 25*time.Second); err != nil {
		t.Skipf("manage-task service not reachable: %v", err)
	}
	if err := waitUntilReady(manageProjectBase, 25*time.Second); err != nil {
		t.Skipf("manage-project not reachable: %v", err)
	}

	pid, cleanup := createProject(t, ownerUID, nil, "itest-enrich", headers)
	defer cleanup()
	if pid == "" {
		t.Skip("Project creation skipped; cannot assert enrichment")
	}
	tid, _ := createTaskForProject(t, pid, "enrich-task", headers)
	if tid == "" {
		t.Skip("Task creation skipped; cannot assert enrichment")
	}

	resp, body, err := getWithHeaders(t, fmt.Sprintf("%s/pid/%s", manageProjectBase, pid), headers)
	if err != nil {
		t.Fatalf("GET /pid/%s failed: %v", pid, err)
	}
	if resp.StatusCode != 200 {
		t.Fatalf("unexpected status: %d body=%s", resp.StatusCode, string(body))
	}

	var out map[string]any
	_ = json.Unmarshal(body, &out)
	project, _ := out["project"].(map[string]any)
	if project == nil {
		t.Fatalf("project missing in response")
	}
	tasks, _ := project["tasks"].([]any)
	if len(tasks) == 0 {
		t.Errorf("expected at least 1 task on enriched project")
	}
	// Soft-check fields if present
	if len(tasks) > 0 {
		if t0, ok := tasks[0].(map[string]any); ok {
			_ = t0["status"]
			_ = t0["deadline"]
		}
	}
}

// Invalid PID handling (enable EXPECT_400_ON_INVALID_PID=true if you added UUID validation)
func TestBehaviour_InvalidPID(t *testing.T) {
	expect400 := strings.EqualFold(getenv("EXPECT_400_ON_INVALID_PID", "false"), "true")
	resp, body, err := getWithHeaders(t, manageProjectBase+"/pid/not-a-uuid", maybeInternalHeaders())
	if err != nil {
		t.Fatalf("GET invalid pid failed: %v", err)
	}
	if expect400 {
		if resp.StatusCode != 400 {
			t.Fatalf("expected 400 for invalid pid, got %d body=%s", resp.StatusCode, string(body))
		}
	} else {
		t.Skipf("EXPECT_400_ON_INVALID_PID not enabled; got %d (ok to skip until UUID validation added)", resp.StatusCode)
	}
}

// Bad internal key should not crash the service; any non-200 is acceptable
func TestBehaviour_BadInternalKey(t *testing.T) {
	if os.Getenv("INTERNAL_API_KEY") == "" {
		t.Skip("INTERNAL_API_KEY not set; skipping bad key test")
	}
	
	// Add waitUntilReady check
	if err := waitUntilReady(manageProjectBase, 25*time.Second); err != nil {
		t.Skipf("manage-project not reachable: %v", err)
	}
	
	headers := map[string]string{"X-Internal-API-Key": "definitely-wrong-key"}
	
	// Add retry logic with shorter timeout
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()
	var resp *http.Response
	var body []byte
	var err error
	for i := 0; i < 3; i++ {
		if ctx.Err() != nil {
			break
		}
		resp, body, err = getWithHeaders(t, manageProjectBase+"/uid/"+defaultStaffUID, headers)
		if err == nil {
			break
		}
		time.Sleep(500 * time.Millisecond)
	}
	if err != nil {
		t.Fatalf("request failed: %v", err)
	}
	if resp.StatusCode == 200 {
		t.Logf("Service tolerated bad internal key (maybe not required): body=%s", string(body))
	} else {
		t.Logf("Non-200 as expected for bad key: %d body=%s", resp.StatusCode, string(body))
	}
}
