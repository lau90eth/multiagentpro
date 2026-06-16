# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class MultiAgentPro(gl.Contract):
    task_count: str
    t0_desc: str
    t0_rubric: str
    t0_reward: str
    t0_status: str
    t0_result: str
    t1_desc: str
    t1_rubric: str
    t1_reward: str
    t1_status: str
    t1_result: str
    t2_desc: str
    t2_rubric: str
    t2_reward: str
    t2_status: str
    t2_result: str
    t3_desc: str
    t3_rubric: str
    t3_reward: str
    t3_status: str
    t3_result: str
    t4_desc: str
    t4_rubric: str
    t4_reward: str
    t4_status: str
    t4_result: str
    rep0_addr: str
    rep0_completed: str
    rep0_failed: str
    rep1_addr: str
    rep1_completed: str
    rep1_failed: str
    rep2_addr: str
    rep2_completed: str
    rep2_failed: str

    def __init__(self):
        self.task_count = "0"
        self.t0_desc = ""; self.t0_rubric = ""; self.t0_reward = ""; self.t0_status = ""; self.t0_result = ""
        self.t1_desc = ""; self.t1_rubric = ""; self.t1_reward = ""; self.t1_status = ""; self.t1_result = ""
        self.t2_desc = ""; self.t2_rubric = ""; self.t2_reward = ""; self.t2_status = ""; self.t2_result = ""
        self.t3_desc = ""; self.t3_rubric = ""; self.t3_reward = ""; self.t3_status = ""; self.t3_result = ""
        self.t4_desc = ""; self.t4_rubric = ""; self.t4_reward = ""; self.t4_status = ""; self.t4_result = ""
        self.rep0_addr = ""; self.rep0_completed = "0"; self.rep0_failed = "0"
        self.rep1_addr = ""; self.rep1_completed = "0"; self.rep1_failed = "0"
        self.rep2_addr = ""; self.rep2_completed = "0"; self.rep2_failed = "0"

    def _get_field(self, tid: int, field: str) -> str:
        if tid == 0:
            if field == "desc": return self.t0_desc
            if field == "rubric": return self.t0_rubric
            if field == "reward": return self.t0_reward
            if field == "status": return self.t0_status
            if field == "result": return self.t0_result
        if tid == 1:
            if field == "desc": return self.t1_desc
            if field == "rubric": return self.t1_rubric
            if field == "reward": return self.t1_reward
            if field == "status": return self.t1_status
            if field == "result": return self.t1_result
        if tid == 2:
            if field == "desc": return self.t2_desc
            if field == "rubric": return self.t2_rubric
            if field == "reward": return self.t2_reward
            if field == "status": return self.t2_status
            if field == "result": return self.t2_result
        if tid == 3:
            if field == "desc": return self.t3_desc
            if field == "rubric": return self.t3_rubric
            if field == "reward": return self.t3_reward
            if field == "status": return self.t3_status
            if field == "result": return self.t3_result
        if tid == 4:
            if field == "desc": return self.t4_desc
            if field == "rubric": return self.t4_rubric
            if field == "reward": return self.t4_reward
            if field == "status": return self.t4_status
            if field == "result": return self.t4_result
        return ""

    def _set_field(self, tid: int, field: str, value: str) -> None:
        if tid == 0:
            if field == "desc": self.t0_desc = value
            elif field == "rubric": self.t0_rubric = value
            elif field == "reward": self.t0_reward = value
            elif field == "status": self.t0_status = value
            elif field == "result": self.t0_result = value
        elif tid == 1:
            if field == "desc": self.t1_desc = value
            elif field == "rubric": self.t1_rubric = value
            elif field == "reward": self.t1_reward = value
            elif field == "status": self.t1_status = value
            elif field == "result": self.t1_result = value
        elif tid == 2:
            if field == "desc": self.t2_desc = value
            elif field == "rubric": self.t2_rubric = value
            elif field == "reward": self.t2_reward = value
            elif field == "status": self.t2_status = value
            elif field == "result": self.t2_result = value
        elif tid == 3:
            if field == "desc": self.t3_desc = value
            elif field == "rubric": self.t3_rubric = value
            elif field == "reward": self.t3_reward = value
            elif field == "status": self.t3_status = value
            elif field == "result": self.t3_result = value
        elif tid == 4:
            if field == "desc": self.t4_desc = value
            elif field == "rubric": self.t4_rubric = value
            elif field == "reward": self.t4_reward = value
            elif field == "status": self.t4_status = value
            elif field == "result": self.t4_result = value
        return None

    @gl.public.write
    def post_task(self, description: str, rubric: str, reward: str) -> None:
        tid = int(self.task_count)
        if tid > 4:
            return None
        self._set_field(tid, "desc", description[:300])
        self._set_field(tid, "rubric", rubric[:200])
        self._set_field(tid, "reward", reward)
        self._set_field(tid, "status", "open")
        self._set_field(tid, "result", "")
        self.task_count = str(tid + 1)
        return None

    @gl.public.write
    def submit_result(self, task_id: int, result: str) -> None:
        tid = task_id
        if self._get_field(tid, "status") != "open":
            return None
        task = self._get_field(tid, "desc")
        rubric = self._get_field(tid, "rubric")
        agent = "0x" + gl.message.sender_address.as_bytes.hex()

        def leader_fn() -> str:
            prompt = (
                f"Judge this AI agent's work.\n"
                f"Task: {task}\n"
                f"Rubric: {rubric}\n"
                f"Result: {result[:500]}\n"
                f"Reply ONLY: APPROVED or REJECTED"
            )
            return gl.nondet.exec_prompt(prompt).replace('\x00', '').strip()

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            r = leaders_res.calldata
            return isinstance(r, str) and r.strip() in ("APPROVED", "REJECTED")

        verdict = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        verdict = verdict.replace('\x00', '').strip()
        self._set_field(tid, "result", result[:300])
        self._set_field(tid, "status", "completed" if verdict == "APPROVED" else "failed")

        for i in range(3):
            addr_field = f"rep{i}_addr"
            addr = getattr(self, addr_field)
            if addr == agent or addr == "":
                setattr(self, addr_field, agent)
                comp = getattr(self, f"rep{i}_completed")
                fail = getattr(self, f"rep{i}_failed")
                if verdict == "APPROVED":
                    setattr(self, f"rep{i}_completed", str(int(comp) + 1))
                else:
                    setattr(self, f"rep{i}_failed", str(int(fail) + 1))
                break
        return None

    @gl.public.view
    def get_task(self, task_id: int) -> str:
        tid = task_id
        desc = self._get_field(tid, "desc")
        if not desc:
            return "not found"
        status = self._get_field(tid, "status")
        reward = self._get_field(tid, "reward")
        return f"Task: {desc} | Status: {status} | Reward: {reward}"

    @gl.public.view
    def get_count(self) -> str:
        return self.task_count

    @gl.public.view
    def get_status(self, task_id: int) -> str:
        return self._get_field(task_id, "status") or "not found"

    @gl.public.view
    def get_result(self, task_id: int) -> str:
        return self._get_field(task_id, "result") or "not found"

    @gl.public.view
    def get_rubric(self, task_id: int) -> str:
        return self._get_field(task_id, "rubric") or "not found"

    @gl.public.view
    def get_reputation(self, agent: str) -> str:
        for i in range(3):
            addr = getattr(self, f"rep{i}_addr")
            if addr == agent:
                c = getattr(self, f"rep{i}_completed")
                f = getattr(self, f"rep{i}_failed")
                return f"Completed: {c} | Failed: {f}"
        return "no reputation"
