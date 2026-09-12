#!/usr/bin/env python3
"""
KUNDALIK — bir kunlik javoblarni kundalik.csv ga yozadigan qat'iy skript.

Bu fayl mavjud bo'lishining sababi: savol Claude orqali erkin matn
ko'rinishida so'raladi, lekin JAVOBNI YOZIB QO'YISH endi erkin
"shunday-shunday qatorlarni fayliga qo'sh, keyin git bilan yubor" tarzidagi
ko'rsatmaga tayanmaydi — chunki amalda bu hech qachon ishlamadi (fayl
oylab bo'sh qolib ketdi). Buning o'rniga bitta skript bor: yoki muvaffaqiyatli
yozadi va push qiladi, yoki aniq xato bilan to'xtaydi. Claude bu skriptni
ISHLATADI, uning ishini o'zi qaytadan qilishga urinmaydi.

Ishlatish:
    python3 KUNDALIK/kayd_qil.py 2026-09-13 "Bomdod:bajarildi" "Peshin:bajarilmadi" "Ish:bajarildi"

    --dry-run bilan git'ga tegmasdan, faqat nima yozilishini ko'rsatadi:
    python3 KUNDALIK/kayd_qil.py --dry-run 2026-09-13 "Bomdod:bajarildi"

Har bir yozuv "Vazifa:holat" ko'rinishida, holat faqat "bajarildi" yoki
"bajarilmadi" bo'lishi mumkin. Shu sana uchun mavjud vazifa qayta
yuborilsa — eskisi yangilanadi (takrorlanmaydi).
"""

from __future__ import annotations

import csv
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

VALID_STATUSES = {"bajarildi", "bajarilmadi"}
BRANCH = "claude/daily-plan-tracker-bot-069e57"

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "KUNDALIK" / "kundalik.csv"


def die(message: str) -> None:
    print(f"✖ XATO: {message}", file=sys.stderr)
    sys.exit(1)


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=60
    )
    if check and result.returncode != 0:
        die(
            f"buyruq muvaffaqiyatsiz: {' '.join(cmd)}\n"
            f"stdout: {result.stdout.strip()}\nstderr: {result.stderr.strip()}"
        )
    return result


def parse_entries(raw_entries: list[str]) -> list[tuple[str, str]]:
    parsed: list[tuple[str, str]] = []
    for raw in raw_entries:
        if ":" not in raw:
            die(f"noto'g'ri format: {raw!r} — kutilgan ko'rinish 'Vazifa:holat'")
        task, _, status = raw.partition(":")
        task = task.strip()
        status = status.strip()
        if not task:
            die(f"vazifa nomi bo'sh: {raw!r}")
        if status not in VALID_STATUSES:
            die(
                f"noto'g'ri holat: {status!r} ({raw!r}) — "
                f"faqat {sorted(VALID_STATUSES)} bo'lishi mumkin"
            )
        parsed.append((task, status))
    return parsed


def read_rows() -> list[dict[str, str]]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_rows(rows: list[dict[str, str]]) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sana", "vazifa", "holat"])
        writer.writeheader()
        writer.writerows(rows)


def upsert(rows: list[dict[str, str]], target_date: str, entries: list[tuple[str, str]]) -> int:
    index = {(r["sana"], r["vazifa"]): i for i, r in enumerate(rows)}
    changed = 0
    for task, status in entries:
        key = (target_date, task)
        row = {"sana": target_date, "vazifa": task, "holat": status}
        if key in index:
            rows[index[key]] = row
        else:
            rows.append(row)
        changed += 1
    return changed


def summarize(rows: list[dict[str, str]], target_date: str) -> str:
    today_rows = [r for r in rows if r["sana"] == target_date]
    today_done = sum(1 for r in today_rows if r["holat"] == "bajarildi")
    today_total = len(today_rows)

    week_start = (date.fromisoformat(target_date) - timedelta(days=6)).isoformat()
    week_rows = [r for r in rows if week_start <= r["sana"] <= target_date]
    week_done = sum(1 for r in week_rows if r["holat"] == "bajarildi")
    week_total = len(week_rows)

    lines = [f"Bugun ({target_date}): {today_done}/{today_total} bajarildi"]
    if week_total:
        percent = round(week_done / week_total * 100)
        lines.append(f"Oxirgi 7 kun: {week_done}/{week_total} ({percent}%)")
    return "\n".join(lines)


def git_sync_and_push(dry_run: bool) -> None:
    if dry_run:
        print("(--dry-run: git bosqichi o'tkazib yuborildi)")
        return

    run(["git", "fetch", "origin", BRANCH])

    current = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], check=False).stdout.strip()
    if current != BRANCH:
        checkout = run(["git", "checkout", BRANCH], check=False)
        if checkout.returncode != 0:
            run(["git", "checkout", "-b", BRANCH, f"origin/{BRANCH}"])

    run(["git", "pull", "--ff-only", "origin", BRANCH])
    run(["git", "add", "KUNDALIK/kundalik.csv"])

    status = run(["git", "status", "--porcelain", "KUNDALIK/kundalik.csv"], check=False)
    if not status.stdout.strip():
        print("(o'zgarish yo'q — fayl allaqachon shu holatda edi)")
        return

    run(
        [
            "git",
            "commit",
            "-m",
            "KUNDALIK: kunlik javoblarni qayd qilish\n\n"
            "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>",
        ]
    )

    push = run(["git", "push", "-u", "origin", BRANCH], check=False)
    if push.returncode != 0:
        die(f"push muvaffaqiyatsiz:\n{push.stdout}\n{push.stderr}")


def main() -> None:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if len(args) < 2:
        die(
            "ishlatish: kayd_qil.py [--dry-run] SANA \"Vazifa:holat\" [\"Vazifa2:holat2\" ...]\n"
            "masalan: kayd_qil.py 2026-09-13 \"Bomdod:bajarildi\" \"Peshin:bajarilmadi\""
        )

    target_date_raw, *raw_entries = args
    try:
        target_date = datetime.strptime(target_date_raw, "%Y-%m-%d").date().isoformat()
    except ValueError:
        die(f"sana YYYY-MM-DD ko'rinishida bo'lsin, olindi: {target_date_raw!r}")

    entries = parse_entries(raw_entries)

    rows = read_rows()
    changed = upsert(rows, target_date, entries)
    write_rows(rows)

    git_sync_and_push(dry_run)

    print(f"✅ {changed} ta band yozildi ({target_date}).")
    print(summarize(rows, target_date))


if __name__ == "__main__":
    main()
