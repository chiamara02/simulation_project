# Fuzzy logic controller configuration for room heater scenario
fuzzy_config = {
    "inputs": {
        "error": {
            "range": [-14.0, 14.0],
            "membership_functions": {
                "comfort": [-0.1, 0.0, 0.1],
                "fresh": [0.1, 1.0, 1.5],
                "warm": [-0.5, -1.0, -0.1],
                "cold": [1.5, 2.0, 13.5, 14],
                "hot": [-14,-13.5, -2.0, -1.5]
            }

        },
        "outsideTemp": {
            "range": [-10.0, 45.0],
            "membership_functions": {
                "cold": [-20.0, -10.0, 5.0, 10.0],
                "fresh": [5.0, 10.0, 15.0, 25.0],
                "warm": [20.0, 25.0, 30.0, 35.0],
                "hot": [25.0, 30.0, 45.0, 45.0]
    }
        },

        "roomAir.der_T": {
            "range": [-5.0, 5.0],
            "membership_functions": {
                "decreasing": [-1.0, -0.1, -0.001, -0.001],
                "stable": [-0.001, 0.0, 0.001],
                "increasing": [0.001, 0.001, 0.1, 1.0]
            }
        },
        },

   "output": {
    "heatSourcePower": {
        "range": [0.0, 2000.0],
        "membership_functions": {
            "off":         [0.0, 0.0, 0.0],           # Left shoulder
            "very-low":    [0.0, 100.0, 200.0],
            "low":         [200.0, 400.0, 600.0],
            "medium-low":  [600.0, 800.0, 1000.0],
            "medium-high": [1000.0, 1200.0, 1400.0],
            "high":        [1200.0, 1400.0, 1600.0],
            "very-high":   [1600.0, 1800.0, 2000.0],   # Right shoulder
            "full":        [1800.0, 1900.0, 2000.0]    # Right shoulder
        }
    }
},

    "rules": [
    {"if": {"error": "comfort", "roomAir.der_T": "stable", "outsideTemp": "cold"}, "then": {"heatSourcePower": "medium-low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "stable", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "stable", "outsideTemp": "warm"}, "then": {"heatSourcePower": "very-low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "stable", "outsideTemp": "hot"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "comfort", "roomAir.der_T": "decreasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "medium-high"}},
    {"if": {"error": "comfort", "roomAir.der_T": "decreasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "medium-low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "decreasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "decreasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "very-low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "increasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "increasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "very-low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "increasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "very-low"}},
    {"if": {"error": "comfort", "roomAir.der_T": "increasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "off"}},

    {"if": {"error": "fresh", "roomAir.der_T": "stable", "outsideTemp": "cold"}, "then": {"heatSourcePower": "very-high"}},
    {"if": {"error": "fresh", "roomAir.der_T": "stable", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "very-high"}},
    {"if": {"error": "fresh", "roomAir.der_T": "stable", "outsideTemp": "warm"}, "then": {"heatSourcePower": "high"}},
    {"if": {"error": "fresh", "roomAir.der_T": "stable", "outsideTemp": "hot"}, "then": {"heatSourcePower": "medium-high"}},
    {"if": {"error": "fresh", "roomAir.der_T": "decreasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "fresh", "roomAir.der_T": "decreasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "fresh", "roomAir.der_T": "decreasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "fresh", "roomAir.der_T": "decreasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "fresh", "roomAir.der_T": "increasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "fresh", "roomAir.der_T": "increasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "very-high"}},
    {"if": {"error": "fresh", "roomAir.der_T": "increasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "very-high"}},
    {"if": {"error": "fresh", "roomAir.der_T": "increasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "high"}},

    {"if": {"error": "warm", "roomAir.der_T": "stable", "outsideTemp": "cold"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "stable", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "stable", "outsideTemp": "warm"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "stable", "outsideTemp": "hot"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "decreasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "very-low"}},
    {"if": {"error": "warm", "roomAir.der_T": "decreasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "very-low"}},
    {"if": {"error": "warm", "roomAir.der_T": "decreasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "decreasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "increasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "increasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "increasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "warm", "roomAir.der_T": "increasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "off"}},

    {"if": {"error": "cold", "roomAir.der_T": "stable", "outsideTemp": "cold"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "stable", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "stable", "outsideTemp": "warm"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "stable", "outsideTemp": "hot"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "decreasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "decreasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "decreasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "decreasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "increasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "increasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "increasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "full"}},
    {"if": {"error": "cold", "roomAir.der_T": "increasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "full"}},

    {"if": {"error": "hot", "roomAir.der_T": "stable", "outsideTemp": "cold"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "stable", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "stable", "outsideTemp": "warm"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "stable", "outsideTemp": "hot"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "decreasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "decreasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "decreasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "decreasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "increasing", "outsideTemp": "cold"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "increasing", "outsideTemp": "fresh"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "increasing", "outsideTemp": "warm"}, "then": {"heatSourcePower": "off"}},
    {"if": {"error": "hot", "roomAir.der_T": "increasing", "outsideTemp": "hot"}, "then": {"heatSourcePower": "off"}}
]
}


