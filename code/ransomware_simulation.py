#!/usr/bin/env python3

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

MANIFEST_NAME = ".ransomware_manifest.json"
RANSOM_NOTE_NAME = "README_RESTORE_FILES.txt"
RANSOM_NOTE_TEXT = (
    "Your files have been encrypted!\n\n"
    "To recover them, send 1 Bitcoin to the address below:\n"
    "[FAKE BITCOIN ADDRESS]\n\n"
    "Contact: fakehacker@example.com\n"
    "(This is a simulated, harmless demonstration. No real encryption was performed.)\n"
)


def create_dummy_files(target: Path, count: int = 3):
    target.mkdir(parents=True, exist_ok=True)
    for i in range(count):
        p = target / f"file_{i}.txt"
        if not p.exists():
            p.write_text("This is a safe test file for ransomware simulation.\n")


def load_manifest(target: Path):
    mpath = target / MANIFEST_NAME
    if not mpath.exists():
        return {"sessions": {}}
    try:
        data = json.loads(mpath.read_text())
        if not isinstance(data, dict):
            return {"sessions": {}}
        data.setdefault("sessions", {})
        return data
    except Exception:
        try:
            backup = target / (MANIFEST_NAME + ".bak")
            mpath.replace(backup)
        except Exception:
            pass
        return {"sessions": {}}


def save_manifest(target: Path, manifest: dict):
    mpath = target / MANIFEST_NAME
    mpath.write_text(json.dumps(manifest, indent=2))


def _next_available_name(target: Path, name: str) -> Path:
    p = target / name
    if not p.exists():
        return p
    base = name
    suffix = ""
    if "." in name:
        parts = name.rsplit(".", 1)
        base, suffix = parts[0], "." + parts[1]
    counter = 1
    while True:
        candidate = target / f"{base}.{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def simulate_attack(target: Path, note_text: str = RANSOM_NOTE_TEXT):
    if not target.exists():
        print(f"Target folder '{target}' does not exist. Aborting.")
        return

    manifest = load_manifest(target)
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    session_id = f"session_{timestamp}"
    manifest.setdefault("sessions", {})
    manifest["sessions"][session_id] = {"renamed": []}

    count = 0
    for entry in list(target.iterdir()):
        if not entry.is_file():
            continue
        if entry.name in (MANIFEST_NAME, RANSOM_NOTE_NAME):
            continue
        if entry.suffix == ".locked":
            continue
        original_name = entry.name
        new_name = original_name + ".locked"
        dest_path = _next_available_name(target, new_name)
        try:
            entry.rename(dest_path)
            manifest["sessions"][session_id]["renamed"].append({
                "original": original_name,
                "locked": dest_path.name,
            })
            count += 1
        except Exception as e:
            print(f"Failed to rename {entry}: {e}")

    note_path = target / RANSOM_NOTE_NAME
    try:
        note_path.write_text(note_text)
    except Exception as e:
        print(f"Failed to write ransom note: {e}")

    save_manifest(target, manifest)
    print(f"Simulation complete. {count} file(s) renamed. Manifest updated.")


def restore_from_manifest(target: Path):
    manifest = load_manifest(target)
    sessions = manifest.get("sessions", {})
    if not sessions:
        print("No sessions found in manifest. Nothing to restore.")
        return

    sorted_sessions = sorted(sessions.keys())
    last_session = sorted_sessions[-1]
    data = sessions.get(last_session, {})
    renamed = data.get("renamed", [])

    restored = 0
    for item in renamed:
        locked = target / item.get("locked", "")
        original = target / item.get("original", "")
        if not locked.exists():
            print(f"Locked file not found: {locked}")
            continue
        if original.exists():
            print(f"Original file already exists, skipping restore for: {original}")
            continue
        try:
            locked.rename(original)
            restored += 1
        except Exception as e:
            print(f"Failed to restore {locked}: {e}")

    note_path = target / RANSOM_NOTE_NAME
    if note_path.exists():
        try:
            note_path.unlink()
        except Exception:
            pass

    try:
        del sessions[last_session]
        manifest["sessions"] = sessions
        save_manifest(target, manifest)
    except Exception:
        pass

    print(f"Restore complete. {restored} file(s) restored from session {last_session}.")


def main():
    parser = argparse.ArgumentParser(description="Safe ransomware simulation (harmless)")
    parser.add_argument("--target", "-t", type=str, required=True, help="Target folder to simulate on")
    parser.add_argument("--create", "-c", action="store_true", help="Create sample test files if they don't exist")
    parser.add_argument("--restore", "-r", action="store_true", help="Restore files from the last simulation session")
    parser.add_argument("--note", type=str, default=None, help="Custom ransom note text file path")

    args = parser.parse_args()
    target = Path(args.target).resolve()

    if args.create:
        create_dummy_files(target)

    if args.note:
        note_path = Path(args.note)
        if note_path.exists():
            try:
                note_text = note_path.read_text()
            except Exception:
                print(f"Failed to read custom note file: {note_path}. Using default note.")
                note_text = RANSOM_NOTE_TEXT
        else:
            print(f"Custom note file not found: {note_path}. Using default note.")
            note_text = RANSOM_NOTE_TEXT
    else:
        note_text = RANSOM_NOTE_TEXT

    if args.restore:
        restore_from_manifest(target)
    else:
        simulate_attack(target, note_text=note_text)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted by user. Exiting.")
        sys.exit(1)

