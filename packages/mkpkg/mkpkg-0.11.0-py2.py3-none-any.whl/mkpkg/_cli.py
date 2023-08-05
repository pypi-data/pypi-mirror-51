#! /usr/bin/env python2

from datetime import datetime
import configparser
import io
import os
import pwd
import sys
import subprocess
import textwrap

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

import click
import jinja2


STATUS_CLASSIFIERS = {
    "planning": "Development Status :: 1 - Planning",
    "prealpha": "Development Status :: 2 - Pre-Alpha",
    "alpha": "Development Status :: 3 - Alpha",
    "beta": "Development Status :: 4 - Beta",
    "stable": "Development Status :: 5 - Production/Stable",
    "mature": "Development Status :: 6 - Mature",
    "inactive": "Development Status :: 7 - Inactive",
}
VERSION_CLASSIFIERS = {
    "pypy": "Programming Language :: Python :: 2.7",
    "pypy3": "Programming Language :: Python :: 3.6",

    "py27": "Programming Language :: Python :: 2.7",
    "py35": "Programming Language :: Python :: 3.5",
    "py36": "Programming Language :: Python :: 3.6",
    "py37": "Programming Language :: Python :: 3.7",
    "py38": "Programming Language :: Python :: 3.8",
    "py39": "Programming Language :: Python :: 3.9",

    "jython": "Programming Language :: Python :: 2.7",
}
TRAVIS_SUPPORTS = {
    "py27": "2.7",
    "py35": "3.5",
    "py36": "3.6",
    "py37": "3.7",
    "py38": "3.8",
    "py39": "3.9",
}
TEST_DEPS = {
    "py.test": ["pytest"],
    "trial": ["twisted"],
}


def dedented(*args, **kwargs):
    return textwrap.dedent(*args, **kwargs).lstrip("\n")


@click.command()
@click.argument("name")
@click.option(
    "--author",
    default=pwd.getpwuid(os.getuid()).pw_gecos.partition(",")[0],
    help="the name of the package author",
)
@click.option(
    "--author-email",
    default=None,
    help="the package author's email",
)
@click.option(
    "-c",
    "--cli",
    multiple=True,
    help="include a CLI in the resulting package with the given name",
)
@click.option(
    "--readme",
    default="",
    help="a (rst) README for the package",
)
@click.option(
    "-t",
    "--test-runner",
    default="trial",
    type=click.Choice(["pytest", "trial"]),
    help="the test runner to use",
)
@click.option(
    "-s",
    "--supports",
    multiple=True,
    type=click.Choice(sorted(VERSION_CLASSIFIERS)),
    default=["py36", "py37", "pypy", "pypy3"],
    help="a version of Python supported by the package",
)
@click.option(
    "--status",
    type=click.Choice(STATUS_CLASSIFIERS),
    default="alpha",
    help="the initial package development status",
)
@click.option(
    "--docs/--no-docs",
    default=False,
    help="generate a Sphinx documentation template for the new package",
)
@click.option(
    "--single",
    "--no-package",
    "single_module",
    is_flag=True,
    default=False,
    help="create a single module rather than a package.",
)
@click.option(
    "--bare/--no-bare",
    "bare",
    default=False,
    help="only create the core source files.",
)
@click.option(
    "--style/--no-style",
    "style",
    default=True,
    help="(don't) run pyflakes by default in tox runs.",
)
@click.option(
    "--init-vcs/--no-init-vcs",
    default=True,
    help="don't initialize a VCS.",
)
@click.option(
    "--closed/--open",
    default=False,
    help="create a closed source package.",
)
def main(
    name,
    author,
    author_email,
    cli,
    readme,
    test_runner,
    supports,
    status,
    docs,
    single_module,
    bare,
    style,
    init_vcs,
    closed,
):
    """
    Oh how exciting! Create a new Python package.
    """

    if name.startswith("python-"):
        package_name = name[len("python-"):]
    else:
        package_name = name
    package_name = package_name.lower().replace("-", "_")

    root = Path(name)
    package = Path(package_name)

    if single_module:
        contents = u"py_modules", name
        tests = u"{toxinidir}/tests.py"

        if len(cli) > 1:
            sys.exit("Cannot create a single module with multiple CLIs.")
        elif cli:
            console_scripts = [u"{} = {}:main".format(cli[0], package_name)]
            script = render(
                "package", "_cli.py",
                package_name=package_name,
                cli=cli[0],
                single_module=single_module,
            )
        else:
            console_scripts = []
            script = u""

        core_source_paths = {
            package_name + ".py": script,
            "tests.py": render(
                "tests.py",
                name=name,
                package_name=package_name,
            ),
        }

    else:
        contents = u"packages", u"find:"
        tests = package_name

        core_source_paths = {
            package / "tests" / "__init__.py": u"",
            package / "__init__.py": template("package", "__init__.py"),
        }

        if len(cli) == 1:
            console_scripts = [
                "{} = {}._cli:main".format(cli[0], package_name),
            ]
            core_source_paths[package / "_cli.py"] = render(
                "package", "_cli.py",
                package_name=package_name,
                cli=cli[0],
                single_module=single_module,
            )
            core_source_paths[package / "__main__.py"] = render(
                "package", "__main__.py", package_name=package_name,
            )
        else:
            console_scripts = [
                "{each} = {package_name}._{each}:main".format(
                    each=each, package_name=package_name,
                ) for each in cli
            ]
            core_source_paths.update(
                (
                    package / ("_" + each + ".py"),
                    render(
                        "package",
                        "_cli.py",
                        package_name=package_name,
                        cli=each,
                        single_module=single_module,
                    ),
                ) for each in cli
            )

    files = {
        "README.rst": render(
            "README.rst",
            name=name,
            contents=readme,
            closed=closed,
            docs=docs,
        ),
        "COPYING": render(
            "COPYING", now=datetime.now(), author=author, closed=closed,
        ),
        "MANIFEST.in": template("MANIFEST.in"),
        "setup.cfg": render(
            "setup.cfg",
            package_name=package_name,
            contents=contents,
            name=name,
            author=author,
            console_scripts=console_scripts,
            single_module=single_module,
            author_email=(
                author_email or u"Julian+" + package_name + u"@GrayVines.com"
            ),
            status_classifier=STATUS_CLASSIFIERS[status],
            version_classifiers={
                VERSION_CLASSIFIERS[each]
                for each in supports
                if each in VERSION_CLASSIFIERS
            },
            closed=closed,
            supports=supports,
            py2=any(
                version.startswith("py2")
                or version in {"jython", "pypy"}
                for version in supports
            ),
            py3=any(
                version.startswith("py3")
                or version == "pypy3"
                for version in supports
            ),
            cpython=any(
                version not in {"jython", "pypy", "pypy3"}
                for version in supports
            ),
            pypy="pypy" in supports or "pypy3" in supports,
            jython="jython" in supports,
        ),
        "setup.py": template("setup.py"),
        ".coveragerc": render(".coveragerc", package_name=package_name),
        "tox.ini": render(
            "tox.ini",
            name=name,
            package_name=package_name,
            supports=supports,
            closed=closed,
            docs=docs,
            style=style,
            test_deps=TEST_DEPS[test_runner],
            test_runner=test_runner,
            tests=tests,
        ),
        ".testr.conf": template(".testr.conf"),
    }

    if not closed:
        files.update(
            {
                ".travis.yml": render(
                    ".travis.yml",
                    travis_supports=sorted(
                        TRAVIS_SUPPORTS.get(each, each)
                        for each in supports
                    ),
                ),
                "codecov.yml": template("codecov.yml"),
            },
        )

    if bare:
        targets = core_source_paths
    else:
        files.update(core_source_paths)
        targets = files
        root.mkdir()

    for path, content in targets.items():
        path = root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(dedented(content))

    if docs:
        (root / "docs").mkdir()
        (root / "docs" / "requirements.txt").write_text(
            template("docs", "requirements.txt"),
        )

        subprocess.check_call(
            [
                sys.executable,
                "-m", "sphinx.cmd.quickstart",
                "--quiet",
                "--project", name,
                "--author", author,
                "--release", "",
                "--ext-autodoc",
                "--ext-coverage",
                "--ext-doctest",
                "--ext-intersphinx",
                "--ext-viewcode",
                "--extensions", "sphinx.ext.napoleon",
                "--extensions", "sphinxcontrib.spelling",
                "--makefile",
                "--no-batchfile",
                str(root / "docs"),
            ],
        )
        (root / "docs" / "index.rst").write_text(
            render("docs", "index.rst", README=files["README.rst"]),
        )

    if init_vcs and not bare:
        subprocess.check_call(["git", "init", "--quiet", name])

        git_dir = root / ".git"
        subprocess.check_call(
            [
                "git",
                "--git-dir", str(git_dir),
                "--work-tree", name,
                "add", "COPYING",
            ])
        subprocess.check_call(
            [
                "git",
                "--git-dir", str(git_dir),
                "commit", "--quiet", "-m", "Initial commit",
            ],
        )

        if not closed:
            click.echo(
                "Set up codecov at: https://codecov.io/gh/Julian/" + name,
            )


def template(*segments):
    path = Path(__file__).with_name("template").joinpath(*segments)
    return path.read_text()


def render(*segments, **values):
    segments = segments[:-1] + (segments[-1] + ".j2",)
    return jinja2.Template(
        template(*segments),
        undefined=jinja2.StrictUndefined,
        keep_trailing_newline=True,
    ).render(values)
