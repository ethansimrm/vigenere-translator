# vigenere-translator

Here, I implement a simple Vigenère translator.

As detailed in the Jupyter Notebook and .py file, I did everything I did in the Morse translator - create a function and a GUI to encode input.

This time, I went further (only recorded in the Jupyter Notebook), and attempted to apply dynamic programming (memoization) to the problem. I conducted runtime analyses to measure its effect, plotted the results of these analyses in matplotlib, and used these to disprove my initial hypotheses. Unfortunately for me, dynamic programming did not yield significant decreases in time complexity, largely due to the structure of the Vigenère problem. Nevertheless, it has been a fun learning experience - at least I've learnt when not to use memoization. 
