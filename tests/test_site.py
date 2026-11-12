"""The packages site generator: spec parsing, release listings and the pages."""

import importlib.machinery
import importlib.util
import os
import shutil
import tempfile
import unittest

ROOT = os.path.join(os.path.dirname(__file__), "..")
loader = importlib.machinery.SourceFileLoader("build_site", os.path.join(ROOT, "scripts", "build-site"))
site = importlib.util.module_from_spec(importlib.util.spec_from_loader("build_site", loader))
loader.exec_module(site)

SPEC = """\
%global commit 0123456789abcdef0123456789abcdef01234567
%global shortcommit %(c=%{commit}; echo ${c:0:7})
Name:           demo
Version:        1.2
Release:        3.git%{shortcommit}%{?dist}
Summary:        Demo tool
License:        MIT
URL:            https://example.org/%{name}
Source0:        %{url}/archive/%{name}.tar.gz

%description
The first line
continues here.

%package -n demo-extra
Summary:        Extra parts of the demo

%description -n demo-extra
Extras for the demo.

%prep
%autosetup
"""


class Specs(unittest.TestCase):
    def test_a_spec_gives_its_packages_with_macros_expanded(self):
        with tempfile.TemporaryDirectory() as directory:
            os.makedirs(os.path.join(directory, "demo"))
            path = os.path.join(directory, "demo", "demo.spec")
            with open(path, "w") as handle:
                handle.write(SPEC)
            spec = site.parse_spec(path)
        self.assertEqual((spec["name"], spec["version"], spec["license"]), ("demo", "1.2", "MIT"))
        self.assertEqual(spec["release"], "3.git0123456")
        self.assertEqual(spec["url"], "https://example.org/demo")
        self.assertEqual([(p["name"], p["summary"]) for p in spec["packages"]],
                         [("demo", "Demo tool"), ("demo-extra", "Extra parts of the demo")])
        self.assertEqual(spec["packages"][0]["description"], "The first line continues here.")

    def test_the_real_specs_all_parse_with_a_name_and_a_summary(self):
        specs = site.load_specs()
        names = {p["name"] for s in specs for p in s["packages"]}
        self.assertTrue({"foundation", "foundationd", "ersa-boot-splash"} <= names, names)
        for spec in specs:
            for package in spec["packages"]:
                self.assertTrue(package["summary"], package["name"])
                self.assertNotIn("%", package["name"])


class Releases(unittest.TestCase):
    def test_rpm_file_names(self):
        self.assertEqual(site.split_rpm("foundation-0.5.0-2.noarch.rpm"),
                         {"name": "foundation", "version": "0.5.0", "release": "2", "arch": "noarch"})
        self.assertEqual(site.split_rpm("ersa-dialer-0.1.0-1.git0605858.x86_64.rpm")["release"], "1.git0605858")
        for ignored in ("foundation-0.5.0-2.src.rpm", "foo-debuginfo-1-1.x86_64.rpm", "foo-debugsource-1-1.x86_64.rpm", "readme.txt"):
            self.assertIsNone(site.split_rpm(ignored), ignored)

    def test_versions_are_grouped_by_package_newest_release_first_and_drafts_are_hidden(self):
        releases = [
            {"tag_name": "old", "published_at": "2026-01-01T00:00:00Z", "assets": [
                {"name": "a-1-1.noarch.rpm", "browser_download_url": "u1", "size": 10}]},
            {"tag_name": "new", "published_at": "2026-02-01T00:00:00Z", "prerelease": True, "assets": [
                {"name": "a-2-1.noarch.rpm", "browser_download_url": "u2", "size": 20},
                {"name": "a-2-1.src.rpm", "browser_download_url": "x", "size": 1}]},
            {"tag_name": "draft", "draft": True, "published_at": "2026-03-01T00:00:00Z", "assets": [
                {"name": "a-3-1.noarch.rpm", "browser_download_url": "u3", "size": 30}]},
        ]
        found = site.versions_by_package(releases)
        self.assertEqual([v["version"] for v in found["a"]], ["2", "1"])
        self.assertTrue(found["a"][0]["prerelease"])
        self.assertEqual(found["a"][1]["url"], "u1")

    def test_sizes(self):
        self.assertEqual(site.size(10), "10 B")
        self.assertEqual(site.size(2048), "2.0 KiB")


class Pages(unittest.TestCase):
    def setUp(self):
        self.out = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.out, True)

    def test_the_site_without_rpms_says_the_repository_is_empty_and_links_every_page(self):
        output = os.path.join(self.out, "site")
        site.build(output, cname="packages.example.org")
        with open(os.path.join(output, "index.html")) as handle:
            index = handle.read()
        self.assertIn("The repository is empty", index)
        self.assertIn("packages/foundation.html", index)
        self.assertIn("not published yet", index)
        for name in ("using.html", "publishing.html", "building.html", "ersa.repo", ".nojekyll", "CNAME",
                     "packages/foundationd.html"):
            self.assertTrue(os.path.exists(os.path.join(output, name)), name)
        with open(os.path.join(output, "CNAME")) as handle:
            self.assertEqual(handle.read().strip(), "packages.example.org")

    def test_a_package_page_lists_its_versions_with_links_to_the_files(self):
        output = os.path.join(self.out, "site")
        releases = [{"tag_name": "r1", "published_at": "2026-11-12T00:00:00Z", "assets": [
            {"name": "foundation-0.5.0-2.noarch.rpm", "browser_download_url": "https://example.org/f.rpm", "size": 2048}]}]
        site.build(output, releases=releases)
        with open(os.path.join(output, "packages", "foundation.html")) as handle:
            page = handle.read()
        self.assertIn('href="https://example.org/f.rpm"', page)
        self.assertIn("0.5.0-2", page)
        self.assertIn("2026-11-12", page)
        with open(os.path.join(output, "index.html")) as handle:
            self.assertIn("0.5.0-2 (release r1)", handle.read())

    def test_links_between_documents_become_pages_and_nothing_is_left_dangling(self):
        pages = {"index", "using"}
        html = site.render_markdown("See [using](using.md) and [the source](https://x.y) and [a file](scripts/build-site).", pages)
        self.assertIn('href="using.html"', html)
        self.assertIn('href="https://x.y"', html)
        self.assertIn("filelink", html)        # a link to a source file is shown as text

    def test_the_repo_file_points_at_the_base_url(self):
        output = os.path.join(self.out, "site")
        site.build(output, base="https://packages.example.org")
        with open(os.path.join(output, "ersa.repo")) as handle:
            text = handle.read()
        self.assertIn("baseurl=https://packages.example.org/repo/", text)
        self.assertIn("gpgkey=https://packages.example.org/ersa-ecpx.asc", text)


if __name__ == "__main__":
    unittest.main()
