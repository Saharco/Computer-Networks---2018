
import numpy as np


class Queue:
    def __init__(self, size):
        self.size = size
        self.current_size = 0

    def push(self, n=1):
        if self.current_size < self.size:
            if self.current_size + n > self.size:
                num_inserted = self.size - self.current_size
                result = n - num_inserted
                self.current_size = self.size
                return result
            else:
                self.current_size += n
                return 0
        else:
            return n

    def pop(self, n):
        if self.current_size >= n:
            self.current_size -= n
            return n
        else:
            result = self.current_size
            self.current_size = 0
            return result


class State:
    def __init__(self, processed, thrown, total_wait, total_service, num_packages):
        self.processed = sum(processed)
        self.processed_per_port = processed
        self.thrown = sum(thrown)
        self.thrown_per_port = thrown
        self.average_wait = total_wait / self.processed if self.processed != 0 else 0
        self.avg_service = total_service / self.processed if self.processed != 0 else 0
        self.num_packages = num_packages


class Switch:
    def __init__(self, N, M, P, Q_sizes, mius):
        self.N = N
        self.M = M
        self.P = P
        self.Q_sizes = Q_sizes
        self.mius = mius
        self.Qs = [Queue(Q_sizes[i]) for i in range(M)]
        self.processed = [0] * M
        self.thrown = [0] * M
        self.total_wait = 0
        self.total_process_time = 0

    def tick(self, packages_per_port):
        sent_packages_per_port = [0] * self.M
        if packages_per_port is not None:
            for in_port in range(self.N):
                for out_port in np.random.choice(self.M, packages_per_port[in_port], p=self.P[in_port]):
                    sent_packages_per_port[out_port] += 1
        temp = self.total_process_time
        for out_port in range(self.M):
            max_processed = np.random.poisson(self.mius[out_port])
            sent_to_port = sent_packages_per_port[out_port]
            delta_time_per_operation = 1 / (sent_to_port + max_processed)
            order = np.random.permutation([0] * sent_to_port + [1] * max_processed)
            for i in range((sent_to_port + max_processed)):
                if order[i] == 0:
                    self.thrown[out_port] += self.Qs[out_port].push(1)
                else:
                    self.processed[out_port] += self.Qs[out_port].pop(1)
                if self.Qs[out_port].current_size != 0:
                    self.total_process_time += delta_time_per_operation
                    self.total_wait += (self.Qs[out_port].current_size - 1) * delta_time_per_operation
        return self.total_process_time - temp


    def state(self):
        return State(self.processed, self.thrown, self.total_wait, self.total_process_time, sum([k.current_size for k in self.Qs]))

    def finish(self):
        return max([self.Qs[i].current_size/self.mius[i] for i in range(self.M)])

