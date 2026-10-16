
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
import susu


def make_group():
    return {
        "name": "Test Group",
        "contribution": 5000,
        "members": [
            {"name": "Ama", "order": 1},
            {"name": "Kofi", "order": 2},
            {"name": "Esi", "order": 3},
        ],
        "week": 1,
        "payments": {},
        "history": [],
    }


class SusuTests(unittest.TestCase):
    def test_partial_payment(self):
        group = make_group()
        with patch("builtins.input", side_effect=["Esi", "30"]):
            susu.record_payment(group)
        self.assertEqual(group["payments"][(1, "esi")], 3000)

    def test_week_cannot_close(self):
        group = make_group()
        group["payments"][(1, "ama")] = 5000
        output = StringIO()
        with redirect_stdout(output):
            susu.close_week(group)
        self.assertIn("cannot close", output.getvalue().lower())
        self.assertEqual(group["week"], 1)
        self.assertEqual(group["history"], [])

    def test_successful_payout(self):
        group = make_group()
        for member in group["members"]:
            group["payments"][(1, member["name"].lower())] = 5000
        with redirect_stdout(StringIO()):
            susu.close_week(group)
        self.assertEqual(group["week"], 2)
        self.assertEqual(group["history"][0]["recipient"], "Ama")
        self.assertEqual(group["history"][0]["amount"], 15000)

    def test_reject_overpayment(self):
        group = make_group()
        with patch("builtins.input", side_effect=["Kofi", "60"]):
            with redirect_stdout(StringIO()):
                susu.record_payment(group)
        self.assertNotIn((1, "kofi"), group["payments"])

    def test_reject_unknown_member(self):
        group = make_group()
        output = StringIO()
        with patch("builtins.input", return_value="Unknown"):
            with redirect_stdout(output):
                susu.record_payment(group)
        self.assertIn("Unknown member", output.getvalue())
        self.assertEqual(group["payments"], {})

    def test_reject_duplicate_member(self):
        group = make_group()
        with patch("builtins.input", return_value="ama"):
            with redirect_stdout(StringIO()):
                susu.add_member(group)
        self.assertEqual(len(group["members"]), 3)

    def test_reject_zero_amount(self):
        with self.assertRaises(ValueError):
            susu.money_to_pesewas("0")


if __name__ == "__main__":
    unittest.main()
