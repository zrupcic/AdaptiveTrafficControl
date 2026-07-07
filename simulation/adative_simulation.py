import traci

from TrafficMetrics import TrafficMetrics
from AdaptiveTrafficControllerV3 import AdaptiveTrafficControllerV3

class AdaptiveSimulation:

    def __init__(self):

        self.metrics = TrafficMetrics()

        self.controller = None

    def run(self):

        traci.start([
            "sumo",
            "-c",
            "projekt.sumocfg"
        ])

        # Create adaptive controller
        self.controller = AdaptiveTrafficControllerV3(
            "288198771", #hardcoded for the intersection we're using in the project
            "network.net.xml"
        )

        while traci.simulation.getMinExpectedNumber() > 0:

            traci.simulationStep()

            # Adaptive control
            self.controller.control_step()

            # Collect metrics
            self.metrics.update()

        traci.close()

        result = self.metrics.get_results()

        result.green_extensions = self.controller.extensions

        return result
