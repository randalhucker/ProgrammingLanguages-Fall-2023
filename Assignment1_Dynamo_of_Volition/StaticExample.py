def outer():
  a = "outer contents of a"
  b = "outer contents of b"
  c = "outer contents of c"
  
  def inner():
    a = "inner contents of a"
    b = "inner contents of b"
    
    def inner_inner():
      a = "inner inner contents of a"
      print(f"{a=}")
      print(f"{b=}")
      print(f"{c=}")    
    inner_inner()
  inner()

if __name__ == "__main__":
    outer()