
You said:
#!/usr/bin/env python3
import asyncio
import json
import os
from telethon import TelegramClient, errors
from telethon.sessions import StringSession
from telethon.tl.functions.account import ReportPeerRequest
from telethon.tl.types import (
    InputReportReasonSpam,
    InputReportReasonViolence,
    InputReportReasonChildAbuse,
    InputReportReasonOther,
)


CONFIG_FILE = "accounts.json"

# 👇 Your API
API_ID = 24826760
API_HASH = "f076c7ec636a8a01e704f4f0d207b8ce"


def load_accounts():
    if not os.path.exists(CONFIG_FILE):
        return {}
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_account(phone: str, session_str: str):
    data = load_accounts()
    data[phone] = session_str
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=2)


def print_title():
    print("\n" + "="*72)
    print("         ⚡ TINESH TELEGRAM GAMBING‑REPORTER – UNLIMITED ACCOUNTS ⚡")
    print("         Channel example: https://t.me/patilpredictionraja")
    print("="*72)


REPORT_REASONS = {
    "1": "spam",
    "2": "violence",
    "3": "child_abuse",
    "4": "other",
}


def get_reason_menu():
    print("\nAvailable reasons (recommended spam for gambling):")
    for key, value in REPORT_REASONS.items():
        print(f"  {key}. {value.replace('_', ' ').title()}")


def get_channel_input():
    print(
        "\nEnter channel URL or username, for example:"
        "\n  https://t.me/patilpredictionraja"
        "\n  or just:            patilpredictionraja"
    )
    link = input("> Channel/target: ").strip()
    if link.startswith("https://t.me/"):
        link = link.replace("https://t.me/", "")
    if link.startswith("@"):
        link = link[1:]
    return link


def get_reason_value(key):
    if key == "1":
        return InputReportReasonSpam()
    elif key == "2":
        return InputReportReasonViolence()
    elif key == "3":
        return InputReportReasonChildAbuse()
    return InputReportReasonOther()


async def add_account():
    phone = input("Phone with country code (e.g. +918XXXXXXXXX): ").strip()
    if not phone.startswith("+"):
        print("❌ Phone must start with + (e.g. +91XXXXXXXXXX)")
        return

    session = StringSession()
    client = TelegramClient(session, API_ID, API_HASH)

    try:
        await client.start(
            phone=phone,
            code_callback=lambda: input("Enter Telegram code: ").strip()
        )

        save_account(phone, session.save())
        print(f"✅ Account added and saved: {phone}")
    except errors.AuthKeyUnregisteredError:
        print("❌ Session expired or not logged in; try again.")
    except Exception as e:
        print(f"❌ Error during login: {e}")


async def single_gambling_report(client, channel: str, reason):
    # show which phone did the report this round
    accounts = load_accounts()
    phone = "unknown"
    sess_str = client.session.save()
    for p, s in accounts.items():
        if s == sess_str:
            phone = p
            break

    try:
        msg = (
            "This channel promotes illegal gambling / prediction‑based betting, "
            "manipulating Indian users into risky wagering and financial loss. "
            "Reported under Indian Public Gambling Act 1867 + IT Act."
        )

        await client(
            ReportPeerRequest(
                peer=channel,
                reason=reason,
                message=msg
            )
        )
        print(f"✅ {phone} → REPORTED (gambling): {channel}")
        await asyncio.sleep(2)
        return True

    except errors.FloodWaitError as e:
        print(f"⏰ {phone} → flood wait {e.seconds} s")
        await asyncio.sleep(e.seconds)
        return False
    except Exception as e:
        msg = str(e)
        if "REPORT_SEND_FAIL" in msg or "PEER_INVALID" in msg:
            print(f"❌ {phone} → invalid peer {channel}")
        else:
            print(f"⚠️  {phone} → report error: {msg[:70]}...")
        await asyncio.sleep(2)
        return False


async def mass_report_gambling_loop():
    accounts = load_accounts()
    if not accounts:
        print("❌ No accounts saved. Use option 1 to add at least one.")
        return

    channel = get_channel_input()

    get_reason_menu()
    choice = input("\nReason (1‑4): ").strip()
    if choice not in REPORT_REASONS:
        print("❌ Invalid choice.")
        return

    reason = get_reason_value(choice)
    print(f"\n🎯 GAMBING‑REPORT MODE ACTIVE ON: {channel}\n")

    # Each round: every account reports once (no unlimited‑per‑account spam)
    while True:
        print("\n🔄 Round start – each account will report once:")

        for phone, session_str in accounts.items():
            session = StringSession(session_str)
            client = TelegramClient(session, API_ID, API_HASH)

            async with client:
                await single_gambling_report(client, channel, reason)

        print("\n📈 One full round done. Press Ctrl+C to stop, or next round will auto‑start in 5s…")

        try:
            await asyncio.sleep(5)
        except KeyboardInterrupt:
            print("🛑 Stopped.")
            break


async def list_accounts():
    accounts = load_accounts()
    if accounts:
        print("\n╠════════════════════════════════════════╗")
        print("║         SAVED ACCOUNTS (UNLIMITED)        ║")
        print("╠════════════════════════════════════════╝")
        for phone in accounts:
            print(f"  • {phone}")
    else:
        print("\n❌ No accounts saved yet.")


async def main():
    while True:
        print_title()
        print("1. ➕ Add Telegram account (NO LIMIT)")
        print("2. 👥 List all saved accounts")
        print("3. 🎲 Mass‑report gambling channel (each account reports per round)")
        print("0. 🚪 Exit")
        print()

        choice = input("Choose (0‑3): ").strip()

        if choice == "0":
            print("Exiting reporter.")
            break

        elif choice == "1":
            try:
                await add_account()
            except KeyboardInterrupt:
                print("\nAborted during login.")

        elif choice == "2":
            await list_accounts()

        elif choice == "3":
            await mass_report_gambling_loop()

        else:
            print("❌ Invalid input. Choose 0, 1, 2, or 3.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBye! Use this calmly and legally.")
