import traci
from sumolib import net


class AdaptiveTrafficControllerV3:

    def __init__(self, tls_id, net_file):

        self.tls = tls_id

        # Load SUMO network
        self.net = net.readNet(net_file)

        # -------------------------------------------------
        # Parameters
        # -------------------------------------------------

        self.min_green = 20
        self.max_green = 70
        self.extension = 10
        self.base_green = 40
        self.current_green_duration = self.base_green
        self.switch_threshold = 3

        self.last_phase = -1
        self.green_start_time = 0

        # -------------------------------------------------
        # Runtime state
        # -------------------------------------------------

        self.current_extensions = 0
        self.extensions = 0
        self.switches = 0

        self.current_green_duration = 40

        self.debug = True

        # -------------------------------------------------
        # Network information
        # -------------------------------------------------

        self.controlled_lanes = []

        self.approaches = {}

        self.main_approach = None

        self.side_approaches = []

        self.main_lanes = []

        self.side_lanes = []

        # -------------------------------------------------
        # Phase mapping
        # -------------------------------------------------

        self.main_green = 0
        self.main_yellow = 1
        self.side_green = 2
        self.side_yellow = 3

        # -------------------------------------------------

        print()

        print("=" * 60)

        print("AdaptiveTrafficController V3")

        print("=" * 60)

        print("Traffic light:", self.tls)

        print()

        self.initialize()

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def initialize(self):

        self.detect_controlled_lanes()

        self.build_approaches()

        self.detect_main_direction()

    # =====================================================

    def detect_controlled_lanes(self):

        print("Detecting controlled lanes...")

        controlled = traci.trafficlight.getControlledLinks(self.tls)

        lanes = set()

        for group in controlled:

            for connection in group:

                from_lane = connection[0]

                lanes.add(from_lane)

        self.controlled_lanes = sorted(list(lanes))

        print()

        for lane in self.controlled_lanes:

            print(lane)

        print()

    # =====================================================

    def build_approaches(self):

        print("Building approaches...")

        print()

        for lane_id in self.controlled_lanes:

            lane = self.net.getLane(lane_id)

            edge = lane.getEdge().getID()

            if edge not in self.approaches:

                self.approaches[edge] = []

            self.approaches[edge].append(lane_id)

        for edge in self.approaches:

            print(edge)

            for lane in self.approaches[edge]:

                print("   ", lane)

            print()

    # =====================================================

    def detect_main_direction(self):

        print()

        print("Analysing approaches...")

        print()

        longest = -1

        for edge_id in self.approaches:

            edge = self.net.getEdge(edge_id)

            length = edge.getLength()

            print(f"{edge_id:25s} {length:8.1f} m")

            if length > longest:

                longest = length

                self.main_approach = edge_id

        print()

        print("Main approach:", self.main_approach)

        self.main_lanes = self.approaches[self.main_approach]

        for edge in self.approaches:

            if edge != self.main_approach:

                self.side_approaches.append(edge)

                self.side_lanes.extend(self.approaches[edge])

        print()

        print("Main lanes")

        for lane in self.main_lanes:

            print("   ", lane)

        print()

        print("Side lanes")

        for lane in self.side_lanes:

            print("   ", lane)

        print()

    # =====================================================

    def get_queue(self, lanes):

        queue = 0

        for lane in lanes:

            queue += traci.lane.getLastStepHaltingNumber(lane)

        return queue

    # =====================================================

    def get_main_queue(self):

        return self.get_queue(self.main_lanes)

    # =====================================================

    def get_side_queue(self):

        return self.get_queue(self.side_lanes)

    # =====================================================

    def update_phase_information(self):

        phase = traci.trafficlight.getPhase(self.tls)

        if phase != self.last_phase:

            self.last_phase = phase

            self.green_start_time = traci.simulation.getTime()

            self.current_extensions = 0
            self.current_green_duration = self.base_green

            if self.debug:

                print()
                print("----------------------------------------")
                print("NEW PHASE:", phase)
                print("Simulation time:", self.green_start_time)

        return phase

    # =====================================================

    def elapsed_green(self):

        return traci.simulation.getTime() - self.green_start_time

    # =====================================================

    def is_main_green(self, phase):

        return phase == self.main_green

    # =====================================================

    def control_step(self):

        phase = self.update_phase_information()

        #
        # Continue only when the light is green on main traffic light
        #

        if not self.is_main_green(phase):
            return

        #
        # Green light should stay on for at least min_green time 
        #

        elapsed = self.elapsed_green()

        if elapsed < self.min_green:
            return

        #
        # Queue calculation
        #

        main_queue = self.get_main_queue()

        side_queue = self.get_side_queue()

        #
        # Debug
        #

        if self.debug:

            print()

            print("=" * 60)

            print("STEP :", int(traci.simulation.getTime()))

            print("Phase:", phase)

            print("Elapsed green:", elapsed)

            print("Main queue:", main_queue)

            print("Side queue:", side_queue)

        #
        # Decision
        #

        if main_queue >= side_queue + self.switch_threshold:

            if self.current_green_duration < self.max_green:

                self.current_green_duration += self.extension

                if self.current_green_duration > self.max_green:

                    self.current_green_duration = self.max_green

                traci.trafficlight.setPhaseDuration(
                    self.tls,
                    self.current_green_duration
                )

                self.current_extensions += 1

                self.extensions += 1

                print(">>> EXTEND GREEN")

        else:

            if self.debug:

                print(">>> KEEP PROGRAM")

    # -------------------------------------------------
    # STATISTICS
    # -------------------------------------------------

    def report(self):

        print()
        print("="*50)
        print("Controller statistics")
        print("="*50)

        print("Green extensions :", self.extensions)
        print("Phase switches   :", self.switches)
