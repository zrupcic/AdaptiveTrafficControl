import traci
from SimulationResult import SimulationResult

class TrafficMetrics:

    def __init__(self):

        # queue statistics
        self.queue_sum = 0
        self.queue_samples = 0
        self.max_queue = 0

        # waiting time
        self.waiting_sum = 0

        # throughput
        self.arrived = 0

        # simulation
        self.steps = 0

    # ---------------------------------------------------------

    def update(self):

        self.steps += 1

        #########################################################
        # QUEUE
        #########################################################

        queue = 0

        for lane in traci.lane.getIDList():

            queue += traci.lane.getLastStepHaltingNumber(lane)

        self.queue_sum += queue
        self.queue_samples += 1

        if queue > self.max_queue:
            self.max_queue = queue

        #########################################################
        # WAITING TIME
        #########################################################

        waiting = 0

        for lane in traci.lane.getIDList():

            waiting += traci.lane.getWaitingTime(lane)

        self.waiting_sum += waiting

        #########################################################
        # THROUGHPUT
        #########################################################

        self.arrived += traci.simulation.getArrivedNumber()

    # ---------------------------------------------------------

    def average_queue(self):

        if self.queue_samples == 0:
            return 0

        return self.queue_sum / self.queue_samples

    # ---------------------------------------------------------

    def average_waiting(self):

        if self.steps == 0:
            return 0

        return self.waiting_sum / self.steps

    # ---------------------------------------------------------

    def report(self):

        print("\n")
        print("=" * 60)
        print("SIMULATION RESULTS")
        print("=" * 60)

        print(f"Simulation steps : {self.steps}")
        print(f"Throughput       : {self.arrived}")
        print(f"Average queue    : {self.average_queue():.2f}")
        print(f"Maximum queue    : {self.max_queue}")
        print(f"Average waiting  : {self.average_waiting():.2f}")

        print("=" * 60)

    # =====================================================
    # Return results object
    # =====================================================

    def get_results(self):

        result = SimulationResult()

        result.steps = self.steps

        result.throughput = self.arrived

        result.average_queue = self.average_queue()

        result.maximum_queue = self.max_queue

        result.average_waiting = self.average_waiting()

        return result

