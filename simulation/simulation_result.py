class SimulationResult:

    def __init__(self):

        self.name = ""

        self.steps = 0

        self.throughput = 0

        self.average_queue = 0

        self.maximum_queue = 0

        self.average_waiting = 0

        self.green_extensions = 0

    def print(self):

        print()
        print("=" * 60)
        print(self.name)
        print("=" * 60)

        print(f"Simulation steps : {self.steps}")
        print(f"Throughput       : {self.throughput}")
        print(f"Average queue    : {self.average_queue:.2f}")
        print(f"Maximum queue    : {self.maximum_queue}")
        print(f"Average waiting  : {self.average_waiting:.2f}")

        if self.green_extensions > 0:
            print(f"Green extensions : {self.green_extensions}")

        print("=" * 60)
