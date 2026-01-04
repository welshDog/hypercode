# HyperCode Governance & Repository Rules 🛡️

This document outlines the governance models, branch protection rules, and security policies for the HyperCode project. As a neurodivergent-first, open-source project, we prioritize stability, clarity, and security.

## 1. Branch & Tag Rulesets 🧱

To ensure the integrity of our code and history, the following rules apply to the `main` branch and all release tags (`v*`).

### Main Branch Protection
The `main` branch is the source of truth. Direct pushes are **blocked**.

- **Require Pull Request Reviews**: All changes must be submitted via Pull Request (PR) and require at least **1 review** from a code owner or maintainer.
- **Block Force Pushes**: History rewriting (`git push --force`) is strictly forbidden on `main` to preserve the immutable history of the project.
- **Block Deletions**: The `main` branch cannot be deleted.
- **Require Status Checks**: All CI/CD pipelines (tests, linters, builds) must pass before merging.
- **Require Signed Commits**: All commits must be cryptographically signed (GPG/SSH) to verify authorship.

### Tag Protection
Release tags (e.g., `v0.1.0`) are immutable. Once published, they cannot be deleted or moved.

## 2. Push Rulesets 🛑

We enforce strict content filtering to prevent sensitive data leaks and repository bloat.

- **Block Secret Files**: Commits containing `.env`, `.pem`, `.key`, or other secret files are rejected automatically.
- **Block Large Files**: Files larger than **100MB** are blocked (use Git LFS if necessary).
- **Block Sensitive Paths**: Direct commits to `.github/workflows/` are restricted to maintainers.

## 3. Contribution Workflow 🔄

1.  **Fork & Branch**: Create a feature branch (`feat/your-feature`) from `main`.
2.  **Commit**: Write clear, atomic commits. Sign your commits!
3.  **Pull Request**: Open a PR to `main`.
4.  **Review**: Wait for automated checks and human review.
5.  **Merge**: Once approved, your code will be squashed and merged.

## 4. Why These Rules? 🧠

- **Neurodivergent-Friendly**: Clear rules reduce anxiety about "breaking things." You literally *cannot* break `main` by accident.
- **Security**: Prevents supply-chain attacks and secret leaks.
- **Quality**: Ensures every line of code is tested and reviewed.

---
*These rules are enforced via GitHub Repository Settings > Rulesets.*
