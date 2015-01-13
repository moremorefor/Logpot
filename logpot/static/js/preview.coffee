'use strict'

do ->

  marked.setOptions({
    highlight: (code) ->
      return hljs.highlightAuto(code).value
  })

  preview = new Vue({
    el: '#editor',
    data: {
      input:
        "
        ### Headline\n\n
        [Link](http://google.co.jp 'Title')\n\n
        ```
        python\n
        print('HellWorld')\n
        ```
        "
    },
    filters: {
      marked: marked
    }
  })

  $('#autosizable').autosize()
