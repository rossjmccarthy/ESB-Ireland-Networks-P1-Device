# Making a release

Releases are what the web flasher installs and what adopted devices are
pinned to, so `main` can change freely in between.

## Version numbers

`vYYYY.MM.N`: the year and month of the release, then a number starting at 0
for the first release that month. For example `v2026.11.0`, then
`v2026.11.1`.

## Steps

1. Make sure the latest **Check firmware builds** run on `main` passed.
2. Tag the commit and push the tag:

   ```bash
   git tag -a v2026.11.1 -m "v2026.11.1"
   ```

   ```bash
   git push origin v2026.11.1
   ```

3. The **Release** workflow builds every board with the version set to the
   tag and adopted devices pinned to it, then creates a GitHub Release with the
   firmware and manifests attached and notes generated from the merged pull
   requests. Edit the notes if anything needs explaining, such as a change
   users must make by hand.
4. When the Release workflow succeeds, **Publish web flasher** puts that
   release on the flasher page. Check the page shows the new version.

## If something goes wrong

- **A build fails:** fix it on `main`, delete the tag
  (`git push origin :refs/tags/v2026.11.1` and `git tag -d v2026.11.1`), and
  tag again.
- **A bad release is already out:** release a fixed version rather than
  deleting the release. Devices pinned to the bad tag keep working with it
  until their owners move them on, and deleting a tag breaks their next
  install.
- **The flasher shows the wrong version:** run **Publish web flasher** by hand
  from the Actions tab. It always uses the latest release.

## Rules of thumb

- Don't rename sensors in `esphome/esb-p1-reader.yaml`. ESPHome derives entity
  ids from the names, so a rename gives every user new entities and splits
  their history.
- Say in the release notes when a change needs action from users, for example
  a new secret or a changed pin.
