#!/usr/bin/env bash
set -e

function version_ge() { test "$(echo "$@" | tr " " "\n" | sort -rV | head -n 1)" == "$1"; }

GIT_REMOTE="git@github.com:gauravchak/sports_predictions.git"
echo $GIT_REMOTE
# Find the current version from __version__.py and create different version tags
version="$(awk -F "=" '/__version__/ {print $2}' __version__.py | tr -d ' ' | tr -d "'" )"
a=( ${version//./ } )
major_version_tag="v${a[0]}"
minor_version_tag="v${a[0]}.${a[1]}"
patch_version_tag="v${a[0]}.${a[1]}.${a[2]}"

# Get remote tags from GIT_REMOTE and find the latest minor and patch version tags corresponding to this version
remote_tags="$(git ls-remote $GIT_REMOTE | awk '{print $2}' | cut -d '/' -f 3 | cut -d '^' -f 1  | sort -b -t . -k 1,1nr -k 2,2nr -k 3,3r -k 4,4r -k 5,5r | uniq) "
latest_minor="$(echo "$remote_tags" | grep $major_version_tag | sort -V -r | head -n 1 | awk '{split($0,a,/\./); print a[1]"."a[2]}')"
echo $latest_minor
latest_patch="$(echo "$remote_tags" | grep $minor_version_tag | sort -V -r | head -n 1)"
echo $latest_patch

# Make git tags.

# We always push the latest tag.
git tag -f -a "latest" -m "Latest tag"
git push $GIT_REMOTE -f "latest"

# We always push the patch tag.
if version_ge $patch_version_tag $latest_patch; then
    git tag -f -a "$patch_version_tag" -m "Version $patch_version_tag"
    git push $GIT_REMOTE -f $patch_version_tag
fi

# We make and push minor version tag only if our patch version is greater than or equal to that on remote.
if version_ge $patch_version_tag $latest_patch; then
    git tag -f -a "$minor_version_tag" -m "Version $minor_version_tag"
    git push $GIT_REMOTE -f $minor_version_tag
fi

# We make and push major version tag only if our minor version is greater than or equal to than on remote.
if version_ge $minor_version_tag $latest_minor; then
    git tag -f -a "$major_version_tag" -m "Version $major_version_tag"
    git push $GIT_REMOTE -f $major_version_tag
fi
