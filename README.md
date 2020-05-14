# tuning

Go to the [tuning notebook](https://github.com/jessebmurray/tuning/blob/master/tuning.ipynb).

The inverse fraction rule that is fundamental to my algorithm suggests the following:

Given two positive integers a and b, and an integer n from 0 through 12, inclusive.

If:


$\frac{a}{b} \approx 2^\frac{n}{12}$

Then:

\begin{equation*}
\LARGE  \frac{2b}{a} \approx 2^\frac{12 - n}{12}
\end{equation*}

We show through simulation that this holds true.
