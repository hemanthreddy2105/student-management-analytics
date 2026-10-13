"""Data-driven insights for the Student Management Analytics project.

Reads students.csv and departments.csv (same folder), prints the key findings
and saves charts to the screenshots/ folder.

Run:  python insights_analysis.py      (needs pandas and matplotlib)
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "screenshots")
os.makedirs(OUT, exist_ok=True)

students = pd.read_csv(os.path.join(BASE, "students.csv"))
departments = pd.read_csv(os.path.join(BASE, "departments.csv"), encoding="utf-8-sig")
df = students.merge(departments, on="department_id")

BLUE, ORANGE, GREY = "#1f6f8b", "#e8833a", "#8a8f98"
plt.rcParams.update({"axes.spines.top": False, "axes.spines.right": False,
                     "font.size": 10, "axes.titleweight": "bold"})

# ---------- key numbers ----------
total = len(df)
low_att = df[df.attendance < 75]
failed = df[df.marks < 50]
at_risk = df[(df.marks < 60) & (df.attendance < 75)]
pending = df[df.fee_status == "Pending"]
pending_low_att = df[(df.fee_status == "Pending") & (df.attendance < 75)]
scholarship = df[(df.marks >= 75) & (df.attendance >= 75)]
corr = df["marks"].corr(df["attendance"])

dept = (df.groupby("department_name")
          .agg(students=("marks", "size"), avg_marks=("marks", "mean"),
               avg_attendance=("attendance", "mean"),
               pending_pct=("fee_status", lambda x: (x == "Pending").mean() * 100))
          .round(1).sort_values("avg_marks"))

print(f"Students                      : {total}")
print(f"Average marks / attendance    : {df.marks.mean():.1f} / {df.attendance.mean():.1f}%")
print(f"Pass rate (marks >= 50)       : {100 - len(failed) / total * 100:.1f}%  ({len(failed)} failed)")
print(f"Attendance below 75%          : {len(low_att)} ({len(low_att) / total:.0%})")
print(f"At risk (marks<60 & att<75)   : {len(at_risk)}")
print(f"Fees pending                  : {len(pending)} ({len(pending) / total:.0%})")
print(f"Pending fees AND att < 75%    : {len(pending_low_att)}")
print(f"Scholarship eligible          : {len(scholarship)}")
print(f"Correlation marks~attendance  : {corr:.3f}")
print("\nDepartment summary (sorted by average marks):\n", dept)

# ---------- charts ----------
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.scatter(df.attendance, df.marks, s=22, color=BLUE, alpha=0.6)
ax.axvline(75, color=ORANGE, ls="--", lw=1)
ax.text(75.4, 46, "75% attendance rule", color=ORANGE, fontsize=9)
ax.set(xlabel="Attendance (%)", ylabel="Marks",
       title=f"Attendance vs marks (correlation r = {corr:.2f})")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "attendance_vs_marks.png"), dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(dept.index, dept.avg_marks, color=BLUE)
ax.axvline(df.marks.mean(), color=ORANGE, ls="--", lw=1)
for y, v in enumerate(dept.avg_marks):
    ax.text(v + 0.3, y, f"{v:.1f}", va="center", fontsize=9)
ax.set(xlim=(55, 82), xlabel="Average marks", title="Average marks by department (dashed = overall)")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "avg_marks_by_department.png"), dpi=150); plt.close(fig)

p = dept.sort_values("pending_pct")
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.barh(p.index, p.pending_pct, color=ORANGE)
for y, v in enumerate(p.pending_pct):
    ax.text(v + 0.5, y, f"{v:.0f}%", va="center", fontsize=9)
ax.set(xlim=(0, 55), xlabel="Students with pending fees (%)", title="Pending fees by department")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "pending_fees_by_department.png"), dpi=150); plt.close(fig)

print(f"\nCharts saved to: {OUT}")
