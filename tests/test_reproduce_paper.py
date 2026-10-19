"""Regression checks for isolated paper builds and stale-output rejection."""

from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import reproduce_paper as target


class PaperBuildTests(unittest.TestCase):
    def test_known_matplotlib_minus_sign_regression_is_rejected(self):
        with patch.object(target.importlib.util, "find_spec", return_value=object()), \
             patch.object(target.shutil, "which", return_value="/usr/bin/tex"), \
             patch.object(target.importlib.metadata, "version", return_value="3.11.0"):
            with self.assertRaisesRegex(ValueError, "drops minus signs"):
                target.prerequisites("build")

    def test_failed_command_does_not_count_partial_output_as_success(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            runner = target.Runner(output, {"commands": []})
            with self.assertRaisesRegex(RuntimeError, "exit 7"):
                runner.run([sys.executable, "-c",
                            "from pathlib import Path; Path('figure.pdf').write_bytes(b'%PDF-partial'); raise SystemExit(7)"],
                           output, ["figure.pdf"])
            self.assertEqual(runner.manifest["commands"][0]["status"], "failed")
            self.assertEqual(runner.manifest["commands"][0]["returncode"], 7)

    def test_success_without_new_output_rejects_stale_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            (output / "figure.pdf").write_bytes(b"%PDF-stale")
            runner = target.Runner(output, {"commands": []})
            with self.assertRaisesRegex(RuntimeError, "did not produce"):
                runner.run([sys.executable, "-c", "pass"], output, ["figure.pdf"])
            self.assertFalse((output / "figure.pdf").exists())

    def test_all_regenerated_figures_replace_manuscript_copies(self):
        class FigureRunner:
            manifest = {}

            def run(self, command, cwd, expected):
                for name in expected:
                    (cwd / name).write_bytes(b"%PDF-fresh:" + name.encode())

        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / "figures").mkdir()
            (source / f"{target.MAIN}.tex").write_text(
                "\n".join(r"\includegraphics{" + name + "}" for name in target.FIGURES))
            for name in target.FIGURES:
                (source / name).write_bytes(b"%PDF-old manuscript figure")
                (source / "figures" / name).write_bytes(b"%PDF-old generated figure")
            runner = FigureRunner()
            target.make_figures(runner, source)
            for name in target.FIGURES:
                self.assertEqual((source / name).read_bytes(), b"%PDF-fresh:" + name.encode())
            self.assertEqual(set(runner.manifest["manuscript_figure_sha256"]), set(target.FIGURES))

    def test_unplanned_manuscript_figure_cannot_use_an_old_copy(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / f"{target.MAIN}.tex").write_text(r"\includegraphics{fig-new.pdf}")
            (source / "fig-new.pdf").write_bytes(b"%PDF-old")
            with self.assertRaisesRegex(RuntimeError, "figure list changed"):
                target.make_figures(None, source)

    def test_staging_preserves_source_and_refuses_reuse(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / "canonical", root / "run"
            source.mkdir()
            (source / "fig1.pdf").write_bytes(b"%PDF-canonical")
            staged = target.prepare_output(source, output)
            (staged / "fig1.pdf").write_bytes(b"%PDF-new")
            self.assertEqual((source / "fig1.pdf").read_bytes(), b"%PDF-canonical")
            with self.assertRaisesRegex(ValueError, "not empty"):
                target.prepare_output(source, output)
            with self.assertRaisesRegex(ValueError, "separate"):
                target.prepare_output(source, source / "run")


if __name__ == "__main__":
    unittest.main()
