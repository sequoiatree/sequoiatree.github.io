# Defining `lambda` functions

Consider the code below. It does two things.

```
def five():
    return 5
```

First of all, it creates a new function whose output is 5. Second, it makes the variable `five` point at that function.

ASSET def-five

To be honest, though, that syntax is a little weird. If I want to bind `five` to the number 5, I write `five = 5`. If I want to bind it to the string `'five'`, I write `five = 'five'`. If I want to make `five` point to a function that returns 5, why can't I do something similar? Why not something like `five = <pointer at a function that returns 5>`? That's where the `lambda` keyword comes in.

## Syntax for defining `lambda` functions

A `lambda` expression **directly evaluates to a pointer at a function**, in the same way that an arithmetic expression directly evaluates to a number. `lambda` expressions follow this format:

```
lambda PARAMETERS: RETURN VALUE
```

For example `lambda: 5` is a pointer at a function named "λ", which has no parameters and returns 5. You could bind the variable `five` to that pointer, by writing something like `five = lambda: 5`.

ASSET lambda-five

Now we have a variable that points at a function. We can call it in the usual way.

```
>>> five = lambda: 5
>>> five()
5
```

Meanwhile `lambda x: x` is a pointer at a function named "λ", which simply returns its input. You could bind the variable `identity` to that pointer, by writing something like `identity = lambda x: x`.

ASSET lambda-identity

```
>>> identity = lambda x: x
>>> identity(4)
4
```

It's also possible to use the `lambda` keyword to make a function that takes in multiple arguments. For instance, consider `average = lambda x, y: (x + y) / 2`.

ASSET lambda-average

```
>>> average = lambda x, y: (x + y) / 2
>>> average(4, 8)
6.0
```

The takeaway? A `lambda` expression evaluates to a pointer at a function. So when we bind a variable to a `lambda` expression, that binds the variable to a pointer at a function. Then we can use the variable to call the function like we're used to.

## `def` statements versus `lambda` expressions 

So ... what's the difference between a `def` statement and a `lambda` expression?

A `def` statement creates a function and binds it to a variable, whereas a `lambda` expression creates a function without binding it to a variable. It's up to you what to do with that `lambda` function — bind it to a variable, call it, whatever. In this way, `def` is just a shorthand way of making a function and binding it to a variable at the same time, without having to explicitly assign the variable using the `=` operator.

The most important difference is what you can actually do with them. Within a `def` statement you can assign local variables, evaluate chains of `if` / `elif` / `else` statements, and do iteration with `while` loops. A `lambda` expression is much more limited. You have your parameters before the colon, and your output after the colon. There's no room to do anything else, like variable assignment or boolean logic or iteration. Literally, a `lambda` expression lets you return a value, and do nothing else.

That means you can also rewrite `lambda` expressions as one-line `def` statements, if you so desire. This might help you get used to them, when you're just starting out. For example, these two snippets of code are basically the same:

```
add = lambda x, y: x + y
```

```
def add(x, y):
    return x + y
```

Make sure you understand everything we've covered so far in this chapter, before reading on.

# Pyagrams with `lambda` functions

In the previous section we saw a few examples of how to draw `lambda` functions in pyagrams. Now it's time to go into more detail.

## Evaluating `lambda` expressions

Remember, a `lambda` expression literally evaluates to a pointer at a function. As we saw earlier the function is named "λ", and as with any function in a pyagram, we write its inputs in parentheses after its name.

```
add = lambda x, y: x + y
```

ASSET lambda-add

Each time you read the word `lambda`, it evaluates to a new pointer at a new `lambda` function, even if that results in having two identical `lamdba` functions. That's because each `lambda` expression is evaluated individually. This code, for instance, creates two separate `lambda` functions that both return 5.

```
f = lambda: 5
g = lambda: 5
```

ASSET different-but-identical-lambdas

Meanwhile this code creates only one `lambda` function. Then it copies the pointer down from `f` into `g` like we learned how to do when we first learned about functions and pointers.

```
f = lambda: 5
g = f
```

ASSET two-pointers-to-same-lambda

Also, a `lambda` function's parent frame is the frame you're in when you actually read the word `lambda`. (This is similar to how the parent of a normal function is the frame you're in when you read the word `def`.) In the code below, we evaluate the `lambda` expression in frame 1 so its parent is frame 1.

```
def make_square():
    return lambda x: x ** 2

square = make_square()
```

STARTSEQUENCE make-square

First we define `make_square` in the global frame with an ordinary `def` statement.

---

Then we see the line `square = make_square()`, which we can't complete until we know the value of `make_square()`.

---

We start a flag for the function call.

---

Then we fill in the flag banner. We look up `make_square` in the global frame to find that it's bound to a pointer at a function. Then we copy that pointer down into the flag banner.

---

With the flag banner complete, we can start frame 1 to evaluate the function call.

---

The only line in `make_square` is `return lambda x: x ** 2`. This creates a `lambda` function and returns a pointer to that `lambda` function. Notably, the parent of the `lambda` function is frame 1, since that's the frame we were in when we created it.

---

Last of all we go back to the global frame, where we can finish binding `square` to the value of `make_square()`.

ENDSEQUENCE

So in summary:

* Whenever you read the word `lambda`, it evaluates to a new pointer at a new `lambda` function, even if that results in having two identical `lambda` functions.
* The parent of the `lambda` function is the frame where you read the word `lambda`.

## Practice: evaluating the same `lambda` expression twice 

Consider this modification of the example from the previous section:

```
def make_square():
    return lambda x: x ** 2

square_1 = make_square()
square_2 = make_square()
```

STARTSEQUENCE make-square-twice

As before, we open up frame 1 for the call to `make_square`, where we evaluate the `lambda` expression to get a new pointer at a new squaring function. The function's parent is frame 1, since that's the frame where we create it. Then we return the pointer from the call to `make_square`, and bind it to the variable `square_1` in the global frame.

---

After we're back in the global frame, we get to `square_2 = make_square()`. Since we're just calling `make_square` again, we will basically repeat the same process from before.

---

First of all, we'll have to make a new flag for the second call to `make_square()`.

---

Then we fill in the flag banner with the value of `make_square`. Again, we just look it up in the global frame since that's the first frame above the flag we're working on.

---

Once the flag is done, we can start a new frame. This one will be called frame 2, since it's the second frame other than the global frame. Like frame 1, it's for `make_square`. Frame 2's parent is the global frame, since it corresponds to a call to `make_square`, and the parent of `make_square` is the global frame.

---

When we evaluate the `lambda` expression for the second time, it produces a new pointer at a new squaring function, rather than referring to the same one from before. (Remember, you get a new function every time you read the word `lambda`.) Its parent is frame 2, since that's the frame we're in when we evaluate it. This pointer gets returned from the call to `make_square`.

---

Finally that pointer is bound to `square_2` in the global frame. Notice how `square_1` and `square_2` end up pointing to different functions. That's because `square_1` got bound to the pointer returned from the function call `make_square()`, and `square_2` got bound to the pointer returned from a _different_ function call `make_square()`. Each function call produced a new pointer and a new `lambda` function.

ENDSEQUENCE

Check that you agree with this example, before you continue.

## Telling apart different `lambda` functions

Occasionally you'll be working with multiple `lambda` functions, and it can be hard to remember which is which. For instance, take a look at this extension of the same example from before:

```
>>> def make_square():
...     return lambda x: x * x
...
>>> square_1 = make_square()
>>> square_2 = make_square()
>>> square_3 = lambda x: 1 / 0
>>> square_2(4)
16
```

Here's the pyagram, right before the last line gets executed:

ASSET ambiguous-lambdas

Now we're at the function call `square_2(4)`. But there's a problem. Which `lambda` function does `square_2` correspond to? Is it the one that squares its input, or the one that tries to divide by 0? The pyagram shows us `square_2` is bound to a function named "λ", but it doesn't show us _which_ `lambda` expression to look at in the code.

To deal with this, we're going to write a little number next to every `lambda` expression in our code. This will help us tell them apart. Then, when we draw the pyagram, we'll write the corresponding number next to every `lambda` function that we create. Let's start by annotating our code:

```
>>> def make_square():
...     return lambda~1~ x: x * x
...
>>> square_1 = make_square()
>>> square_2 = make_square()
>>> square_3 = lambda~2~ x: 1 / 0
>>> square_2(4)
16
```

Now when we draw `lambda~1~` in our pyagram we'll name the function "λ~1~" rather than "λ", and when we draw `lambda~2~` in our pyagram we'll name the function "λ~2~".

ASSET unambiguous-lambdas

With this modification to the pyagram, it shows that `square_2` in the global frame corresponds to `lambda~1~` in our code. So when it's time to do the function call `square_2(4)`, it's easy to see we should do `4 * 4` rather than `1 / 0`.

## Practice: a `lambda` function as an argument

This may get confusing. If you find yourself lost, refer back to [the procedure for drawing pyagrams](functions.html#the-order-of-evaluation). Draw the pyagram for this code:

```
def f(x, g):
    y = g() + g()
    return lambda y: x + y

x = 10
y = f(x - 9, lambda: x)(x)
```

First let's number the `lambda` expressions so we can tell them apart later. Here's the code after we annotate it, like we just learned in the previous section:

```
def f(x, g):
    y = g() + g()
    return lambda~1~ y: x + y

x = 10
y = f(x - 9, lambda~2~: x)(x)
```

STARTSEQUENCE lambda-argument

We'll start the pyagram by binding `f` and `x` in the global frame.

---

Then we reach the last line. To complete it, we need to know the value of `f(x - 9, lambda~2~: x)(x)`.

---

As always, the function call corresponds to a new flag in the pyagram. It consists of two parts: a function, and a single argument. The function is `f(x - 9, lambda~2~: x)`, and the argument is `x`.

---

The next step is to fill in the first flag banner with the value of `f(x - 9, lambda~2~: x)`. Since this is itself a function call, we'll require another flag in the pyagram. This second flag goes inside the first one. It consists of a function `f`, as well as two arguments `x - 9` and `lambda~2~: x`.

---

First we will need to evaluate `f`. We look for it in the global frame, since that's the first frame above the flag we're working on. There we see it is bound to a pointer, which we copy down into the flag banner.

---

Then we will need to evaluate the arguments. To get `x - 9` we need to know what `x` is. Just look it up in the first frame above the flag we're working on. That's the global frame, where `x` is 10 so `x - 9` is 1.

We also need to know the value of `lambda~2~: x`. This expression directly evaluates to a new pointer at a new function, which we'll call "λ~2~" to indicate it corresponds to `lambda~2~` in our annotated code above. **Notice how its parent is the global frame, since we haven't yet transitioned to frame 1.**

---

Now the flag banner is complete, so we start a new frame. It's the first frame other than the global frame, so we'll call it frame 1. It corresponds to a call on the function `f`, whose parent is the global frame.

---

As always, don't forget to bind the parameters to their respective arguments! In this case we have the parameter `x` bound to the argument 1, and the parameter `g` bound to a pointer at the function λ~2~.

---

The first line of code inside the function `f` is `y = g() + g()`. We will need to know what `g() + g()` is, before we go assigning the value of `y`.

---

Let's start a frame for the first function call, `g()`.

---

We will look up `g` in frame 1, since that's the first frame above the flag we're working on. It is a pointer to the function λ~2~.

---

The flag is done so we can start frame 2. The function we're calling is λ~2~, and its parent is the global frame.

---

Take a look at the code above. It says λ~2~ just returns `x`. But `x` isn't defined in frame 2, so we will look for it in frame 2's parent frame. That's the global frame, where we can see `x` is 10.

---

But that's only half the answer to `y = g() + g()`. We also have to do a second identical function call, which will require another flag for `g()`.

---

Once more we look up `g` in frame 1 to find that it is a pointer to λ~2~.

---

Then, with the flag done, we can start frame 3. Just like frame 2, it is for a call to the function λ~2~ whose parent is the global frame.

---

It also returns `x`, which we look up in the global frame to find bound to 10.

---

Finally we know `g() + g()` is 20, so we can bind `y` to 20 in frame 1.

---

Then we proceed with frame 1, which was for a call on the function `f`. We arrive at the line `return lambda~1~ y: x + y`. This means we're making a new pointer to a new function named λ~1~, and then returning that pointer. Notice how λ~1~'s parent is frame 1, since that's the frame where we created it.

---

Now that frame 1 is complete, we can go back to the flag banner for `f(x - 9, lambda~2~: x)(x)`. At last we know `f(x - 9, lambda~2~: x)` is a pointer to λ~1~, so we can fill that in.

---

To complete the flag banner for `f(x - 9, lambda~2~: x)` we just need to know what `x` is. Since the global frame is the first frame above the flag, we look for it there. It's bound to 10.

---

The flag banner for `f(x - 9, lambda~2~: x)` is complete, and it tells us we're calling λ~1~ on the argument 10. It's time to start the corresponding frame, which is frame 4. Notice how its parent frame is 1, since that's the parent of λ~1~, the function we're calling.

---

First up, we need to bind the parameter `y` to its argument, which is 10.

---

According to the code above, we can see λ~1~ is just supposed to return `x + y`. `x` isn't in frame 4 so we have to look for it in frame 4's parent frame. That's frame 1, which says `x` is 1. On the other hand `y` is already defined in frame 4, where it's bound to 10. So in the end we're just adding 1 + 10 to get 11.

---

Now that the function call it complete, we can go back to the global frame where we left off on the line `y = f(x - 9, lambda~2~: x)(x)`. Since we just learned that `f(x - 9, lambda~2~: x)(x)` is 11, it looks `y` is getting bound to 11. This completes the pyagram.

ENDSEQUENCE

Again, if this exercise was confusing you may want to review [the procedure for drawing pyagrams](functions.html#the-order-of-evaluation). In fact, you may even want to skim or re-read some of the stuff in the sections above, just to check that everything jives with you. `lambda` functions can be a tricky topic, but they're something you should get familiar with.

# Calling `lambda` functions

Now that we're familiar with defining `lambda` functions, let's talk about how to use them. Calling a `lambda` function is pretty much the same as calling any regular function, but there are a few subtle points that we should talk about explicitly.

## Calling `lambda` functions on-the-spot

So far we've only been able to call a `lambda` function by first binding a variable to it. In the code below, for instance, we make `square` point to the function created by the `lambda` expression. Then we are able to call the function in the usual way by writing `square(4)`.

```
>>> square = lambda x: x * x
>>> square(4)
16
```

But we could also just plug in the value of `square` directly:

```
>>> (lambda x: x * x)(4)
16
```

The only difference is that now we're creating the squaring function on-the-spot when we evaluate `(lambda x: x * x)`, rather than referring to it with the variable `square`. The important thing is that `(lambda x: x * x)(4)` is still a function call, since it has both a function and an argument in parentheses. (The function is `(lambda x: x * x)` and 4 is the argument in parentheses.)

Brief aside here, also notice how we had to use parentheses around the `lambda` expression. That's important. Without the parentheses you get `lambda x: x * x(4)`, which is a function that seems to take a parameter `x` and then multiply `x` with the result of a function call `x(4)`. Whenever you want to call a `lambda` function on-the-spot like this, you should use parentheses to denote exactly what is part of the `lambda` expression, and what isn't.

Here's another example, where we use a `lambda` expression to get the average of 4 and 8. In this case the function is `(lambda x, y: (x + y) / 2)`, and the arguments in parentheses are 4 and 8.

```
>>> (lambda x, y: (x + y) / 2)(4, 8)
6.0
```

## Review: functions and function calls

Sometimes this stuff can get tricky. To avoid getting confused, you should get good at telling the difference betwen a function and a function call. Functions can either be bound to variables, or created on-the-spot by a `lambda` expression. When either of these things are followed by parentheses, that's a function call. For example:

```
>>> identity         # Function.
>>> identity(4)      # Function call.
>>> lambda x: x      # Function.
>>> (lambda x: x)(4) # Function call.
```

Also, be careful to evaluate things only when you should. Remember how you only do the stuff inside a `def` statement, once you call the function? The same goes for `lambda` expressions. You only do the stuff after the colon once you call the function. This is a pretty common mistake so be vigilant. Consider this code for example:

```
both_prime = lambda x, y: is_prime(x) and is_prime(y)
```

This binds `both_prime` to a pointer at a function. It does not yet call any functions. The calls to `is_prime` only happen after you call `both_prime`.