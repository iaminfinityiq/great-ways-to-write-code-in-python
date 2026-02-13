# Requirements
Only requirements is `Python 3.11` or above. That's literally the only requirements...
If you don't have that, then you can always use an online interpreter to run on as there is only one file

# Statements and expressions
Expressions are basically something that has a value, for example: `(1 + 2) * 3` is an expression because it has a value of `9`. In this language, expressions are evaluated like how you learned `PEMDAS` or `BODMAS` at school

On the other hand, statements don't have a value, but they are like commands that tell the language what to do. In this language, each statement must end with a `;`

# Data types
This language currently has `int`, `float`, `boolean`, and `null_t` implemented

# `int`
`int` is a data type that represents an integer, like `-67` or `2026` (definitely didn't put those on purpose)

You can perform `7` different operations on `int`, these include:

1. `int + int` or `int + float`: addition
2. `int - int` or `int - float`: subtraction
3. `int * int` or `int * float`: multiplication
4. `int / int`: integer division (does NOT return fractional parts)
5. `int / float`: normal division
6. `+int`: unary plus
7. `-int`: unary minus, also known as negation

# `float`
`float` is a data type that represents a real number value, people would know it as decimals, like `-2026.67` or `61.2025` (definitely didn't put those on purpose again)

You can perform `6` different operations on `float`, these include:

1. `float + int` or `float + float`: addition
2. `float - int` or `float - float`: subtraction
3. `float * int` or `float * float`: multiplication
4. `float / int` or `float / float`: normal division
5. `+float`: unary plus
6. `-float`: unary minus, also known as negation

# `boolean`
`boolean` is a data type that only has `2` different values: `TRUE` or `FALSE`, although you have to access it through `true` or `false`

# `null_t`
`null_t` is a data type that only has **`1`** and only **`1`** single value: `NULL`. But you have to access it through `null`

# Variables
Variables are like containers of data. Each variable can store one value. To get the value of a variable, just type the name of it.

You can use variables in different kinds of operation like `+` or `*`. You can basically replace a variable with a number

Variable names also have rules in order to support programming languages, these include:

1. Variable names must start with alphabetical letters (`a` to `z`, `A` to `Z`) or underscore for some reason (`_`)
2. Variable names can only have alphabetical letters, digits (`0` to `9`), and underscore for some reason (`_`), no special characters, no space characters
3. Variable names must not match with the keywords list of the language

# Variable declaration
But the program does not know what values do the variables start with? That's why we have variable declarations, which is a statement

Variable declarations basically just creates a variable and store it with some value. To declare a variable, choose one of the following ways:

1. `let <variable_name> = <value>;`: initializes the variable with the value specified
2. `const <variable_name> = <value>;`: initializes the variable with the value specified, but the variable later can't be changed as the variable now is a **constant**
3. `let <variable_name>;`: initializes the variable with the value `null`
4. `const <variable_name>;`: initializes the variable with the value `null` and the variable later can't be changed as the variable now is a **constant**
