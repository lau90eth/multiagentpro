# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class MultiAgentPro(gl.Contract):
    task_count: str
    t0d: str
    t0r: str
    t0w: str
    t0s: str
    t0x: str
    t1d: str
    t1r: str
    t1w: str
    t1s: str
    t1x: str
    t2d: str
    t2r: str
    t2w: str
    t2s: str
    t2x: str
    t3d: str
    t3r: str
    t3w: str
    t3s: str
    t3x: str
    t4d: str
    t4r: str
    t4w: str
    t4s: str
    t4x: str

    def __init__(self):
        self.task_count = "0"
        self.t0d=""; self.t0r=""; self.t0w=""; self.t0s=""; self.t0x=""
        self.t1d=""; self.t1r=""; self.t1w=""; self.t1s=""; self.t1x=""
        self.t2d=""; self.t2r=""; self.t2w=""; self.t2s=""; self.t2x=""
        self.t3d=""; self.t3r=""; self.t3w=""; self.t3s=""; self.t3x=""
        self.t4d=""; self.t4r=""; self.t4w=""; self.t4s=""; self.t4x=""

    @gl.public.write
    def post_task(self, d: str, r: str, w: str) -> None:
        tid = int(self.task_count)
        if tid == 0: self.t0d=d[:200]; self.t0r=r[:150]; self.t0w=w; self.t0s="open"; self.t0x=""
        elif tid == 1: self.t1d=d[:200]; self.t1r=r[:150]; self.t1w=w; self.t1s="open"; self.t1x=""
        elif tid == 2: self.t2d=d[:200]; self.t2r=r[:150]; self.t2w=w; self.t2s="open"; self.t2x=""
        elif tid == 3: self.t3d=d[:200]; self.t3r=r[:150]; self.t3w=w; self.t3s="open"; self.t3x=""
        elif tid == 4: self.t4d=d[:200]; self.t4r=r[:150]; self.t4w=w; self.t4s="open"; self.t4x=""
        else: return None
        self.task_count = str(tid + 1)
        return None

    @gl.public.write
    def submit_result(self, task_id: int, result: str) -> None:
        tid = task_id
        if tid == 0: desc=self.t0d; rubric=self.t0r; status=self.t0s
        elif tid == 1: desc=self.t1d; rubric=self.t1r; status=self.t1s
        elif tid == 2: desc=self.t2d; rubric=self.t2r; status=self.t2s
        elif tid == 3: desc=self.t3d; rubric=self.t3r; status=self.t3s
        elif tid == 4: desc=self.t4d; rubric=self.t4r; status=self.t4s
        else: return None
        if status != "open": return None

        def leader_fn() -> str:
            prompt = (f"Judge this work.\nTask: {desc}\nRubric: {rubric}\n"
                      f"Result: {result[:400]}\nReply ONLY: APPROVED or REJECTED")
            return gl.nondet.exec_prompt(prompt).replace('\x00','').strip()

        def validator_fn(lr) -> bool:
            if not isinstance(lr, gl.vm.Return): return False
            r = lr.calldata
            return isinstance(r, str) and r.strip() in ("APPROVED","REJECTED")

        verdict = gl.vm.run_nondet_unsafe(leader_fn, validator_fn).replace('\x00','').strip()
        vs = "completed" if verdict == "APPROVED" else "failed"
        res = result[:200]

        if tid == 0: self.t0s=vs; self.t0x=res
        elif tid == 1: self.t1s=vs; self.t1x=res
        elif tid == 2: self.t2s=vs; self.t2x=res
        elif tid == 3: self.t3s=vs; self.t3x=res
        elif tid == 4: self.t4s=vs; self.t4x=res
        return None

    @gl.public.view
    def get_task(self, task_id: int) -> str:
        if task_id == 0: d=self.t0d; s=self.t0s; w=self.t0w
        elif task_id == 1: d=self.t1d; s=self.t1s; w=self.t1w
        elif task_id == 2: d=self.t2d; s=self.t2s; w=self.t2w
        elif task_id == 3: d=self.t3d; s=self.t3s; w=self.t3w
        elif task_id == 4: d=self.t4d; s=self.t4s; w=self.t4w
        else: return "not found"
        if not d: return "not found"
        return f"Task: {d} | Status: {s} | Reward: {w}"

    @gl.public.view
    def get_count(self) -> str:
        return self.task_count

    @gl.public.view
    def get_status(self, task_id: int) -> str:
        if task_id == 0: return self.t0s or "not found"
        if task_id == 1: return self.t1s or "not found"
        if task_id == 2: return self.t2s or "not found"
        if task_id == 3: return self.t3s or "not found"
        if task_id == 4: return self.t4s or "not found"
        return "not found"

    @gl.public.view
    def get_result(self, task_id: int) -> str:
        if task_id == 0: return self.t0x or "not found"
        if task_id == 1: return self.t1x or "not found"
        if task_id == 2: return self.t2x or "not found"
        if task_id == 3: return self.t3x or "not found"
        if task_id == 4: return self.t4x or "not found"
        return "not found"
