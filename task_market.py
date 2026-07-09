# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class MultiAgentPro(gl.Contract):
    n: str
    d0: str; r0: str; s0: str; w0: str; x0: str
    d1: str; r1: str; s1: str; w1: str; x1: str
    d2: str; r2: str; s2: str; w2: str; x2: str
    d3: str; r3: str; s3: str; w3: str; x3: str
    d4: str; r4: str; s4: str; w4: str; x4: str
    d5: str; r5: str; s5: str; w5: str; x5: str
    d6: str; r6: str; s6: str; w6: str; x6: str
    d7: str; r7: str; s7: str; w7: str; x7: str
    d8: str; r8: str; s8: str; w8: str; x8: str
    d9: str; r9: str; s9: str; w9: str; x9: str
    rep0_addr: str; rep0_ok: str; rep0_fail: str
    rep1_addr: str; rep1_ok: str; rep1_fail: str
    rep2_addr: str; rep2_ok: str; rep2_fail: str
    rep3_addr: str; rep3_ok: str; rep3_fail: str
    rep4_addr: str; rep4_ok: str; rep4_fail: str

    def __init__(self):
        self.n = "0"
        self.d0=""; self.r0=""; self.s0=""; self.w0=""; self.x0=""
        self.d1=""; self.r1=""; self.s1=""; self.w1=""; self.x1=""
        self.d2=""; self.r2=""; self.s2=""; self.w2=""; self.x2=""
        self.d3=""; self.r3=""; self.s3=""; self.w3=""; self.x3=""
        self.d4=""; self.r4=""; self.s4=""; self.w4=""; self.x4=""
        self.d5=""; self.r5=""; self.s5=""; self.w5=""; self.x5=""
        self.d6=""; self.r6=""; self.s6=""; self.w6=""; self.x6=""
        self.d7=""; self.r7=""; self.s7=""; self.w7=""; self.x7=""
        self.d8=""; self.r8=""; self.s8=""; self.w8=""; self.x8=""
        self.d9=""; self.r9=""; self.s9=""; self.w9=""; self.x9=""
        self.rep0_addr=""; self.rep0_ok="0"; self.rep0_fail="0"
        self.rep1_addr=""; self.rep1_ok="0"; self.rep1_fail="0"
        self.rep2_addr=""; self.rep2_ok="0"; self.rep2_fail="0"
        self.rep3_addr=""; self.rep3_ok="0"; self.rep3_fail="0"
        self.rep4_addr=""; self.rep4_ok="0"; self.rep4_fail="0"

    @gl.public.write
    def post_task(self, d: str, r: str, w: str) -> None:
        tid = int(self.n)
        if tid == 0: self.d0=d[:200]; self.r0=r[:150]; self.s0="open"; self.w0=str(w); self.x0=""
        elif tid == 1: self.d1=d[:200]; self.r1=r[:150]; self.s1="open"; self.w1=str(w); self.x1=""
        elif tid == 2: self.d2=d[:200]; self.r2=r[:150]; self.s2="open"; self.w2=str(w); self.x2=""
        elif tid == 3: self.d3=d[:200]; self.r3=r[:150]; self.s3="open"; self.w3=str(w); self.x3=""
        elif tid == 4: self.d4=d[:200]; self.r4=r[:150]; self.s4="open"; self.w4=str(w); self.x4=""
        elif tid == 5: self.d5=d[:200]; self.r5=r[:150]; self.s5="open"; self.w5=str(w); self.x5=""
        elif tid == 6: self.d6=d[:200]; self.r6=r[:150]; self.s6="open"; self.w6=str(w); self.x6=""
        elif tid == 7: self.d7=d[:200]; self.r7=r[:150]; self.s7="open"; self.w7=str(w); self.x7=""
        elif tid == 8: self.d8=d[:200]; self.r8=r[:150]; self.s8="open"; self.w8=str(w); self.x8=""
        elif tid == 9: self.d9=d[:200]; self.r9=r[:150]; self.s9="open"; self.w9=str(w); self.x9=""
        else: return None
        self.n = str(tid + 1)
        return None

    @gl.public.write
    def submit_result(self, task_id: int, result: str, agent_id: str) -> None:
        tid = task_id
        if tid == 0: desc=self.d0; rubric=self.r0; status=self.s0
        elif tid == 1: desc=self.d1; rubric=self.r1; status=self.s1
        elif tid == 2: desc=self.d2; rubric=self.r2; status=self.s2
        elif tid == 3: desc=self.d3; rubric=self.r3; status=self.s3
        elif tid == 4: desc=self.d4; rubric=self.r4; status=self.s4
        elif tid == 5: desc=self.d5; rubric=self.r5; status=self.s5
        elif tid == 6: desc=self.d6; rubric=self.r6; status=self.s6
        elif tid == 7: desc=self.d7; rubric=self.r7; status=self.s7
        elif tid == 8: desc=self.d8; rubric=self.r8; status=self.s8
        elif tid == 9: desc=self.d9; rubric=self.r9; status=self.s9
        else: return None
        if status != "open": return None

        agent = str(agent_id)[:42]

        def leader_fn() -> str:
            prompt = (
                f"You are a fair judge evaluating an AI agent's work.\n"
                f"Task: {desc}\n"
                f"Evaluation rubric: {rubric}\n"
                f"Submitted result: {result[:400]}\n"
                f"Does the result satisfy the rubric? Reply ONLY: APPROVED or REJECTED"
            )
            return gl.nondet.exec_prompt(prompt).replace('\x00','').strip()

        def validator_fn(lr) -> bool:
            if not isinstance(lr, gl.vm.Return): return False
            leader_answer = lr.calldata
            if not isinstance(leader_answer, str): return False
            leader_answer = leader_answer.replace('\x00','').strip()
            if leader_answer not in ("APPROVED", "REJECTED"): return False
            prompt = (
                f"You are a fair judge evaluating an AI agent's work.\n"
                f"Task: {desc}\n"
                f"Evaluation rubric: {rubric}\n"
                f"Submitted result: {result[:400]}\n"
                f"Does the result satisfy the rubric? Reply ONLY: APPROVED or REJECTED"
            )
            validator_answer = gl.nondet.exec_prompt(prompt).replace('\x00','').strip()
            if 'APPROVED' in validator_answer: validator_answer = 'APPROVED'
            else: validator_answer = 'REJECTED'
            return validator_answer == leader_answer

        verdict = gl.vm.run_nondet_unsafe(leader_fn, validator_fn).replace('\x00','').strip()
        vs = "completed" if verdict == "APPROVED" else "failed"
        res = result[:150]

        if tid == 0: self.s0=vs; self.x0=res
        elif tid == 1: self.s1=vs; self.x1=res
        elif tid == 2: self.s2=vs; self.x2=res
        elif tid == 3: self.s3=vs; self.x3=res
        elif tid == 4: self.s4=vs; self.x4=res
        elif tid == 5: self.s5=vs; self.x5=res
        elif tid == 6: self.s6=vs; self.x6=res
        elif tid == 7: self.s7=vs; self.x7=res
        elif tid == 8: self.s8=vs; self.x8=res
        elif tid == 9: self.s9=vs; self.x9=res

        for i in range(5):
            addrs = [self.rep0_addr,self.rep1_addr,self.rep2_addr,self.rep3_addr,self.rep4_addr]
            if addrs[i] == agent or addrs[i] == "":
                if i == 0:
                    self.rep0_addr = agent
                    if vs == "completed": self.rep0_ok = str(int(self.rep0_ok)+1)
                    else: self.rep0_fail = str(int(self.rep0_fail)+1)
                elif i == 1:
                    self.rep1_addr = agent
                    if vs == "completed": self.rep1_ok = str(int(self.rep1_ok)+1)
                    else: self.rep1_fail = str(int(self.rep1_fail)+1)
                elif i == 2:
                    self.rep2_addr = agent
                    if vs == "completed": self.rep2_ok = str(int(self.rep2_ok)+1)
                    else: self.rep2_fail = str(int(self.rep2_fail)+1)
                elif i == 3:
                    self.rep3_addr = agent
                    if vs == "completed": self.rep3_ok = str(int(self.rep3_ok)+1)
                    else: self.rep3_fail = str(int(self.rep3_fail)+1)
                elif i == 4:
                    self.rep4_addr = agent
                    if vs == "completed": self.rep4_ok = str(int(self.rep4_ok)+1)
                    else: self.rep4_fail = str(int(self.rep4_fail)+1)
                break
        return None

    @gl.public.view
    def get_task(self, task_id: int) -> str:
        if task_id == 0: d=self.d0; s=self.s0; w=self.w0; r=self.r0
        elif task_id == 1: d=self.d1; s=self.s1; w=self.w1; r=self.r1
        elif task_id == 2: d=self.d2; s=self.s2; w=self.w2; r=self.r2
        elif task_id == 3: d=self.d3; s=self.s3; w=self.w3; r=self.r3
        elif task_id == 4: d=self.d4; s=self.s4; w=self.w4; r=self.r4
        elif task_id == 5: d=self.d5; s=self.s5; w=self.w5; r=self.r5
        elif task_id == 6: d=self.d6; s=self.s6; w=self.w6; r=self.r6
        elif task_id == 7: d=self.d7; s=self.s7; w=self.w7; r=self.r7
        elif task_id == 8: d=self.d8; s=self.s8; w=self.w8; r=self.r8
        elif task_id == 9: d=self.d9; s=self.s9; w=self.w9; r=self.r9
        else: return "not found"
        if not d: return "not found"
        return f"Task: {d} | Rubric: {r} | Status: {s} | Reward: {w}"

    @gl.public.view
    def get_count(self) -> str:
        return self.n

    @gl.public.view
    def get_status(self, task_id: int) -> str:
        if task_id == 0: return self.s0 or "not found"
        if task_id == 1: return self.s1 or "not found"
        if task_id == 2: return self.s2 or "not found"
        if task_id == 3: return self.s3 or "not found"
        if task_id == 4: return self.s4 or "not found"
        if task_id == 5: return self.s5 or "not found"
        if task_id == 6: return self.s6 or "not found"
        if task_id == 7: return self.s7 or "not found"
        if task_id == 8: return self.s8 or "not found"
        if task_id == 9: return self.s9 or "not found"
        return "not found"

    @gl.public.view
    def get_result(self, task_id: int) -> str:
        if task_id == 0: return self.x0 or "not found"
        if task_id == 1: return self.x1 or "not found"
        if task_id == 2: return self.x2 or "not found"
        if task_id == 3: return self.x3 or "not found"
        if task_id == 4: return self.x4 or "not found"
        if task_id == 5: return self.x5 or "not found"
        if task_id == 6: return self.x6 or "not found"
        if task_id == 7: return self.x7 or "not found"
        if task_id == 8: return self.x8 or "not found"
        if task_id == 9: return self.x9 or "not found"
        return "not found"

    @gl.public.view
    def get_reputation(self, agent: str) -> str:
        addrs = [self.rep0_addr,self.rep1_addr,self.rep2_addr,self.rep3_addr,self.rep4_addr]
        oks = [self.rep0_ok,self.rep1_ok,self.rep2_ok,self.rep3_ok,self.rep4_ok]
        fails = [self.rep0_fail,self.rep1_fail,self.rep2_fail,self.rep3_fail,self.rep4_fail]
        for i in range(5):
            if addrs[i] == agent:
                return f"Completed: {oks[i]} | Failed: {fails[i]}"
        return "no reputation"

    @gl.public.view
    def get_all(self) -> str:
        n = int(self.n)
        parts = []
        ds = [self.d0,self.d1,self.d2,self.d3,self.d4,self.d5,self.d6,self.d7,self.d8,self.d9]
        ss = [self.s0,self.s1,self.s2,self.s3,self.s4,self.s5,self.s6,self.s7,self.s8,self.s9]
        ws = [self.w0,self.w1,self.w2,self.w3,self.w4,self.w5,self.w6,self.w7,self.w8,self.w9]
        for i in range(n):
            if ds[i]: parts.append(f"{ds[i]}|{ss[i]}|{ws[i]}")
        return ";;".join(parts)
