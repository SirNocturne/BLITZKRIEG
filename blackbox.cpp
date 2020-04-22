/* blackbox.cpp
*    This file contains the blackbox code for the Blitzkrieg Robot Air Hockey System.
*    Purpose: After receiving inputs from the control-loop, either through the automated system or through the controller, convert 
* requested motion into commands to the motor controllers.
*
*    Authors: Joshua Fabel
*    Last Editted: 3.18.2020
*    Version No: 0.0.0.1
*/

/*
*    blackbock()
*    inputs:
*  -targetLocation [double]: location between 0.0 and 100.0 where the puck is predicted to intercept the robot.  The goal is to move the robot to here.
*  -currentLocation [double]: location between 0.0 and 100.0 where the robot currently believes that it is located.
*  -targetRotation [double]: rotational offset between 0.0 and 200.0 where the robot expects to want to place the flipper.
*  -currentRotation [double]: rotation between 0.0 and 200.0 which the robot believes is it's current orientation.
*  -controllerOverride [bool]: flag variable to ignore the prediction/PID loop in order to rely on controller input.
*  -controllerTranslation [double]: desired horizontal movement input from the controller scaled between -1.0 and 1.0.
*  -controllerRotation [double]: desired rotational movement input from the controller scaled between -1.0 and 1.0.
*/
void blackbox(double targetLocation, double currentLocation, double targetRotation, double currentRotation, bool controllerOverride, double controllerTranslation, double controllerRotation) {

  if (controllerOverride) {
    //Use the controller inputs to determine subsequent movement.
    
    if (controllerTranslation > 0) {
      //Move Right
      int speed = controllerTranslation * 255.0;
      string translateCommand = "\STX" + "R" + "0" + itoa(speed) + "\END"; //Motor ID 0 is our translation motor.
      sendCommand(translateCommand);
    } else {
      //Move Left
      int speed = controllerTranslation * -255.0;
      string translateCommand = "\STX" + "L" + "0" + itoa(speed) + "\END"; //Motor ID 0 is our translation motor.
      sendCommand(translateCommand);
    }
    
    if (controllerRotation > 0) {
      //rotate clockwise
      int speed = controllerRotation * 255.0;
      string rotateCommand = "\STX" + "R" + "1" + itoa(speed) + "\END"; //Motor ID 1 is our rotation motor
      sendCommand(translateCommand);
      
    } else {
      //rotate counterclockwise
      int speed = controllerRotation * -255.0;
      string rotateCommand = "\STX" + "L" + "1" + itoa(speed) + "\END"; //Motor ID 1 is our rotation motor
      sendCommand(translateCommand);
    }
    
    
  } else {
     //Use PID Loop predictions to determine movement.
     double deltaTranslation = targetLocation - currentLocation;
     double deltaRotation = targetRotation - currentRotation;
     
     if (deltaTranslation > 0) {
        //move right.
        int speed = deltaTranslation * 25.50; //scale slower if moving less than 10 units
        if (speed > 255)
          speed = 255;
          
      string translateCommand = "\STX" + "R" + "0" + itoa(speed) + "\END"; //Motor ID 0 is our translation motor.
      sendCommand(translateCommand);
     } else {
     //move left.
        int speed = deltaTranslation * -25.50; //scale slower if moving less than 10 units
        if (speed > 255)
          speed = 255;
          
      string translateCommand = "\STX" + "L" + "0" + itoa(speed) + "\END"; //Motor ID 0 is our translation motor.
      sendCommand(translateCommand);
     }
     
     if (deltaRotation > 0) {
      //rotate clockwise
      int speed = controllerRotation * 25.50;
      if (speed > 255)
        speed = 255;
      string rotateCommand = "\STX" + "R" + "1" + itoa(speed) + "\END"; //Motor ID 1 is our rotation motor
      sendCommand(translateCommand);
     } else {
     //rotate counterclockwise
      int speed = controllerRotation * -25.50;
      if (speed > 255)
        speed = 255;
      string rotateCommand = "\STX" + "L" + "1" + itoa(speed) + "\END"; //Motor ID 1 is our rotation motor
      sendCommand(translateCommand);
     }
  
  }
  
  //stuff that needs to happen regardless of controller vs pid-loop.

}
