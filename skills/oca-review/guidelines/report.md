# Tone

- Start by thanking the contributor for the work. Whatever the issue of the
  PR, somebody has done work for the project.
- Be cordial and polite. Nothing is obvious in a pull request: when you are
  not sure about the purpose or the design, ask instead of assuming.
- Say what is good as well as what is wrong, when there is something good.

# Review type and verdict

- **Review type.** Say which one it is, so that people know:
  - *Code review*: you looked at the code. This skill does one.
  - *Test*: you tested the change functionally. Claim it only if you ran the
    change or its tests, and say what you ran and what the result was.
- **Verdict.** Propose one of: comment, approve, rejected, needs information.
  It is a proposal: a person decides and posts the review. Propose approve
  only when every finding is a suggestion and no question is left open.

# Approvals

At least one of the reviews of a pull request must come from a member of the
PSC, or from someone with write access to the repository: one of the
OCA core maintainers, who can be notified on GitHub with
`@OCA/core-maintainers`. This review cannot check who the reviewer is and does
not stand for that one: remind the person who posts it.

When the PR is merged, the author is respected: the rules are in `oca-git`.

# A finding

Each finding has:

- the file and the line;
- the defect;
- the concrete scenario in which it fails, or the rule it breaks;
- a fix;
- the section it applies, written as `skill: section`, or *judgement* when it
  came from the merits pass;
- a mark: **blocking**, when the change must not be merged as it is, or
  **suggestion**.

A finding that rests on a rule that its file marks as *Recommended* (the OCA
guide does not write it down: `orm.md`, "Which module the code goes in",
the recommended part of `oca-web-guidelines`) is always a **suggestion**,
never **blocking**. Only a rule of the OCA guide, a security defect or a
failure scenario blocks.

A finding that rests on code outside the diff names the revision it was read
at. Flag; fix only what is unambiguous.

# Close the report

Draft the review as a Markdown comment that a person can paste in the pull
request: the thanks, the review type, the findings, and the proposed verdict.
End it with a **Skills read:** line that lists every section opened, so that
the person can see what was checked. Do not publish it, and do not merge: under the OCA AI policy the person who
posts it must have verified every point first.
