# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class MultiAgentPro(gl.Contract):
    n: str
    d0: str
    s0: str
    w0: str
    x0: str
    d1: str
    s1: str
    w1: str
    x1: str
    d2: str
    s2: str
    w2: str
    x2: str

    def __init__(self):
        self.n = "0"
        self.d0 = ""; self.s0 = ""; self.w0 = ""; self.x0 = ""
        self.d1 = ""; self.s1 = ""; self.w1 = ""; self.x1 = ""
        self.d2 = ""; self.s2 = ""; self.w2 = ""; self.x2 = ""

    @gl.public.write
    def post_task(self, d: str, r: str, w: str) -> None:
        tid = int(self.n)
        if tid == 0: self.d0=d[:200]; self.s0="open"; self.w0=str(w); self.x0=""
        elif tid == 1: self.d1=d[:200]; self.s1="open"; self.w1=str(w); self.x1=""
        elif tid == 2: self.d2=d[:200]; self.s2="open"; self.w2=str(w); self.x2=""
        else: return None
        self.n = str(tid + 1)
        return None

    @gl.public.write
    def submit_result(self, task_id: int, result: str) -> None:
        if task_id == 0: desc=self.d0; status=self.s0
        elif task_id == 1: desc=self.d1; status=self.s1
        elif task_id == 2: desc=self.d2; status=self.s2
        else: return None
        if status != "open": return None

        def leader_fn() -> str:
            prompt = f"Task: {desc}\nResult: {result[:300]}\nReply ONLY: APPROVED or REJECTED"
            return gl.nondet.exec_prompt(prompt).replace('\x00','').strip()

        def validator_fn(lr) -> bool:
            if not isinstance(lr, gl.vm.Return): return False
            r = lr.calldata
            return isinstance(r, str) and r.strip() in ("APPROVED","REJECTED")

        verdict = gl.vm.run_nondet_unsafe(leader_fn, validator_fn).replace('\x00','').strip()
        vs = "completed" if verdict == "APPROVED" else "failed"

        if task_id == 0: self.s0=vs; self.x0=result[:150]
        elif task_id == 1: self.s1=vs; self.x1=result[:150]
        elif task_id == 2: self.s2=vs; self.x2=result[:150]
        return None

    @gl.public.view
    def get_task(self, task_id: int) -> str:
        if task_id == 0: return f"Task: {self.d0} | Status: {self.s0} | Reward: {self.w0}" if self.d0 else "not found"
        if task_id == 1: return f"Task: {self.d1} | Status: {self.s1} | Reward: {self.w1}" if self.d1 else "not found"
        if task_id == 2: return f"Task: {self.d2} | Status: {self.s2} | Reward: {self.w2}" if self.d2 else "not found"
        return "not found"

    @gl.public.view
    def get_count(self) -> str:
        return self.n

    @gl.public.view
    def get_status(self, task_id: int) -> str:
        if task_id == 0: return self.s0 or "not found"
        if task_id == 1: return self.s1 or "not found"
        if task_id == 2: return self.s2 or "not found"
        return "not found"

    @gl.public.view
    def get_result(self, task_id: int) -> str:
        if task_id == 0: return self.x0 or "not found"
        if task_id == 1: return self.x1 or "not found"
        if task_id == 2: return self.x2 or "not found"
        return "not found"

    @gl.public.view
    def get_all(self) -> str:
        n = int(self.n)
        parts = []
        if n > 0 and self.d0: parts.append(f"{self.d0}|{self.s0}|{self.w0}")
        if n > 1 and self.d1: parts.append(f"{self.d1}|{self.s1}|{self.w1}")
        if n > 2 and self.d2: parts.append(f"{self.d2}|{self.s2}|{self.w2}")
        return ";;".join(parts)
