# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class MultiAgentPro(gl.Contract):
    task_count: str
    tasks_json: str
    rep_json: str

    def __init__(self):
        self.task_count = "0"
        self.tasks_json = "{}"
        self.rep_json = "{}"

    @gl.public.write
    def post_task(self, description: str, rubric: str, reward: str) -> None:
        task_id = self.task_count
        tasks = json.loads(self.tasks_json)
        tasks[task_id] = {
            "description": description[:500],
            "rubric": rubric[:300],
            "reward": reward,
            "status": "open",
            "result": "",
            "submitter": ""
        }
        self.tasks_json = json.dumps(tasks)
        self.task_count = str(int(self.task_count) + 1)
        return None

    @gl.public.write
    def submit_result(self, task_id: int, result: str) -> None:
        tasks = json.loads(self.tasks_json)
        task_id = str(task_id)
        if task_id not in tasks:
            return None
        if tasks[task_id]["status"] != "open":
            return None
        task = tasks[task_id]["description"]
        rubric = tasks[task_id]["rubric"]
        agent = str(gl.message.sender_address)

        def leader_fn() -> str:
            prompt = (
                f"Judge this AI agent's work.\n"
                f"Task: {task}\n"
                f"Rubric: {rubric}\n"
                f"Result: {result[:600]}\n"
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

        tasks[task_id]["result"] = result[:500]
        tasks[task_id]["submitter"] = agent

        rep = json.loads(self.rep_json)
        if agent not in rep:
            rep[agent] = {"completed": "0", "failed": "0"}

        if verdict == "APPROVED":
            tasks[task_id]["status"] = "completed"
            rep[agent]["completed"] = str(int(rep[agent]["completed"]) + 1)
        else:
            tasks[task_id]["status"] = "failed"
            rep[agent]["failed"] = str(int(rep[agent]["failed"]) + 1)

        self.tasks_json = json.dumps(tasks)
        self.rep_json = json.dumps(rep)
        return None

    @gl.public.view
    def get_task(self, task_id: int) -> str:
        tasks = json.loads(self.tasks_json)
        task_id = str(task_id)
        if task_id not in tasks:
            return "not found"
        t = tasks[task_id]
        return f"Task: {t['description']} | Status: {t['status']} | Reward: {t['reward']}"

    @gl.public.view
    def get_reputation(self, agent: str) -> str:
        rep = json.loads(self.rep_json)
        if agent not in rep:
            return "no reputation"
        r = rep[agent]
        return f"Completed: {r['completed']} | Failed: {r['failed']}"

    @gl.public.view
    def get_count(self) -> str:
        return self.task_count

    @gl.public.view
    def get_status(self, task_id: int) -> str:
        tasks = json.loads(self.tasks_json)
        task_id = str(task_id)
        if task_id not in tasks:
            return "not found"
        return tasks[task_id]["status"]

    @gl.public.view
    def get_result(self, task_id: int) -> str:
        tasks = json.loads(self.tasks_json)
        task_id = str(task_id)
        if task_id not in tasks:
            return "not found"
        return tasks[task_id]["result"]
