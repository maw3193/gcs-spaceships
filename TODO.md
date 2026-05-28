To-Do list
===

* Replace with github issues
* Parse config.
* use slimit to parse and reinsert scripts.
  - program = slimit.parser.Parser().parse(text)
    - top-level members come from program.children()
  - hard part: recognising calls to other functions or upvalues and tracking that those should be imported too.
* Use ruamel or something to parse yaml then validate it by throwing it into a class with pydantic.
* Use Richard's article to make arg parsing nice.
  - declare a class Args in your main function
  - call parser.add_arg() after declaring each value in the class
  - use namespace= parameter to set the class.
