#!/usr/bin/env python3
import random
import math


class Ticket:
    last = -1

    def __init__(self):
        self.pos = -1
        self.ended_ok = False
        self.time_in_queue = 0
        self.state = "default"


class Simulation:
    def __init__(self):
        self.u = 0.5
        self.hl = 0.45
        self.p = 0.4
        self.p1 = self.p
        self.p2 = 1 - self.p
        self.denial_count1 = 0
        self.denial_count2 = 0

        self.ticket1 = 0
        self.ticket2 = 0

        self.iterations = 1000000
        #  self.iterations = 10
        self.queue_max = 1

    def imitate(self, input_stream):
        queue_count = 0
        denial_count1 = 0
        denial_count2 = 0

        output_stream1 = 0
        output_stream2 = 0

        link = 0

        link = input_stream[0][1]
        current_request = 1
        current_time = input_stream[0][0]
        while current_request < len(input_stream):
            if input_stream[current_request][0] < current_time:
                if link == 0:
                    link = input_stream[current_request][1]
                else:
                    if link == 1:
                        if queue_count == 0:
                            queue_count = input_stream[current_request][1]
                        if queue_count == 1:
                            if input_stream[current_request][1] == 1:
                                denial_count1 += 1
                            else:
                                denial_count2 += 2
                        if queue_count == 2:
                            if input_stream[current_request][1] == 2:
                                denial_count2 += 1
                            else:
                                queue_count = 1
                                denial_count2 += 1
                    if link == 2:
                        if input_stream[current_request][1] == 1:
                            link = 1
                            if queue_count == 0:
                                queue_count = 2
                            else:
                                denial_count2 += 1
                        if input_stream[current_request][1] == 2:
                            if queue_count == 0:
                                queue_count = 2
                            else:
                                denial_count2 += 1

                current_request += 1
            else:
                if link > 0:
                    if queue_count > 0:
                        current_time += -math.log(random.uniform(0.0, 1.0)) / self.u
                        if link == 1:
                            output_stream1 += 1
                        else:
                            output_stream2 += 1
                        link = queue_count
                        queue_count = 0
                    else:
                        if link == 1:
                            output_stream1 += 1
                        else:
                            output_stream2 += 1
                        link = 0
                        current_time = input_stream[current_request][0] + -math.log(random.uniform(0.0, 1.0)) / self.u

        self.denial_count1 = denial_count1
        self.denial_count2 = denial_count2

    def start(self):
        request_stream = []
        current_time = 0.0
        counter = 0

        while counter < self.iterations:
            current_time += -math.log(random.uniform(0.0, 1.0)) / self.hl
            val = random.uniform(0.0, 1.0)
            if val <= self.p:
                self.ticket1 += 1
                request_stream.append((current_time, 1))
            else:
                self.ticket2 += 1
                request_stream.append((current_time, 2))
            counter += 1

        self.imitate(request_stream)

        print("Q1 =", 1 - self.denial_count1 / self.ticket1)
        print("Q2 =", 1 - self.denial_count2 / self.ticket2)


if __name__ == '__main__':
    simulation = Simulation()
    simulation.start()
