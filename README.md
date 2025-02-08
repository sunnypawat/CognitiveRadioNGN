# Cognitive Radio for Next Generation Network

### About
This is the git repository for the Cognitive Radio Project for the NEXT GENERATION NETWORK class at UNITN

This is a project developed by xxxxx, xxxxxx, and xxxxxx, as the exam for the Next Generation Network course at the University of Trento

### Assignment
- Expanding the lab experience on walkie-talkie, develop a cognitive walkie-talkie or WiFi transmission system
- The system is capable of sensing available communication channels and automatically switching to a free channel for transmission
- The receiver should be able to decode all channels simultaneously
- The cognitive transmitter can either transmit an NBFM signal (walkie-talkie) or WiFi-like (of course with very limited bandwidth)

### Configuration
- 2 USRPs (One for the transmitter and one for the receiver)
- Computer (Linux) installed with gnuradio

## Setup
### Installing gnuradio on Linux
If you have a modern Ubuntu, you might simply try with
`sudo apt-get install gnuradio`

If this fails, try adding the repos first:
```
sudo add-apt-repository ppa:gnuradio/gnuradio-releases
sudo apt-get update
sudo apt-get install gnuradio python3-packaging
```

To check your configuration, try starting the gnuradio GUI with
`gnuradio-companion`

### Installing gnuradio on macOS
Download and install [Radioconda](https://github.com/ryanvolz/radioconda) by following the instructions at the link 

## Run
Start by running
`gnuradio-companion`
and load [cognitive_transmitter.grc](NGN/cognitive_transmitter.grc) and [cognitive_receiver.grc](NGN/cognitive_receiver.grc)
