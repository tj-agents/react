from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("sync_generated", ROOT / ".agents" / "sync_generated.py")
sync_generated = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_generated)


class SourceLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads((ROOT / ".agents/plugins/sources.json").read_text(encoding="utf-8"))
        cls.payloads = json.loads((ROOT / ".agents/plugins/payloads.json").read_text(encoding="utf-8"))
        cls.skills = sync_generated.discover(ROOT, cls.config)

    def test_inventory_is_fifteen_contracts(self) -> None:
        self.assertEqual(15, len(self.skills))
        self.assertEqual({"contract"}, {skill["metadata"]["kind"] for skill in self.skills.values()})
        self.assertFalse((ROOT / ".agents/skills").exists())

    def test_core_does_not_select_optional_libraries_or_app_tiers(self) -> None:
        profiles = self.payloads["profiles"]
        self.assertEqual(["contract-naming", "structure", "typescript-style"], profiles["core"])
        optional = {
            "client-state", "data-tables", "date-formatting", "frontend-testing", "http-layer",
            "routing", "server-state", "stack-defaults", "tiered-shared-code", "ui-components", "write-boundary",
        }
        self.assertTrue(optional.isdisjoint(profiles["core"]))
        core_requires = ", ".join(self.skills[name]["metadata"]["requires"] for name in profiles["core"]).lower()
        for forbidden in ("tanstack", "zustand", "tailwind", "axios", "multi-app"):
            self.assertNotIn(forbidden, core_requires)
        assigned = [name for names in profiles.values() for name in names]
        self.assertEqual(len(assigned), len(set(assigned)))
        self.assertEqual({"react-structure": "structure"}, self.payloads["compatibilitySkillAliases"])
        self.assertEqual(set(self.skills), set(assigned) | set(self.payloads["compatibilitySkillAliases"]))
        self.assertIn("[react:structure](../structure/SKILL.md)", self.skills["react-structure"]["body"])

    def test_optional_profiles_name_their_prerequisites(self) -> None:
        expected = {
            "client-state": "zustand",
            "data-tables": "tanstack-table",
            "http-layer": "axios",
            "routing": "tanstack-router",
            "server-state": "tanstack-query",
            "tiered-shared-code": "multi-app-repository",
            "ui-components": "tailwind",
            "write-boundary": "zod",
        }
        for name, prerequisite in expected.items():
            self.assertIn(prerequisite, self.skills[name]["metadata"]["requires"])

    def test_generated_adapters_reference_canonical_and_package_is_self_contained(self) -> None:
        for name, skill in self.skills.items():
            source = ROOT / skill["relative"]
            package = ROOT / "plugins/react/skills" / name / "SKILL.md"
            self.assertEqual(source.read_bytes(), package.read_bytes())
            for adapter_root in (".codex/skills", ".claude/skills"):
                adapter = (ROOT / adapter_root / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("canonical shared definition", adapter)
                self.assertNotEqual(source.read_text(encoding="utf-8"), adapter)

    def test_local_references_resolve_and_retired_sources_are_absent(self) -> None:
        identifiers = re.compile(r"(?<![-/\w])(react|engineering):(?!:)([a-z][a-z0-9-]+)")
        offenders = []
        for name, skill in self.skills.items():
            body = skill["body"]
            self.assertNotIn("concertable", body.lower())
            self.assertNotIn("standards/", body.lower())
            for namespace, target in identifiers.findall(body):
                if namespace == "react" and target not in self.skills:
                    offenders.append(f"{name}: {namespace}:{target}")
        self.assertEqual([], offenders)

    def test_bare_and_qualified_skill_references_resolve(self) -> None:
        broken = dict(self.skills["structure"])
        broken["body"] = broken["body"] + "\nSee the `missing-capability` skill.\n"
        copied = dict(self.skills)
        copied["structure"] = broken
        with self.assertRaisesRegex(ValueError, "missing bare skill reference"):
            sync_generated.validate(ROOT, self.config, self.payloads, copied)

    def test_host_manifests_reject_drift_and_cache_pinning(self) -> None:
        codex = json.loads((ROOT / ".agents/plugins/manifests/codex/react.json").read_text(encoding="utf-8"))
        claude = json.loads((ROOT / ".agents/plugins/manifests/claude/react.json").read_text(encoding="utf-8"))
        codex_marketplace = json.loads((ROOT / ".agents/plugins/manifests/codex/marketplace.json").read_text(encoding="utf-8"))
        claude_marketplace = json.loads((ROOT / ".agents/plugins/manifests/claude/marketplace.json").read_text(encoding="utf-8"))
        sync_generated.validate_host_metadata(codex, claude, codex_marketplace, claude_marketplace)
        changed = dict(claude)
        changed["description"] = "drifted"
        with self.assertRaisesRegex(ValueError, "disagree on description"):
            sync_generated.validate_host_metadata(codex, changed, codex_marketplace, claude_marketplace)
        changed = dict(claude)
        changed["version"] = None
        with self.assertRaisesRegex(ValueError, "omit version"):
            sync_generated.validate_host_metadata(codex, changed, codex_marketplace, claude_marketplace)
        changed_codex, changed_claude = dict(codex), dict(claude)
        changed_codex["name"] = changed_claude["name"] = "other"
        with self.assertRaisesRegex(ValueError, "react identity"):
            sync_generated.validate_host_metadata(changed_codex, changed_claude, codex_marketplace, claude_marketplace)
        changed_codex, changed_claude = dict(codex), dict(claude)
        changed_codex["skills"] = changed_claude["skills"] = "./missing/"
        with self.assertRaisesRegex(ValueError, "packaged skills path"):
            sync_generated.validate_host_metadata(changed_codex, changed_claude, codex_marketplace, claude_marketplace)

    def test_canonical_definitions_have_no_embedded_bom(self) -> None:
        for skill in self.skills.values():
            self.assertNotIn("\ufeff", skill["body"])

    def test_generated_selection_matches_metadata(self) -> None:
        selection = json.loads((ROOT / "plugins/react/selection.json").read_text(encoding="utf-8"))
        self.assertEqual(self.payloads["profiles"], selection["profiles"])
        by_name = {item["name"]: item for item in selection["skills"]}
        self.assertEqual(set(self.skills), set(by_name))
        for name, skill in self.skills.items():
            self.assertEqual(skill["metadata"]["profile"], by_name[name]["profile"])


if __name__ == "__main__":
    unittest.main()
