import matplotlib.pyplot as plt

class ResultPlotter:

    def __init__(self):

        pass

    def plot_metric(
            self,
            title,
            baseline,
            adaptive,
            filename):

        plt.figure(figsize=(6,4))

        bars = plt.bar(
            ["Baseline", "Adaptive"],
            [baseline, adaptive]
        )

        plt.title(title, fontsize=14)
        plt.ylabel(title)

        plt.grid(axis="y", alpha=0.3)

        for bar in bars:

            height = bar.get_height()

            plt.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"{height:.2f}",
                ha="center",
                va="bottom"
            )

        plt.tight_layout()

        plt.savefig(filename, dpi=300)

        plt.close()

    def plot_results(self, baseline, adaptive):

        self.plot_metric(
            "Throughput",
            baseline.throughput,
            adaptive.throughput,
            "throughput.png"
        )

        self.plot_metric(
            "Average Queue (vehicles)",
            baseline.average_queue,
            adaptive.average_queue,
            "average_queue.png"
        )

        self.plot_metric(
            "Maximum Queue (vehicles)",
            baseline.maximum_queue,
            adaptive.maximum_queue,
            "maximum_queue.png"
        )

        self.plot_metric(
            "Average Waiting Time (s)",
            baseline.average_waiting,
            adaptive.average_waiting,
            "average_waiting.png"
        )
