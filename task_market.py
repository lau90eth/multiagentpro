# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class MultiAgentPro(gl.Contract):
    task_count: str
    tasks_json: str

    def __init__(self):
        self.task_count = "0"
        self.tasks_json = "{}"

    @gl.public.write
    def post_task(self, description: str, rubric: str, reward: str) -> None:
        task_id = self.task_count
        tasks = json.loads(self.tasks_json)
        tasks[task_id] = {
            "d": description[:300],
            "r": rubric[:150],
            "w": str(reward),
            "s": "open",
            "x": "",
            "a": ""
        }
        self.tasks_json = json.dumps(tasks)
        self.task_count = str(int(self.task_count) + 1)
        return None

    @gl.public.write
    def submit_result(self, task_id: str, result: str, agent_id: str) -> None:
        tasks = json.loads(self.tasks_json)
        if task_id not in tasks or tasks[task_id]["s"] != "open":
            return None
        desc = tasks[task_id]["d"]
        rubric = tasks[task_id]["r"]
        agent = str(agent_id)[:42]

        def leader_fn() -> str:
            prompt = (
                f"You are a fair judge evaluating an AI agent's work.\n"
                f"Task: {desc}\n"
                f"Rubric: {rubric}\n"
                f"Result: {result[:400]}\n"
                f"Reply ONLY: APPROVED or REJECTED"
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
                f"Rubric: {rubric}\n"
                f"Result: {result[:400]}\n"
                f"Reply ONLY: APPROVED or REJECTED"
            )
            val_answer = gl.nondet.exec_prompt(prompt).replace('\x00','').strip()
            if 'APPROVED' in val_answer: val_answer = 'APPROVED'
            else: val_answer = 'REJECTED'
            return val_answer == leader_answer

        verdict = gl.vm.run_nondet_unsafe(leader_fn, validator_fn).replace('\x00','').strip()
        vs = "completed" if verdict == "APPROVED" else "failed"
        tasks[task_id]["s"] = vs
        tasks[task_id]["x"] = result[:100]
        tasks[task_id]["a"] = agent
        self.tasks_json = json.dumps(tasks)
        return None

    @gl.public.view
    def get_task(self, task_id: str) -> str:
        tasks = json.loads(self.tasks_json)
        if task_id not in tasks: return "not found"
        t = tasks[task_id]
        return f"Task: {t['d']} | Status: {t['s']} | Reward: {t['w']}"

    @gl.public.view
    def get_count(self) -> str:
        return self.task_count

    @gl.public.view
    def get_status(self, task_id: str) -> str:
        tasks = json.loads(self.tasks_json)
        if task_id not in tasks: return "not found"
        return tasks[task_id]["s"]

    @gl.public.view
    def get_result(self, task_id: str) -> str:
        tasks = json.loads(self.tasks_json)
        if task_id not in tasks: return "not found"
        return tasks[task_id]["x"]

    @gl.public.view
    def get_reputation(self, agent: str) -> str:
        tasks = json.loads(self.tasks_json)
        ok = 0
        fail = 0
        for tid in tasks:
            t = tasks[tid]
            if t.get("a","") == agent:
                if t["s"] == "completed": ok += 1
                elif t["s"] == "failed": fail += 1
        if ok == 0 and fail == 0: return "no reputation"
        return f"Completed: {ok} | Failed: {fail}"

    @gl.public.view
    def get_all(self) -> str:
        tasks = json.loads(self.tasks_json)
        n = int(self.task_count)
        parts = []
        for i in range(n):
            tid = str(i)
            if tid in tasks and tasks[tid]["d"]:
                t = tasks[tid]
                parts.append(f"{t['d']}|{t['s']}|{t['w']}")
        return ";;".join(parts)
