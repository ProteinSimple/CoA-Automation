import io
import json
import os
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import Mock

import pandas as pd
from pypdf import PdfReader

# Program Imports
import action
import saturn
from util import PathCorrection

from .context import TestContext


def test_print(msg):
    print(msg, file=sys.__stdout__)


class ActionTest(unittest.TestCase):

    def test_check_action(self):
        config = TestContext.get_config()
        args = Mock()
        out = io.StringIO()
        sys.stdout = out
        sys.stderr = out

        cases = [
            (os.getenv("API_USER"), os.getenv("API_PASS"), "1"),  # BASE CASE
            (None, None, "1"),  # No need to provide cred after previous case
            ("jiber", "ish", "0"),  # Bad case
        ]

        for user, passkey, exp in cases:
            args.user = user
            args.passkey = passkey
            action.action_check(args, config)
            self.assertEqual(
                out.getvalue().strip()[0], exp
            )  # Only check if fail or success !
            out.seek(0)
            out.truncate(0)

    def test_fetch_action(self):
        config = TestContext.get_config()
        args = Mock()
        args.verbose = True
        out = io.StringIO()
        sys.stdout = out
        sys.stderr = out
        args.user = os.getenv("API_USER")
        args.passkey = os.getenv("API_PASS")

        args.start = "2025-07-15"
        args.end = "2025-07-15"
        action.action_fetch(args, config)
        self.assertEqual(out.getvalue().strip()[0], "1")
        try:
            data = out.getvalue()[1:].strip()
            parsed = json.loads(data)
            self.assertIsInstance(parsed, list)
            for val in parsed:
                for f in ["id", "b_date", "type", "passed_qc"]:
                    self.assertIn(f, val)
                self.assertIsInstance(int(val["id"]), int)
                self.assertIsInstance(val["type"], int)
                self.assertIn(val["type"], saturn.CartridgeData.code_map)
        except Exception:
            self.fail()

    def test_config_add_action(self):
        config = TestContext.get_config()
        args = Mock()
        args.verbose = True
        args.config_mode = "add"
        prev_pdf = set(config["pdf_output_dir"])
        prev_csv = set(config["mapping_output_dir"])

        cases = [
            (["newPath"], ["newPath"]),
            (["newPath", "newPath2"], []),
            ([], ["newPath", "newPath2"]),
            (["newPath", "newPath2"], ["newPath", "newPath2"]),
            (["newPath", "newPath2", "newPath"],
             ["newPath", "newPath3", "newPath3"]),
            ([], []),
        ]

        for pdf_path, csv_path in cases:
            config_cp = deepcopy(config)
            args.pdf = pdf_path
            args.csv = csv_path
            action.action_config_add(args, config_cp)
            new_pdf = set(config_cp["pdf_output_dir"])
            new_csv = set(config_cp["mapping_output_dir"])
            self.assertEqual(new_pdf, prev_pdf | set(pdf_path))
            self.assertEqual(new_csv, prev_csv | set(csv_path))

    def test_config_del_action(self):
        config = TestContext.get_config()
        args = Mock()
        args.config_mode = "delete"
        config["pdf_output_dir"] = ["p1", "p2", "p3"]
        config["mapping_output_dir"] = ["p1", "p2", "p4"]
        prev_pdf = set(config["pdf_output_dir"])
        prev_csv = set(config["mapping_output_dir"])

        cases = [
            (["p1"], ["p1"]),
            (["p1", " p5"], []),
            ([], ["p1", " p5"]),
            (["p2", "p1"], ["p3", "p4"]),
            ([], []),
        ]

        for pdf_path, csv_path in cases:
            config_cp = deepcopy(config)
            args.pdf = pdf_path
            args.csv = csv_path
            action.action_config_del(args, config_cp)
            new_pdf = set(config_cp["pdf_output_dir"])
            new_csv = set(config_cp["mapping_output_dir"])
            self.assertEqual(new_pdf, prev_pdf - set(pdf_path))
            self.assertEqual(new_csv, prev_csv - set(csv_path))

    def test_config_list_action(self):
        config = TestContext.get_config()
        args = Mock()
        out = io.StringIO()
        sys.stdout = out
        sys.stderr = out
        args.config_mode = "list"

        action.action_config(args, config)
        self.assertEqual(out.getvalue().strip()[0], "1")
        try:
            data = out.getvalue()[1:].strip()
            parsed = json.loads(data)
            self.assertEqual(parsed, config)
        except Exception:
            self.fail()

    def test_coa_action(self):
        config = TestContext.get_config()
        tests_path = PathCorrection(config["test_coa_exp_dir"]).as_path()
        exp_map = {}
        START = "2025-03-15"
        END = "2025-03-31"
        user = os.getenv("API_USER")
        passkey = os.getenv("API_PASS")
        for file in os.listdir(tests_path):
            exp_map[int(file.split("_")[0])] = tests_path / file

        args = Mock()
        out = io.StringIO()
        sys.stdout = out
        # sys.stderr = out
        args.user = user
        args.passkey = passkey
        args.ids = list(exp_map.keys())
        args.start = START
        args.end = END
        args.name = "TESTER"
        action.action_coa(args, config)
        res = out.getvalue().strip()
        self.assertEqual(res[0], "1")

        files = res[1:].split("\n")
        pdf_files = [f for f in files if f.endswith(".pdf")]
        csv_files = [f for f in files if f.endswith(".csv")]
        ids = set()
        for pdf in pdf_files:
            if not pdf.endswith(".pdf"):  # ignore non- .pdf files
                continue
            id = int(Path(pdf).name.split("_")[0])
            ids.add(id)
            exp = exp_map[id]
            pdf_r = PdfReader(pdf)
            exp_r = PdfReader(exp)
            # Check if pdf is encrypted
            self.assertTrue(pdf_r.is_encrypted)

            pdf_f = pdf_r.get_form_text_fields()
            exp_f = exp_r.get_form_text_fields()

            for field, val in exp_f.items():
                field = str(field)
                val = str(val)
                if "text" in field.lower():
                    # Sign date
                    continue
                try:
                    produced = pdf_f[field]
                except Exception:
                    self.fail()
                self.assertEqual(produced, val)

        exp_column: list[str] = []
        with open(PathCorrection(config["mapping_columns"]).as_path()) as f:
            exp_column = json.load(f)

        seen_ids = set()
        for csv in csv_files:
            values = pd.read_csv(csv)
            # check if column names are correct
            self.assertEqual(set(values.columns.values), set(exp_column))
            for val in values["LotNumber"].values:
                # No Duplicate values in mapping
                self.assertNotIn(int(val), seen_ids)
                seen_ids.add(int(val))
        self.assertEqual(ids, seen_ids)  # all ids were in the mapping
