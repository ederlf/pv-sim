# pvsim

Pvsim is a very basic tool to simulate the generation of output values from a photo voltaic system along with the simulated measurement of a household meter.

## Installation

0. **Check your Python version**

The code requires functionalities of Python above 3.6. Thus, make sure your systems has a proper version.

```bash
$ python -V
```

or

```bash
$ python3 -V
```

1. **Install and start RabbitMQ** 

This might be tricky depending on the version of your OS. In Ubuntu 16.04 and 18.04, it is as simple as:

```bash
$ sudo apt-get install erlang
$ sudo apt-get install rabbitmq-server
$ sudo systemctl start rabbitmq-server
```

For more information about installing RabbitMQ in Ubuntu and Debian systems,
go to the [official documentation](https://www.rabbitmq.com/install-debian.html).

2. **Install the required Python packages (You need to install pip if you do not have it)**

```bash
$ pip install -r requirements.txt
```

## Usage

The most basic way to use the simulator is to use the run.py script. The file is found in the folder pv_sim. We assume that the commands are executed from this the pv_sim folder, however the script can be execute from different locations. 

The script has multiple options to configure the meter and the photo voltaic
simulators. You can check the options with:

```bash
$ python run.py -h
```

The current implementation selects PV values according to file samples. An example of a file is provided in the data directory (Jul2013.csv). This data comes from this [dataset](http://www.networkrevolution.co.uk/project-library/dataset-tc5-enhanced-profiling-solar-photovoltaic-pv-users/).

To run a test using the sample file do:

```bash
$ python run.py --pv_gen_file ../data/Jul2013.csv
```

The execution of the command above will generate a file named pv-data.csv in your working directory. The is a CSV that contains:

```
Timestamp,MeterValue,PVValue,MeterValue+PVValue
```

The timestamp format is the number of seconds since [Epoch](https://en.wikipedia.org/wiki/Unix_time). This choice makes it much easier to 
further process the data, rather than using a human readable timestamp.

The unit of the MeterValue, PVValue and the sum of both are in Kw.

# Extending the code

Currently the simulator only supports RabbitMQ as message broker and picks PV values from file samples. 

Adding another message broker is just a matter of creating a class to the broker and adding to the interface when creating a MsgBroker.

The same is true for the PV generation. Other implementations are just a matter of creating a class that implements the number generation and passing it to a PVGenerator. For example, one can create a class that uses an equation, a probabilistic method or another way to generate PV values. 

The main takeaway here is that extensibility is possible thanks to the use of composition.

# Running tests

There are only a few tests that test picking a value from a file sample. 
To run them, execute:

```bash
$ cd tests
$ python -m unittest pvsim_test.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[BSD 3-Clause License](https://choosealicense.com/licenses/bsd-3-clause/)
