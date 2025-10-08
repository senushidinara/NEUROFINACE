// ----------------------------------------------------------------------
// Transaction Service Microservice (GoLang)
// Handles high-concurrency transaction processing and Checkpoint enforcement.
// ----------------------------------------------------------------------
package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

// TransactionRequest struct for incoming data
type TransactionRequest struct {
	UserID    string  `json:"userId"`
	Amount    float64 `json:"amount"`
	Recipient string  `json:"recipient"`
	// Includes real-time AI context inputs
	Stress      float64 `json:"stress"`
	TypingSpeed int     `json:"typingSpeed"`
}

// CheckpointResponse struct for returning results to the frontend
type CheckpointResponse struct {
	Status        string `json:"status"` // PENDING, BLOCKED, APPROVED
	ECS           int    `json:"ecs"`
	CheckNeeded   bool   `json:"checkNeeded"`
	Reason        string `json:"reason"`
}

func checkpointHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Only POST method is allowed", http.StatusMethodNotAllowed)
		return
	}

	var req TransactionRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// 1. Mock Call to Fusion Engine (in a real app, this is an HTTP/gRPC call)
	// For demo: Assume we received an ECS score from the Fusion Engine Service
	mockECS := 45 // Simulating a RED ZONE score based on request inputs

	// 2. Checkpoint Logic
	if mockECS < 50 {
		// Enforce the Emotional Checkpoint
		response := CheckpointResponse{
			Status:      "PENDING",
			ECS:         mockECS,
			CheckNeeded: true,
			Reason:      fmt.Sprintf("ECS is %d. Mandatory 5-second checkpoint initiated.", mockECS),
		}
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(response)
		return
	}

	// 3. Approved Transaction
	response := CheckpointResponse{
		Status:      "APPROVED",
		ECS:         mockECS,
		CheckNeeded: false,
		Reason:      "Emotional confidence is stable. Transaction approved.",
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(response)
}

func main() {
	// Go is chosen for the transaction service due to its high-concurrency performance.
	http.HandleFunc("/api/v1/pay/initiate_checkpoint", checkpointHandler)
	fmt.Println("Transaction Service running on :8082...")
	http.ListenAndServe(":8082", nil)
}
// ----------------------------------------------------------------------
