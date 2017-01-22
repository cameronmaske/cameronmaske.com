title: ES6 Cheatsheet
date: 2017-01-12
published: true
topic: ES6, JAVASCRIPT
intro: Recently, I've switched to working with ES6. Here I've documented my every growing ES6 personal cheatsheet.

This is not intended to be an in an depth guide, but rather a quick reference of the most elegant javascript approaches I've found to dealing with various common scenarios.

## Immutable operations on an array.

### Adding an element.

<script src="//repl.it/embed/FQ67/0.js"></script>

### Removing an element.

<script src="//repl.it/embed/FQ6d/0.js"></script>

## Immutable operations on an object.

### Adding key/value.

<script src="//repl.it/embed/FQ6h/1.js"></script>

### Removing a key.

<script src="//repl.it/embed/FQ6n/1.js"></script>

### Adding a nested key/value.

<script src="//repl.it/embed/FQ7W/1.js"></script>

*Bad*: **Be careful**, directly deleting nested keys doesn't work as you might expect with the spread operation.

<script src="//repl.it/embed/FQ76/1.js"></script>

### Removing a nested key.

<script src="//repl.it/embed/FQ70/1.js"></script>

### Looping over keys of an object.

<script src="//repl.it/embed/FQ8O/2.js"></script>

### Looping over values of an object.

<script src="//repl.it/embed/FQ8O/3.js"></script>

### Looping over key/values of an object.

<script src="//repl.it/embed/FQ8O/1.js"></script>

Require's [`Object.entries`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/entries). You may need to install [Babel Runtime transform](https://babeljs.io/docs/plugins/transform-runtime/).


## Additional Resources

* [`lodash` documentation](https://lodash.com)
* The [`...` spread syntax](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_operator)
* [Spread syntax vs `Object.assign`](http://stackoverflow.com/questions/32925460/spread-operator-vs-object-assign)
* [Immutable Update Patters](http://redux.js.org/docs/recipes/reducers/ImmutableUpdatePatterns.html)
