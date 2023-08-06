Stupid command to download YouTube's `watch later` videos.

# Release a new version

TODO: make it a script
```
# git diff must be empty
git tag -l
git tag v0.x.0
bash scripts/build.sh
bash scripts/publish.sh
git push origin --tags
```
