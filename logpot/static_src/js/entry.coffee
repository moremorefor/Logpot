'use strict'

do ->

  $('.highlight').each( (i, block) ->
    hljs.highlightBlock(block)
  )
