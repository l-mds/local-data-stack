# GitHub: push fixes and metrics (local guidance)

This page explains how to fix push permission errors and how to view common GitHub repo metrics.

## Fixing `403` when pushing (common options)

1) Push to your fork (recommended if you don't have push access to the upstream repo)

```powershell
# create a fork on github.com (web UI), then in your local repo:
git remote add my-fork https://github.com/<your-github-username>/local-data-stack.git
git fetch my-fork
git push -u my-fork cleanup/remove-generated
```

2) Push via SSH to the original repo (requires an SSH key added to GitHub and write permissions)

```powershell
# test SSH auth
ssh -T git@github.com
# push using SSH origin
git push -u origin cleanup/remove-generated
```

3) Use a Personal Access Token (HTTPS) if required

```powershell
# set origin to HTTPS to push with PAT
git remote set-url origin https://github.com/<your-github-username>/local-data-stack.git
git push -u origin cleanup/remove-generated
# When prompted, use your username and PAT (with repo scope)
```

## Useful `gh` commands (install GitHub CLI first)

```powershell
# install (Windows)
winget install --id GitHub.cli -e
gh auth login

# fork the repo and add remote automatically
gh repo fork l-mds/local-data-stack --remote=true

# view actions runs
gh api repos/l-mds/local-data-stack/actions/runs --paginate
```

## GitHub web UI (links in repo)
- Pulse: `Repo -> Insights -> Pulse`
- Contributors: `Repo -> Insights -> Contributors`
- Community: `Repo -> Community`
- Code frequency: `Repo -> Insights -> Code frequency`
- Dependency graph: `Repo -> Insights -> Dependency graph`
- Network: `Repo -> Insights -> Network`
- Actions: `Repo -> Actions` (workflow runs and logs)

## Want me to do this for you?
- I can attempt to add your fork remote and push the `cleanup/remove-generated` branch (I will fail if the fork doesn't exist or you have no auth). Tell me the preferred option: `fork` / `ssh` / `https-with-pat`.
