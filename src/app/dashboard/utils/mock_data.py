import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Fake main data
np.random.seed(42)
data = pd.DataFrame({
    "timestamp": [datetime.now() - timedelta(days=i) for i in range(100)],
    "value": np.random.normal(50, 10, 100),
    "category": np.random.choice(["A", "B", "C"], 100)
})

# Fake metadata table
metadata = pd.DataFrame({
    "file_name": [f"file_{i}.csv" for i in range(20)],
    "status": np.random.choice(["success", "error"], 20, p=[0.8, 0.2]),
    "processed_at": [datetime.now() - timedelta(minutes=30*i) for i in range(20)]
})
