'''
Postfix interpreter

Austin V
'''

import commands

## Globals
valid_commands = [ 'sub','add','mul','div','rem', 'lt','gt',
                   'eq','pop','swap', 'sel', 'nget','exec']
parens = [')','(']
interactive = True
failure = [False, 0]

### Helpers
def is_int(string):
    '''
    string -> boolean
    '''
    try: 
        isinstance(int(string), int)
        return True
    except (ValueError, TypeError):
        return False


def convert_int(string):
    '''
    if the string can be converted to an integer, convert it
    string -> string || int
    '''
    if is_int(string):
        return int(string)
    else:
        return string


### Logic
def check_program_syntax(program):
    '''
    Takes a postfix program as a string, verifies that it has the correct syntax
    and returns a boolean representing whether it's valid. If it is valid, it also 
    returns an int which is the number of required args

    string -> boolean, int
    '''

    # Separate parens into their own tokens by adding appropriate spaces
    token_list = program.replace('(', '( ').replace(')', ' )').split()

    # check for header, argnum, and end paren
    if (token_list[0] != '(' or
       token_list[1] != 'postfix' or
       not is_int(token_list[2]) or
       int(token_list[2]) < 0 or
       token_list[-1] != ')'):

        print('syntax error: bad header')
        return failure
    
    # check if all tokens are valid 
    for token in token_list[2:]:
        if not token in valid_commands and not token in parens and not is_int(token):
            print('syntax error: bad command', token)
            return failure

    # check for balanced parens, ignoring first and last
    depth = 0
    for token in token_list[2:-1]:
        if token == '(': depth += 1
        elif token == ')': depth -= 1

        if depth < 0:
            return failure

    if depth != 0:
        return failure

    # success
    return True, int(token_list[2])


def check_arg_syntax(args):
    '''
    Given a string, verifies that every word in the string can be converted to an
    integer, and returns the number of arguments encountered

    string -> boolean
    '''
    arg_list = args.split()

    for arg in arg_list:
        if not is_int(arg):
            print('syntax error: bad argument: ', arg)
            return failure

    return True, len(arg_list)


def tokenize(token_list, index):
    '''
    Clumps elements of nested parens together

    list of strings -> list of strings
    '''
    out_list = []
    index += 1

    while token_list[index] != ')':
        # recursive step
        if token_list[index] == '(':
            new_list, new_index = tokenize(token_list, index)
            out_list.append(new_list)
            index = new_index

        else:
            out_list.append(token_list[index])
        index += 1

    return out_list, index


def run_program(program, arguments):
    '''
    string, string -> string
    '''
    
    prog = program.replace('(', '( ').replace(')', ' )').split()
    prog = list(map(convert_int, prog))
    prog, index = tokenize(prog, 0)
    
    # put args on stack
    args = list(map(int, arguments.split()))
    args.reverse()

    stack = []
    if args:
        for arg in args:
            stack.append(arg)

    # build the command stack
    command_stack = prog[2:]
    command_stack.reverse()

    command_dict = {
        'add' : commands.pf_add,
        'sub' : commands.pf_sub,
        'mul' : commands.pf_mul,
        'div' : commands.pf_div,
        'rem' : commands.pf_rem,
        'lt'  : commands.pf_lt,
        'gt'  : commands.pf_gt,
        'eq'  : commands.pf_eq,
        'pop' : commands.pf_pop,
        'swap': commands.pf_swap,
        'sel' : commands.pf_sel,
        'nget': commands.pf_nget,
        'exec': commands.pf_exec
        }

    while command_stack:
        # print out stacks for trace
        command_stack.reverse()
        print('stack   ', stack)
        print('commands', command_stack)
        print('')
        command_stack.reverse()
        
        token = command_stack.pop()
        
        # push integer onto the stack
        if is_int(token):
            print('pushing ', token)
            stack.append(convert_int(token))

        # execute command, pass command_stack for exec
        elif token in valid_commands:
            print('running ', token)
            stack, command_stack = command_dict[token](stack, command_stack)

            # stack may contain an error message if there was a problem
            if isinstance(stack, str):
                return stack
        
        # push command sequence onto the stack
        else:
            print('pushing ', token)
            stack.append(token)

        if not stack:
            return 'runtime error: stack became empty'

    return stack.pop()


# Main
def main():
    '''
    Gets user input, checks syntax, and runs the program

    none -> none
    '''
    print('POSTFIX INTERPRETER v0.1')

    if interactive:
        while True:
            # get program
            print
            print('------------------------')
            program = input('Type a postfix program: ')
            if not program: break
            valid_program, num_req_args = check_program_syntax(program)

            # get arguments
            if num_req_args > 0:
                args = input('Type the arguments: ')
                valid_args, num_prov_args = check_arg_syntax(args)

                if num_prov_args != num_req_args:
                    print('syntax error: incorrect number of arguments')

            else:
                args = ''
                valid_args = True

            # run
            if valid_program and valid_args:
                output = run_program(program, args)
                print('output  ', output)

    else:
        prog1 = '(postfix 0 1 2 add 5 add)'
        prog2 = '(postfix 0 5 0 div)'
        prog3 = '(postfix 0 3 4 add 5 mul 6 sub 7 div)'
        prog4 = '(postfix 0 (3 4) 4 add 5 mul 6 sub 7 div)'
        prog5 = '(postfix 4 lt (add) (mul) sel exec)'
        prog6 = '(postfix 1 1 nget 0 lt (0 swap sub) () sel exec)'
        prog7 = '(postfix 1 ((3 nget swap exec) (2 mul swap exec) swap) (5 sub) swap exec exec)'
        print(prog6)
        output = run_program(prog7, '-7')
        print(output)

    return


if __name__ == '__main__':
    # python 2.x uses raw_input(), 3.x input()
    try:
        import __builtin__
        input = getattr(__builtin__, 'raw_input')
    except (ImportError, AttributeError):
         pass

    main()
