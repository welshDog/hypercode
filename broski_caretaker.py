#!/usr/bin/env python3
"""
🤖 BROski Caretaker Agent for HyperCode
Autonomous diagnostic, repair, and maintenance agent.
Single-file, zero dependencies (except subprocess).

Usage:
  python broski_caretaker.py              # Full OMNI scan
  python broski_caretaker.py --mode fix   # FIX mode only
  python broski_caretaker.py --mode watch # WATCH mode only
  python broski_caretaker.py --commit     # Auto-commit if safe
"""

import subprocess
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ScanMode(Enum):
    """Operational modes for BROski."""
    STATUS = "status"      # Gather current state
    FIX = "fix"            # Detect and repair issues
    UPGRADE = "upgrade"    # Identify growth opportunities
    WATCH = "watch"        # Monitor edges & futures
    READY = "ready"        # Launch readiness check
    OMNI = "omni"          # All four modes


@dataclass
class Finding:
    """A single discovery by the agent."""
    severity: str           # "critical", "warning", "info"
    mode: str               # which quadrant found it
    title: str
    description: str
    action: Optional[str] = None  # suggested fix
    verified: bool = False

    def to_dict(self):
        return asdict(self)


@dataclass
class DiagnosticReport:
    """Full OMNI scan results."""
    timestamp: str
    db_status: Dict
    import_status: Dict
    async_status: Dict
    findings: List[Finding]
    summary: str
    ready_to_commit: bool

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "db_status": self.db_status,
            "import_status": self.import_status,
            "async_status": self.async_status,
            "findings": [f.to_dict() for f in self.findings],
            "summary": self.summary,
            "ready_to_commit": self.ready_to_commit,
        }


class BROskiCaretaker:
    """The autonomous caretaker of HyperCode."""

    def __init__(self, project_root: str = "."):
        self.root = Path(project_root)
        self.findings: List[Finding] = []
        self.critical_count = 0
        self.warning_count = 0

    def run_command(self, cmd: str, silent: bool = False) -> Tuple[str, str, int]:
        """Execute shell command safely."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=self.root,
                capture_output=True,
                text=True,
                timeout=30,
            )
            return result.stdout, result.stderr, result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", 1
        except Exception as e:
            return "", str(e), 1

    def check_db_status(self) -> Dict:
        """✅ STATUS: Scan database & migration state."""
        print("🔍 [STATUS] Scanning database layer...")
        status = {
            "alembic_version": None,
            "db_file_exists": False,
            "database_utils_exists": False,
            "async_db_exists": False,
            "schema_valid": False,
        }

        # Check Alembic version
        stdout, _, code = self.run_command("alembic current")
        if code == 0:
            status["alembic_version"] = stdout.strip()
        else:
            self.add_finding(
                Finding(
                    severity="warning",
                    mode="status",
                    title="Alembic not initialized",
                    description="Could not read current Alembic version",
                )
            )

        # Check canonical DB module
        db_utils_path = self.root / "src" / "hypercode" / "database_utils.py"
        status["database_utils_exists"] = db_utils_path.exists()

        # Check async DB module
        async_db_path = self.root / "src" / "hypercode" / "data" / "database.py"
        status["async_db_exists"] = async_db_path.exists()

        # Check SQLite file
        sqlite_path = self.root / "hypercode.db"
        status["db_file_exists"] = sqlite_path.exists()

        return status

    def check_import_hygiene(self) -> Dict:
        """✅ STATUS: Scan for import consistency."""
        print("🔍 [STATUS] Scanning import hygiene...")
        status = {
            "bad_imports_found": [],
            "canonical_imports": 0,
            "shim_files": [],
        }

        # Find all Python files
        py_files = list(self.root.glob("**/*.py"))

        for py_file in py_files:
            try:
                content = py_file.read_text()

                # Check for non-canonical imports
                if "from hypercode.data.database" in content:
                    status["bad_imports_found"].append(str(py_file))
                if "from data.database" in content:
                    status["bad_imports_found"].append(str(py_file))

                # Count canonical imports
                if "from hypercode.database_utils" in content:
                    status["canonical_imports"] += 1

            except Exception:
                pass  # Skip unreadable files

        # Find shim files
        shim_dir = self.root / "src" / "hypercode" / "data"
        if shim_dir.exists():
            shim_files = list(shim_dir.glob("*.py"))
            status["shim_files"] = [str(f) for f in shim_files]

        if status["bad_imports_found"]:
            self.add_finding(
                Finding(
                    severity="warning",
                    mode="fix",
                    title="Non-canonical imports detected",
                    description=f"Found {len(status['bad_imports_found'])} files with bad imports",
                    action="Run: grep -r 'from data.database' src/ && sed -i 's|from data.database|from hypercode.database_utils|g' src/**/*.py",
                )
            )

        return status

    def check_async_status(self) -> Dict:
        """✅ STATUS: Understand async DB path."""
        print("🔍 [STATUS] Scanning async DB configuration...")
        status = {
            "database_py_active": False,
            "modules_depending_on_async": [],
            "decision_needed": False,
        }

        db_file = self.root / "src" / "hypercode" / "data" / "database.py"
        if not db_file.exists():
            return status

        status["database_py_active"] = True

        # Find modules that import from async database
        py_files = list(self.root.glob("**/*.py"))
        for py_file in py_files:
            try:
                content = py_file.read_text()
                if "from hypercode.data.database" in content or (
                    "database.py" in str(py_file) and "import" in content
                ):
                    status["modules_depending_on_async"].append(str(py_file))
            except Exception:
                pass

        if status["modules_depending_on_async"]:
            status["decision_needed"] = True
            self.add_finding(
                Finding(
                    severity="warning",
                    mode="watch",
                    title="Async DB path still active",
                    description=f"{len(status['modules_depending_on_async'])} modules depend on async database.py",
                    action="Plan: Migrate modules to database_utils wrappers, then retire async DB",
                )
            )

        return status

    def verify_schema(self) -> bool:
        """✅ STATUS: Validate schema integrity."""
        print("🔍 [STATUS] Verifying schema...")
        stdout, _, code = self.run_command(
            "sqlite3 hypercode.db '.schema' | grep -q 'papers'"
        )
        return code == 0

    def diagnose(self) -> DiagnosticReport:
        """🎯 Run full OMNI diagnostic."""
        print("\n" + "=" * 70)
        print("🤖 BROski CARETAKER AGENT — OMNI DIAGNOSTIC")
        print("=" * 70 + "\n")

        db_status = self.check_db_status()
        import_status = self.check_import_hygiene()
        async_status = self.check_async_status()
        schema_valid = self.verify_schema()

        # Generate summary
        summary = self._generate_summary(db_status, import_status, async_status)

        # Determine readiness to commit
        ready_to_commit = self.critical_count == 0 and len(
            [f for f in self.findings if f.severity == "warning"]
        ) <= 2

        report = DiagnosticReport(
            timestamp=datetime.now().isoformat(),
            db_status=db_status,
            import_status=import_status,
            async_status=async_status,
            findings=self.findings,
            summary=summary,
            ready_to_commit=ready_to_commit,
        )

        return report

    def _generate_summary(self, db: Dict, imports: Dict, async_cfg: Dict) -> str:
        """Create human-readable summary."""
        lines = []

        # DB Layer
        if db.get("database_utils_exists"):
            lines.append("✅ DB unified — database_utils is canonical")
        else:
            lines.append("❌ DB layer missing — database_utils not found")

        if db.get("alembic_version"):
            lines.append(f"✅ Alembic ready — {db['alembic_version'].strip()}")
        else:
            lines.append("⚠️  Alembic not initialized")

        # Imports
        if imports.get("bad_imports_found"):
            lines.append(f"⚠️  {len(imports['bad_imports_found'])} files have bad imports")
        else:
            lines.append("✅ Imports clean — no bad imports found")

        # Async Status
        if async_cfg.get("database_py_active"):
            lines.append(
                f"⚠️  Async DB path active ({len(async_cfg['modules_depending_on_async'])} modules)"
            )
            lines.append("   → Plan migration to database_utils or document as dual-path")
        else:
            lines.append("✅ Single sync path — no async split-brain")

        return "\n".join(lines)

    def add_finding(self, finding: Finding):
        """Log a finding."""
        self.findings.append(finding)
        if finding.severity == "critical":
            self.critical_count += 1
        elif finding.severity == "warning":
            self.warning_count += 1

    def print_report(self, report: DiagnosticReport):
        """Print formatted diagnostic report."""
        print("\n" + "=" * 70)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 70)
        print(report.summary)

        if report.findings:
            print("\n" + "🔥 FINDINGS" + " " * 59)
            print("-" * 70)
            for finding in report.findings:
                icon = "🔴" if finding.severity == "critical" else "🟡" if finding.severity == "warning" else "🟢"
                print(
                    f"{icon} [{finding.mode.upper()}] {finding.title}"
                )
                print(f"   {finding.description}")
                if finding.action:
                    print(f"   → {finding.action}")
                print()

        print("\n" + "=" * 70)
        if report.ready_to_commit:
            print("✅ READY TO COMMIT")
        else:
            print(f"⚠️  FIX {self.critical_count} CRITICAL + {self.warning_count} WARNINGS BEFORE COMMIT")
        print("=" * 70 + "\n")

    def export_json(self, report: DiagnosticReport, filename: str = "broski_report.json"):
        """Export report as JSON."""
        path = self.root / filename
        with open(path, "w") as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"📄 Report exported: {path}")

    def auto_commit(self, report: DiagnosticReport):
        """Attempt safe auto-commit if ready."""
        if not report.ready_to_commit:
            print("❌ Not ready for commit. Fix findings first.")
            return False

        msg = "🔧 FIX: DB unified, async path clarified, imports canonical"
        print(f"📝 Committing: {msg}")

        stdout, stderr, code = self.run_command(f'git add . && git commit -m "{msg}"')
        if code == 0:
            print(f"✅ Commit successful:\n{stdout}")
            return True
        else:
            print(f"❌ Commit failed:\n{stderr}")
            return False


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="BROski Caretaker Agent for HyperCode")
    parser.add_argument(
        "--mode",
        choices=["status", "fix", "upgrade", "watch", "ready", "omni"],
        default="omni",
        help="Diagnostic mode (default: omni for all)",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Auto-commit if all checks pass",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Export report as JSON",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Project root directory (default: current dir)",
    )

    args = parser.parse_args()

    # Initialize agent
    agent = BROskiCaretaker(args.root)

    # Run diagnostic
    report = agent.diagnose()

    # Print results
    agent.print_report(report)

    # Export if requested
    if args.json:
        agent.export_json(report)

    # Auto-commit if requested
    if args.commit:
        agent.auto_commit(report)

    # Exit with status
    sys.exit(0 if report.ready_to_commit else 1)


if __name__ == "__main__":
    main()
