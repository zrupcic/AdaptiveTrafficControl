from baseline_simulation import BaselineSimulation
from adaptive_simulation import AdaptiveSimulation
from result_exporter import ResultExporter
from result_plotter import ResultPlotter

class ExperimentRunner:

    def __init__(self):

        self.baseline = None
        self.adaptive = None

    def run(self):

        print()
        print("=" * 60)
        print("RUNNING BASELINE SIMULATION")
        print("=" * 60)

        self.baseline = BaselineSimulation().run()
        self.baseline.name = "Baseline"

        print()
        print("=" * 60)
        print("RUNNING ADAPTIVE SIMULATION")
        print("=" * 60)

        self.adaptive = AdaptiveSimulation().run()
        self.adaptive.name = "Adaptive"

        print()
        print("=" * 60)
        print("EXPERIMENT FINISHED")
        print("=" * 60)

        self.baseline.print()

        self.adaptive.print()

        self.compare_results()

        exporter = ResultExporter()

        exporter.export(
            self.baseline,
            self.adaptive
        )

        print()
        print("Results exported to results.csv")

        plotter = ResultPlotter()

        plotter.plot_results(
            self.baseline,
            self.adaptive
        )

        print("Graphs exported.")
        
    def compare_results(self):

        print()
        print("=" * 60)
        print("COMPARISON")
        print("=" * 60)

        self.compare_metric(
            "Throughput",
            self.baseline.throughput,
            self.adaptive.throughput,
            higher_is_better=True
        )

        self.compare_metric(
            "Average queue",
            self.baseline.average_queue,
            self.adaptive.average_queue,
            higher_is_better=False
        )

        self.compare_metric(
            "Maximum queue",
            self.baseline.maximum_queue,
            self.adaptive.maximum_queue,
            higher_is_better=False
        )

        self.compare_metric(
            "Average waiting",
            self.baseline.average_waiting,
            self.adaptive.average_waiting,
            higher_is_better=False
        )

    def compare_metric(self, name, baseline, adaptive, higher_is_better):

        if baseline == 0:
            improvement = 0

        else:

            if higher_is_better:
                improvement = (adaptive - baseline) / baseline * 100
            else:
                improvement = (baseline - adaptive) / baseline * 100

        print()

        print(name)

        print(f"   Baseline : {baseline:.2f}")
        print(f"   Adaptive : {adaptive:.2f}")
        print(f"   Improvement : {improvement:.2f}%")
