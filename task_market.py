# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *

class MultiAgentPro(gl.Contract):
    task_count: u256
    tasks: gl.TreeMap[u256, str]
    rubrics: gl.TreeMap[u256, str]
    rewards: gl.TreeMap[u256, u256]
    results: gl.TreeMap[u256, str]
    submitters: gl.TreeMap[u256, str]
    status: gl.TreeMap[u256, str]
    rep_completed: gl.TreeMap[str, u256]
    rep_failed: gl.TreeMap[str, u256]

    def __init__(self):
        self.task_count = 0

    @gl.public.write
    def post_task(self, description: str, rubric: str) -> None:
        reward = gl.message.value
        if reward == 0:
            raise Exception("Must send nonzero reward")
        task_id = self.task_count
        self.tasks[task_id] = description[:500]
        self.rubrics[task_id] = rubric[:300]
        self.rewards[task_id] = reward
        self.status[task_id] = "open"
        self.task_count = self.task_count + 1

    @gl.public.write
    def submit_result(self, task_id: u256, result: str) -> None:
        if self.status[task_id] != "open":
            raise Exception("Task not open")
        task = self.tasks[task_id]
        rubric = self.rubrics[task_id]
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

        self.results[task_id] = result[:500]
        self.submitters[task_id] = agent

        prev_completed = self.rep_completed.get(agent) or u256(0)
        prev_failed = self.rep_failed.get(agent) or u256(0)

        if verdict == "APPROVED":
            self.status[task_id] = "completed"
            self.rep_completed[agent] = prev_completed + u256(1)
            reward = self.rewards[task_id]
            gl.chain.account(gl.message.sender_address).emit_transfer(reward)
        else:
            self.status[task_id] = "failed"
            self.rep_failed[agent] = prev_failed + u256(1)

    @gl.public.view
    def get_task(self, task_id: u256) -> str:
        return f"Task: {self.tasks[task_id]} | Rubric: {self.rubrics[task_id]} | Status: {self.status[task_id]} | Reward: {self.rewards[task_id]}"

    @gl.public.view
    def get_reputation(self, agent: str) -> str:
        completed = self.rep_completed.get(agent) or u256(0)
        failed = self.rep_failed.get(agent) or u256(0)
        return f"Completed: {completed} | Failed: {failed}"

    @gl.public.view
    def get_count(self) -> str:
        return str(self.task_count)

    @gl.public.view
    def get_status(self, task_id: u256) -> str:
        return self.status[task_id]

    @gl.public.view
    def get_result(self, task_id: u256) -> str:
        return self.results[task_id]
