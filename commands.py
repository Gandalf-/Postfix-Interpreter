'''
commands.py
Implementation for each postfix command

Austin V
'''

### globals
bad_args = 'not enough args'
bad_int = 'arg not int'
bad_zero = 'illegal operation by zero'

### Helpers
def not_int(elem):
  '''
  unknown -> boolean
  '''
  if isinstance(elem, int):
    return False
  else:
    return True

def get_two_args(stack):
  '''
  list -> int, int || bool, bool
  '''
  try:
    v1 = stack.pop()
    v2 = stack.pop()
    return v1, v2

  except (IndexError, TypeError):
    return False, False

def pf_error(command, message):
  '''
  string, string -> string, boolean
  '''
  return ['runtime error: '+command+': '+message, False]


### Commands
def pf_add(stack, command_stack):
  '''
  pops v1,v2, pushes v2 + v1 on stack

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)

  if type(v1) == bool:
    return pf_error('add',bad_args)
  if not_int(v1) or not_int(v2):
    return pf_error('add',bad_int)

  stack.append(v2 + v1)
  return stack, command_stack


def pf_sub(stack, command_stack):
  '''
  pops v1,v2, pushes v2 - v1 on stack

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)

  if type(v1) == bool:
    return pf_error('sub',bad_args)
  if not_int(v1) or not_int(v2):
    return pf_error('sub',bad_int)

  stack.append(v2 - v1)
  return stack, command_stack


def pf_mul(stack, command_stack):
  '''
  pops v1,v2, pushes v2 * v1 on stack

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)

  if type(v1) == bool:
    return pf_error('mul',bad_args)
  if not_int(v1) or not_int(v2):
    return pf_error('mul', bad_int)

  stack.append(v2 * v1)
  return stack, command_stack


def pf_div(stack, command_stack):
  '''
  pops v1,v2, pushes v2 / v1 on stack

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)

  if type(v1) == bool:
    return pf_error('div',bad_args)
  if not_int(v1) or not_int(v2):
    return pf_error('div',bad_int)
  if v1 == 0: 
    return pf_error('div',bad_zero)

  stack.append(v2 / v1)
  return stack, command_stack


def pf_rem(stack, command_stack):
  '''
  pops v1,v2, pushes v2 * v1 on stack

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)
  
  if type(v1) == bool:
    return pf_error('rem', bad_args)
  if not_int(v1) or not_int(v2):
    return pf_error('rem', bad_int)
  if v1 == 0:
    return pf_error('rem', bad_zero)

  stack.append(v2 % v1)
  return stack, command_stack


def pf_lt(stack, command_stack):
  '''
  pops v1,v2, pushes result of 'less than' comparison

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)

  if type(v1) == bool:
    return pf_error('lt', bad_args)
  if not_int(v1) or not_int(v2):
    return pf_error('lt', bad_int)

  if v2 < v1:
    stack.append(1)
  else:
    stack.append(0)
  return stack, command_stack


def pf_gt(stack, command_stack):
  '''
  pops v1,v2, pushes result of 'greater than' comparison

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)

  if type(v1) == bool:
    return pf_error('gt', bad_args)
  if not_int(v1) or not_int(v2):
    return pf_error('gt', not_int)

  if v2 > v1:
    stack.append(1)
  else:
    stack.append(0)
  return stack, command_stack


def pf_eq(stack, command_stack):
  '''
  pops v1,v2, pushes result of 'equal to' comparison

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)

  if type(v1) == bool:
    return pf_error('eq', bad_args)
  if not_int(v1) or not_int(v2):
    return pf_error('eq', not_int)

  if v2 == v1:
    stack.append(1)
  else:
    stack.append(0)
  return stack, command_stack


def pf_pop(stack, command_stack):
  '''
  pops v1

  list, list -> list, list
  '''
  try:
    stack.pop()
    return stack, command_stack

  except IndexError:
    return pf_error('pop','stack empty')


def pf_swap(stack, command_stack):
  '''
  pops v1,v2, pushes v1, v2 on the stack.

  list, list -> list, list
  '''
  v1,v2 = get_two_args(stack)

  if type(v1) == bool:
    return pf_error('swap', bad_args)

  stack.append(v1)
  stack.append(v2)
  return stack, command_stack


def pf_sel(stack, command_stack):
  '''
  pops v1,v2,v3. if v3: push v1 else: push v2

  list, list -> list, list
  '''
  try:
    v1 = stack.pop()
    v2 = stack.pop()
    v3 = stack.pop()

  except IndexError:
    return pf_error('sel', bad_args)
  if not_int(v3):
    return pf_error('sel', 'v3 must be int')

  if v3 == 0:
    stack.append(v1)
  else:
    stack.append(v2)
  return stack, command_stack


def pf_nget(stack, command_stack):
  '''
  pops v1, pushes the stack element at that position on the stack

  list, list -> list, list
  '''
  try:
    v1 = stack.pop()

  except IndexError:
    return pf_error('nget', bad_args)
  if not_int(v1):
    return pf_error('nget', bad_int)

  try:
    stack.append(stack[len(stack) - v1])
  except IndexError:
    return pf_error('nget', 'bad index')

  return stack, command_stack


def pf_exec(stack, command_stack):
  '''
  pops v1, prepends it to the command stack

  list, list -> list, list
  '''
  try:
    v1 = stack.pop()

    if type(v1) != list:
      return pf_error('exec', 'arg is not executable sequence')

    v1.reverse()
    map(command_stack.append, v1)

    return stack, command_stack

  except IndexError:
    return pf_error('exec', bad_args)
