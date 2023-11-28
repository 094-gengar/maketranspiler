import maketranspiler as mt

transpiler = mt.transpiler_class("Python")

transpiler.add_example( \
"""out("hello, world!")""",
"""print("hello, world!")""")

transpiler.add_example( \
"""out(10, 20, 30)""",
"""print(10, 20, 30)""")

transpiler.add_example( \
"""for i in 1..1000 {
    out(i)
}""",
"""for i in range(1, 1000):
print(i)""")

transpiler.update_transpiler()
print(transpiler.transpile_code( \
"""for i in 0..10 {
    out("No.", i)
}"""))
