from dynamic_scope import get_dynamic_re
from typing import Any

def outer():
    a = "outer_a"
    b = "outer_b"
    c = "outer_c"
    return get_dynamic_re()

if __name__ == "__main__":
    dre = outer()
    print(f"{dre['a']=}")
    print(f"{dre['b']=}")
    print(f"{dre['c']=}")
    
    
def test_late_local():
  def outer():
    a = "outer_a"
    def inner():
      dre = get_dynamic_re()
      a = "inner_a"
      return dre
    return inner()
  return outer()
dre = test_late_local() 
print(f"{dre['a']=}")