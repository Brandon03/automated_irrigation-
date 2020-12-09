# SKETCH VERSION ( BRAINSTORM )

## Objective

Addressing the challenges & problems from SysReq_1.md

## schedule and duration

1. Average discharge for mini dripper.
2. How does the length of the pipe would effect the discharge of the mini dripper ?
3. Discharge for the water sources.
4. How does the discharge of the water sources would effect the discharge of the
mini dripper
5. After 2) and 4), the discharge for the mini dripper should be predicted. 
6. How much does level of humid is required from the soil ?
7. Measure time taken from the mini dripper to maintain healthy level.
8. Pump discharge level and time taken to maintain the pressure and discharge of the dripper.
9. pump + valve opening time.

    **Challenges**
    1. How does the length of the pipe would effect the discharge of the mini dripper.
    2. How does the discharge of the water sources would effect the discharge of the mini dripper.
    3. Discharge and pressure is the variables for the design

    **Adds On**
    1. Discharge refers the quantity flow rate. 
    2. Pressure concerns the amount of discharge, as the higher the fluid pressure, the lesser the discharge from mini dripper.

***STEPS TAKEN***
    1. Revise piping fluid notes. ( 7 days )
    2. Experiment the challenges faces and collect data. ( 1 day )

## Multi channel capable

Refer to client messages : 

*“ Shift registers; we are not programming PLCs or chipsets, we’re using HPIB bus on RPI! 
Use Python to poll the bus to see which channel is active. Polling is OK as
we’re not dealing with milli-second real-time situation. You will also need to learn algorithms 
like ‘messaging queues’ & worker processes/threads, to keep the system concurrent and mon blocking.
That’s the advantage of using a high level Single Board Computer (SBC) like RPI instead of Arduino or PLC, custom HW. “*

From above, few technicals are addressed :
1. Python polling
2. Messaging queues
3. worker processes/threads
4. keep system concurrent & non-blocking

***STEPS TAKEN***
    1. 
