# utils.py
import random

# ------------------------------
# Compute Consciousness
# ------------------------------
def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    """
    Compute consciousness using the refined complex equation.
    """
    try:
        return (R * (alpha ** theta) * S * Q * (1.3 * A) * E * (1.6 * M)) / (Dn * (beta ** theta))
    except ZeroDivisionError:
        return 0

# ------------------------------
# Compute Creativity (Beginner Equation)
# ------------------------------
def compute_creativity(R, D3):
    """
    Beginner equation for creativity.
    """
    try:
        return R / (D3 ** 3)
    except ZeroDivisionError:
        return 0

# ------------------------------
# Generate Random Scenario
# ------------------------------
def generate_random_scenario(current_values):
    """
    Generate random scenario values for all variables based on current slider values.
    """
    return {k: round(random.uniform(0.1, 10.0), 1) for k in current_values.keys()}

# ------------------------------
# AI Buddy Suggestions
# ------------------------------
def ai_suggestions(current_values):
    """
    Returns preset AI-guided suggestions for sliders.
    """
    suggestions = []

    # Balanced
    balanced = {k: 5.0 for k in current_values.keys()}
    suggestions.append(("Balanced", balanced))

    # High Consciousness
    high_c = {k: round(random.uniform(7.5, 10.0), 1) for k in current_values.keys()}
    suggestions.append(("High Consciousness", high_c))

    # Creative Insight
    creative = {k: round(random.uniform(0.5, 10.0), 1) for k in current_values.keys()}
    suggestions.append(("Creative AI Insight", creative))

    return suggestions
