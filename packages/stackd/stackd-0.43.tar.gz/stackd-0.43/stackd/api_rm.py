import sys
from .run_shell import run_shell

def api_rm(env_vars, args=[]):

  # process = run_shell(['docker','stack','rm',env_vars['STACKD_STACK_NAME'],args])

  # in future
  # process = run_shell(['docker','stack','rm','--detach=false',env_vars['STACKD_STACK_NAME'],args])

  process = run_shell(['docker-stack-rm',env_vars['STACKD_STACK_NAME'],args])

  if(process.returncode != 0):
      sys.exit(process.returncode)