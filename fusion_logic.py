# ----------------------------------------------------------------------
# Unit Test: Verifies the core ECS calculation logic.
# ----------------------------------------------------------------------
import unittest
import sys
import os

# Add the fusion engine service directory to the path to import the function
sys.path.insert(0, os.path.abspath('../../services/fusion_engine'))
from app import calculate_ecs

class TestFusionLogic(unittest.TestCase):
    
    def test_low_risk_scenario(self):
        """Test case: User is calm, should result in high ECS (GREEN ZONE)."""
        ecs, factors = calculate_ecs(stress=0.1, typing_risk=0.1, behavioral_risk=0.1)
        self.assertGreaterEqual(ecs, 80)
        self.assertIn('Emotional', factors)

    def test_critical_risk_scenario(self):
        """Test case: User is highly stressed, should result in low ECS (RED ZONE)."""
        # High stress (0.9), high typing risk (0.8)
        ecs, factors = calculate_ecs(stress=0.9, typing_risk=0.8, behavioral_risk=0.5)
        self.assertLess(ecs, 50)
        self.assertGreaterEqual(factors['Emotional'], 40) # Emotional factor dominates
        
    def test_yellow_zone_scenario(self):
        """Test case: User is moderately risky, should land in YELLOW ZONE."""
        ecs, factors = calculate_ecs(stress=0.5, typing_risk=0.4, behavioral_risk=0.2)
        self.assertTrue(50 <= ecs < 75)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
# ----------------------------------------------------------------------
