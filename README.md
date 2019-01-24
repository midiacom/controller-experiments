# TODO

`sudo apt install tcpreplay`

- [X] Implement topology: h1 <-> s1 <-> h2
- [X] Experiment script:
  - [x] First draft
  - [X] Capture controller log
  - [X] Capture mininet log
  - [X] Implement scapy script to generate several packets with different sources
- [ ] Test with different controllers, such as:
  - [ ] ONOS
  - [ ] OpenDaylight
  - [ ] Ryu
- [ ] Results script:
  - [ ] Parse the .pcaps to .csv
  - [ ] Measure the delay between the source, the switch, the controller and the destination
  - [ ] Draw graphs
