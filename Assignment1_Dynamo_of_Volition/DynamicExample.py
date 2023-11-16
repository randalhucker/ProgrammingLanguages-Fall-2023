def outer():
  a = "outer_a"
  b = "outer_b"
  c = "outer_c"

  def inner1():
    a = "inner1_a"
    b = "inner1_b"
    inner3()

  def inner2():
    a = "inner2_a"
    b = "inner2_b"
    inner3()

  def inner3():
    a = "inner3_a"
    print(f"{a=}")
    print(f"{b=}")
    print(f"{c=}")

  print("Calling inner1:")
  inner1()

  print("Calling inner2:")
  inner2()

if __name__ == "__main__":
  outer()