from llama_cpp import Llama # I use `codellama-13b-instruct.Q5_K_M.gguf`
from secret_information import *
import re

"""
デバッグ出力とエラー出力
"""
debug = False
def debug_print(a):
    if debug:
        print("# # # # # #")
        print(a)
        print("# # # # # #")

def error_print(s: str):
    print("error: " + s)

"""
インタプリタクラスの補助クラス
"""
class inner_transpiler_class():
    def __init__(self, base_lang: str) -> None:
        self.base_lang = base_lang
        self.history = []

    llm = Llama(model_path=LLAMA_PATH, seed=0, verbose=debug, n_ctx=2048)
    def query(self, s: str) -> str:
        messages = self.history
        messages.append({
            "role": "user",
            "content": f"Please transpile this 'Mylang' code to {self.base_lang} (please write the code to the end) :\n```\n{s}\n```\n",
        })
        streamer = self.llm.create_chat_completion(messages, stream=True)
        ans = ""
        for msg in streamer:
            message = msg["choices"][0]["delta"]
            if "content" in message:
                ans += message["content"]

        debug_print(ans)
        return ans

"""
インタプリタクラス
"""
class transpiler_class():
    def __init__(self, base_lang: str) -> None:
        self.base_lang = base_lang
        self.inner_transpiler = inner_transpiler_class(base_lang=base_lang)
        self.inner_transpiler.history.append({"role" : "user", "content" : f"Please transpile some 'Mylang' codes to {base_lang}.\n"})
        self.inner_transpiler.history.append({"role" : "system", "content" : "Ok.\n"})

    def add_example(self, before: str, after: str) -> None:
        self.inner_transpiler.history.append({"role" : "user", "content" : f"Please transpile this 'Mylang' code to {self.base_lang} (please write the code to the end) :\n```\n{before}\n```\n"})
        self.inner_transpiler.history.append({"role" : "system", "content" : f"```\n{after}\n```\n"})

    def transpile_code(self, code: str) -> str:
        debug_print(self.inner_transpiler.history)
        ret = self.inner_transpiler.query(s=code)
        matches = re.findall(r'```(.*?)```', ret, re.DOTALL)
        if len(matches) == 0:
            error_print("INNER ERROR (not matched)")
            return ""
        return matches[0]

    def make_documents(self) -> str:
        pass # TODO
