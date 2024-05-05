#  Copyright 2024 Christopher Barber
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
"""
Unit tests for whl2conda build subcommand.
"""

from __future__ import annotations

import re
from pathlib import Path

# third party
import pytest

# this project
from whl2conda.cli import main
from whl2conda.cli.build import CondaBuild

this_dir = Path(__file__).parent
root_dir = this_dir.parent.parent
test_projects = root_dir / "test-projects"


class CondaBuildWhitebox(CondaBuild):
    def _render_recipe(self):
        super()._render_recipe()

    def _check_recipe(self) -> str:
        new_script = super()._check_recipe()
        return new_script

    def _build_wheel(self) -> Path:
        return super()._build_wheel()

    def _build_package(self, wheel: Path) -> Path:
        pkg = super()._build_package(wheel)
        return pkg

    def _test_package(self, pkg: Path) -> None:
        pass
        # super()._test_package(pkg)

    def _install_package(self, pkg: Path) -> None:
        pass

    def _cleanup(self) -> None:
        super()._cleanup()


@pytest.fixture
def build_whitebox(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
):
    monkeypatch.setattr("whl2conda.cli.build.CondaBuild", CondaBuildWhitebox)


def test_simple(
    build_whitebox,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    monkeypatch.chdir(test_projects / "simple")
    main(["build", "conda.recipe"])
    out, err = capsys.readouterr()
    assert not err
    assert re.search(
        r"Elapsed time: .* seconds",
        out,
        flags=re.MULTILINE,
    )
