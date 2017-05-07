# channel-sim

#Architecture
The basic unit of this project is a node. Nodes are owned by 
either an agent or a bot. Agents will run a given program in response
to input given by players, while bots will be running one of a set of 
prespecified programs. 

Each node will be placed on a simulated field, where the start position
and the way the nodes move will be according to a scenario. The distance
between nodes will determine the gains recieved.

In addition, there will be a set of traffic and sink nodes.
Agents can randomly receive traffic from traffic nodes, which must be 
delivered to a destination sink node. This determines the score. 

#Operation
The standard data unit is a blob, a sequence of complex numbers.
At each time step, agents can listen or transmit. 
If they listen, they recieve 32 blobs, representing 2 antennae on 16 channels.
If they transmit, they can instead send 32 blobs. 

The simulation will run on 3 different levels. 
The lowest level is analog simulation, where the programs will recieve a sequence of complex numbers
from each antenna and have to interpret.
The second level is where each the program calculates a Signal-to-Interference-Plus-Noise (SINR) power ratio from two blobs, then returns a data token if it is high enough.

The third level will calculate SINR from only 1 blob, and return a data token as above. 

## No-MIMO level of simulation

Decoding function
  * When agent listens, it receives 32 blobs (one per antenna, per channel).
  * Decoding function takes in each blob, and checks SINR from MIMI-unlock level of simulation. 
      * If SINR is greater than threshold specified, then return token that was received. Otherwise we return an error token.
