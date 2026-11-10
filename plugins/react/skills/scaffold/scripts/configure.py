import argparse
import json
import shutil
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parents[1] / "templates"
CONFIGURATION_FILES = (
    "eslint.config.mjs",
    "tsconfig.json",
    ".node-version",
    ".github/workflows/react-checks.yml",
)
LEGACY_ESLINT_FILES = (
    ".eslintrc",
    ".eslintrc.js",
    ".eslintrc.cjs",
    ".eslintrc.json",
    ".eslintrc.yml",
    ".eslintrc.yaml",
    ".eslintignore",
    "eslint.config.js",
    "eslint.config.cjs",
    "eslint.config.ts",
    "eslint.config.mts",
    "eslint.config.cts",
)


def load_package(path: Path) -> dict[str, object]:
    data: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(isinstance(key, str) for key in data):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def string_fields(package: dict[str, object], name: str) -> dict[str, str]:
    data = package.get(name, {})
    if not isinstance(data, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in data.items()
    ):
        raise ValueError(f"package.json {name} must contain string values")
    return data


def configure(target: Path) -> None:
    target = target.resolve(strict=True)
    package_path = target / "package.json"
    package = load_package(package_path)
    if "eslintConfig" in package:
        raise ValueError(
            "Resolve the existing package.json eslintConfig before configuring"
        )
    for name in (*CONFIGURATION_FILES, *LEGACY_ESLINT_FILES):
        if (target / name).exists():
            raise ValueError(f"Resolve the existing {name} before configuring")
    tooling = load_package(TEMPLATES / "package.json")
    for field in ("scripts", "devDependencies"):
        current = string_fields(package, field)
        supplied = string_fields(tooling, field)
        conflicts = current.keys() & supplied.keys()
        if conflicts:
            raise ValueError(
                f"Resolve existing {field}: {', '.join(sorted(conflicts))}"
            )
        package[field] = current | supplied
    for name in CONFIGURATION_FILES:
        destination = target / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(TEMPLATES / name, destination)
    package_path.write_text(json.dumps(package, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Configure React linting and type checks"
    )
    parser.add_argument("target", type=Path)
    arguments = parser.parse_args()
    try:
        configure(arguments.target)
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
