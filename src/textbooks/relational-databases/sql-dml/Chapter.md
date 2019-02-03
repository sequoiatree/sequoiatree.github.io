In the previous chapter we learned how to use SQL for creating tables and populating them with data. Now it's time for us to learn how to query that data, and manipulate it.

# Querying a table

The most fundamental SQL query looks like this:

```
SELECT <columns>
FROM <table>;
```

The `FROM` clause tells SQL which table you're interested in, and the `SELECT` clause tells SQL which columns of that table you want to see. For example, consider a table `Person(name, age, num_dogs)` containing the data below:

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ada |18 |3
Ben |7  |2
Cho |27 |3
```

If we executed this SQL query ...

```
SELECT name, num_dogs
FROM Person;
```

... then we would get any of the following outputs, which are all equivalent:

```
name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs    name|num_dogs
----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------    ----+--------
Ace |4           Ace |4           Ace |4           Ace |4           Ace |4           Ace |4           Ada |3           Ada |3           Ada |3           Ada |3           Ada |3           Ada |3           Ben |2           Ben |2           Ben |2           Ben |2           Ben |2           Ben |2           Cho |3           Cho |3           Cho |3           Cho |3           Cho |3           Cho |3
Ada |3           Ada |3           Ben |2           Ben |2           Cho |3           Cho |3           Ace |4           Ace |4           Ben |2           Ben |2           Cho |3           Cho |3           Ace |4           Ace |4           Ada |3           Ada |3           Cho |3           Cho |3           Ace |4           Ace |4           Ada |3           Ada |3           Ben |2           Ben |2
Ben |2           Cho |3           Ada |3           Cho |3           Ada |3           Ben |2           Ben |2           Cho |3           Ace |4           Cho |3           Ace |4           Ben |2           Ada |3           Cho |3           Ace |4           Cho |3           Ace |4           Ada |3           Ada |3           Ben |2           Ace |4           Ben |2           Ace |4           Ada |3
Cho |3           Ben |2           Cho |3           Ada |3           Ben |2           Ada |3           Cho |3           Ben |2           Cho |3           Ace |4           Ben |2           Ace |4           Cho |3           Ada |3           Cho |3           Ace |4           Ada |3           Ace |4           Ben |2           Ada |3           Ben |2           Ace |4           Ada |3           Ace |4
```

These tables are all permutations of one another, and you may get a different permutation depending on which version of SQL you're using. Typically in this book I'll only show one possible permutation when I talk about the output of a SQL query, but you shouldn't make any assumptions about which permutation you'll get — that is, unless you use the `ORDER BY` clause, which I'll discuss later in this chapter.

# Filtering out uninteresting rows

Frequently we are interested in only a subset of the data available to us. That is, even though we might have data about many people or things, we often only want to see the data that we have about very specific people or things. This is where the `WHERE` clause comes in handy; it lets us specify which specific rows of our table we're interested in. Here's the syntax:

```
SELECT <columns>
FROM <table>
WHERE <predicate>;
```

Once again, let's consider our table `Person(name, age, num_dogs)`. Suppose we want to see how many dogs each person owns — same as before — but this time we only care about the dog-owners who are adults. Let's walk through this SQL query, one step at a time:

```
SELECT name, num_dogs
FROM Person
WHERE age >= 18;
```

STARTSEQUENCE markdown

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ada |18 |3
Ben |7  |2
Cho |27 |3
```

-

As always, we begin with the `FROM` clause. (Each clause in a SQL query happens in the order it's written, except for `SELECT` which happens last. That's important, so remember it.) The `FROM` clause tells us we're interested in the `Person` table.

---

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ada |18 |3
Cho |27 |3
```

-

Next we move on to the `WHERE` clause. It tells us that we only want to keep the rows satisfying the predicate `age >= 18`, so we remove the row with Ben.

---

```
name|num_dogs
----+--------
Ace |4
Ada |3
Cho |3
```

-

And finally, we `SELECT` the columns `name` and `num_dogs` to obtain our final result. (Again, any permutation of this result is equally valid so you shouldn't make any assumptions about the order of the rows.)

ENDSEQUENCE

## Boolean operators

If you want to filter on more complicated predicates, you can use the boolean operators `NOT`, `AND`, and `OR`. For instance, if we only cared about dog-owners who are not only adults, but also own more than 3 dogs, then we would write the following query:

```
SELECT name, num_dogs
FROM Person
WHERE age >= 18
  AND num_dogs > 3;
```

As in Python, this is the order of evaluation for boolean operators:

1. `NOT`
2. `AND`
3. `OR`

That said, it is good practice to avoid ambiguity by adding parentheses even when they are not strictly necessary.

## Filtering `NULL` values

Bear in mind that some values in your database may be `NULL` whether you like it or not, so it's good to know how SQL handles them. Pretty much it boils down to the following:

* If you do anything with `NULL`, you'll just get `NULL`. For instance if `x` is `NULL`, then `x > 3`, `1 = x`, and `x + 4` all evaluate to `NULL`. Even `x = NULL` would evaluate to `NULL`; if you want to check whether `x` is `NULL`, then write `x IS NULL` or `x IS NOT NULL` instead.
* `WHERE NULL` is just like `WHERE FALSE`. The row in question does not get included.
* `NULL` short-circuits with boolean operators. That means a boolean expression involving `NULL` will evaluate to:
   * `TRUE`, if it'd evaluate to `TRUE` regardless of whether the unknown value is really `TRUE` or `FALSE`.
   * `FALSE`, if it'd evaluate to `FALSE` regardless of whether the unknown value is really `TRUE` or `FALSE`.
   * Or `NULL`, if it depends on the unknown value.

Let's walk through this query as an example:

```
SELECT name, num_dogs
FROM Person
WHERE age <= 20
   OR num_dogs = 3;
```

STARTSEQUENCE markdown

```
name|age |num_dogs
----+----+--------
Ace |20  |4
Ada |NULL|3
Ben |NULL|NULL
Cho |27  |NULL
```

-

As always, we begin with the `FROM` clause. (Recall that each clause in a SQL query happens in the order it's written, except for `SELECT` which happens last.) The `FROM` clause tells us we're interested in the `Person` table. (You may notice I've nulled out a couple values, for the sake of demonstration.)

---

```
name|age |num_dogs
----+----+--------
Ace |20  |4
Ada |NULL|3
```

-

Next we move on to the `WHERE` clause. It tells us that we only want to keep the rows satisfying the predicate `age <= 20 OR num_dogs = 3`. Let's consider each row one at a time:

* For Ace, `age <= 20` evaluates to `TRUE` so the claim is satisfied.
* For Ada, `age <= 20` evaluates to `NULL` but `num_dogs = 3` evaluates to `TRUE` so the claim is satisfied.
* For Ben, `age <= 20` evaluates to `NULL` and `num_dogs = 3` evaluates to `NULL` so the claim is not satisfied.
* For Cho, `age <= 20` evaluates to `FALSE` so the claim is not satisfied.

Thus we keep only Ace and Ada.

---

```
name|num_dogs
----+--------
Ace |4
Ada |3
```

-

And finally, we `SELECT` the columns `name` and `num_dogs` to obtain our final result.

ENDSEQUENCE

# Grouping and aggregation

When you're working with a very large database, it is useful to be able to summarize your data so that you can better understand the general trends at play. Let's see how.

## Summarizing columns of data

With SQL you are able to summarize entire columns of data using built-in aggregate functions. The most common ones are `SUM`, `AVG`, `MAX`, `MIN`, and `COUNT` — but there are more, and you can even make your own using the `CREATE AGGREGATE` command. I don't want to get sidetracked, though, so here are the important takeaways:

* The input to an aggregate function is the name of a column, and the output is a single value that summarizes all the data within that column.
* Every aggregate ignores `NULL` values except for `COUNT(*)`. (So `COUNT(<column>)` returns the number of non-`NULL` values in the specified column, whereas `COUNT(*)` returns the number of rows in the table overall.)

For example consider this variant of our table `People(name, age, num_dogs)` from earlier, where we are now unsure how many dogs Ben owns:

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ada |18 |3
Ben |7  |NULL
Cho |27 |3
```

With this table in mind ...

* `SUM(age)` is `72.0`, and `SUM(num_dogs)` is `10.0`.
* `AVG(age)` is `18.0`, and `AVG(num_dogs)` is `3.3333333333333333`.
* `MAX(age)` is `27`, and `MAX(num_dogs)` is `4`.
* `MIN(age)` is `7`, and `MIN(num_dogs)` is `3`.
* `COUNT(age)` is `4`, `COUNT(num_dogs)` is `3`, and `COUNT(*)` is `4`.

So, if we desired the range of ages represented in our database, then we could use the query below and it would produce the result 20. (Technically it would produce a one-by-one table containing the number 20, but SQL treats it the same as the number 20 itself.)

```
SELECT MAX(age) - MIN(age)
FROM Person;
```

Or, if we desired the average number of dogs owned by adults, then we could write this:

```
SELECT AVG(num_dogs)
FROM Person
WHERE age >= 18;
```

STARTSEQUENCE markdown

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ada |18 |3
Ben |7  |NULL
Cho |27 |3
```

-

As always, we begin with the `FROM` clause. (One last time, at risk of sounding like a broken record: each clause in a SQL query happens in the order it's written, except for `SELECT` which happens last.) The `FROM` clause tells us we're interested in the `Person` table.

---

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ada |18 |3
Cho |27 |3
```

-

Next we move on to the `WHERE` clause. It tells us that we only want to keep the rows satisfying the predicate `age >= 18`, so we remove the row with Ben.

---

```
AVG(num_dogs)
------------------
3.3333333333333333
```

-

And finally, we `SELECT` the average of the `num_dogs` column to obtain our final result, `3.3333333333333333`.

ENDSEQUENCE

## Summarizing groups of data

Now you know how to summarize an entire column of your database into a single number. More often than not, though, we want a little finer accuracy than that. This is possible with the `GROUP BY` clause, which allows us to split our data into groups and then summarize each group separately. Here's the syntax:

```
SELECT <columns>
FROM <table>
WHERE <predicate>   -- Filter out rows (before grouping).
GROUP BY <columns>
HAVING <predicate>; -- Filter out groups (after grouping).
```

Notice we also have a brand new `HAVING` clause, which is actually very similar to `WHERE`. The difference?

* `WHERE` occurs _before_ grouping. It filters out uninteresting _rows_.
* `HAVING` occurs _after_ grouping. It filters out uninteresting _groups_.

To explore all these new mechanics let's see another step-by-step example. This time our query will find the average number of dogs owned, for each adult age represented in our database. We will exclude any age for which we only have one datum.

```
SELECT age, AVG(num_dogs)
FROM Person
WHERE age >= 18
GROUP BY age
HAVING COUNT(*) > 1;
```

STARTSEQUENCE markdown

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ada |18 |3
Ben |7  |2
Cho |27 |3
Ema |20 |2
Ian |20 |3
Jay |18 |5
Mae |33 |8
Rex |27 |1
```

-

First we evaluate the `FROM` clause; it tells us to look at the `Person` table, which I've somewhat expanded since we last saw it.

---

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ada |18 |3
Cho |27 |3
Ema |20 |2
Ian |20 |3
Jay |18 |5
Mae |33 |8
Rex |27 |1
```

-

Next we move on to the `WHERE` clause. It tells us that we only want to keep the rows satisfying the predicate `age >= 18`, so we remove the row with Ben.

---

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ema |20 |2
Ian |20 |3
----+---+--------
Ada |18 |3
Jay |18 |5
----+---+--------
Cho |27 |3
Rex |27 |1
----+---+--------
Mae |33 |8
```

-

Now for the interesting part. We arrive at the `GROUP BY` clause, which tells us to categorize the data by `age`. We end up with a group of all the adults 20 years old, a group of all the adults 18 years old, a group of all the adults 27 years old, and a group of all the adults 33 years old.

---

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ema |20 |2
Ian |20 |3
----+---+--------
Ada |18 |3
Jay |18 |5
----+---+--------
Cho |27 |3
Rex |27 |1
```

-

The `HAVING` clause tells us we only want to keep the groups satisfying the predicate `COUNT(*) > 1` — that is, the groups that contain more than one row. We discard the group that contains only Mae.

---

```
age|AVG(num_dogs)
---+-------------
20 |3.0
18 |4.0
27 |2.0
```

-

Last but not least, every group gets collapsed into a single row. According to our `SELECT` clause, each such row must contain two things:

* The `age` corresponding to the group.
* The `AVG(num_dogs)` for the group.

This completes the query.

ENDSEQUENCE

So, to recap, here's how you should go about a query that follows the template above:

1. Start with the table specified in the `FROM` clause.
2. Filter out uninteresting rows, keeping only the ones that satisfy the `WHERE` clause.
3. Put data into groups, according to the `GROUP BY` clause.
4. Filter out uninteresting groups, keeping only the ones that satisfy the `HAVING` clause.
5. Collapse each group into a single row, containing the fields specified in the `SELECT` clause.

In passing, note that you can also group data on multiple columns at the same time. Here's an example:

```
SELECT name, age, COUNT(*)
FROM Person
GROUP BY name, age;
```

STARTSEQUENCE markdown

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ace |20 |3
Ace |7  |2
Ada |18 |3
Ada |18 |4
Ada |27 |3
```

-

First we evaluate the `FROM` clause; it tells us to look at the `Person` table, which I've modified to include several people named Ace and several people named Ada.

---

```
name|age|num_dogs
----+---+--------
Ace |20 |4
Ace |20 |3
----+---+--------
Ace |7  |2
----+---+--------
Ada |18 |3
Ada |18 |4
----+---+--------
Ada |27 |3
```

-

Since there's no `WHERE` clause, we go directly to `GROUP BY`. It tells us to categorize the data by both `name` and `age`. We end up with a group of all the people named Ace who are 20 years old, a group of all the people named Ace who are 7 years old, a group of all the people named Ada who are 18 years old, and a group of all the people named Ada who are 27 years old.

---

```
name|age|COUNT(*)
----+---+--------
Ace |20 |2
Ace |7  |1
Ada |18 |2
Ada |27 |1
```

-

Last but not least, every group gets collapsed into a single row. According to our `SELECT` clause, each such row must contain three things:

* The `name` corresponding to the group.
* The `age` corresponding to the group.
* The number of rows within the group.

ENDSEQUENCE

## A word of caution

So that's how grouping and aggregation work, but before we move on I must emphasize one last thing regarding illegal queries. We'll start by considering these two examples:

1. Though it's not immediately obvious, this query actually produces an error:

   ```
   SELECT age, AVG(num_dogs)
   FROM Person;
   ```

    What's the issue? `age` is an entire column of numbers, whereas `AVG(num_dogs)` is just a single number. This is problematic because a properly formed table must have the same amount of rows in each column.

2. This one is bad too, for a very similar reason:

   ```
   SELECT age, num_dogs
   FROM Person
   GROUP BY age;
   ```

   After grouping by `age` we obtain a table like this:

   ```
   name|age|num_dogs
   ----+---+--------
   Ace |20 |4
   Ema |20 |2
   Ian |20 |3
   ----+---+--------
   Ada |18 |3
   Jay |18 |5
   ----+---+--------
   Cho |27 |3
   Rex |27 |1
   ----+---+--------
   Mae |33 |8
   ```

   Then the `SELECT` clause's job is to collapse each group into a single row. Each such row must contain two things:

   * The `age` corresponding to the group, which is a single number.
   * The `num_dogs` for the group, which is an entire column of numbers.

   So once again, we have this issue of trying to make a table with mismatching dimensions.

The takeaway from all this? If you're going to do _any_ grouping / aggregation at all, then you must _only_ `SELECT` grouped / aggregated columns. Make sure you understand this rule before you keep reading. It's such a common point of confusion that I'd even recommend writing it down, getting a tattoo of it, or likewise. At the very least, re-read this section later to make sure it still makes sense to you.

# More to come ...

This chapter is a work in progress. I'll try to add more details soon.