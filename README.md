
# UDI Polyglot V3 IFTTT Webhooks Nodeserver

This is the [IFTTT Maker Webhooks](https://ifttt.com/maker_webhooks) Poly for the [Universal Devices Polisy](https://www.universal-devices.com) with [Polyglot Version 3 (PG3)](https://github.com/UniversalDevicesInc/pg3)

(c) JimBo.Automates aka Jim Searle
MIT license.

## Reason

I dislike IFTTT as much as anyone for many reasons, but sometimes it can not be avoided.  This Nodeserver allows you to trigger IFTTT Webook Events from the ISY.

Currently this can be done easily with ISY Network Resources but this method provides many improvements.
1. Ability to Check for failures
    * Network Problems
    * Authentication Error
    * But, IFTTT doesn't return errors for incorrect event names, so must check the log when creating them
1. Allows the nodes to be placed in a scene

### Limitations

It does not allow sending the three Value's that are supported by Webhook Events, but this will be added in the future if there is a need.

It does not retry when there is a failure because you may not want the event to be triggered at a later time, so it's up to the user to handle this within the ISY program.  I may add an option to retry in the future.

It can only send events, it should be possible to also receive events thru the Portal but that is not supported and will be a major effort so will require more funding :)

## Nodes

### Controller

The main node which shows status of Nodeserver connection.

The Nodeserver also sends a DON/DOF at every long poll, known as a heartbeat which you can monitor to confirm it is receiving .

### Webhook

The Webhook node created based on the configuration.  May have "Trigger On Event" and/or "Trigger Off Event" if the are defined.  See [CONFIGURATION](CONFIGURATION.md).

## Help

If you have any issues are questions you can ask on [PG3 IFTTT Webhooks SubForum](https://forum.universal-devices.com/forum/338-ifttt-webhooks/) or report an issue at [PG3 IFTT Webook Github issues](https://github.com/UniversalDevicesInc-PG3/udi-poly-IFTTT-Webhooks/issues).

# Issues

If you have an issue where the nodes are not showing up properly, open the Polyglot UI and go to IFTTT Webhooks -> Details -> Log, and click 'Download Log Package' and send that to Jimbo.Automates@gmail.com as an email attachment, or send it in a PM [Universal Devices Forum](https://forum.universal-devices.com/messenger)

## Installation

This nodeserver will only work on a machine running on your local network, it will not work with Polyglot Cloud until TP-Link releases a public API for their cloud interface.

1. Backup Your ISY in case of problems!
   * Really, do the backup, please
2. Go to the Polyglot Store in the UI and install.
3. Open the admin console (close and re-open if you had it open) and you should see a new node 'IFTTT Webhooks Controller'

# Upgrading

Restart the Nodeserver by selecting it in the Polyglot dashboard and select Control -> Restart, then watch the log to make sure everything goes well.

# Release Notes
- 3.0.0: 02/27/2022
  - First Release
