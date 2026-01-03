TARGET DECK: All_Cards::technical::high-performance-browser-networking::Primer on Latency and Bandwidth

Q: What is latency?                        
A: The time from the source sending a packet to the destination receiving it.
<!--ID: 1767473356073-->

Q: What is bandwidth?
A: bandwidth is the maximum throughput of a logical or physical communication path.
<!--ID: 1767473356075-->

C: bandwidth is the {maximum throughput} of a logical or physical communication path.
<!--ID: 1767473356084-->

C: {Propagation delay} - Amount of time required for a message to travel from the sender to the receiver, which is a function of distance over speed with which the signal propagates; Dicated by distance and medium.
<!--ID: 1767473356086-->

C: {Transmission delay} - Amount of time required to push all the packet's bits into the link, which is a function of the packet's length and data rate of the link; dictated by the available data rate of the transmitting link.
<!--ID: 1767473356090-->

C: {Processing delay} - Amount of time required to process the packet header, check for bit-level errors, and determine the packet's destination.
<!--ID: 1767473356092-->

C: {Queuing delay} - Amount of time the packet is waiting in the queue until it can be processed.
<!--ID: 1767473356093-->

Q: What is the last mile problem?
A: In the final segments of a telecommunications network, significant latency is introduced.
<!--ID: 1767473356077-->

C: {Latency} not {bandwidth} is the performance bottleneck for most websites.
<!--ID: 1767473356096-->

Q: What distinct advantage do optical fibers have over metal wires?
A: Each fiber can carry many wavelengths (channels) of light through a process called wavelength-division multiplexing (WDM); bandwidth then is per channel data rate times number of channels.
<!--ID: 1767473356080-->

C: High variability of {throughput} and {latency} is an inherent property of our data networks - predicting, managing, and adapting to the continuously changing "network weather" is a complex task.
<!--ID: 1767473356099-->

Q: How can we improve the performance of our applications?
A: Reduce round trips, move data closer to the client, and build applications that can hide the latency through caching, pre-fetching, and other techniques.
<!--ID: 1767473356082-->

