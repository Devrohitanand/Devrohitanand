import json
import re
import requests
from bs4 import BeautifulSoup

USERNAME = "Devrohitanand"
URL = f"https://github.com/users/{USERNAME}/contributions"


def fetch_days():
    html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")

    counts = {}
    for tip in soup.find_all("tool-tip"):
        m = re.match(r"(\d+) contribution", tip.get_text(strip=True))
        counts[tip.get("for")] = int(m.group(1)) if m else 0

    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        date = td.get("data-date")
        if not date:
            continue
        days.append({
            "date": date,
            "level": int(td.get("data-level", 0)),
            "count": counts.get(td.get("id"), 0),
        })
    days.sort(key=lambda d: d["date"])
    return days


def compute_stats(days):
    total = sum(d["count"] for d in days)
    best = max(days, key=lambda d: d["count"]) if days else None

    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)

    current = 0
    rev = list(reversed(days))
    if rev and rev[0]["count"] == 0:
        rev = rev[1:]
    for d in rev:
        if d["count"] > 0:
            current += 1
        else:
            break

    months = {}
    for d in days:
        key = d["date"][:7]
        months[key] = months.get(key, 0) + d["count"]

    return {
        "total": total,
        "current_streak": current,
        "longest_streak": longest,
        "best_day": best,
        "months": months,
    }


if __name__ == "__main__":
    days = fetch_days()
    stats = compute_stats(days)
    with open("data/contributions.json", "w", encoding="utf-8") as f:
        json.dump({"days": days, "stats": stats}, f, indent=2)
    print(f"Days: {len(days)} | Total: {stats['total']} | Current streak: {stats['current_streak']}")