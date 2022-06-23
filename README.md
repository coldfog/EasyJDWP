# EasyJDWP
An easy way to communicate with JDWP. (**NOTE: It is not finish yet!**)

some backgroud infomation you may want to know:
+ [Hacking the Java Debug Wire Protocol – or – “How I met your Java debugger”](https://ioactive.com/hacking-java-debug-wire-protocol-or-how/)
+ [JDWP SPEC](https://docs.oracle.com/javase/8/docs/technotes/guides/jpda/jdwp-spec.html)
+ [JDWP-protocol detail](https://docs.oracle.com/javase/8/docs/platform/jpda/jdwp/jdwp-protocol.html)

# What is it?

This is a project inspired by [jdwp-shellifier.py](https://github.com/IOActive/jdwp-shellifier). It is designed to communicate with `Java Debug Wire Protocol(JDWP)` but in a more pythonic and easier way. 
 
The primary purpose of this project is shown below:

1. ~~Single file~~ Two file, no extra dependency, esay to integrate and use
2. Keep the annoying detail away
3. Support python3
4. A full implementation of JDWP protocol
