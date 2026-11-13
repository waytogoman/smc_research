"""Archive the autumn 2026 research inside smc_hedge and take bulk output out of the tree.

Dry run by default: it only reports. Nothing is deleted in either mode.

    python tools/cleanup_smc_hedge.py --repo C:/dev/projects/smc_hedge
    python tools/cleanup_smc_hedge.py --repo C:/dev/projects/smc_hedge --apply

What --apply does, in this order:
  1. Checks the repo is on master, has no uncommitted changes and matches origin/master.
  2. Tags the current state (pre-cleanup-2026-11-13) so everything can be recovered.
  3. Moves every file git does not track (run outputs, scratch, caches, zips) out of the
     folders listed below into a holding folder next to the repo, keeping relative paths.
  4. Moves the tracked research into archive/2026_autumn_research/ with `git mv`,
     keeping the same relative layout so links between pages and studies still work.
  5. Writes the replacement README.md, AGENTS.md, docs/README.md, .gitattributes and the
     archive README, makes five small wording changes in CONTRIBUTING.md and CLAUDE.md,
     repoints the six research links in data/README.md, and stages exactly those changes.

Before step 4 it also restores the committed line endings of any moving text file that
has Windows line endings on disk only, so that the commit is a pure move.

On the second machine, after `git pull`, run it with --bulk-only --apply: that only moves
the untracked leftovers out of the old folders and changes nothing in git.
It does not commit. Review with `git status`, run the tests, then commit and push.

If it stops during step 3, it can simply be run again. If it stops during step 4 or 5,
it refuses to run again; first undo with `git reset --hard pre-cleanup-2026-11-13` and
delete what is left of archive/2026_autumn_research. That reset restores every tracked
file, and the untracked content sits in the holding folder under the same relative paths.

See docs/smc_hedge_cleanup_plan.md in smc_research for the reasons behind each move.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

ARCHIVE = "archive/2026_autumn_research"
TAG = "pre-cleanup-2026-11-13"

# Tracked content: (current path, path under ARCHIVE). Layout is preserved on purpose.
TRACKED_MOVES = [
    ("research", "research"),
    ("docs/research", "docs/research"),
    ("docs/SESSION_SYNC.md", "docs/SESSION_SYNC.md"),
    ("backtest/runs/alpha_rankings", "backtest/runs/alpha_rankings"),
    ("archive/research", "archive/research"),
    ("tools/build_alpha_programme_map.py", "tools/build_alpha_programme_map.py"),
    ("tools/restore_research_evidence.py", "tools/restore_research_evidence.py"),
    ("tools/windows_process_supervisor.py", "tools/windows_process_supervisor.py"),
    ("tools/check_session_sync.py", "tools/check_session_sync.py"),
    ("tests/test_windows_process_supervisor.py", "tests/test_windows_process_supervisor.py"),
    # Used only by the supervisor test above, and imports the archived supervisor tool.
    ("tests/helpers/supervisor_fixture.py", "tests/helpers/supervisor_fixture.py"),
    ("AGENTS.md", "AGENTS_2026-11.md"),
]

# Folders removed at the end if no file is left in them.
EMPTY_AFTER = ["work", "~archived_code", "scripts", "research", "docs/research", "tests/helpers"]

# Folders whose untracked content leaves the tree. The last three are wholly untracked.
BULK_ROOTS = [
    "research", "docs/research", "backtest/runs/alpha_rankings", "archive/research",
    "work", "~archived_code", "scripts",
]

# Replacement files: (file in cleanup_files/, destination in the repo).
NEW_FILES = [
    ("smc_hedge_README.md", "README.md"),
    ("smc_hedge_AGENTS.md", "AGENTS.md"),
    ("smc_hedge_docs_README.md", "docs/README.md"),
    ("smc_hedge_gitattributes", ".gitattributes"),
    ("archive_README.md", f"{ARCHIVE}/README.md"),
]


# Small wording changes in files that otherwise stay: (file, old text, new text).
TEXT_EDITS = [
    ("CONTRIBUTING.md",
     "| `research/` | experiments, `yyyy-mm_slug/` folders; nothing here powers anything | code another module imports (graduate it first) |",
     "| *(research)* | lives in the separate `smc_research` repository, which imports this package | any research code, plan or study folder in this repository |"),
    ("CONTRIBUTING.md",
     "| `docs/` | `app/` (current code + serving schema) · `research/` · `backtest/` | history (that's `archive/`) |",
     "| `docs/` | `app/` (current code + serving schema) · `backtest/` | history (that's `archive/`), research pages |"),
    ("CONTRIBUTING.md",
     "| `archive/` | everything dead: the sealed v1 tree, retired code, old scripts | anything a live module imports |",
     "| `archive/` | everything dead: the sealed v1 tree, the autumn 2026 research, retired code, old scripts | anything a live module imports |"),
    ("CONTRIBUTING.md",
     "- Follow [the desktop/laptop session procedure](docs/SESSION_SYNC.md): fetch at\n"
     "  the start, then finish authorized changes with a reviewed commit, verified\n"
     "  push and current handoff. Report ignored evidence transfer separately.\n",
     "- Two machines: pull at the start, commit and push after each finished chunk.\n"),
    ("CLAUDE.md",
     "governance register) lives in `archive/v1/` — treat as read-only history,\nnot as instructions.\n",
     "governance register) lives in `archive/v1/` — treat as read-only history,\nnot as instructions. "
     "The same holds for the autumn 2026 research in\n`archive/2026_autumn_research/`. "
     "Research is now done in the separate\n`smc_research` repository.\n"),
]

# Whole-section replacement: (file, start marker, end marker, new body between them).
SECTION_EDITS = [
    ("CONTRIBUTING.md", "## 5. Research\n\n", "\n## 6. Data and inputs",
     "Research is done in the separate `smc_research` repository, which imports this\n"
     "package and never edits it. Promising code reaches `smc_hedge/` or `smc_backtest/`\n"
     "only through the §2/§3 flow, as a deliberate production change.\n\n"
     "The research done here between September and November 2026 is preserved,\n"
     "read-only, under `archive/2026_autumn_research/`. Its byte-exact `.gitattributes`\n"
     "rule is deliberate.\n"),
]


# Links in files that stay but point at pages that move: (file, old text, new text).
# Every occurrence is replaced. The data README still links to the September factor
# pages at docs/research/, where they have not been since the October reorganisation.
LINK_EDITS = [
    ("data/README.md", "](../docs/research/2026-09-10_",
     f"](../{ARCHIVE}/docs/research/factors_review/2026-09-10_"),
]


def crlf_only_on_disk(repo: Path, paths: list[str]) -> list[str]:
    """Tracked text files that git stores with LF but that have CRLF on disk.

    Git treats them as unchanged today. The archive is byte-exact (-text), so once
    moved they would show as modified. Restoring the committed bytes first keeps the
    commit a pure move."""
    existing = [p for p in paths if (repo / p).exists()]
    if not existing:
        return []
    hits = []
    for rec in git(repo, "ls-files", "--eol", "-z", "--", *existing).split("\0"):
        info, _, path = rec.partition("\t")
        f = info.split()
        if (len(f) >= 3 and f[0] == "i/lf" and f[1] in ("w/crlf", "w/mixed")
                and f[2].startswith("attr/text")):
            hits.append(path)
    return hits


def apply_text_edits(repo: Path) -> None:
    touched = set()
    for name, old, new in LINK_EDITS:
        path = repo / name
        text = path.read_bytes().decode("utf-8")
        count = text.count(old)
        if not count:
            print(f"  link text not found, edit {name} by hand: {old!r}")
            continue
        path.write_bytes(text.replace(old, new).encode("utf-8"))
        print(f"  repointed {count} links in {name}")
        touched.add(name)
    for name, old, new in TEXT_EDITS:
        path = repo / name
        text = path.read_bytes().decode("utf-8")
        crlf = "\r\n" in text
        body = text.replace("\r\n", "\n")
        if old not in body:
            print(f"  wording not found, edit {name} by hand: {old[:60]!r}")
            continue
        body = body.replace(old, new, 1)
        path.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))
        touched.add(name)
    for name, start, end, new in SECTION_EDITS:
        path = repo / name
        text = path.read_bytes().decode("utf-8")
        crlf = "\r\n" in text
        body = text.replace("\r\n", "\n")
        i = body.find(start)
        j = body.find(end, i + len(start)) if i >= 0 else -1
        if i < 0 or j < 0:
            print(f"  section not found, edit {name} by hand: {start.strip()!r}")
            continue
        body = body[: i + len(start)] + new + body[j:]
        path.write_bytes((body.replace("\n", "\r\n") if crlf else body).encode("utf-8"))
        touched.add(name)
    for name in sorted(touched):
        git(repo, "add", "--", name)


def git(repo: Path, *args: str, check: bool = True) -> str:
    out = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True,
                         encoding="utf-8", errors="replace")
    if check and out.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed:\n{out.stderr.strip()}")
    return out.stdout


def tree_size(path: Path) -> tuple[int, int]:
    """Number of files and total bytes under path. Unreadable entries are skipped."""
    if path.is_file():
        try:
            return 1, path.stat().st_size
        except OSError:
            return 1, 0
    files = size = 0
    stack = [str(path)]
    while stack:
        try:
            with os.scandir(stack.pop()) as it:
                for e in it:
                    try:
                        if e.is_dir(follow_symlinks=False):
                            stack.append(e.path)
                        else:
                            files += 1
                            size += e.stat(follow_symlinks=False).st_size
                    except OSError:
                        pass
        except OSError:
            pass
    return files, size


def human(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:,.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return f"{n} B"


def merge_move(src: Path, dst: Path) -> int:
    """Move src to dst. Folders that already exist are merged; files are never overwritten.
    Returns the number of items that could not be moved."""
    if not dst.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.move(str(src), str(dst))
        except OSError as exc:  # for example a file held open by another program
            print(f"  could not move {src}: {exc}")
            return 1
        return 0
    if src.is_dir() and dst.is_dir():
        failures = sum(merge_move(child, dst / child.name) for child in list(src.iterdir()))
        if not failures:
            try:
                src.rmdir()
            except OSError:
                pass
        return failures
    print(f"  left in place, already in the holding folder: {src}")
    return 1


def untracked_entries(repo: Path) -> list[str]:
    """Untracked and ignored entries under BULK_ROOTS; whole untracked folders as one entry."""
    roots = [r for r in BULK_ROOTS if (repo / r).exists()]
    if not roots:
        return []
    out = git(repo, "ls-files", "--others", "--directory", "-z", "--", *roots)
    return [p for p in out.split("\0") if p]


def preconditions(repo: Path, skip_remote: bool, bulk_only: bool = False) -> None:
    if not (repo / ".git").exists():
        sys.exit(f"{repo} is not a git repository")
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD").strip()
    if branch != "master":
        sys.exit(f"Expected branch master, found {branch}")
    dirty = [l for l in git(repo, "status", "--porcelain").splitlines() if not l.startswith("??")]
    if dirty:
        sys.exit("Uncommitted changes to tracked files. Commit or discard them first:\n" + "\n".join(dirty[:20]))
    if bulk_only:
        if not (repo / ARCHIVE).exists():
            sys.exit(f"--bulk-only is for a machine that has already pulled the cleanup commit, "
                     f"but {ARCHIVE} is not here. Run `git pull` first.")
        return
    if (repo / ARCHIVE).exists():
        sys.exit(f"{ARCHIVE} already exists. The cleanup looks done already. "
                 "On a second machine, use --bulk-only.")
    if not skip_remote:
        subprocess.run(["git", "-C", str(repo), "fetch", "--quiet"], capture_output=True)
        head = git(repo, "rev-parse", "HEAD").strip()
        remote = git(repo, "rev-parse", "origin/master", check=False).strip()
        if head != remote:
            sys.exit("Local master differs from origin/master. Pull or push first, "
                     "or pass --skip-remote-check.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", required=True, help="path to the smc_hedge working copy")
    ap.add_argument("--cold", help="holding folder for untracked content "
                                   "(default: <repo parent>/_cold/smc_hedge_2026_autumn)")
    ap.add_argument("--apply", action="store_true", help="make the changes (default is a dry run)")
    ap.add_argument("--no-sizes", action="store_true", help="skip measuring folder sizes (faster)")
    ap.add_argument("--skip-remote-check", action="store_true")
    ap.add_argument("--bulk-only", action="store_true",
                    help="second machine, after `git pull`: only move the untracked leftovers out")
    a = ap.parse_args()

    repo = Path(a.repo).resolve()
    cold = Path(a.cold).resolve() if a.cold else repo.parent / "_cold" / "smc_hedge_2026_autumn"
    templates = Path(__file__).resolve().parent / "cleanup_files"
    missing = [t for t, _ in NEW_FILES if not (templates / t).exists()]
    if missing:
        sys.exit(f"Missing template files in {templates}: {missing}")

    preconditions(repo, a.skip_remote_check, a.bulk_only)
    mode = "APPLY" if a.apply else "DRY RUN"
    print(f"== {mode} on {repo}\n")

    # ---- report -----------------------------------------------------------------
    print("Tracked content that moves to", ARCHIVE)
    for src, dst in ([] if a.bulk_only else TRACKED_MOVES):
        if not (repo / src).exists():
            print(f"  (absent) {src}")
            continue
        n = len([l for l in git(repo, "ls-files", "--", src).splitlines() if l])
        print(f"  {n:6d} tracked files   {src}  ->  {ARCHIVE}/{dst}")

    crlf = [] if a.bulk_only else crlf_only_on_disk(repo, [src for src, _ in TRACKED_MOVES])
    if crlf:
        print("\nFiles whose committed line endings are restored on disk before the move")
        for p in crlf:
            print("  ", p)

    bulk = untracked_entries(repo)
    print(f"\nUntracked content that leaves the tree for {cold}")
    by_root: dict[str, list[int]] = {}
    for p in bulk:
        root = next(r for r in sorted(BULK_ROOTS, key=len, reverse=True) if p == r or p.startswith(r + "/"))
        f, s = (0, 0) if a.no_sizes else tree_size(repo / p)
        acc = by_root.setdefault(root, [0, 0, 0])
        acc[0] += 1; acc[1] += f; acc[2] += s
    total = 0
    for root, (entries, files, size) in sorted(by_root.items()):
        total += size
        detail = "" if a.no_sizes else f"{files:9,d} files  {human(size):>12}  "
        print(f"  {detail}{entries:5d} entries   {root}")
    if not a.no_sizes:
        print(f"  total {human(total)}")
    if cold.exists() and any(cold.iterdir()):
        print(f"\nNote: {cold} already has content. Existing items are never overwritten.")
    same_drive = os.path.splitdrive(str(cold))[0].lower() == os.path.splitdrive(str(repo))[0].lower()
    if not same_drive:
        print("\nWarning: the holding folder is on another drive, so files will be copied, "
              "which is slow for large outputs.")

    if not a.apply:
        print("\nDry run only. Nothing was changed. Add --apply to proceed.")
        return

    # ---- apply ------------------------------------------------------------------
    if not a.bulk_only and TAG not in git(repo, "tag", "--list", TAG):
        git(repo, "tag", "-a", TAG, "-m", "State before archiving the autumn 2026 research")
        print(f"\nTagged current state as {TAG}")

    moved = skipped = 0
    for p in bulk:
        failures = merge_move(repo / p.rstrip("/"), cold / p.rstrip("/"))
        if failures:
            skipped += failures
        else:
            moved += 1
    print(f"Moved {moved} untracked entries to {cold}" + (f"; {skipped} skipped" if skipped else ""))
    if skipped:
        sys.exit("Some untracked entries could not be moved. Resolve them, then run again.")

    left = untracked_entries(repo)
    if left:
        sys.exit("Untracked content is still present, stopping before git mv:\n" + "\n".join(left[:20]))

    if a.bulk_only:
        for name in EMPTY_AFTER:
            d = repo / name
            if d.is_dir() and tree_size(d)[0] == 0:
                shutil.rmtree(d)
        print("Bulk-only run finished. Nothing in git was changed.")
        return

    if crlf:
        # `git checkout-index -f` skips files it believes are unchanged, so write the
        # committed bytes directly.
        for p in crlf:
            blob = subprocess.run(["git", "-C", str(repo), "cat-file", "blob", f":{p}"],
                                  capture_output=True)
            if blob.returncode != 0:
                sys.exit(f"Could not read the committed version of {p}, stopping before git mv.")
            (repo / p).write_bytes(blob.stdout)
        # Stages nothing, since the content is what is committed; it only refreshes
        # git's record of the files so they are not reported as modified after the move.
        git(repo, "add", "--", *crlf)
        still = crlf_only_on_disk(repo, crlf)
        if still:
            sys.exit("Could not restore committed line endings, stopping before git mv:\n"
                     + "\n".join(still))
        print(f"Restored committed line endings on disk in {len(crlf)} files")

    for src, dst in TRACKED_MOVES:
        if not (repo / src).exists():
            continue
        target = repo / ARCHIVE / dst
        target.parent.mkdir(parents=True, exist_ok=True)
        git(repo, "mv", src, f"{ARCHIVE}/{dst}")
    print("Moved tracked research into", ARCHIVE)

    for name in EMPTY_AFTER:
        d = repo / name
        if d.is_dir() and tree_size(d)[0] == 0:
            shutil.rmtree(d)

    for tmpl, dest in NEW_FILES:
        target = repo / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((templates / tmpl).read_bytes())
        git(repo, "add", "--", dest)
    print("Wrote replacement README.md, AGENTS.md, docs/README.md, .gitattributes and the archive README")
    apply_text_edits(repo)

    stray = [l for l in git(repo, "ls-files", "--others", "--exclude-standard").splitlines() if l]
    if stray:
        print("\nWarning: untracked files that are not ignored remain. Do not `git add -A`:")
        for l in stray[:20]:
            print("  ", l)
    changed = [l for l in git(repo, "status", "--porcelain").splitlines() if l]
    renames = sum(1 for l in changed if l.startswith("R"))
    print(f"\nStaged: {renames} renames, {len(changed) - renames} other changes.")
    unstaged = [l for l in changed if not l.startswith("??") and l[1] != " "]
    if unstaged:
        print("\nWarning: files differ on disk from what is staged. Look at these before committing:")
        for l in unstaged[:20]:
            print("  ", l)
    print("Next: review `git status`, run `python -m pytest -q`, then\n"
          '  git commit -m "Archive autumn 2026 research; keep production tree only"\n'
          "  git push --follow-tags")


if __name__ == "__main__":
    main()
