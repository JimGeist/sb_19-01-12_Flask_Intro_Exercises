from flask import Flask, request
from operations import add, sub, mult, div

app = Flask(__name__)


def build_message_values_missing(url_operation, operation):
    """ function returns a helper message with an example of how to format the url """

    return f"""
            <h1>{url_operation}:</h1>
            <h2>Number(s) to {operation} are missing. To {operation} 2 numbers:</h2>
            <p><span style="font-size: 2em;">http://..site_url../{url_operation}<strong>?a=:operand1&b=:operand2</strong></span></p>
        """


def build_message_values_not_numeric(operation, a_str, b_str):
    """ function returns an error message that either a or b were not numeric """

    return f"""
            <h1><span style="color: #800000;">Awww SNAP!</span></h1>
            <p style="font-size: 1.5em;">
            Please check your values for the '{operation}' operation. Both a and b should be numeric.<br>
            a = {a_str}<br>
            b = {b_str}
            </p>
    """


@app.route("/add")
def addition():
    """ Handle an add request. a and b are passed in via query string """

    try:
        a_str = request.args["a"]
        b_str = request.args["b"]
    except:
        # either a, b, or both a and b were not in the query string.
        return build_message_values_missing("add", "add")

    # print(request.args, flush=True)
    # print(f"a={a_str}, b={b_str}", flush=True)

    try:
        # a and b should be numeric. int was too restrictive so float was used instead
        a = float(a_str)
        b = float(b_str)
    except:
        # a and/or b were not numeric and could not get converted.
        return build_message_values_not_numeric("add", a_str, b_str)

    result = add(a, b)

    return f"""
            <p style="font-size: 1.5em;"><br>{a} + {b} = {result}</p>
        """


@app.route("/sub")
def subtraction():
    """ Handle a subtraction request. a and b are passed in via query string """

    try:
        a_str = request.args["a"]
        b_str = request.args["b"]
    except:
        # either a, b, or both a and b were not in the query string.
        return build_message_values_missing("sub", "subtract")

    try:
        # a and b should be numeric. int was too restrictive so float was used instead
        a = float(a_str)
        b = float(b_str)
    except:
        # a and/or b were not numeric and could not get converted.
        return build_message_values_not_numeric("sub", a_str, b_str)

    result = sub(a, b)

    return f"""
            <p style="font-size: 1.5em;"><br>{a} - {b} = {result}</p>
        """


@app.route("/mult")
def multiplcation():
    """ Handle a multiplication request. a and b are passed in via query string """

    try:
        a_str = request.args["a"]
        b_str = request.args["b"]
    except:
        # either a, b, or both a and b were not in the query string.
        return build_message_values_missing("mult", "multiply")

    try:
        # a and b should be numeric. int was too restrictive so float was used instead
        a = float(a_str)
        b = float(b_str)
    except:
        # a and/or b were not numeric and could not get converted.
        return build_message_values_not_numeric("mult", a_str, b_str)

    result = mult(a, b)

    return f"""
            <p style="font-size: 1.5em;"><br>{a} &times; {b} = {result}</p>
        """


@app.route("/div")
def division():
    """ Handle a division request. a and b are passed in via query string """

    try:
        a_str = request.args["a"]
        b_str = request.args["b"]
    except:
        # either a, b, or both a and b were not in the query string.
        return build_message_values_missing("div", "divide")

    try:
        # a and b should be numeric. int was too restrictive so float was used instead
        a = float(a_str)
        b = float(b_str)
    except:
        # a and/or b were not numeric and could not get converted.
        return build_message_values_not_numeric("div", a_str, b_str)

    try:
        result = div(a, b)
    except ZeroDivisionError:
        return f"""
            <h1><span style="color: #800000;">Division by 0 . . . really??</span></h1>
            <p style="font-size: 1.5em;">
            Division by 0 is not allowed. Ever. Not even on this jangy website! Please change b from {b_str} to a value that is not 0.
            </p>            
            """

    return f"""
            <p style="font-size: 1.5em;"><br>{a} &divide; {b} = {result}</p>
        """


@app.route("/math/<url_operation>")
def basic_math(url_operation):
    """ Handle a basic math (add, sub, mult, or div) request. a and b are passed in via query string """

    VALID_OPERATIONS = ["add", "sub", "mult", "div"]

    operators = {
        "add": {
            "verb": "add",
            "fx": add,
            "symbol": "+"
        },
        "sub": {
            "verb": "subract",
            "fx": sub,
            "symbol": "-"
        },
        "mult": {
            "verb": "multipy",
            "fx": mult,
            "symbol": "&times;"
        },
        "div": {
            "verb": "divide",
            "fx": div,
            "symbol": "&divide;"
        }
    }

    operation = url_operation.lower()
    if (operation in VALID_OPERATIONS):

        # before we do anything, make sure we have a valid operation
        try:
            a_str = request.args["a"]
            b_str = request.args["b"]
        except:
            # either a, b, or both a and b were not in the query string.
            return build_message_values_missing(operation, operators[operation]['verb'])

        try:
            # a and b should be numeric. int was too restrictive so float was used instead
            a = float(a_str)
            b = float(b_str)
        except:
            # a and/or b were not numeric and could not get converted.
            return build_message_values_not_numeric(operation, a_str, b_str)

        try:
            result = operators[operation]['fx'](a, b)
        except ZeroDivisionError:
            return f"""
                <h1><span style="color: #800000;">Nein!</span></h1>
                <h2>Division by 0 . . . really??</h2>
                <p style="font-size: 1.5em;">
                Division by 0 is not allowed. Ever. Not even on this jangy website! Please change b from {b_str} to a value that is not 0.
                </p>
                """

        return f"""
                <p style="font-size: 1.5em;"><br>{a} {operators[operation]['symbol']} {b} = {result}</p>
            """

    else:
        # operation was not "add", "sub", "mult", "div"
        return f"""
                <h1><span style="color: #800000;">{url_operation} is not a valid operation.</span></h1>
                <p style="font-size: 1.5em;">
                '{url_operation}' is not a valid operations. <br>
                Please use: {VALID_OPERATIONS[0]}, {VALID_OPERATIONS[1]}, {VALID_OPERATIONS[2]}, or {VALID_OPERATIONS[3]}.
                </p>
                """


# operators = {
#     "add": {
#         "aka": "add",
#         "fx": add,
#         "symbol": "+"
#     }
# }


def poc(operation):

    VALID_OPERATIONS = ["add", "sub", "mult", "div"]

    operators = {
        "add": {
            "aka": "add",
            "fx": add,
            "symbol": "+"
        }
    }

    if (operation.lower() in VALID_OPERATIONS):
        print(operation)
        print(operators)
        print(operators[operation])
        print(operators[operation]["aka"])
        print(f"add aka: {operators[operation]['aka']}")
