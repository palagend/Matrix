#!/bin/bash

echo -e "\033[0;32mDeploying updates to GitHub...\033[0m"
set -e
if [[ ! -e public/.git ]]; then
    rm -rf public && \
    git clone github:palagend/palagend.github.io public
fi
[[ ! -d public/.git ]] && exit 1

# Build the project.
hugo -t nagisa # if using a theme, replace with `hugo -t <YOURTHEME>`

# Go To Public folder
cd public
# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site `date`"
if [ $# -eq 1 ]
  then msg="$1"
fi
git commit --amend -m "$msg"

# Push source and build repos.
git push origin master -f

# Come Back up to the Project Root
cd ..
