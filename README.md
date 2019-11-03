# antsim
A simulation where ants struggle to survive on finite ressources.

Executing the programm will create an ant.mp4 file in the subfolder results. This mp4 is a movie where one frame equals one timestep in the simulation.

## Installation
Requires Python 3.7, tested with Python 3.7.5

To install this programm on Linux machines please follow these steps:
1. go to project directory
2. enter:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
now you should have all needed packages in your virtualenviroment and you can run main.py

## Usage
You can change various settings in the settings.txt file:
* number_of_turns -> how many turns are simulated. The higher the number, the longer it will take.
* number_of_ants  -> how many starting ants are on the board.
* field_size      -> sets the size of the playing board. The board is quadratic so only input one integer.
* maximum_age     -> how old ants can get. Equals number of turns ants are alive.

To run the programm simple execute the main.py function.
```
python3 ant_main.py
```

## Modules
**antsim** provides you with the following Modules:
* [controller](src/controller.py): Coordinates all functionalities
* [field](src/field.py): Implements the playing board and the creation of the mp4
* [objects](src/objects.py): Implements all the playing figueres, like the ants, the food and the hive.
* [utils](src/utils.py): Some support functions
* [errors](src/errors.py): One custom error, raised when ant can't move
* [test area](src/test_area.py): unittests to guarantee working functions
