# pyfathom
Text comprehension library for python

## Example
Given a collection of input strings with varying syntax:
```
    '180g | 1 cup uncooked brown rice',
    '½ small butternut squash , cubed',
    '5½ tablespoons tahini (you can sub cashew butter)',
    'pecans 125g',
    'flat-leaf parsley a bunch, roughly chopped',
    'rocket 70g',
    'leftover marinade from the mushrooms',
    '15 oz (425 g) black beans, drained (reserve ¼ cup (60 ml) of the juice) and rinsed well',
    '1/4 teaspoon Garam Masala, for garnish',
    '2 tablespoons chopped cilantro, for garnish',
```
and a set of "knowledge" rules defining what is known about the inputs, e.g.:
```
/\d+/ is number
number,/-|–/,number is range
/tbsp/ is unit
/cups?/ is unit
range|number,unit,/of/? is amount
amount,/\w+/+ is ,ingredient
```
PyFathom attempts to label each part of the string with a type name:
```
    '<amount><number>180</number><unit>g</unit><amount>|<amount><number>1</number><unit>cup</unit></amount><ingredient>uncooked brown rice</ingredient>',
    '<amount><number>½</number></amount><ingredient>small butternut squash</ingredient>,<ingredient>cubed</ingredient>',
    '<amount><number>5½<number><unit>tablespoons</unit></amount><ingredient>tahini</ingredient>(<ingredient>you can sub cashew butter</ingredient>)',
    '<ingredient>pecans</ingredient><amount><number>125</number><unit>g</unit></amount>',
    '<ingredient>flat-leaf parsley a bunch</ingredient>,<ingredient>roughly chopped</ingredient>',
    '<ingredient>rocket</ingredient><amount><number>70</number><unit>g</unit></amount>',
    '<ingredient>leftover marinade from the mushrooms</ingredient>',
    '<amount><number>15<number><unit>oz</unit></amount>(<amount><number>425</number><unit>g</unit></amount>)<ingredient>black beans</ingredient>,<ingredient>drained</ingredient>(<ingredient>reserve</ingredient><amount><number>¼</number><unit>cup</unit></amount>(<amount><number>60<number><unit>ml</unit></amount>)<ingredient>of the juice</ingredient>)<ingredient>and rinsed well</ingredient>',
    '<amount><number>1/4</number><unit>teaspoon</unit></amount><ingredient>Garam Masala</ingredient>,<ingredient>for garnish</ingredient>',
    '<amount><number>2<number><unit>tablespoons</unit></amount><ingredient>chopped cilantro</ingredient>,<ingredient>for garnish</ingredient>',
```
and can extract the parts of a particular type, e.g. ingredient:
```
    'uncooked brown rice',
    'small butternut squash',
    'tahini',
    'pecans',
    'flat-leaf parsley a bunch',
    'rocket',
    'leftover marinade from the mushrooms',
    'black beans',
    'Garam Masala',
    'chopped cilantro',
```
