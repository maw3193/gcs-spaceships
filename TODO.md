To-Do list
===

* Replace with github issues
* ARGH TYPES!
  - I do, in fact, still need pydantic, because I'm making a tree of classes from json.
  - typeddicts can be constructed from dicts by unpacking into the constructor,
    giving me access to child methods, but this isn't going to be smart enough
    to recursively do that.
  - Supposedly, pydantic can take a dict which includes variables we don't care about.
  - https://stackoverflow.com/a/77021677 model_config extra=allow, then there's .model_extra.
* use slimit to parse and reinsert scripts.
  - program = slimit.parser.Parser().parse(text)
    - top-level members come from program.children()
  - hard part: recognising calls to other functions or upvalues and tracking that those should be imported too.
* Use Richard's article to make arg parsing nice.
  - declare a class Args in your main function
  - call parser.add_arg() after declaring each value in the class
  - use namespace= parameter to set the class.
* use coroutines to centralise modifying notes?
  ```python
  a = [1, 2, 3, 4, 5, 6]
  
  def mutate_array(arr):
      for i in range(len(a)):
          a[i] = yield a[i]
  
  gen = mutate_array(a)
  try:
      val = next(gen)
      while True:
          val = gen.send(val * 2)
  except StopIteration:
      pass
  
  print(a)
  ```
* tried to mutate a string with scripts in it
  ```python
  def mutate_scripted_string(s: str) -> str:
      script_open = "<script>"
      script_open_len = len(script_open)
      script_close = "</script>"
      script_close_len = len(script_close)
      script_expr = r"<script>(.*?)</script>"
      tokens = []
      last_index = 0
      for match in re.finditer(script_expr, s):
          start, end = match.span()
          before_str = s[last_index:start + script_open_len]
          tokens.append(before_str)
          last_index = end
          script = match.groups()[0]
          tokens.append(yield script)
          tokens.append(script_close) # just the closing tag
          end_str = script_close
          tokens.append(script)
          tokens.append(end_str)
      tokens.append(s[last_index:])
      print(tokens)
      return "".join(tokens)
  ```
