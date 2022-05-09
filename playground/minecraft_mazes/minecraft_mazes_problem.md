# Mazes in Minecraft

## Problem Description

A maze was built in minecraft, but try as you might, you cannot find the path to the temple. So you have decided to
write a program to find the path. Luckily, you were able to write a command block program to print out the state of
the blocks to the chat, and have copied that to a file. You quickly count the number of rows and columns and add that to
the document as well as the starting and ending position. Now you just have to write a program to find the path to the
center, and you can show off your maze skills to the other players.

## Input Format

The input consists of the size of the map, the map itself, the starting position, and finally the ending position:

1. The first line will be a single number equaling the number of rows of map input.
2. The second line will be a single number equaling the number of columns in each row of map input.
3. A number of lines equal to the number of rows, each with a number of characters equal to the number of columns, will
   consist of either `0` meaning traversable space or `1` meaning an impassable space.
4. The first line after the map will have two numbers separated by a space representing the row and column that is the
   starting position of the map.
5. The second line after the map will have two numbers separated by a space representing the row and column that is the
   ending or goal position of the map.

## Output Format

The expected output format will be a list cardinal directions, representing the moves that need to be made to get from
the starting position to the ending position. Once the ending position is achieved, a single line saying "fin" should
be printed.

## Example

**Input**

```text
5
4
1101
1001
1011
1001
1101
0 2
4 2
```

**Output**

```text
south
west
south
south
east
south
fin
```

