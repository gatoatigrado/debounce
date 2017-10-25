# debounce

Demo of a debounce method that's reasoanbly efficient with threads. It still
needs to create and end threads, otherwise the interpreter will hang, but
doesn't cancel and re-create threads if there are no more remaining.

Note that debounce waits `interval` seconds after the last call. If you want
to ensure the function will run with a continuous stream of events, you want
something like `throttle` (in `lodash.js` terminology).

See `debounce.py`.
