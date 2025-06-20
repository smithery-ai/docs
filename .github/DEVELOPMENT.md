# Development Workflow Guidelines

## Branch Management

### Current State
- Cleaned up from 31 branches to 18 branches
- Removed obsolete experimental branches
- Maintained essential remote tracking

### Branch Naming Convention
```
feature/<feature-name>
fix/<bug-description>
docs/<documentation-update>
refactor/<refactor-scope>
```

### Workflow Rules

1. **Create branches from clean main**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/your-feature-name
   ```

2. **Short-lived branches**: Complete features in 1-3 days max

3. **Regular cleanup**: Delete merged branches immediately
   ```bash
   git branch -d feature-branch-name
   git push origin --delete feature-branch-name
   ```

4. **No orphaned work**: All significant changes must be committed

5. **Descriptive commits**: Use conventional commit format
   ```
   feat: add new feature
   fix: resolve bug description
   docs: update documentation
   refactor: improve code structure
   ```

## Lost Work Prevention

### What Happened
- The 165-line improved FastMCP tutorial was never committed
- All branches contained the longer 734-line version
- Good work was lost due to not committing incremental improvements

### Prevention Strategies

1. **Commit early, commit often**: Save work every 15-30 minutes
2. **Use draft PRs**: Push work-in-progress to remote branches
3. **Tag important versions**: 
   ```bash
   git tag -a v1.0-short-tutorial -m "165-line improved tutorial"
   ```
4. **Document in commit messages**: Be specific about improvements

## Current Branches

### Local Branches
- `main` - Primary development branch

### Remote Branches
- `origin/main` - Our fork's main branch  
- `origin/auto-troubleshooting-updates` - Active PR branch
- `upstream/main` - Original Smithery docs main
- `container-use/*` - Container environment branches (keep for reference)

## Best Practices Going Forward

1. **One feature per branch**
2. **Test before merging**
3. **Update documentation with changes**
4. **Use squash merges for clean history**
5. **Delete merged branches immediately**

## Recovery Process

When work is lost:
1. Check git stash: `git stash list`
2. Check recent commits: `git log --oneline -20`
3. Check editor recovery files: `.swp`, `~`, `.bak`
4. Check system trash if files were deleted
5. Recreate from memory (last resort)

## Current Status: DISCIPLINED ✅

Reduced branches: 31 → 18
Cleaned up obsolete branches: ✅
Established workflow guidelines: ✅
Prevention strategies documented: ✅