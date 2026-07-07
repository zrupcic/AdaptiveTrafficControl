import csv

class ResultExporter:

    def __init__(self, filename="results.csv"):

        self.filename = filename

    def export(self, baseline, adaptive):

        with open(self.filename, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Metric",
                "Baseline",
                "Adaptive",
                "Improvement (%)"
            ])

            self.write_metric(
                writer,
                "Throughput",
                baseline.throughput,
                adaptive.throughput,
                higher_is_better=True
            )

            self.write_metric(
                writer,
                "Average Queue",
                baseline.average_queue,
                adaptive.average_queue,
                higher_is_better=False
            )

            self.write_metric(
                writer,
                "Maximum Queue",
                baseline.maximum_queue,
                adaptive.maximum_queue,
                higher_is_better=False
            )

            self.write_metric(
                writer,
                "Average Waiting",
                baseline.average_waiting,
                adaptive.average_waiting,
                higher_is_better=False
            )

    def write_metric(
            self,
            writer,
            name,
            baseline,
            adaptive,
            higher_is_better):

        if baseline == 0:

            improvement = 0

        elif higher_is_better:

            improvement = (
                adaptive - baseline
            ) / baseline * 100

        else:

            improvement = (
                baseline - adaptive
            ) / baseline * 100

        writer.writerow([
            name,
            round(baseline, 2),
            round(adaptive, 2),
            round(improvement, 2)
        ])
