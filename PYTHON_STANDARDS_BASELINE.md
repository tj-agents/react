# Python standards baseline

Existing violations at `38e987e0027fa964bedebcb5517135fbbead0e70` are baselined by exact authored file and rule. New files receive all enabled checks. Remove an exception when repairing its source. The tool configuration owns enforcement; this document records the rollout evidence and rationale.

## Ruff

Reason: preserve existing implementations during the standards rollout. Each row records the existing count and a representative required repair. No wildcard path or whole-rule ignores were added.

| File | Rule | Existing count | Required repair |
| --- | --- | ---: | --- |
| `.agents/tests/test_core_profile.py` | `E501` | 9 | Line too long (103 > 88) |
| `.agents/tests/test_core_profile.py` | `I001` | 1 | Import block is un-sorted or un-formatted |
| `.agents/tests/test_core_profile.py` | `PT009` | 10 | Use a regular `assert` instead of unittest-style `assertTrue` |
| `.agents/tests/test_core_profile.py` | `TID251` | 2 | `importlib.util.spec_from_file_location` is banned: Import the installed public API; do not load another checkout by path. |

## Ruff formatter

Exact existing files requiring formatting are excluded from the formatter during this rollout. Regenerate payloads after formatting authored source and then remove its exception. New files are checked.

- `.agents/tests/test_core_profile.py`

## Mypy

Existing typing debt is baselined by exact module and diagnostic code, with its source file and count below. Add the missing annotations or fix the indicated type mismatch, then remove the corresponding module/code override. No wildcard modules or whole-module ignore was added.

| File | Module | Rule | Existing count | Required repair |
| --- | --- | --- | ---: | --- |
| `.agents/tests/test_core_profile.py` | `test_core_profile` | `arg-type` | 1 | Argument 1 to "module_from_spec" has incompatible type "ModuleSpec \| None"; expected "ModuleSpec" |
| `.agents/tests/test_core_profile.py` | `test_core_profile` | `attr-defined` | 15 | "type[ReactCoreProfileTests]" has no attribute "config" |
| `.agents/tests/test_core_profile.py` | `test_core_profile` | `union-attr` | 2 | Item "None" of "ModuleSpec \| None" has no attribute "loader" |

## Custom checker

Reason: preserve exact pre-existing custom-checker findings during the standards rollout. Each entry maps to one authored path and rule; repair the stated design issue and remove its exception. No generated or vendored path is included.

No pre-existing custom-checker findings were recorded.
