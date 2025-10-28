import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# === Your data (Effort %) ===
df = pd.DataFrame([
    dict(Task="Initial Supervisor Meeting", Start='2025-10-02', Finish='2025-10-02', Effort=40),
    dict(Task="Research: Reading Vicky Notes", Start='2025-09-23', Finish='2025-10-24', Effort=80),
    dict(Task="Planning Lecture", Start='2025-10-17', Finish='2025-10-17', Effort=20),
    dict(Task="Research: Read Varities book", Start='2025-10-25', Finish='2025-12-15', Effort=100),
    dict(Task="Look into algorithms", Start='2025-11-15', Finish='2026-01-01', Effort=50),
    dict(Task="Chapter 1 Draft", Start='2026-01-30', Finish='2026-02-15', Effort=60),
    dict(Task="Project Plan", Start='2025-10-25', Finish='2025-11-7', Effort=70),
    dict(Task="Literature Review", Start='2025-11-7', Finish='2026-01-01', Effort=60),
    dict(Task="Literature Review", Start='2026-01-01', Finish='2026-01-30', Effort=30),
    dict(Task="Supervision Meeting 2", Start='2025-10-28', Finish='2025-10-28', Effort=40),
    dict(Task="Draft Start", Start='2026-02-05', Finish='2026-03-13', Effort=100),
    dict(Task="Feedback Meeting", Start='2025-11-11', Finish='2025-11-11', Effort=40),
    dict(Task="Draft Feedback Meeting", Start='2026-03-23', Finish='2026-03-23', Effort=70),
    dict(Task="Final Writeup", Start='2026-03-13', Finish='2026-04-27', Effort=40),

])


df["Start"] = pd.to_datetime(df["Start"])
df["Finish"] = pd.to_datetime(df["Finish"])

# Split single vs multi-day (milestones vs bars)
multi_day = df[df["Start"] != df["Finish"]]
single_day = df[df["Start"] == df["Finish"]]

# === Color scale for Effort (low→green, high→red) ===
effort_scale = [(0.0, "green"), (0.5, "gold"), (1.0, "red")]

fig = px.timeline(
    multi_day,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Effort",
    color_continuous_scale=effort_scale,
    range_color=(0, 100),
    title="Project Timeline (Color = Effort %)"
)

# Single-day milestones as diamonds (share same color axis)
if not single_day.empty:
    fig.add_trace(go.Scatter(
        x=single_day["Start"],
        y=single_day["Task"],
        mode="markers",
        marker=dict(symbol="diamond", size=14),
        marker_color=single_day["Effort"],
        marker_coloraxis="coloraxis",
        name="Single-day milestone",
        hovertemplate="<b>%{y}</b><br>Date: %{x|%Y-%m-%d}<br>Effort: %{marker.color:.0f}%<extra></extra>"
    ))

fig.update_yaxes(autorange="reversed")
fig.update_layout(
    template="plotly_white",
    hovermode="closest",
    margin=dict(l=110, r=70, t=80, b=40),
    title_x=0.5
)
fig.update_coloraxes(
    colorbar=dict(title="Effort %", tickvals=[0, 25, 50, 75, 100], thickness=16, len=0.9),
    cmin=0, cmax=100, colorscale=effort_scale
)

# === Milestone adder (by date) ===
# Provide any list of dicts with Date + Label (+ optional Color).
milestones = [
    {"Date": "2025-09-23", "Label": "Kickoff",   "Color": "black"},
    {"Date": "2026-01-30", "Label": "Chapter 1 start",  "Color": "purple"},
    {"Date": "2025-11-07", "Label": "Project Plan Due",  "Color": "darkorange"},
    {"Date": "2025-11-11", "Label": "Feedback Meeting",  "Color": "blue"},
    {"Date": "2026-04-27", "Label": "Final Submission",  "Color": "red"},
    {"Date": "2026-03-13", "Label": "Draft Submission",  "Color": "red"},
    {"Date": "2026-03-23", "Label": "Draft Feedback",  "Color": "blue"},
]

milestones = [{**m, "Date": pd.to_datetime(m["Date"])} for m in milestones]

def add_milestones(fig, items, show_today=False):
    # Extend x-range to include milestones (so labels aren’t clipped)
    if items:
        min_ms = min(m["Date"] for m in items)
        max_ms = max(m["Date"] for m in items)
        x0 = min(df["Start"].min(), min_ms)
        x1 = max(df["Finish"].max(), max_ms)
    else:
        x0, x1 = df["Start"].min(), df["Finish"].max()

    if show_today:
        today = pd.Timestamp("today").normalize()
        x0 = min(x0, today)
        x1 = max(x1, today)

    fig.update_xaxes(range=[x0, x1])

    # Add vertical lines + top labels
    for m in items:
        color = m.get("Color", "black")
        fig.add_vline(x=m["Date"], line_width=2, line_dash="dash", line_color=color, opacity=0.7)
        fig.add_annotation(
            x=m["Date"], y=1.02, xref="x", yref="paper",
            text=m.get("Label", "Milestone"),
            showarrow=True, arrowhead=2, ax=0, ay=-22,
            font=dict(size=12, color=color),
            bgcolor="rgba(255,255,255,0.75)", bordercolor=color
        )

    if show_today:
        today = pd.Timestamp("today").normalize()
        fig.add_vline(x=today, line_width=2, line_dash="dot", line_color="royalblue", opacity=0.9)
        fig.add_annotation(
            x=today, y=1.02, xref="x", yref="paper",
            text="Today",
            showarrow=True, arrowhead=2, ax=0, ay=-22,
            font=dict(size=12, color="royalblue"),
            bgcolor="rgba(255,255,255,0.75)", bordercolor="royalblue"
        )

# Use it:
add_milestones(fig, milestones, show_today=True)

fig.show()

# Optional: export for GitHub Pages
# fig.write_html("index.html", include_plotlyjs="cdn", full_html=True, config={"responsive": True})



# Write an HTML page you can host anywhere
fig.write_html(
    "index.html",
    include_plotlyjs="cdn",   # loads Plotly from a CDN so the file stays small
    full_html=True,
    config={"responsive": True}  # makes it resize to the window
)