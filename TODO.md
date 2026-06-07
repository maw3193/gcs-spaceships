To-Do list
===

* Replace with github issues
* use slimit to parse and reinsert scripts.
  - program = slimit.parser.Parser().parse(text)
    - top-level members come from program.children()
  - hard part: recognising calls to other functions or upvalues and tracking that those should be imported too.
