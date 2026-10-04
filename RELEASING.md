# Release Process

Every release is a governed release event:

1. Confirm scope, target version, lifecycle phase, and working-tree cleanliness.
2. Update `VERSION.md`, `CHANGELOG.md`, and `README.md` as applicable.
3. Validate the exact release contents and preserve the evidence.
4. Promote the release branch into `main` through an explicit merge.
5. Create an annotated tag matching the version exactly.
6. Push the authoritative branch and tag to GitHub.
7. Publish a GitHub release when authorized and applicable.
8. Verify the tagged commit, documentation, and clean working tree.

A release is not complete merely because a branch or tag exists. The remote repository must reflect the final authoritative state.

