import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import check_skills  # noqa: E402


def skill(name="oca-x", extra=""):
    return f"---\nname: {name}\ndescription: A test skill.\n---\n\n# {name}\n{extra}"


class CheckSkillsTests(unittest.TestCase):
    def setUp(self):
        holder = tempfile.TemporaryDirectory()
        self.addCleanup(holder.cleanup)
        self.root = Path(holder.name)

    def add(self, folder, files):
        for relative, text in files.items():
            path = self.root / "skills" / folder / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def errors(self):
        (self.root / "skills").mkdir(exist_ok=True)
        return check_skills.check(self.root)[0]

    def test_valid_skill(self):
        self.add("oca-x", {"SKILL.md": skill()})
        self.assertEqual(self.errors(), [])

    def test_name_must_match_folder(self):
        self.add("oca-x", {"SKILL.md": skill("other")})
        self.assertIn("frontmatter name is 'other'", self.errors()[0])

    def test_description_is_required(self):
        self.add("oca-x", {"SKILL.md": "---\nname: oca-x\n---\n\n# x\n"})
        self.assertIn("no description", self.errors()[0])

    def test_frontmatter_is_required(self):
        self.add("oca-x", {"SKILL.md": "# no header\n"})
        self.assertIn("no frontmatter", self.errors()[0])

    def test_folded_description_is_accepted(self):
        text = "---\nname: oca-x\ndescription: >-\n  Long\n  text.\n---\n\n# x\n"
        self.add("oca-x", {"SKILL.md": text})
        self.assertEqual(self.errors(), [])

    def test_line_limit(self):
        self.add("oca-x", {"SKILL.md": skill(extra="line\n" * 500)})
        self.assertIn("max 500", self.errors()[0])

    def test_folder_without_skill_md(self):
        (self.root / "skills" / "empty").mkdir(parents=True)
        self.assertIn("SKILL.md not found", self.errors()[0])

    def test_version_files_are_named_like_a_version(self):
        self.add("oca-x", {"SKILL.md": skill(), "versions/20.0.md": "x",
                           "versions/twenty.md": "x"})
        errors = self.errors()
        self.assertEqual(len(errors), 1)
        self.assertIn("versions/twenty.md is not named", errors[0])

    def test_mentioned_version_file_must_exist(self):
        self.add("oca-x", {"SKILL.md": skill(extra="Read versions/21.0.md\n"),
                           "versions/20.0.md": "x"})
        self.assertIn("versions/21.0.md, which does not exist", self.errors()[0])

    def test_mentioned_version_file_exists(self):
        self.add("oca-x", {"SKILL.md": skill(extra="Read versions/20.0.md\n"),
                           "versions/20.0.md": "x"})
        self.assertEqual(self.errors(), [])


class LinkTests(unittest.TestCase):
    setUp = CheckSkillsTests.setUp
    add = CheckSkillsTests.add
    errors = CheckSkillsTests.errors

    def two_files(self, link, other="# Title\n\n# Second part\n"):
        self.add("oca-x", {"SKILL.md": skill(extra=f"See [x]({link}).\n"),
                           "guidelines/a.md": other})

    def test_valid_link_and_anchor(self):
        self.two_files("guidelines/a.md#second-part")
        self.assertEqual(self.errors(), [])

    def test_missing_file(self):
        self.two_files("guidelines/nope.md")
        self.assertIn("does not exist", self.errors()[0])

    def test_missing_anchor(self):
        self.two_files("guidelines/a.md#third-part")
        self.assertIn("no heading #third-part", self.errors()[0])

    def test_anchor_in_the_same_file(self):
        self.add("oca-x", {"SKILL.md": skill(extra="## Part one\n\n[x](#part-one)\n")})
        self.assertEqual(self.errors(), [])

    def test_slug_drops_punctuation_and_keeps_underscores(self):
        self.assertEqual(check_skills.slug("Open files with `file_open`"),
                         "open-files-with-file_open")
        self.assertEqual(check_skills.slug("Routes, auth, POST and CSRF"),
                         "routes-auth-post-and-csrf")
        self.assertEqual(check_skills.slug("Do not over-sudo"), "do-not-over-sudo")

    def test_links_and_headings_in_code_fences_are_ignored(self):
        fenced = "```python\n# not a heading\nx[0](bad)\n```\n"
        self.add("oca-x", {"SKILL.md": skill(extra=fenced + "[x](#not-a-heading)\n")})
        self.assertIn("no heading #not-a-heading", self.errors()[0])
        self.assertEqual(len(self.errors()), 1)

    def test_external_links_are_not_checked(self):
        self.add("oca-x", {"SKILL.md": skill(extra="[x](https://example.com/a#b)\n")})
        self.assertEqual(self.errors(), [])


class RealRepositoryTests(unittest.TestCase):
    def test_skills_are_valid(self):
        errors, count = check_skills.check(REPO)
        self.assertEqual(errors, [])
        self.assertGreaterEqual(count, 1)

    def test_oca_git_does_not_depend_on_an_odoo_skill(self):
        text = (REPO / "skills" / "oca-git" / "SKILL.md").read_text()
        self.assertNotIn("../odoo-", text)


if __name__ == "__main__":
    unittest.main()
