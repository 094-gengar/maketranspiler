import maketranspiler as mt

transpiler = mt.transpiler_class("C++")

transpiler.add_example( \
"""out("hello, world!")""",
"""#include <iostream>
using namespace std;
int main() {
  cout << "hello, world!" << endl;
}""")

transpiler.add_example( \
"""f = true
g = false
if f {
    out("a")
} else if g {
    out("b")
} else {
    out("c")
}""",
"""#include <iostream>
using namespace std;
int main() {
  bool f = true, g = false;
  if (f) {
    cout << "a" << endl;
  } else if (g) {
    cout << "b" << endl;
  } else {
    cout << "c" << endl;
  }
}""")

transpiler.add_example( \
"""for i in 1..1000 {
    out(i)
}""",
"""#include <iostream>
using namespace std;
int main() {
  for (int i = 1; i < 1000; i++) {
    cout << i << endl;
  }
}""")

print(transpiler.transpile_code( \
"""for i in 1..101 {
    if i % 15 == 0 {
        out("FizzBuzz")
    } else if i % 3 == 0 {
        out("Fizz")
    } else if i % 5 == 0 {
        out("Buzz")
    } else {
        out(i)
    }
}"""))

