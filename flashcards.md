# GridScript Flashcards

## Card 1

**Q:** What programming language component uses regular expressions and finite automata to produce tokens?

**A:** The lexer

---

## Card 2

**Q:** In the GridScript project, which component is responsible for turning tokens into a parse tree or Abstract Syntax Tree (AST)?

**A:** The parser

---

## Card 3

**Q:** Which language design topic describes how the constructs of a language actually execute or evaluate?

**A:** Operational semantics

---

## Card 4

**Q:** The GridScript lexer principle that takes the longest matching token is known as _____.

**A:** Maximal munch

---

## Card 5

**Q:** What is the regular expression used for the GridScript 'NUMBER' token?

**A:** $[0-9]+$

---

## Card 6

**Q:** In GridScript, how are keywords distinguished from identifiers during lexical analysis?

**A:** They are lexed as identifiers then looked up in a keyword table.

---

## Card 7

**Q:** What happens to comments beginning with // in the GridScript lexer?

**A:** They are stripped and produce no tokens.

---

## Card 8

**Q:** Which GridScript operators are described as 'single- and two-character operators'?

**A:** The OP tokens ($=, ==, !=, <, >, +, -, *, /$)

---

## Card 9

**Q:** What formal notation is used to define the GridScript grammar?

**A:** BNF (Backus-Naur Form)

---

## Card 10

**Q:** According to the GridScript grammar, which set of operators binds more tightly: comparisons or addition/subtraction?

**A:** Addition and subtraction ($+ -$)

---

## Card 11

**Q:** In the GridScript grammar, what does an 'else' block always attach to?

**A:** The nearest unmatched 'if'.

---

## Card 12

**Q:** GridScript function calls can be used inside arithmetic expressions because they are classified as _____.

**A:** Expressions (specifically inside Factor)

---

## Card 13

**Q:** What parsing technique is suggested for the GridScript grammar due to its LL(1)-friendly nature?

**A:** Recursive descent

---

## Card 14

**Q:** In GridScript, what are the three basic types of values?

**A:** Number, String, and Boolean.

---

## Card 15

**Q:** Does GridScript use static typing or dynamic typing?

**A:** Dynamic typing

---

## Card 16

**Q:** In GridScript, what is the result of using the '+' operator on two String values?

**A:** String concatenation

---

## Card 17

**Q:** What is the runtime result of the GridScript expression $1 == "1"$?

**A:** The Boolean value 'false'.

---

## Card 18

**Q:** In GridScript, what occurs if an 'if' or 'while' condition evaluates to a Number instead of a Boolean?

**A:** A runtime TypeError.

---

## Card 19

**Q:** How does GridScript handle division by zero during interpretation?

**A:** It is treated as a run-time error.

---

## Card 20

**Q:** Which scoping rule does GridScript implement: static or dynamic?

**A:** Static (lexical) scoping

---

## Card 21

**Q:** In GridScript, which language construct is the only one that creates a new scope?

**A:** A function call

---

## Card 22

**Q:** What is the scope-binding behavior of the GridScript command 'set x = e'?

**A:** It always binds or updates 'x' in the current environment only.

---

## Card 23

**Q:** How are variable names resolved in GridScript's lexical scoping?

**A:** The current environment is searched first, then enclosing environments out to the global level.

---

## Card 24

**Q:** When a GridScript function is defined, what environment becomes the parent of its future execution frames?

**A:** The environment where the function was defined ($\\sigma_{def}$).

---

## Card 25

**Q:** What term describes a local variable in a function having the same name as a global variable, making the global inaccessible?

**A:** Shadowing

---

## Card 26

**Q:** In GridScript operational semantics, what does the symbol $\\sigma$ represent?

**A:** The current environment (a name to value mapping).

---

## Card 27

**Q:** What does the notation $\\langle e, \\sigma \\rangle \\Downarrow v$ signify in language semantics?

**A:** Expression 'e' evaluates to value 'v' in environment '$\\sigma$'.

---

## Card 28

**Q:** In GridScript, what three components make up a function closure?

**A:** The parameter list, the body, and the environment at definition time.

---

## Card 29

**Q:** What value does a GridScript function return if control reaches the end of the body without a 'return' statement?

**A:** The Number 0.

---

## Card 30

**Q:** Which GridScript built-in action restores the actor's health?

**A:** use_potion()

---

## Card 31

**Q:** What is the return value of the GridScript built-in 'step_forward()' if the actor is blocked?

**A:** The Number 0.

---

## Card 32

**Q:** The ability to call a function within its own body in GridScript is supported because each call gets its own _____.

**A:** Frame (or fresh environment)

---

## Card 33

**Q:** Which language construct is used to provide the lexer with the rules for identifiers and literals?

**A:** Regular expressions

---

## Card 34

**Q:** Why was static scoping chosen for GridScript over dynamic scoping?

**A:** It allows a function's meaning to be understood from its text alone without tracing call history.

---

## Card 35

**Q:** What is the benefit of dynamic typing in a small scripting language like GridScript?

**A:** It keeps the grammar and parser small by removing the need for type annotations.

---

## Card 36

**Q:** In the GridScript semantics, what happens to the environment $\\sigma$ when a function returns?

**A:** The call environment is discarded, returning to the previous scope.

---

## Card 37

**Q:** What is the expected result of the GridScript expression 'true == 1'?

**A:** The Boolean value 'false'.

---

## Card 38

**Q:** Which GridScript token matches the regular expression $[a-zA-Z_][a-zA-Z0-9_]*$?

**A:** IDENT (Identifiers)

---

## Card 39

**Q:** In GridScript, what are the allowed operands for the unary minus operator?

**A:** Numbers only.

---

## Card 40

**Q:** How does the GridScript parser handle an 'if' statement without an 'else' block?

**A:** The absent 'else' is treated as an empty body.

---

## Card 41

**Q:** Which course topic covers the rules for names and binding?

**A:** Scoping

---

## Card 42

**Q:** What does a 'lexical chain' refer to in the context of GridScript environments?

**A:** The sequence of parent environments used to resolve variable names.

---

## Card 43

**Q:** What is the result of the GridScript operation 'Number < Number'?

**A:** A Boolean value.

---

## Card 44

**Q:** What must each group member submit to prove their individual contribution to the code?

**A:** A short video walkthrough (2-3 minutes).

---

## Card 45

**Q:** Which specific operator is used for assignment in GridScript?

**A:** The single equals sign ($=$).

---

## Card 46

**Q:** In the GridScript grammar, what category of tokens includes 'def', 'if', and 'while'?

**A:** Keywords

---

## Card 47

**Q:** What is the primary role of the environment $\\sigma$ during interpreting?

**A:** Mapping names to their current run-time values.

---

## Card 48

**Q:** Under GridScript semantics, when is the parameter of a function bound to its argument value?

**A:** At the time the function is called.

---

## Card 49

**Q:** What type of error is 'undefined variable mana' in GridScript?

**A:** A run-time error.

---

## Card 50

**Q:** What type of error is 'expected then' in GridScript?

**A:** A parser (syntax) error.

---

## Card 51

**Q:** How many arguments can GridScript functions accept according to the updated grammar?

**A:** A comma-separated list of zero or more arguments.

---

## Card 52

**Q:** What is the return value of 'turn_left()' or 'turn_right()' in GridScript?

**A:** The Number 1.

---

## Card 53

**Q:** Which operator has the lowest precedence in GridScript: multiplication, addition, or comparison?

**A:** Comparison ($==, !=, <, >$)

---

## Card 54

**Q:** In the context of interpretation, what is a 'runtime value' ($v$)?

**A:** The data resulting from evaluating an expression (e.g., 5, "hello", or true).

---

## Card 55

**Q:** What is the result of applying '!=' to a String and a Number in GridScript?

**A:** The Boolean value 'true' (different types are not equal).

---

## Card 56

**Q:** In the project brief, what is the 'handful of constructs' recommended for the language?

**A:** Arithmetic, variables/assignment, one conditional or loop, and simple function calls.

---

## Card 57

**Q:** What is the specific file format used for GridScript source code samples in the design document?

**A:** .gsc

---

## Card 58

**Q:** According to the lexer notes, why is '>=' a syntax error in GridScript?

**A:** Operators like '>=' were deliberately omitted to simplify the lexer.

---

## Card 59

**Q:** What does a 'DFA' (Deterministic Finite Automaton) represent in the context of the lexer?

**A:** The state machine that implements the regular expression matching.

---

## Card 60

**Q:** What happens when a GridScript interpreter encounters the 'return' keyword inside a function?

**A:** It halts the function execution immediately and yields the evaluated value of the expression.

---
