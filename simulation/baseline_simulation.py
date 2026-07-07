import traci

from TrafficMetrics import TrafficMetrics

class BaselineSimulation:

    def __init__(self):

        self.metrics = TrafficMetrics()

    def run(self):

        traci.start([
            "sumo",
            "-c",
            "projekt.sumocfg"
        ])

        while traci.simulation.getMinExpectedNumber() > 0:

            traci.simulationStep()

            self.metrics.update()

        traci.close()

        return self.metrics.get_results()
