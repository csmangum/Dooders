
# Dooders

![dooders logo](./docs/dooder_logo.png)

> Reality works; simulate it.  
  
## Overview

Dooders is a Python library to conduct *complex model-based simulations* for research in cognitive AI.[^1] Its primary purpose is to facilitate the exploration and analysis of advanced designs for Artificial Intelligence systems with cognitive capabilities.

Unpacking some of the terminology: 

* **Complex**: The library simulates not only a single system, but systems of systems.[^2]  
* **Model-based**: A model is like a map, it's an imperfect and simplified representation of reality.
* **Simulation**: An imitation of a system via models; executed to study the behavior.  

Systems are collections of interacting and dynamic components. These can range from the complex ecological system of the Earth's environment, the chemical system of a [reef tank](https://www.saltwateraquariumblog.com/9-most-important-reef-tank-aquarium-water-parameters/), to even digital systems such as a company's [internal network](https://online.visual-paradigm.com/servlet/editor-content/knowledge/network-diagram/what-is-network-diagram/sites/7/2020/03/network-diagram-example-internal-network-diagram.png).

Systems are everywhere.[^3]  

A [Dooder](docs/Dooder.md) is an agent object in the simulation with an amount of causal control. It acts in the simulation only as long as it consumes [Energy](https://github.com/csmangum/Dooders/blob/main/docs/Energy.md).

Take a look on how a Dooder will [learn and act](https://github.com/csmangum/Dooders/blob/main/docs/Learning.md), get an overview of the [core components](https://github.com/csmangum/Dooders/blob/main/docs/Core.md) of the library, or read [why I started the project](https://github.com/csmangum/Dooders/blob/main/docs/Why.md).

This project is a space where I can experiment, learn more about complexity theory and gain a deeper understanding of concepts like feedback loops, attractors, adaptation, etc.

I will also be documenting experiments in [substack](https://rememberization.substack.com/p/experiment-list). Including the results from my [first experiment](https://rememberization.substack.com/p/experiment-1-single-simulation).

***The code, content, and concepts will change over time as I explore different ideas.***  
  
### How to use it

```python
from dooders import Experiment

experiment = Experiment()

experiment.simulate()

experiment.experiment_summary()


# Example output using the default settings
# This simulation ended after 53 cycle when 
# all Dooders died from starvation

{'SimulationID': 'XGZBhzoc8juERXpZjLZMPR',
 'Timestamp': '2023-03-09, 18:20:33',
 'CycleCount': 53,
 'TotalEnergy': 634,
 'ConsumedEnergy': 41,
 'StartingDooderCount': 10,
 'EndingDooderCount': 0,
 'ElapsedSeconds': 0,
 'AverageAge': 14}
```
For more details, see the [Quick Start guide](docs/QuickStart.md).  

### Future Plans

| Idea                                                                                          | Description                                                                                                                                                  |
| :-------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Full featured interface                                                                       | Responsive UI with many dashboards showing the simulation results                                                                                            |
| Dockerize deployment                                                                          | Make it simple to spin up the entire platform                                                                                                                |
| Cognition model | Build out the Dooder capability to take in information and evaluate its value                                                                                |
| Reproduction model                                                                            | Design a function to combine the Genetic models of two Dooders                                                                                               |
| Continuous time                                                                               | Switch from step based, to continuous time. Brings on tons of potential issues                                                                               |
| Performance & Efficiency                                                                      | Right now I'm focused on function and composition but that will quickly hit the performance wall if I don't optimize at some point                           |
  
### Footnotes

[^1]: [Here](https://towardsdatascience.com/the-rise-of-cognitive-ai-a29d2b724ccc) is a great reference outlining cognitive AI
[^2]: Complex systems have a number of components with non-linear (random or unpredictable) relationships.  
[^3]: A great book about complex systems is [Thinking in Systems](https://www.amazon.com/Thinking-Systems-Donella-H-Meadows/dp/1603580557/ref=nodl_?dplnkId=c7d91e2b-3d9e-4f2f-b62d-b83301ddb81d)
