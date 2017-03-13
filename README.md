# channel-sim

## No-MIMO level of simulation

Decoding function
  When agent listens, it receives 32 blobs (one per antenna, per channel).
  Decoding function takes in each blob, and checks SINR from MIMI-unlock level of simulation. If SINR is greater than threshold specified, then return token that was received. Otherwise we return an error token.
