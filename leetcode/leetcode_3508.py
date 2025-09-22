import bisect
from collections import defaultdict, deque
from typing import List


class Router:
    def __init__(self, memoryLimit: int):
        """unique_packets set is for efficiently checking for duplicates.
        Timestamps are for executing getCount efficiently."""
        self.memoryLimit = memoryLimit
        self.packets = deque(maxlen=memoryLimit)
        self.unique_packets = set()
        self.timestamps = defaultdict(deque)

    def removePacket(self):
        source, destination, timestamp = self.packets.popleft()
        self.unique_packets.remove((source, destination, timestamp))
        self.timestamps[destination].popleft()
        return (source, destination, timestamp)

    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        if (source, destination, timestamp) in self.unique_packets:
            return False
        if len(self.packets) == self.memoryLimit:
            self.removePacket()
        self.packets.append((source, destination, timestamp))
        self.unique_packets.add((source, destination, timestamp))
        self.timestamps[destination].append(timestamp)
        return True

    def forwardPacket(self) -> List[int]:
        if self.packets:
            return self.removePacket()
        return []

    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        left = bisect.bisect_left(self.timestamps[destination], startTime)
        right = bisect.bisect_right(self.timestamps[destination], endTime, lo=left)
        return right - left


# Your Router object will be instantiated and called as such:
# obj = Router(memoryLimit)
# param_1 = obj.addPacket(source,destination,timestamp)
# param_2 = obj.forwardPacket()
# param_3 = obj.getCount(destination,startTime,endTime)# param_3 = obj.getCount(destination,startTime,endTime)
