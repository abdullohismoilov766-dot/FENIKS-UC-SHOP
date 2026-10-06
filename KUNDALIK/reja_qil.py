#!/usr/bin/env python3
"""
KUNDALIK — foydalanuvchi aytgan rejani rejalar.csv ga qat'iy yozadigan skript.

Oqim shunday ishlaydi: foydalanuvchi suhbatda erkin matn bilan reja aytadi
(masalan: "13-oktyabrga soat 10:00ga dentist yoz"). Claude buni tushunib,
Google Calendar'ga MCP orqali hodisa yaratadi (create_event) — bu qadam
FAQAT suhbat ichida bo'ladi, chunki Calendar ulanishi skriptga emas, shu
sessiyaga tegishli. Shundan keyin SHU SKRIPT chaqiriladi — u rejani
rejalar.csv faylida qat'iy qayd qiladi (tarix/audit uchun) va git'ga
commit+push qiladi. Demak: kalendar yozuvini Claude qiladi, bu skript esa
shu yozuvni ishonchli saqlaydi — ikkisi birga "reja yozish botini" hosil
qiladi.

Ishlatish:
    python3 KUNDALIK/reja_qil.py SANA SOAT "Tavsif" [EVENT_ID]

    masalan:
    python3 KUNDALIK/reja_qil.py 2026-10-13 10:00 "Dentist bilan uchrashuv" f7l4mnc1ud9fl31lutv5deo138

    EVENT_ID ixtiyoriy — Calendar hodisasi yaratilganda qaytgan id, keyinchalik
    "bu reja qaysi hodisaga tegishli" deb tekshirish uchun saqlanadi.

    --dry-run bilan git'ga va faylga umuman tegmasdan, nima yozilishi
    ko'rsatiladi:
    python3 KUNDALIK/reja_qil.py --dry-run 2026-10-13 10:00 "Dentist bilan uchrashuv"
"""

from __future__ import annotations

import csv
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BRANCH = "claude/daily-plan-tracker-bot-069e57"
COMMIT_TRAILER = (
    "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>\n"
    "Claude-Session: https://claude.ai/code/session_01Spb4p33DEcCk6sY9e86Q2H"
)

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "KUNDALIK" / "rejalar.csv"
FIELDNAMES = ["sana", "soat", "tavsif", "event_id", "yozilgan_vaqt"]


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


def git_prepare() -> None:
    run(["git", "fetch", "origin", BRANCH])

    current = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], check=False).stdout.strip()
    if current != BRANCH:
        checkout = run(["git", "checkout", BRANCH], check=False)
        if checkout.returncode != 0:
            run(["git", "checkout", "-b", BRANCH, f"origin/{BRANCH}"])

    run(["git", "pull", "--ff-only", "origin", BRANCH])


def append_row(sana: str, soat: str, tavsif: str, event_id: str) -> None:
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    is_new = not CSV_PATH.exists()
    with CSV_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if is_new:
            writer.writeheader()
        writer.writerow(
            {
                "sana": sana,
                "soat": soat,
                "tavsif": tavsif,
                "event_id": event_id,
                "yozilgan_vaqt": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
        )


def git_commit_and_push() -> None:
    run(["git", "add", "KUNDALIK/rejalar.csv"])

    status = run(["git", "status", "--porcelain", "KUNDALIK/rejalar.csv"], check=False)
    if not status.stdout.strip():
        print("(o'zgarish yo'q — fayl allaqachon shu holatda edi)")
        return

    run(["git", "commit", "-m", f"KUNDALIK: yangi reja qayd qilindi\n\n{COMMIT_TRAILER}"])

    push = run(["git", "push", "-u", "origin", BRANCH], check=False)
    if push.returncode != 0:
        die(f"push muvaffaqiyatsiz:\n{push.stdout}\n{push.stderr}")


def main() -> None:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if len(args) not in (3, 4):
        die(
            "ishlatish: reja_qil.py [--dry-run] SANA SOAT \"Tavsif\" [EVENT_ID]\n"
            "masalan: reja_qil.py 2026-10-13 10:00 \"Dentist bilan uchrashuv\""
        )

    sana_raw, soat_raw, tavsif_raw = args[0], args[1], args[2]
    event_id = args[3] if len(args) == 4 else ""

    try:
        sana = datetime.strptime(sana_raw, "%Y-%m-%d").date().isoformat()
    except ValueError:
        die(f"SANA YYYY-MM-DD ko'rinishida bo'lsin, olindi: {sana_raw!r}")

    try:
        soat = datetime.strptime(soat_raw, "%H:%M").strftime("%H:%M")
    except ValueError:
        die(f"SOAT HH:MM (24-soatlik) ko'rinishida bo'lsin, olindi: {soat_raw!r}")

    tavsif = tavsif_raw.strip()
    if not tavsif:
        die("Tavsif bo'sh bo'lmasligi kerak")

    if dry_run:
        print("(--dry-run: fayl yozilmadi, hech narsa commit qilinmadi)")
        print(f"Yoziladigan qator: {sana} {soat} — {tavsif} (event_id={event_id or '-'})")
        return

    git_prepare()
    append_row(sana, soat, tavsif, event_id)
    git_commit_and_push()

    print(f"✅ Reja qayd qilindi: {sana} {soat} — {tavsif}")


if __name__ == "__main__":
    main()
