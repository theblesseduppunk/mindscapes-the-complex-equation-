# utils.py
import random

# ------------------------------
# Random Scenario Generator
# ------------------------------
def generate_random_scenario(current_values):
    """
    Generate a random scenario based on current slider keys.
    Returns a dictionary with random values between 0.1 and 10.0.
    """
    return {k: round(random.uniform(0.1,10.0),1) for k in current_values.keys()}

# ------------------------------
# Complex Equation Function
# ------------------------------
def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    """
    Computes the Complex Equation for Consciousness (C).
    """
    try:
        C = (R * (alpha**theta) * S * Q * (1.3*A) * E * (1.6*M)) / (Dn * (beta**theta))
        return C
    except Exception as e:
        print("Error computing consciousness:", e)
        return 0

# ------------------------------
# Beginner Creativity Equation
# ------------------------------
def compute_creativity(R, D3):
    """
    Computes the Beginner Creativity equation: C = R / D^3
    """
    try:
        return R / (D3**3)
    except Exception as e:
        print("Error computing creativity:", e)
        return 0
