# Susu Group Tracker

A Python command-line application for managing a rotating savings group.

## Features

- Create a savings group with a weekly contribution.
- Add unique members.
- Record full or partial payments.
- Reject unknown members, duplicate members, invalid amounts, and overpayments.
- Prevent a week from closing while members have outstanding balances.
- Pay the completed weekly pot to the next member in joining order.
- Display payment balances and payout history.

## Requirements

- Python 3.10 or later
- No external packages required

## Run the program

Open a terminal in the project directory and run:

```bash
python susu.py
```

Follow the on-screen menu to add members, record payments, close a week, or view the report.

## Run automated tests

```bash
python -m unittest -v
```

The tests cover partial payments, blocked week closure, successful payouts, overpayments, unknown members, duplicate members, and zero amounts.

## Example

For three members contributing GHS 50 each, the completed weekly pot is GHS 150. The week cannot close until every member has paid GHS 50.
