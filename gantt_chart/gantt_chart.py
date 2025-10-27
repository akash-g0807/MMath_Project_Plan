import pandas as pd
import matplotlib.pyplot as plt

print("Hello, World! This is the Gantt chart module.")

tasks = ["Supervisor Meeting", "Research: Reading Vicky notes", "Planning Lecture", ]
start_dates = ["2025-10-02", "2025-09-23", "2025-10-17"]
end_dates = ["2025-10-02", "2025-10-24", "2025-10-17"]

df = pd.DataFrame(data={"Task": tasks, "Start": start_dates, "End": end_dates})

df["Start"] = pd.to_datetime(df["Start"])
df["End"] = pd.to_datetime(df["End"])

df["Duration"] = df["End"] - df["Start"]
df["Color"] = plt.cm.Set1.colors[:len(df)]

df
