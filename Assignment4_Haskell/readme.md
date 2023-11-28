# Testing/Debugging
## Haskell has a built-in REPL for testing/debugging. From the command line, you can run

```cabal new-repl```
from the directory that contains the CS3003-HaskellAssignment.cabal file. If your code compiles, you will get a prompt that looks like

```*HaskellAssignment> ```

at the prompt you can invoke the functions that you have defined and check whether their output is what you expect. There is plenty of documentation for the REPL available onlineLinks to an external site.. 

To test whether your code passes all the unit tests, you can run

```cabal new-run```

and you should see

```Pass```

printed 20 times.