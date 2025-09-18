import heapq
from typing import List


class TaskManager:
    def __init__(self, tasks: List[List[int]]):
        """Only keep dict up to date.
        When popping from sorted prio queue, check if item still correct.
            If not proceed with popping.
        """
        self.tasks = dict()
        self.sorting = list()
        for task in tasks:
            self.add(*task)

    def __str__(self):
        return f"{self.tasks=}, {self.sorting=}"

    def add(self, userId: int, taskId: int, priority: int) -> None:
        self.tasks[taskId] = (priority, userId)
        heapq.heappush(self.sorting, (-priority, -taskId))

    def edit(self, taskId: int, newPriority: int) -> None:
        _, userId = self.tasks[taskId]
        self.add(userId, taskId, newPriority)

    def rmv(self, taskId: int) -> None:
        del self.tasks[taskId]

    def execTop(self) -> int:
        while self.sorting:
            neg_prio, neg_taskId = heapq.heappop(self.sorting)
            taskId = -neg_taskId
            if taskId in self.tasks and self.tasks[taskId][0] == -neg_prio:
                # it must be in the current tasks and prio must still match, since
                # I only update the prio in the dict and push a new item when edited.
                _, userId = self.tasks[taskId]
                self.rmv(taskId)
                return userId
        return -1


# Your TaskManager object will be instantiated and called as such:
# obj = TaskManager(tasks)
# obj.add(userId,taskId,priority)
# obj.edit(taskId,newPriority)
# obj.rmv(taskId)
# param_4 = obj.execTop()
