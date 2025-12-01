basic tight list
.
- item1

- item2

- item3
.
- item1
- item2
- item3
.

numbered tight list
.
1. first

2. second

3. third
.
1. first
2. second
3. third
.

mixed markers preserved
.
- item1
- item2

* item3
* item4
.
- item1
- item2

* item3
* item4
.

list after paragraph
.
Some text here.

- item1

- item2
.
Some text here.

- item1
- item2
.

paragraph after list
.
- item1

- item2

Some text here.
.
- item1
- item2

Some text here.
.

nested lists with alternating markers
.
- Outer 1
  * Inner 1
  * Inner 2
- Outer 2
  * Inner 3
  * Inner 4
.
- Outer 1
  - Inner 1
  - Inner 2
- Outer 2
  - Inner 3
  - Inner 4
.

multiple list types
.
Some intro text.

- List 1 item 1

- List 1 item 2

* List 2 item 1

* List 2 item 2

1. Numbered item 1

2. Numbered item 2
.
Some intro text.

- List 1 item 1
- List 1 item 2

* List 2 item 1
* List 2 item 2

1. Numbered item 1
2. Numbered item 2
.

complex nested structure
.
1. First ordered item
   - Nested unordered
   - Another nested
2. Second ordered item
   * Different marker
   * Maintains structure
.
1. First ordered item
   - Nested unordered
   - Another nested
2. Second ordered item
   - Different marker
   - Maintains structure
.

list with blank lines in items
.
- First item with multiple paragraphs

  Second paragraph of first item

- Second item
.
- First item with multiple paragraphs

  Second paragraph of first item

- Second item
.

empty list items
.
- First item
- 
- Third item
.
- First item
-
- Third item
.

mixed single and multi paragraph items
.
- Simple item 1

- Item with multiple paragraphs

  Second paragraph here

- Simple item 2
.
- Simple item 1

- Item with multiple paragraphs

  Second paragraph here

- Simple item 2
.
nested to top-level marker change
.
- Dash list
  - Nested dash
  - Another nested
* Asterisk list at top level
.
- Dash list
  - Nested dash
  - Another nested

* Asterisk list at top level
.

deep nesting all tight
.
- Level 1
  * Level 2 asterisk
    1. Level 3 ordered
    2. Another ordered
    - Level 3 dash
  * Back to level 2
- Back to level 1
.
- Level 1
  - Level 2 asterisk
    1. Level 3 ordered
    2. Another ordered
    - Level 3 dash
  - Back to level 2
- Back to level 1
.

marker normalization nested
.
1. Ordered parent
   - Unordered child
   - Another unordered
2. Another ordered
   + Plus marker nested
   + Still converted to dash
.
1. Ordered parent
   - Unordered child
   - Another unordered
2. Another ordered
   - Plus marker nested
   - Still converted to dash
.

binary marker alternation
.
- Dash list item
- Another dash item
* Asterisk list (alternates)
* Another asterisk
+ Plus list (becomes dash)
+ Another plus
.
- Dash list item
- Another dash item

* Asterisk list (alternates)
* Another asterisk

- Plus list (becomes dash)
- Another plus
.

complex alternation pattern
.
- First dash list
- Another dash
+ Plus list (will become asterisk for alternation)
+ Another plus
* Original asterisk (will become dash for alternation)
* Another asterisk
.
- First dash list
- Another dash

* Plus list (will become asterisk for alternation)
* Another plus

- Original asterisk (will become dash for alternation)
- Another asterisk
.