#!/usr/bin/env bash

_stackd_completions()
{
  local cmds=()
  cmds+=("shellenv")
  cmds+=("infos")
  cmds+=("getname")
  cmds+=("deploy")
  cmds+=("up")
  cmds+=("rm")
  cmds+=("remove")
  cmds+=("ls")
  cmds+=("ps")
  cmds+=("compo")
  cmds+=("compo-freeze")
  cmds+=("pull")
  cmds+=("getimagelist")
  cmds+=("printenv")
  cmds+=("deploy-with-portainer")
  cmds+=("rm-with-portainer")
  cmds+=("config-prune")
  cmds+=("logs")
  cmds+=("build")
  cmds+=("bundle")
  cmds+=("vc")
  cmds+=("clear")
  cmds+=("before-clear")
  cmds+=("after-clear")
  cmds+=("reset")
  cmdsStr=$( IFS=$'\n'; echo "${cmds[*]}" )

  local cmd="${COMP_WORDS[1]}"
  local cur_word="${COMP_WORDS[COMP_CWORD]}"
  local prev_word="${COMP_WORDS[COMP_CWORD-1]}"
  local words_len=${#COMP_WORDS[@]}

  COMPREPLY=()

  if [ "$cmd" = "logs" ]; then

    if [ ! $words_len -eq 3 ]; then
      return
    fi

    local stackname=$("${COMP_WORDS[0]}" getname)
    local stackname_len=${#stackname}
    local services=$(docker service ls \
      --filter label=com.docker.stack.namespace=$stackname \
      --format "{{.Name}}" \
    )
    local service
    local serviceShortnames=()

    while IFS= read -r service
    do
      serviceShortnames+=( "${service:$((stackname_len+1))}" )
    done < <(printf '%s\n' "$services")

    serviceShortnamesStr=$( IFS=$'\n'; echo "${serviceShortnames[*]}" )

    COMPREPLY=( $( compgen -W '$serviceShortnamesStr' ${COMP_WORDS[2]} ) )


  else

    if [ ! $words_len -eq 2 ]; then
      return
    fi
    COMPREPLY=( $( compgen -W '$cmdsStr' $cmd ) )
  fi
}

complete -F _stackd_completions stackd