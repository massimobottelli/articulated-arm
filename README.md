# Robot Arm

![Robot Arm](public/img/capture-02.jpeg)

This project (currently under development) aims at creating a software to control a robotic articulated arm.

The projects is composed by two Python scripts:

## RoboLink

First script represents the interface between the user and the robot arm: it allow users to select the target point where the robot arm must move to, then calculates the angles for moving the two segments of the robot arm and finally sends the angles to the robot controller


## ArmController

Second script actually is the piece of software that controls the robot movement: it receives the commands from RoboLink and moves the segments of the robot arm accordingly.

