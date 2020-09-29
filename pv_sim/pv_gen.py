# SPDX-License-Identifier: BSD-3-Clause


class PVGenerator(object):
    """This class is the interface of the generators for the photo voltaic 
    (PV) system values

    :param generator: The object that implements the generation of PV values
    """

    def __init__(self, generator):
        self.generator = generator

    def gen_value(self, time):
        """ Calls the gen method of the generator. Every generator must 
        implement the gen method

        :param time: The current time of the simulation, in seconds.
        :type: float
        """
        return self.generator.gen(time)


class PVFile(object):
    """ This class implements the generation of PV values by fetching values
     from a provided file

    :param pv_file: the location and name of the file
    :type pv_file: str
    """

    def __init__(self, pv_file):
        pv_file = open(pv_file, 'r')
        self.times = []
        self.power_values = {}
        for entry in pv_file.readlines():
            time, pv_value = entry.strip('\n').split(',')
            # The times are stored in a list, so we can retrieve the nearest
            # entry to a time not in the dataset
            self.times.append(float(time))
            self.power_values[float(time)] = float(pv_value)
        pv_file.close()

    def gen(self, time):
        """ Returns the PV value associated with a provided time. Every 
        generator must implement this method

        :param time: The current time of the simulation, in seconds.
        :type time: float
        """

        # As the provided time may not match the provided sample, the method
        # picks the value associated with the closest entry.
        closest_time = min(self.times, key=lambda x: abs(x-time))
        return self.power_values[closest_time]
