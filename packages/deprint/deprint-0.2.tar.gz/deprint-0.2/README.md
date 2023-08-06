# Deprint - Declarative Python fancy print statement

Deprint allows you to write a complex yet easy to understand print statement in Python, resulting in beautiful CLI interface on any ANSI/VT100 terminal emulators.

## Installation

Install via pip

```
pip install deprint
```

## Basic usage

Deprint can be used in either the declarative style or the imperative (persistent) style.

### Declarative style

Declarative syntax of Deprint only applies the style to the text only once with no effect to other print statements.
```
from deprint import deprint

dp = deprint()

# clear screen
dp.clear()

# print red text
dp.colour('red').print('red text)

# print bold text
dp.style('bold').print('bold text')

# print light_blue text on yellow background
dp.colour('blue').bg('yellow').print('blue on yellow text')

# print green underlined text on white background
dp.style('underlined').colour('green').bg('white').print('underlined green text')
```

### Persistent style

Persistent syntax of Deprint applies the style globally to the terminal session. All print statements (including Python's native print()) are affected by the persistent styling.

```
from deprint import deprint

dp = deprint()

# clear screen
dp.clear()

# print red text
dp.setColour('red')
dp.print('red text')
print('This text is also red')

# print light_blue text on yellow background
dp.setColour('light_blue')
dp.setBackground('yellow')
dp.print('blue on yellow text')

# print green underlined text on white background
dp.setColour('green')
dp.setBackground('white')
dp.setStyle('underlined')
dp.print('underlined green text)

# reset to default style
dp.reset()
```

## API documentation

### *class* deprint.deprint()

Print fancy terminal output.

#### Methods

deprint.deprint.**clear**()

Clear entire terminal screen.

---

deprint.deprint.**emptylines**(num=1)

Print *num* empty lines to the terminal.

---

deprint.deprint.**reset**()

Reset all style to terminal's default.

---

deprint.deprint.**print**(text)

Print *text* to the terminal with the applied style.

The print method will maintain the style if the style is set through the persistent methods, or reset to default if the style is set through the declarative methods.

##### Declarative

deprint.deprint.**colour**(colour)

Apply colour to the printed text.

Colour can be either a number between 1 - 256 (8bit colour) or one of the following strings:
black, red, green, yellow, blue, magenta, cyan, light_grey,dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, white, default, reset.

---

deprint.deprint.**bg**(colour)

Apply background colour to the printed text.

Colour can be either a number between 1 - 256 (8bit colour) or one of the following strings:
black, red, green, yellow, blue, magenta, cyan, light_grey,dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, white, default, reset.

---

deprint.deprint.**style**(style)

Apply text style to the printed text.

Style can be on of the following stings: bold, dim, underlined, blink, inverse, hidden, default, reset.

---

deprint.deprint.**hold**()

Prevent the print statement to end with a new line.

##### Persistent

deprint.deprint.**setColour**(colour)

Change the colour of the terminal's printed text.

Colour can be either a number between 1 - 256 (8bit colour) or one of the following strings:
black, red, green, yellow, blue, magenta, cyan, light_grey,dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, white, default, reset.

---

deprint.deprint.**setBackground**(colour)

Change the colour of the terminal's printed text's background.

Colour can be either a number between 1 - 256 (8bit colour) or one of the following strings:
black, red, green, yellow, blue, magenta, cyan, light_grey,dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan, white, default, reset.

---

deprint.deprint.**setStyle**(style)

Change the text style of the terminal's printed text.

Style can be on of the following stings: bold, dim, underlined, blink, inverse, hidden, default, reset.