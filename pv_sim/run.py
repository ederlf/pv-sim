import argparse
import sys
import threading
import meter
import msgbroker
import pv_gen
import pv

parser = argparse.ArgumentParser()

# Broker arguments
parser.add_argument(
    "-b", "--broker", help="Chooses the msg broker. If not set, the simulator "
    "uses rabbitmq", default="rabbitmq")
parser.add_argument(
    "--broker_ip", help="Sets the IP location of the broker. If not set, "
    "localhost (127.0.0.1) is used")
parser.add_argument(
    "--broker_port", help="Sets the TCP port used to connect to the broker. If"
    " not set, uses the default of the selected broker")

# Meter arguments
parser.add_argument("-d", "--duration", type=int,
                    help="Sets the duration of the simulated time, in seconds."
                    "If not set, defaults to one day (86400 seconds)",
                    default=86400)
parser.add_argument("-s", "--step", type=int,
                    help="Sets the advance of time and the interval of meter "
                    "messages, in seconds. If not set, the simulator uses 5 "
                    "seconds If not set, defaults to one day (86400 seconds)",
                    default=5)
parser.add_argument("--seed", type=int,
                    help="Sets the seed for the random number generation. If "
                    "not set, the simulator uses 42", default=42)

#!/usr/bin/env python
# SPDX-License-Identifier: BSD-3-Clause

# PVSim arguments
parser.add_argument("--pv_gen",
                    help="Sets the form of generation of PV values. By "
                    "default, it retrieves values from data files",
                    default="file")
parser.add_argument("--pv_gen_file",
                    help="Set the file used to retrieve PV values.")
parser.add_argument("--out_file",
                    help="Sets the output file of the PV simulator. By the "
                    "default, the data is saved in the execution directory, as"
                    " pv-data.csv",
                    default="pv-data.csv")


def main():

    args = parser.parse_args()

    # PV Thread
    pv_broker = msgbroker.broker_factory(args.broker, args.broker_ip,
                                         args.broker_port)

    # Chooses a PV generator. For now there is only support to files.
    pv_generator = None
    if args.pv_gen == "file":
        if args.pv_gen_file:
            pv_generator = pv_gen.PVGenerator(pv_gen.PVFile(args.pv_gen_file))
        else:
            print("Error: The PV generator is of type \"file\". You must pass "
                  "a file name with --pv_gen_file FILENAME\n")
            sys.exit(0)

    if pv_generator:
        pv_sim = pv.PVSim(pv_generator, pv_broker)
        pv_thread = threading.Thread(target=pv_sim.run)
        pv_thread.start()
    else:
        print("Error: You must define a value generator for the PV system. "
              " --pv_gen\nTip: the simulator uses file by default, so you "
              "might be missing the file name")
        sys.exit(0)

    # Meter Thread
    meter_broker = msgbroker.broker_factory(args.broker, args.broker_ip,
                                            args.broker_port)
    meter_sim = meter.Meter(args.duration, args.step, meter_broker, args.seed)
    meter_thread = threading.Thread(target=meter_sim.run)
    meter_thread.start()


if __name__ == '__main__':
    main()
