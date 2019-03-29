# TODO

The experiments use the `packets.pcap` which is inside `packets.zip`.

First you need to extract the `packets.pcap` and place it inside your test-folder (either inband or outband folder).

Then, you will need to install [tcpreplay](https://linux.die.net/man/1/tcpreplay). Tcpreplay replicates the traffic inside the `packets.pcap`.

In Ubuntu you can use the advanced package tool:

```bash
sudo apt install tcpreplay
```

To run the experiment, simple type `. run.sh`. Don't forget the **dot**!!!
