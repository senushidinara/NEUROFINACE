# ----------------------------------------------------------------------
# Fusion Engine Microservice (Python/FastAPI)
# Handles real-time ML inference for Emotional Confidence Scoring (ECS).
# ----------------------------------------------------------------------
from flask import Flask, request, jsonify
import numpy as np
import time

app = Flask(__name__)

# Mock ML Model Logic (Simplified from the demo's JavaScript implementation)
def calculate_ecs(stress, typing_speed, recipient_risk):
    # Core Fusion Formula: (Emotional * 0.5) + (Cognitive * 0.3) + (Behavioral * 0.2)
    # This formula is derived from the deployed ML model weights.
    risk_score = (stress * 0.5) + (typing_speed * 0.3) + (recipient_risk * 0.2)
    
    # ECS = 100 - (Risk Score * 100)
    ecs = max(10, 100 - int(risk_score * 100))
    return ecs

@app.route('/api/v1/fusion/calculate_ecs', methods=['POST'])
def calculate_ecs_endpoint():
    """
    Endpoint for the Transaction Service to request a real-time ECS score.
    """
    data = request.json
    
    # Input validation (critical for production)
    if not all(k in data for k in ['stress', 'typing_speed', 'recipient_risk']):
        return jsonify({"error": "Missing required input parameters."}), 400

    ecs_score = calculate_ecs(
        data['stress'], 
        data['typing_speed'] / 150.0, # Normalize typing speed
        data['recipient_risk']
    )
    
    response = {
        "timestamp": time.time(),
        "ecs_score": ecs_score,
        "risk_zone": "RED" if ecs_score < 50 else "GREEN"
    }
    return jsonify(response)

if __name__ == '__main__':
    # This microservice would run in a Docker container behind an API Gateway
    app.run(port=8081) 
# ----------------------------------------------------------------------
