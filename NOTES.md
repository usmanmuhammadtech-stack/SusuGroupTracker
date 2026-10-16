# Project Notes

## Assumptions and decisions

- Each member contributes the same fixed amount every week.
- Member names are unique, ignoring letter case and surrounding spaces.
- Partial payments are allowed.
- Payments use integer pesewas internally to avoid floating-point money errors.
- A week closes only when every member has paid the full contribution.
- The full pot is paid to one member in joining order.
- Payouts rotate through the member list and repeat after every member has received a payout.
- New members cannot be added after payments or payouts have started.
- Group data is stored in memory and is not saved after the program exits.

## Improvements with more time

- Save group data between sessions.
- Add more tests for invalid inputs and multiple payout cycles.
- Separate business logic from the command-line interface.
- Support multiple groups and member IDs.
- Improve reports and add payment dates.
