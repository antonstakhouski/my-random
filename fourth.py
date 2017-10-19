#!/usr/bin/env python3
import random


class Ticket:
    last = -1

    def __init__(self):
        self.pos = -1
        self.ended_ok = False
        self.time_in_queue = 0
        self.state = "default"


class Simulation:
    def __init__(self, p=0.5, pi1=0.4, pi2=0.4):
        self.p = p
        self.pi1 = pi1
        self.pi2 = pi2
        self.iterations = 100
        self.queue_max = 2
        self.out_counter = 0

    def start(self):
        tickets = []
        counter = 0
        queue = []
        channel1 = -1
        channel2 = -1
        ticket = -1

        while counter < self.iterations:
            ticket_prob = random.uniform(0.0, 1.0)

            # new ticket
            if ticket_prob < (1 - self.p):
                ticket = Ticket()
                ticket.pos = Ticket.last + 1
                Ticket.last += 1
                tickets.append(ticket)

            # channel2 state
            if channel2 > -1:
                channel2_prob = random.uniform(0.0, 1.0)
                if channel2_prob < (1 - self.pi2):
                    tickets[channel2].state = "finished"
                    channel2 = -1
                    self.out_counter += 1

            # channel1 state
            if channel1 > -1:
                channel1_prob = random.uniform(0.0, 1.0)
                if channel1_prob < (1 - self.pi1):
                    pos = channel1
                    channel1 = -1
                    if channel2 < 0:
                        channel2 = pos
                        tickets[pos].state = "ch2"
                    else:
                        tickets[pos].state = "passed"

            # ticket goes to channel1
            if channel1 < 0:
                if len(queue) > 0:
                    channel1 = queue[-1].pos
                    tickets[channel1].state = "ch1"
                    queue.pop()
                elif type(ticket) is Ticket:
                    channel1 = ticket.pos
                    tickets[channel1].state = "ch1"
                    ticket = -1

            if (len(queue) in range(0, self.queue_max + 1) and type(ticket) is Ticket) or\
                    (len(queue) == 0 and type(ticket) is Ticket and channel1 > -1):
                queue.append(ticket)
                queue[-1].state = "queue"
                ticket = -1

            if len(queue) == self.queue_max and type(ticket) is Ticket:
                tickets[ticket.pos].state = "passed"
                ticket = -1

            ticket = -1
            counter += 1

        A = self.out_counter / self.iterations
        print("A =", A)


if __name__ == '__main__':
    simulation = Simulation()
    simulation.start()