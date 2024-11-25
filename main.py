def symbol_name(symbol):
    if symbol == '+':
        return "Addition"
    elif symbol == '-':
        return "Subtraction"
    elif symbol == '*':
        return "Multiplication"
    elif symbol == '/':
        return "Division"
    elif symbol == '!':
        return "Exclamatory"
    elif symbol == '#':
        return "Hash"
    elif symbol == '%':
        return "Percentage"
    elif symbol == '&':
        return "Ampersand"
    elif symbol == '(':
        return "Opening braces"
    elif symbol == ')':
        return "Closing braces"
    elif symbol == '{':
        return "Left curly braces"
    elif symbol == '}':
        return "Right curly braces"
    elif symbol == '[':
        return "Left square bracket"
    elif symbol == ']':
        return "Right square bracket"
    elif symbol == ':':
        return "Colon"
    elif symbol == ';':
        return 'Semicolon'
    elif symbol == '_':
        return "Underscore"
    elif symbol == '=':
        return "Assignment"
    elif symbol == '<':
        return "Less than"
    elif symbol == '>':
        return "Greater than"
    elif symbol == ',':
        return "Comma"
    elif symbol == '.':
        return "Full stop"
    elif symbol == '?':
        return "Question mark"
    elif symbol == '|':
        return "Bar"
    elif symbol == '"':
        return "Quote"
    elif symbol == "'":
        return "Quote"

def keyword_list(token):
    keywords = [
        "alignas", "asm", "auto", "bitand", "bitor",
        "bool", "break", "case", "catch", "char", "char16_t",
        "char32_t", "class", "const", "constexpr", "const_cast",
        "continue", "decltype", "default", "delete", "do", "double",
        "dynamic_cast", "else", "enum", "explicit", "export", "extern",
        "false", "float", "for", "friend", "goto", "if", "inline",
        "int", "include", "long", "main", "mutable", "namespace", "new", "noexcept",
        "not", "not_eq", "nullptr", "operator", "or", "or_eq",
        "private", "protected", "public", "register", "reinterpret_cast",
        "return", "short", "signed", "sizeof", "static", "static_assert",
        "static_cast", "struct", "switch", "synchronized", "template",
        "this", "thread_local", "throw", "true", "try", "typedef",
        "typeid", "typename", "union", "unsigned", "using", "virtual",
        "void", "volatile", "wchar_t", "while", "xor", "xor_eq", "std", "stdio", "h"
    ]

    if token in keywords:
        return token
    else:
        return ""

def remove_comments(cpp_code):
    """
    Function to remove both single-line (//) and multi-line (/* */) comments from the C++ code.
    """
    in_multiline_comment = False  # To track multi-line comments
    result = []

    for line in cpp_code.splitlines():
        if not in_multiline_comment:
            if "/*" in line and "*/" in line:
                # Remove inline multi-line comments
                line = line.split("/*")[0] + line.split("*/")[-1]
            elif "/*" in line:
                # Start of multi-line comment
                line = line.split("/*")[0]
                in_multiline_comment = True
            elif "//" in line:
                # Remove single-line comments
                line = line.split("//")[0]
        else:
            # End of multi-line comment
            if "*/" in line:
                line = line.split("*/")[-1]
                in_multiline_comment = False
            else:
                # Inside a multi-line comment; ignore this line
                line = ""

        if line.strip():
            result.append(line)

    return "\n".join(result)


def tokens_and_analysis():
    # Read input from 'lab.txt'
    with open("input.txt", "r") as text:
        cpp_code = text.read()

    # Remove comments from the C++ code
    cleaned_code = remove_comments(cpp_code)

    # Tokenizer logic
    tokenizer = []
    i = 0  # Pointer for tracking character index in a line

    for line in cleaned_code.splitlines():
        i = 0
        while i < len(line):
            char = line[i]

            # Handle numbers (including floating-point numbers)
            if char.isdigit():
                number = char
                i += 1
                while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                    number += line[i]
                    i += 1
                tokenizer.append(number)
                continue

            # Handle identifiers and keywords
            elif char.isalpha() or char == '_':
                word = char
                i += 1
                while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                    word += line[i]
                    i += 1
                tokenizer.append(word)
                continue

            # Handle special symbols and operators
            elif not char.isspace():
                tokenizer.append(char)

            i += 1

    # Writing token information to the file
    with open("output.txt", "w") as output:
        output.write(f"{'Lexemes':<20} {'Token Name':<20} {'Attribute Value':<20}\n")
        token_details = []

        # Process tokens and classify them
        for token in tokenizer:
            if token.replace('.', '', 1).isdigit():  # Check for numbers (int and float)
                output.write(f"{token:<20} {'Number':<20} {'Constant':<20}\n")
                token_details.append((token, "Number", "Constant"))
            elif not token.isalnum():
                # Handle operators and special symbols
                a = symbol_name(token)
                if token in "+-*/=":
                    output.write(f"{token:<20} {'Operator':<20} {a:<20}\n")
                    token_details.append((token, "Operator", a))
                else:
                    output.write(f"{token:<20} {'Special symbol':<20} {a:<20}\n")
                    token_details.append((token, "Special symbol", a))
            else:
                # Check if token is a keyword or an identifier
                found_token = keyword_list(token)
                if found_token:
                    output.write(f"{token:<20} {found_token:<20} {'-----':<20}\n")
                    token_details.append((token, found_token, "-----"))
                else:
                    output.write(f"{token:<20} {'id':<20} {'Pointer to symbol table':<20}\n")
                    token_details.append((token, "id", "Pointer to symbol table"))

        # List variables and constants with their types
        variables, constants = list_variables_and_constants(tokenizer)

        output.write("\nVariables:\n")
        for var, var_type in variables:
            output.write(f"Name: {var}, Type: {var_type}\n")

        output.write("\nConstants:\n")
        for const, const_type in constants:
            output.write(f"Value: {const}, Type: {const_type}\n")


def list_variables_and_constants(tokens):
    # Identify variables and constants
    variables = []
    constants = []
    type_keywords = {"int", "float", "double", "char", "string"}
    prev_token = None  # To track the previous token for variable declarations

    for token in tokens:
        if token in type_keywords:
            prev_token = token  # Store the type for the next identifier
        elif prev_token and token.isidentifier():
            # If the previous token was a type and this is an identifier, it's a variable
            variables.append((token, prev_token))

        elif token.replace('.', '', 1).isdigit():
            # Check for numeric constants (int or float)
            if '.' in token:
                constants.append((token, "float"))
                prev_token = None
            else:
                constants.append((token, "int"))
                prev_token = None
        elif token != ',' :
            prev_token = None

    return variables, constants

# Call the function to process the input and generate the output
tokens_and_analysis()
