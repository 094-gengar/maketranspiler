from llama_cpp import Llama # I use `codellama-13b-instruct.Q5_K_M.gguf`
import re

from secret_information import *

"""
デバッグ出力とエラー出力
"""
debug = True
def debug_print(a):
    if debug:
        print("# # # # # #")
        print(a)
        print("# # # # # #")

def error_print(s: str):
    print("error: " + s)



"""
インタプリタクラス
"""
class inner_transpiler_class():
    llm = Llama(model_path=LLAMA_PATH, seed=0)
    def query(self, s: str) -> str:
        prompt = self.llm("[PROMPT]\n" + s + "[/PROMPT]\n", temperature=2, repeat_penalty=1.0, max_tokens=500, stop=["\n\n\n\n"], echo=True)
        # prompt = self.llm(s, temperature=2, repeat_penalty=1.0, max_tokens=500, stop=["\n\n\n\n"], echo=True)
        return prompt["choices"][0]["text"]

class transpiler_class():
    def __init__(self, base_lang: str) -> None:
        self.base_lang = base_lang
        self.example_list = []
        self.example_stack = []
        self.transpile_prompt = "These are some examples of conversion between 'MyLang' and {} :\n".format(base_lang)
        self.inner_transpiler = inner_transpiler_class()

    def add_example(self, before: str, after: str) -> None:
        self.example_stack.append((before, after))

    def update_transpiler(self) -> None:
        while self.example_stack:
            before, after = self.example_stack.pop()
            self.example_list.append((before, after))
            self.transpile_prompt += \
f"""
# example {len(self.example_list)}:

## before (MyLang code) :
```
{before}
```

## after (code transpiled to {self.base_lang}) :
```
{after}
```

"""
        # debug_print(self.transpile_prompt)

    def transpile_code(self, code: str) -> str:
        prompt = self.transpile_prompt + "\nReferring to the above examples, transpile the following code to {}.\n\n".format(self.base_lang)
        prompt += f"""
## before (MyLang code) :
```
{code}
```
"""
        # debug_print(prompt)
        ret = self.inner_transpiler.query(prompt)
        matches = re.findall(r'\[/PROMPT][\s\S]*?```(.*?)```', ret, re.DOTALL)
        if len(matches) == 0:
            error_print("INNER ERROR (not matched)")
            return ""
        return matches[0]

        # output = self.inner_transpiler.llm(prompt, temperature=2, repeat_penalty=1.0, max_tokens=1000, stop=["\n\n\n\n"], echo=True)
        # return output["choices"][0]["text"]

    def update_and_transpile_code(self, code: str) -> str:
        self.update_transpiler()
        self.transpile_code(code)

    def make_documents(self) -> str:
        prompt = "Make the short documentation of this programming language."
        return self.inner_transpiler.query(prompt)
        # output = self.inner_transpiler.llm(prompt, temperature=2, repeat_penalty=1.0, max_tokens=1000, stop=["\n\n\n\n"], echo=True)
        # return output["choices"][0]["text"]
