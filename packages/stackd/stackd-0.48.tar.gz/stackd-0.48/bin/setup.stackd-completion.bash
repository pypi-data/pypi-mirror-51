#!/bin/sh
if which bash>/dev/null && [ ! -f /etc/bash_completion.d/stackd ] && which stackd-completion.bash>/dev/null; then
  read -p "Install bash completion for stackd (Y/n)?" CONT
  if [ "$CONT" != "n" ]; then
    sudo ln -s -f /etc/bash_completion.d/stackd $(which stackd-completion.bash)
  fi
fi