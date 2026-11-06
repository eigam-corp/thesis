import sys
from datetime import date, timedelta

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

out = sys.argv[1]

groups = [
    ("Fundação", [
        ("infra (Terraform, Compose e implantação)", date(2026, 8, 27), date(2026, 11, 5)),
        ("shared (contratos e criptografia)", date(2026, 8, 27), date(2026, 11, 5)),
        ("docs (ADRs e golden sets)", date(2026, 8, 28), date(2026, 11, 5)),
    ]),
    ("Serviços", [
        ("api-gateway", date(2026, 8, 28), date(2026, 11, 5)),
        ("chat-service", date(2026, 8, 28), date(2026, 11, 5)),
        ("finance-service", date(2026, 8, 28), date(2026, 11, 5)),
        ("outbound-worker", date(2026, 8, 28), date(2026, 11, 5)),
        ("notification-service", date(2026, 8, 28), date(2026, 11, 4)),
        ("billing-service", date(2026, 8, 28), date(2026, 11, 2)),
        ("audit-service", date(2026, 8, 28), date(2026, 11, 2)),
        ("render-service", date(2026, 8, 31), date(2026, 11, 5)),
        ("identity-service", date(2026, 9, 1), date(2026, 11, 4)),
        ("ai-service", date(2026, 9, 1), date(2026, 11, 5)),
        ("analytics-service", date(2026, 9, 1), date(2026, 11, 2)),
    ]),
    ("Interfaces web", [
        ("admin-panel (painel de operação)", date(2026, 10, 27), date(2026, 11, 4)),
        ("ui (design system)", date(2026, 10, 29), date(2026, 11, 2)),
        ("holder-panel (painel do titular)", date(2026, 10, 30), date(2026, 11, 5)),
    ]),
]

milestones = [
    ("Prophet descartado (ADR-009)", date(2026, 9, 9)),
    ("Direitos do titular executados (ADR-026)", date(2026, 10, 22)),
    ("Painel do titular ligado (ADR-031)", date(2026, 10, 30)),
    ("Validação de alertas, metas e projeção", date(2026, 11, 2)),
    ("Teste de carga", date(2026, 11, 3)),
]

colors = {"Fundação": "#9BB7D4", "Serviços": "#A8D5A2", "Interfaces web": "#F4B6C2"}

plt.rcParams["font.family"] = "Arial"
rows = []
for group, items in groups:
    rows.append(("group", group, None, None))
    for name, start, end in items:
        rows.append(("task", name, start, end, group))
rows.append(("group", "Marcos", None, None))
for name, day in milestones:
    rows.append(("milestone", name, day))

fig, ax = plt.subplots(figsize=(12, 8.2))
y = 0
labels = []
for row in rows:
    kind = row[0]
    if kind == "group":
        labels.append((y, row[1], True))
    elif kind == "task":
        _, name, start, end, group = row
        ax.barh(y, (end - start).days + 1, left=mdates.date2num(start), height=0.6,
                color=colors[group], edgecolor="#555555", linewidth=0.6)
        labels.append((y, name, False))
    else:
        _, name, day = row
        ax.plot(mdates.date2num(day), y, marker="D", color="#333333", markersize=7)
        ax.text(mdates.date2num(day) + 1.2, y, name, va="center", fontsize=9)
        labels.append((y, "", False))
    y += 1

ax.set_yticks([p for p, _, _ in labels])
ax.set_yticklabels([text for _, text, _ in labels], fontsize=9)
for tick, (_, _, bold) in zip(ax.get_yticklabels(), labels):
    if bold:
        tick.set_fontweight("bold")
ax.invert_yaxis()

ax.set_xlim(mdates.date2num(date(2026, 8, 24)), mdates.date2num(date(2026, 11, 16)))
weeks = [date(2026, 8, 24) + timedelta(weeks=i) for i in range(13)]
ax.set_xticks([mdates.date2num(d) for d in weeks])
ax.set_xticklabels([d.strftime("%d/%m") for d in weeks], fontsize=8.5)
ax.grid(axis="x", color="#DDDDDD", linewidth=0.7)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
ax.set_xlabel("Semanas de 2026", fontsize=9)

plt.tight_layout()
plt.savefig(out, dpi=200)
print("ok", out)
