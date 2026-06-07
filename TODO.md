To-Do list
===

* Replace with github issues
* use slimit to parse and reinsert scripts.
  - I can parse into an AST.
  - I want to identify where Identifiers are used vs. where Identifiers are created, so I can identify what's missing and should be added.
  - `var foo = 1;` becomes `VarStatement(children=[VarDecl(Identifier("foo"), Number(1))])`
  - `function bar(n) { return n * 2 }` becomes `FuncDecl(Identifier("bar"), parameters=[Identifier("n")], elements=[Return(BinOp("*", Identifier("n"), Number(2)))])`
  - `foo + bar(1)` becomes `ExprStatement(BinOp("+", Identifier("foo"), FunctionCall(Identifier("bar"), [Number(1)])))`
  - I need to work out what part of the AST describes creating an identifier, and which describes using an identifier.
  - Creators
    - NewExpr, probably, but I don't want to use it
    - VarDecl definitely does, and for some reason includes `_mangle_candidate = True`
    - what's Label?
    - FuncDecl and FuncExpr may both declare a new identifier. those also set `_mangle_candidate = True`
  - That sounds logical, but the results disagree.
