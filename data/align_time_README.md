Steps to "align" the nsecs since boot timestamps in the traces with the local time.

We want to estimate a nsecs since boot timestamp for a specific second in local time s.t. 15:27:39.000000000. This will allow us to align with some precision the timestamps with the millisecond precision UNIX timestamps we get from the mllog, or other logging libraries.

To do this, take the `trace_time_align.out` trace and look at some 1 sec transitions. Note the timestamps on either side of the transition and find the smallest difference we can between timestamps. 

Example:

1380327127403885  15:27:39 // dif = 368165 ns
1380327127772050  15:27:40 

1380360127432329  15:28:12 // dif = 52711 ns   -- smallest dif
1380360127485040  15:28:13 

1380328127311181  15:27:40 // dif = 254060 ns   
1380328127565241  15:27:41 

1380346131360213  15:27:58 // dif = 230119 ns  
1380346131590332  15:27:59

1380329127177703  15:27:41 // dif = 376942 ns
1380329127554645  15:27:42 


The smallest is 52711 nsecs btw the timestamps for 15:28:12 and 15:28:13. 
We can interpolate that the second change happens at the middle timestamp
1380360127485040 + 1380360127432329/ 2 =~ 1380360127458684

Thus, we will estimate that 1380360127458684 ~= 15:28:13.000000000



Note: We see there is some drift happening since not all second changes seem to occur at the ~127msec mark in the timestamps