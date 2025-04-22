# Feedback for ss23.1.2/team503

**Team members:** we06quxo-1, zo97mobe-1

**Total points:** 75

**General notes:**
1. Please reach out if you think there was a mistake with the grading.
2. If the feedback below provides suggestions how your submission could be improved, this is not a request that you actually update your submission (unless stated otherwise). However, you might use some of the suggestions in future assignments.

-----------------

As I understand it, you used a greedy approach, which works quite well for the easy environments, but for the more difficult ones you will probably need something that looks a bit more ahead (min-max etc.).
In your case, you always make the move that will result in a peg as close as possible to the goal.
That seems to work well, but I think a problem is that often that means that you will have to move the front peg a single space forward, which is slow. Sometimes other pegs in the back could do a long hop chain, which would be more helpful.
So a different approach would be to select the move that brings changes the distance of a peg to the goal as much as possible.

Anyway, your agent performed quite well in the easy environments (and seems to be the second strongest agent of all).
That gives you 55 points for getting a 0.86 rating in the easy three player environment and another 20 for the description = 75 points in total.


