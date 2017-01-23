# PyOrbit
PyOrbit is a simple orbit simulation which uses the gravitational force equation to calculate a force between a fixed body (ressembling a star) and other orbiting bodies. The oribiting bodies also interact with each other using the same principles.
![Alt Text](https://media.giphy.com/media/l0ExlQ8Ob4hzqA5va/source.gif)

# Setup and customisation
PyOrbit allows you to change every aspect of the simulations. Including the gravitational constant, mass of the fixed body, mass of the orbitting bodies, inital vector velocity of the orbiting bodies and more

# Variable definitions
Withing the Planet object:
  * vel - the inital vecloity of the orbiting object
  * mass - the mass of the orbiting object, this will be used to find the gravitational force between the bodies
  * pos - the inital position of the orbiting object
  * pathLength - the number of points the trail behind the object can be
  * size - the size of the object, this is calculated using the mass of the object
  
  
