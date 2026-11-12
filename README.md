# user_prompt
A cross-platform python package for handling user input prompts, allow timeouts and hidden input

I used the python 2.7 version of [inputimeout](https://github.com/johejo/inputimeout) as a starting point, then modified it to handle untimed prompts and secure input with the optional argument `hide_input`

# Example
```
from user_input import user_input
import sys

# timed prompt with default value, no timeout Exception
name = user_input("username: ", 20, default='')

# timed prompt with input not displayed to terminal
password = user_input("Password: ", 35, True)

```
