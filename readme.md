I want to do some text mining on scientific papers
to get better search engine results.

In particular, I have a corpus of four or five related papers
each between three and six thousand words
(the "good" papers that I want to show up in search results)
and another corpus of papers from the same field
which have shown up in search engine results
but don't do the characterization methods I'm interested in
(the "false positives").

Related:

>   My first, rather naive, thought was to segment each of the docs into
>   sentences and then compare sentences using a variety of fuzzy matching
>   techniques, retaining the ones that sort-of matched. That approach was a
>   bit ropey (I’ll describe it in another post), but whilst pondering it over
>   a dog walk a much neater idea suggested itself – compare n-grams of various
>   lengths over the two documents. At it’s heart, all we need to do is find
>   the intersection of the ngrams that occur in each document.

<https://blog.ouseful.info/2015/12/13/finding-common-phrases-or-sentences-across-different-documents/>
