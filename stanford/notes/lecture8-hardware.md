# Deep Learning hardware

## GPU vs CPU

Both can execute commands.

Overall, CPU's are more general-purpose, GPU's are better for running lots of small operations that can occur concurrently. The perfect example of a thing a GPU is better at is matrix multiplication.

So yeah GPU much better for CNN.

### GPU

Graphics processing unit. These use much more power that CPUs. There are two main brands, Nvidia vs AMD.

Thousands of cores, so thousands of threads. None of these cores are very powerful though, and they often cannot function independently. They are expected to perform operations together toward a common outcome.

Slower clock speed.

Good for *concurrency* especially if the concurrent behavior is simple and uniform.

GPU's have their own RAM built-in RAM, like 8GB.

#### Why Nvidia is better

They are trying to make their graohics cards good for deep learning.

### CPU

Central Processing Unit.

Has up to maybe 10 cores, so 20 threads at once max. These threads are very powerful.

Very small amount of its own memory, uses system memory.


## GPU Coding

There are languages that exist that let you code directly on to GPU's. The main one is **CUDA** by nvidia, but it is a pain in the ass. There are libraries for this language that are pretty ok, so you generally never actually use CUDA. All of this only works on CUDA though. 

Nvidia has some official CUDA libraries that are very well optimized. These libraries are generally about 3x faster than hand-written CUDA in the open source community (cuDNN).

Another language called OPEN-CL works on all GPU's not just nvidia, but it's kind of slower.

## Benchmarking

It is very very easy to sneakily be unfair in benchmark comparisons of stuff to do with deep learning, so be wary unless you actually understand how you're supposed to run the things being benchmarked.

## GPU communication

Communication between the GPU and the rest of the system can be quite slow by comparison. It is possible that reading the data and sending it to your GPU might be your bottleneck.

### Solotuions:

1. use SSD
3. load your entire dataset into RAM
2. use multiple CPU threads to load bits of the dataset into ram as needed and then quickly feed it into the GPU on request (hard)


## In practice

Try not to run everything sequentially. Have like, one thread reading the data, another getting the CPU to run on that data, one thread synchronizing, etc. Luckily people have written software for this.