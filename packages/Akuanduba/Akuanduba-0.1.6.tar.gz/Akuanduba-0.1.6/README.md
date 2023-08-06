# Akuanduba

<p align="center">
  <img src="https://raw.githubusercontent.com/gabriel-milan/Akuanduba/master/img/Akuanduba.jpg">
</p>

Image source: [link](https://my-bestiario.fandom.com/pt-br/wiki/Akuanduba)

Akuanduba is a Python framework that eases manipulation of multiple running threads and shared resources. Its name was inspired by a god of the Brazilian mythology: Akuanduba, the god of order.

This framework's been based on the [Gaugi](https://gitlab.cern.ch/jodafons/gaugi) project, a framework that João, the author of Gaugi, presented to me.

# Top 5 reasons for Akuanduba

This is really a TL;DR section:

* Flexible;
* Easy developing and debugging;
* Robust structure;
* Effortless threading and shared resources manipulation;
* Smooth attaching and removing features from your script.

# First steps

* Clone this repository:

```
git clone https://github.com/gabriel-milan/Akuanduba
```

* Install this library:

```
pip3 install Akuanduba
```

* Go to the example script folder:

```
cd Akuanduba/examples/TimedCounterFileSaving
```

* Read the script, in order to understand what's supposed to happen when you run it:

```
vim SampleScript.py
```

* Run the example script:

```
python3 SampleScript.py
```

# The paradigm

## Base classes

Using Akuanduba, you'll have three base classes you can use to attend your needs, as they relate to one another through a common class called *Context* (this will be explained really soon). The three classes are:

* *AkuandubaTool*;
* *AkuandubaService*;
* *AkuandubaDataframe*.

**AkuandubaDataframe** is a base class for data models that will be attached to the *Context*. In other words, these *data frames* can store anything you desire and be accessible from any *tool* or *service* running on your main script. **Example:** Use data frames for storing data acquired with a service.

**AkuandubaTool** is a base class for methods that will run once on every call, processing data from any *data frame* attached to the *Context* and appending the results to another *data frame* (or even the same). *Tools* have one main method: the "execute", where all the calculations will occur every time they're called. **Example:** Use tools to process data acquired by a service and store it on a data frame.

**AkuandubaService** is a base class for parallel threads. These *services* have two main methods: "run", which is a loop that will be running parallel to the whole framework and "execute", that's executed once in every call. **Example**: Use services to acquire data.

## Other main concepts

Besides these base classes, Akuanduba relies on few other main concepts:

* *Context*;
* *DataframeManager*;
* *ToolManager*;
* *ServiceManager*;
* *AkuandubaTrigger*.

The **Context** is an abstraction that holds every single thing attached to the framework: *tools*, *services* and *data frames*. This way, everything is accessible from any other component attached to Akuanduba. Every *dataframe* you get from the context is locked to your *execute* method and released only after its execution.

The **Managers** (*DataframeManager*, *ToolManager* and *ServiceManager*) are all based on the *Manager* class, the only difference among them is that they manage different things. You can manage *data frames*, *tools* and *services*, respectively. In other words, you can attach them with the *\_\_add\_\_* operation and retrieve them with the *retrieve* method. The things you attach to these managers will run in the order you do it (execution will be better discussed later).

The **AkuandubaTrigger** is a class that inherits from *AkuandubaTool*. Its purpose is to build an object you can attach multiple hypothesis tests (that must inherit from *TriggerCondition*) and *tools* in order to trigger the *execute* method of all these *tools*. You can use three types of triggers: 'and', 'or' and 'xor', all of them self-explanatory.

## Execution

Akuanduba itself has three main methods: *initialize*, *execute* and *finalize*.

The *initialize* method follows these steps:

* Insert the framework status into the *Context*;
* Insert all the *data frames* on the *DataframeManager* into the *Context*;
* Insert all the *services* on the *ServiceManager* into the *Context*, running them;
* Insert all the *tools* on the *ToolManager* into the *Context*, running them;
* Checks for error in the *Context* initialization.

The *execute* method is the main execution loop. Its tasks are:

* Loop through the *services*, calling their *execute* methods;
* Loop through the *tools*, calling their *execute* methods;

And finally, the *finalize* method just tries to kill every thread created by the Akuanduba framework.

### Example

Let's say you have two *services* that acquire data from different sources and one single *tool* that process the whole data. You could build a script that attaches both *services* to the *ServiceManager* and the *tool* to the *ToolManager*. Let's say that, for this purpose, you've created two *data frames*, one for storing the raw data and one for the processed data. A diagram for your script's execution would be the following:

<p  align="center">

<img  src="https://raw.githubusercontent.com/gabriel-milan/Akuanduba/master/img/execution.png">

</p>

As you may see, the *run* method of the *services* acquire data in real time (∞) and append it to its own queue. On the main Akuanduba loop, the *execute* methods are called and the data is stored on the *data frames* (1 and 2). After that, the *tools* *execute* method will be called, where the data will be processed and stored on another *data frame* (3).

# To-Do! (next releases)

* Remove deprecated implementation of triggers.