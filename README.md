# Elevator_Simulation_Django
An Elevator System design made using Django, MySQL and DRF.

What does Simulation can do :
1. Create an Elevator System with N elevators
2. Make an elevator non operational
3. When call(s) are made from multiple floors, a FCFS algorithm is used to get the nearest elevator for each call.
4. Record all requests made to an elevator.

# Thought Process 

1. There should be a single class (System) to take requests for the API Calls.
2. There are variables which are only initialised once and never changes throughout the lifecycle of the application. (Cache is used)
3. We can mark an elevator as out of use and these elevators must be omitted when a request is made.
4. When a list of requests is made, an algorithm is used to find the nearest elevator and the life is marked as in moving state,
so this elevator is not selected again by any other request.
5. All requests to any elevator should be recorded, hence a schema is needed.

# APIs endpoints :

/api/elevator/initialise : Takes number of lifts, nax_floor and min_floor and staring points as a parameter

/api/elevator/patch : Make a lift out of use or change the door status

/api/elevators/call : Take a list of floors as a parameter and returns the nearest elevator for each floor

/api/elevator/moving_status = Get the direction in which the elevator is moving

/api/elevator/get_destination = Get the destination in which the elevator is currently

/api/elevator/get_requests = Get all requests for an elevator made so far.


# Library/Framework

1. Django
2. DRF
3. VirtualEnv

# Steps to setup

1. Clone the repository
2. Run pip install -r requirements.txt (PIP, Django must be installed in the system)
3. python manage.py runserver

