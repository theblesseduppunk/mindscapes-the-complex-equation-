import random

def generate_random_scenario(slider_keys):
    """Generates random values for each slider variable."""
    return {k: round(random.uniform(0.1, 10.0), 1) for k in slider_keys}

def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    """Computes the main consciousness value."""
    return (R * (alpha**theta) * S * Q * (1.3*A) * E * (1.6*M)) / (Dn * (beta**theta))

def compute_creativity(R, D3):
    """Computes beginner equation for creativity."""
    return R / (D3**3)

def ai_suggestions(current_values):
    """Provides AI-guided scenario suggestions."""
    suggestions = []
    balanced = {k: 5.0 for k in current_values.keys()}
    suggestions.append(("Balanced", balanced))
    high_c = {k: round(random.uniform(7.5,10.0),1) for k in current_values.keys()}
    suggestions.append(("High Consciousness", high_c))
    creative = {k: round(random.uniform(0.5,10.0),1) for k in current_values.keys()}
    suggestions.append(("Creative AI Insight", creative))
    return suggestions
