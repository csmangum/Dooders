# Movement Policy

Develop and test different movement possibilities for a Dooder

## Goals

- [ ] Create a movement system that allows the Dooder to move in 1 of 9 directions (includes the current position)
- [ ] Develop and test three movement policies (Random, Rule-based, and Simple Neural Network)
- [ ] Determine which policy maximizes Energy consumption and a Dooder's lifespan

## Requirements

- Input: The Dooder object which will have the current position and details about its neighboring locations
- Output: The recommended position a Dooder should move to
- Action: The Dooder will move to the recommended position and consume Energy, if there is any

## Plan

1. Create a Policy class to register and manage the different movement policies
2. Create each Movement policy
3. Adapt Dooder class to use the Movement policy

## Details

### RandomMove
This policy will take a list of all adjacent locations and will choose a random location 

### RuleBased
This policy will identify all neighboring objects and creates a list of locations with energy. Then a random locstion is chosen, if there are no neighboring energy objects, the Dooder will not move.

### Simple Artificial Neural Network


## Thoughts