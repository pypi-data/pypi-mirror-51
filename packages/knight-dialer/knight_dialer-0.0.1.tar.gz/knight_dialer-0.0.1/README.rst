=============
Knight Dialer
=============

This library shows how to solve the infamous knight dialer (KD) interview problem.  There are many problems like it in interviews (see the staircase problem) but the basic premise is the same:

You have some start position and some end point, and at each point you can take one of a few possible steps.  How many ways can you reach your end goal?

The Knight Dialer
-----------------

The KD problem involves the standard phone keypad::

        1 2 3
        4 5 6
        7 8 9
          0

How many possible phone numbers can you make by moving from one number to the next in the formation of the chess knight?  So for instance, starting on 1, you can go to 6 or 8, and from 6 you have three choices: 1, 7, 0, but from 8 you have only two: back to 1 or to 3. As you can see, this is not a trivial programming problem you can just punch out in excel.  Places have anywhere from 0 to 3 possible moves.  You can try every possible permutation and then root out the non-knight move ones, but that probably starts to get prohibitively expensive, with 10! being over three million, that means that you're starting to look at on the order of a billion operations to filter out. Probably that's not the approach the interviewers want.

Before we get started though it's worth just mentioning in this problem that you can drop 5 immediately because there's no possible moves from there.

The Class of Problems
---------------------

There are a number of classes of problems that behave like this one, and if you know how to solve this one, then you know how to solve most of them.  They go like this, "given a starting point and a finish point, how many possible paths are there through the intervening space, given that at any point you have more than one choice you can make?"  

Another example of such a problem given out at some point by google is "you have a staircase with 10 stairs. At each point you can either step 2 or 3 steps. How many possible paths are there to the top of the staircase?" Or in my library chemify, "can you write this sequence of letters in chemical elements given that they are either 1 or 2 characters in length?"

These problems are tricky and require some insight into how to solve them, but there is more than one way.  I don't ever see the multiple ways catalogued side by side, so herein lies the opportunity of this library.

Using the Library
-----------------

The library contains three possible solutions to the problem.  The first is a pure recursive solution.  That is, the function calls itself down the number of dials, and then returns the answer back up.  The second is a method that calls itself but doesn't return the answer.  Instead when it gets to the bottom it appends the finished work ot a list and returns that instead of itself.  The final one is my personal recommendation for how to solve these kinds of problems in a no-stress way: a backtracking/todo system (as seen in my other library chemify).  In this case, you add the initial items to a todo list, process each node, and then return the answer back to the todo list if it isn't done yet, or to a 'done' list if it is.  Once you have nothing on your todo list, return your done list.

IDES
-----

If you want to get the best bang for your buck, look at the source code of this library with your IDE.  You'll find that the three functions, KD_pure_recursive, KD_recursive_addition, and KD_backtrack have documentation related to their overall structure and function, but if you dive into the source I've also annotated it line by line so you can see the thinking.

If you run the source file and have numpy and matplotlib installed it will run a speed test.  Usually it seems that pure recursion wins out on my machine.  These will probably be similar for problems like the knight dialer, but you may see more substantive differences for problems of greater depth or more branching.

In conclusion
-------------

Enjoy the library and let me know if you have questions! Thanks!


