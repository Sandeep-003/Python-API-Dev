# Git Cheatsheet (Python-API-Dev)

Quick reference for everyday Git tasks when working on this project.

---

## 1. Global Setup (once per machine)

```powershell
git config --global user.name "Your Name"        # Set your display name
git config --global user.email "you@example.com" # Set your email
git config --global core.autocrlf true           # Good default on Windows
```

---

## 2. Repository Basics

```powershell
git status          # See changed, staged, and untracked files
git init            # Initialize a new repo in current folder
git clone <URL>     # Download an existing repo from remote
```

---

## 3. Remotes (origin)

```powershell
git remote -v
# List remotes (see 'origin' URLs)

git remote add origin https://github.com/<USER>/<REPO>.git
# Link local repo with remote named 'origin'

git remote set-url origin https://github.com/<USER>/<REPO>.git
# Change the URL for 'origin' (e.g., moved repo / HTTPS->SSH)
```

---

## 4. Staging and Committing

```powershell
git add .                           # Stage ALL modified & new files
git add path/to/file.py             # Stage a specific file
git commit -m "Describe the change" # Save staged changes as a commit
git commit -am "Msg"                # Stage + commit only tracked files
```

---

## 5. Sync with Remote (pull / push)

```powershell
git pull                 # Fetch + merge remote into current branch
git pull origin master   # Explicitly pull from origin/master
git pull --rebase        # Keep history linear (advanced, but useful)
```

```powershell
git push                  # Push current branch to its configured remote
git push -u origin master
# First push: set 'origin/master' as upstream for local master

git push origin <branch-name>
# Push a specific branch
```

---

## 6. Branching (create, switch, list)

```powershell
git branch                      # List local branches
git branch -a                   # List local + remote branches

git checkout -b feature/auth-api
# Create and switch to new branch from current commit

git checkout feature/auth-api   # Switch to existing branch

git branch -d feature/auth-api
# Delete local branch (already merged)

git push origin --delete feature/auth-api
# Delete remote branch
```

---

## 7. Keep Branch Up to Date with master

```powershell
git checkout feature/auth-api
git pull origin master
# Merge latest master into your feature branch

# Or (cleaner history, more advanced):
git fetch origin
git rebase origin/master
# Replay your commits on top of latest master
```

---

## 8. Merging Branches

```powershell
git checkout master
git pull origin master           # Update local master
git merge feature/auth-api       # Merge feature into master
git push origin master           # Push updated master
```

---

## 9. Resolving Merge Conflicts (local)

```powershell
git status
# See which files have conflicts

# 1. Open conflicted files -> resolve markers <<<<<<<, =======, >>>>>>>
# 2. Keep right content, remove markers, save file.

git add <file1> <file2>          # Mark conflicts resolved
git commit                       # Finish merge commit
git push                         # Push resolved merge
```

If you were rebasing and hit conflicts:

```powershell
git add <file1>
git rebase --continue            # Continue rebase after fixing conflicts
git rebase --abort               # Abort rebase if things go wrong
```

---

## 10. Viewing History & Diffs

```powershell
git log --oneline --graph --all
# Compact, graphical commit history

git log -p
# History with patches (line changes)

git diff
# Show unstaged changes

git diff --staged
# Show staged changes (that will be committed)
```

---

## 11. Undo & Safety Nets

```powershell
git restore path/to/file.py
# Discard local changes in a file (not staged yet)

git restore --staged path/to/file.py
# Unstage a file (keep its changes)

git reset --soft HEAD~1
# Undo last commit, keep changes staged

git reset --hard HEAD~1
# WARNING: Drop last commit AND its changes

git reflog
# Show where HEAD has been (helps recover lost commits)
```

---

## 12. Stashing WIP (work in progress)

```powershell
git stash
# Save uncommitted changes and clean working tree

git stash list
# View saved stashes

git stash apply
# Reapply the most recent stash (keeps stash entry)

git stash pop
# Reapply and remove from stash list
```

---

## 13. Everyday "Hassle‑Free" Flow Example

```powershell
# 1. Update main branch
git checkout master
git pull

# 2. Create feature branch
git checkout -b feature/some-change

# 3. Work, then commit
git status
git add .
git commit -m "Implement some change"

# 4. Push branch & open PR
git push -u origin feature/some-change

# 5. After PR merged, update and clean up
git checkout master
git pull
git branch -d feature/some-change
git push origin --delete feature/some-change
```

Use this file as a quick reference while working on this repo. Add or adjust commands as you discover a personal workflow you like.