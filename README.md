# Recon Sentinel Hacking

Misc. experiments with what is being sold as a $15 dev kit, but in fact is a recycled product called the [Recon Sentinel](https://www.reconsentinel.com).

Right now most of the information can be found in the [journal](./journal.md).  As things move along I'll work on adding more to this readme.

## LCD Connections

| Wire | ROCK64 Pin | LCD Module Pin |
|------|------------|----------------|
| red | 2/5v | VCC |
| grey | 6/gnd | GND
| brown | 28/GPIO2_A5/I2C1_SCL | SCL |
| blue | 27/GPIO2_A4/I2C1_SDA | SDA |


## References

* http://files.pine64.org/doc/rock64/ROCK64_Pi-2%20_and_Pi_P5+_Bus.pdf
* https://www.armbian.com/rock64/
* https://forum.pine64.org/showthread.php?tid=5902
* https://shiroku.net/robotics/using-i2c-lcd-on-raspberry-pi/
