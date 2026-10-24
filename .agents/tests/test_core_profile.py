from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("sync_generated", ROOT / ".agents" / "sync_generated.py")
sync_generated = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_generated)


class ReactCoreProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = sync_generated.load_config(ROOT)
        cls.plugins = sync_generated.discover(ROOT, cls.config["namespace"])
        cls.skills = cls.plugins["react"]
        cls.payloads = json.loads((ROOT / ".agents/plugins/payloads.json").read_text(encoding="utf-8"))

    def test_required_stack_contracts_are_core_and_present(self) -> None:
        required = {"style", "structure", "domain-design", "errors", "testing", "build", "libraries"}
        self.assertTrue(required.issubset(self.skills))
        for name in required:
            self.assertEqual("contract", self.skills[name]["kind"])
            self.assertEqual("core", self.skills[name]["metadata"]["profile"])

    def test_core_is_exactly_the_stack_free_contracts(self) -> None:
        core_names = {
            name for name, skill in self.skills.items()
            if skill["metadata"]["profile"] == "core"
        }
        self.assertEqual(
            {
                "naming-contracts", "structure", "style",
                "domain-design", "errors", "build", "libraries", "testing", "explanation",
            },
            core_names,
        )
        must_not_be_core = {
            "state-client", "data-tables", "date-formatting", "http-layer", "routing", "state-server",
            "tiered-shared-code", "ui-components", "validation", "styling", "testing-frontend",
        }
        self.assertTrue(must_not_be_core.isdisjoint(core_names))
        core_requires = ", ".join(self.skills[name]["metadata"]["requires"] for name in core_names).lower()
        for forbidden in ("tanstack", "zustand", "tailwind", "axios", "dayjs", "zod", "multi-app"):
            self.assertNotIn(forbidden, core_requires)

    def test_optional_skills_name_their_prerequisites(self) -> None:
        expected = {
            "state-client": "zustand",
            "data-tables": "tanstack-table",
            "http-layer": "axios",
            "routing": "tanstack-router",
            "state-server": "tanstack-query",
            "tiered-shared-code": "multi-app-repository",
            "ui-components": "radix-or-shadcn",
            "styling": "tailwind",
            "validation": "zod",
            "testing-frontend": "adopted-frontend-tests",
        }
        for name, prerequisite in expected.items():
            self.assertIn(prerequisite, self.skills[name]["metadata"]["requires"])

    def test_retired_skill_names_are_absent(self) -> None:
        retired = {
            "react-structure", "client-state", "server-state", "contract-naming",
            "typescript-style", "frontend-testing", "stack-defaults", "write-boundary", "libraries-selected",
        }
        self.assertTrue(retired.isdisjoint(self.skills))
        self.assertFalse(self.payloads.get("compatibilitySkillAliases"))

    def test_structure_declares_its_file_structure_section(self) -> None:
        body = self.skills["structure"]["body"]
        self.assertIn("## File structure", body)


if __name__ == "__main__":
    unittest.main()
