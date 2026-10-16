
from decimal import Decimal, InvalidOperation


def money_to_pesewas(amount):
    try:
        value = Decimal(amount)
    except (InvalidOperation, ValueError):
        raise ValueError("Enter a valid amount.")

    if not value.is_finite() or value <= 0:
        raise ValueError("Amount must be greater than zero.")

    if value != value.quantize(Decimal("0.01")):
        raise ValueError("Maximum two decimal places allowed.")

    return int(value * 100)


def money(amount):
    return f"GHS {amount // 100}.{amount % 100:02d}"


def create_group():
    name = input("Group name: ").strip()
    if not name:
        print("Group name cannot be empty.")
        return None

    try:
        contribution = money_to_pesewas(
            input("Weekly contribution (GHS): ").strip()
        )
    except ValueError as error:
        print("Error:", error)
        return None

    return {
        "name": name,
        "contribution": contribution,
        "members": [],
        "week": 1,
        "payments": {},
        "history": [],
    }


def find_member(group, name):
    name = name.strip().casefold()
    return next(
        (m for m in group["members"]
         if m["name"].casefold() == name),
        None,
    )


def add_member(group):
    if group["payments"] or group["history"]:
        print("Members cannot be added after the first payment.")
        return

    name = input("Member name or ID: ").strip()

    if not name:
        print("Member name cannot be empty.")
        return

    if find_member(group, name):
        print("Error: Duplicate member.")
        return

    group["members"].append({
        "name": name,
        "order": len(group["members"]) + 1,
    })
    print("Member added:", name)


def record_payment(group):
    name = input("Member name: ").strip()
    member = find_member(group, name)

    if member is None:
        print("Error: Unknown member.")
        return

    key = (group["week"], member["name"].casefold())
    paid = group["payments"].get(key, 0)
    due = group["contribution"] - paid

    try:
        amount = money_to_pesewas(
            input("Payment amount (GHS): ").strip()
        )
    except ValueError as error:
        print("Error:", error)
        return

    if amount > due:
        print("Error: Member only owes", money(due))
        return

    group["payments"][key] = paid + amount
    print("Payment recorded:", money(amount))
    print("Remaining balance:", money(due - amount))


def show_report(group):
    week = group["week"]
    print(f"\n=== {group['name']} | Week {week} ===")

    if not group["members"]:
        print("No members added.")
        return

    for member in group["members"]:
        key = (week, member["name"].casefold())
        paid = group["payments"].get(key, 0)
        due = group["contribution"] - paid
        status = "PAID IN FULL" if due == 0 else "OWES"

        print(
            f"{member['name']}: Paid {money(paid)} | "
            f"{status}: {money(due)}"
        )

    print("\n=== Payout History ===")
    if not group["history"]:
        print("No payouts yet.")
    else:
        for item in group["history"]:
            print(
                f"Week {item['week']}: {item['recipient']} "
                f"received {money(item['amount'])}"
            )


def close_week(group):
    members = group["members"]

    if not members:
        print("Add members before closing the week.")
        return

    week = group["week"]
    unpaid = []

    for member in members:
        key = (week, member["name"].casefold())
        paid = group["payments"].get(key, 0)
        due = group["contribution"] - paid

        if due > 0:
            unpaid.append((member["name"], due))

    if unpaid:
        print(f"Week {week} cannot close. No payout made.")
        for name, due in unpaid:
            print(f"{name} owes {money(due)}")
        return

    recipient_index = len(group["history"]) % len(members)
    recipient = members[recipient_index]
    pot = group["contribution"] * len(members)

    group["history"].append({
        "week": week,
        "recipient": recipient["name"],
        "amount": pot,
    })

    print(f"Week {week} closed successfully!")
    print(f"Payout recipient: {recipient['name']}")
    print(f"Payout amount: {money(pot)}")

    group["week"] += 1


def main():
    print("=== SUSU GROUP TRACKER ===")
    group = create_group()

    if group is None:
        return

    while True:
        print(f"\nGroup: {group['name']} | Week: {group['week']}")
        print("1. Add member")
        print("2. Record contribution")
        print("3. Close week and pay recipient")
        print("4. Show report")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_member(group)
        elif choice == "2":
            record_payment(group)
        elif choice == "3":
            close_week(group)
        elif choice == "4":
            show_report(group)
        elif choice == "5":
            print("Thank you for using Susu Group Tracker.")
            break
        else:
            print("Invalid option. Choose 1 to 5.")


if __name__ == "__main__":
    main()
