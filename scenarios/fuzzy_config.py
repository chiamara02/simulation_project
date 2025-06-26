# Fuzzy logic controller configuration for room heater scenario
fuzzy_config = {
    "inputs": {
        "error": {
            "range": [-10.0, 10.0],
            "membership_functions": {
                "cold": [-10.0, -5.0, 0.0],
                "ok": [-1.0, 0.0, 1.0],
                "hot": [0.0, 5.0, 10.0]
            }
        }
    },
    "output": {
        "heatSourcePower": {
            "range": [0.0, 2000.0],
            "membership_functions": {
                "low": [0.0, 500.0, 1000.0],
                "medium": [500.0, 1000.0, 1500.0],
                "high": [1000.0, 1500.0, 2000.0]
            }
        }
    },
    "rules": [
        {"if": {"error": "cold"}, "then": {"heatSourcePower": "high"}},
        {"if": {"error": "ok"}, "then": {"heatSourcePower": "medium"}},
        {"if": {"error": "hot"}, "then": {"heatSourcePower": "low"}}
    ]
}
