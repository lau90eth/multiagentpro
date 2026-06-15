# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import json

class MultiAgentPro(gl.Contract):
    task_count: u256
    tasks_json: str
    rep_json: str

    def __init__(self):
        self.task_count = 0
        self.tasks_json = "{}"
        self.rep_json = "{}"

    def _get_tasks(self) -> dict:
        return json.loads(self.tasks_json)

    def _set_tasks(self, d: dict):
        self.tasks_json = json.dumps(d)

    def _get_rep(self) -> dict:
        return json.loads(self.rep_json)

    def _set_rep(self, d: dict):
        self.rep_json = json.dumps(d)

    @gl.public.write
    def post_task(self, description: str, rubric: str) -> None:
        task_id = int(self.task_count)
        tasks = self._get_tasks()
        tasks[str(task_id)] = {
            "description": description[:500],
            "rubric": rubric[:300],
            "status": "open",
            "result": "",
            "submitter": ""
        }
        self._set_tasks(tasks)
        self.task_count = self.task_count + 1

    @gl.public.write
    def submit_result(self, task_id: u256, result: str) -> None:
        tasks = self._get_tasks()
        tid = str(int(task_id))
        if tid not in tasks:
            raise Exception("Task not found")
        if tasks[tid]["status"] != "open":
            raise Exception("Task not open")
        task = tasks[tid]["description"]
        rubric = tasks[tid]["rubric"]
        agent = str(gl.message.sender_address)

        def leader_fn() -> str:
            prompt = (
                f"You are a fair judge evaluating an AI agent's work.\n\n"
                f"Task: {task}\n\n"
                f"Evaluation rubric: {rubric}\n\n"
                f"Submitted result: {result[:800]}\n\n"
                f"Does the result satisfy the rubric? Reply ONLY: APPROVED or REJECTED"
            )
            return gl.nondet.exec_prompt(prompt).replace('\x00', '').strip()

        def validator_fn(leaders_res) -> bool:
            if not isinstance(leaders_res, gl.vm.Return):
                return False
            r = leaders_res.calldata
            return isinstance(r, str) and r.strip() in ("APPROVED", "REJECTED")

        verdict = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        verdict = verdict.replace('\x00', '').strip()

        tasks[tid]["result"] = result[:500]
        tasks[tid]["submitter"] = agent

        rep = self._get_rep()
        if agent not in rep:
            rep[agent] = {"completed": 0, "failed": 0}

        if verdict == "APPROVED":
            tasks[tid]["status"] = "completed"
            rep[agent]["completed"] += 1
        else:
            tasks[tid]["status"] = "failed"
            rep[agent]["failed"] += 1

        self._set_tasks(tasks)
        self._set_rep(rep)

    @gl.public.view
    def get_task(self, task_id: u256) -> str:
        tasks = self._get_tasks()
        tid = str(int(task_id))
        if tid not in tasks:
            return "Task not found"
        t = tasks[tid]
        return f"Task: {t['description']} | Rubric: {t['rubric']} | Status: {t['status']}"

    @gl.public.view
    def get_reputation(self, agent: str) -> str:
        rep = self._get_rep()
        if agent not in rep:
            return "No reputation yet"
        r = rep[agent]
        return f"Completed: {r['completed']} | Failed: {r['failed']}"

    @gl.public.view
    def get_count(self) -> str:
        return str(self.task_count)

    @gl.public.view
    def get_status(self, task_id: u256) -> str:
        tasks = self._get_tasks()
        tid = str(int(task_id))
        if tid not in tasks:
            return "not found"
        return tasks[tid]["status"]
