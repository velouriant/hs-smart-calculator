from re import findall


variables = {}


class VariableException(Exception):
    pass


def calculate(form):
    try:
        postfixed_form = postfix(form)
    except Exception:
        return "Invalid expression"
    result = []
    for x in postfixed_form:
        if x not in ["*", "/", "+", "-"]:
            try:
                result.append(make_num(x))
            except VariableException:
                return "Unknown variable"
            except Exception:
                return "Invalid expression"
        else:
            try:
                a = result.pop()
                b = result.pop()
                if x == "*":
                    result.append(b * a)
                elif x == "/":
                    result.append(b / a)
                elif x == "+":
                    result.append(b + a)
                elif x == "-":
                    result.append(b - a)
            except Exception:
                return "Invalid expression"
    if len(result) > 1:
        return "Invalid expression"
    else:
        return int(result[0])


def make_num(num):
    try:
        return int(num)
    except ValueError:
        if num in variables:
            return variables[num]
        elif num in ["(", ")", "*", "/", "+", "-"]:
            raise Exception
        else:
            raise VariableException


def interp_sign(sign):
    if sign[0] == "+":
        return "+"
    elif sign[0] == "-" and len(sign) % 2 == 0:
        return "+"
    elif sign[0] == "-" and len(sign) % 2 == 1:
        return "-"


def parse(text_input):
    pattern = r"\d+|[\(\)\*/]|\++|-+|[a-zA-Z]+"
    formula_list = findall(pattern, text_input)
    for index, x in enumerate(formula_list):
        if x[0] in ["+", "-"] and len(x) > 1:
            formula_list[index] = interp_sign(x)
        if x in variables:
            formula_list[index] = variables[x]
    return formula_list


def assign(variable, form):
    if not variable.isalpha():
        print("Invalid identifier")
        return
    else:
        num = calculate(form)
        if isinstance(num, int):
            variables[variable] = num
            return
        else:
            print("Invalid assignment")
            return


def postfix(formula_list):
    result = []
    operator_stack = []
    if formula_list[0] == "-":
        formula_list[1] = make_num(formula_list[1])
        formula_list[1] *= -1
        del formula_list[0]
    for x in formula_list:
        if x not in ["(", ")", "*", "/", "+", "-"]:
            result.append(x)
        else:
            if operator_stack == [] or operator_stack[-1] == ["("]:
                operator_stack.append(x)
            elif x in ["*", "/"] and operator_stack[-1] in ["+", "-"]:
                operator_stack.append(x)
            elif x in ["*", "/"]:
                while len(operator_stack) > 0 and \
                        operator_stack[-1] not in ["+", "-", "("]:
                    result.append(operator_stack.pop())
                operator_stack.append(x)
            elif x in ["+", "-"]:
                while len(operator_stack) > 0 and \
                        operator_stack[-1] not in ["("]:
                    result.append(operator_stack.pop())
                operator_stack.append(x)
            elif x == "(":
                operator_stack.append(x)
            elif x == ")":
                if "(" not in operator_stack:
                    raise Exception
                else:
                    while operator_stack[-1] not in ["("]:
                        result.append(operator_stack.pop())
                    operator_stack.pop()
    while operator_stack:
        result.append(operator_stack.pop())
    return result


while True:
    inp = input()
    if len(inp) == 0:
        continue
    elif inp[0] == "/":
        if inp == "/exit":
            print("Bye!")
            break
        elif inp == "/help":
            print("The program calculates additions and subtractions "
                  "of numbers")
        else:
            print("Unknown command")
    elif "=" in inp:
        var, formula = inp.split("=", 1)
        assign(var.strip(), parse(formula))
    else:
        formula = parse(inp)
        print(calculate(formula))
