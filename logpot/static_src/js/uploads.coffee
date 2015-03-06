'use strict'

addImageFieldButton = document.getElementById 'addImageField'
imageFieldset = document.getElementById 'imageFieldset'

initialize = ->
  imagefieldset = $('#imageFieldset').clone()
  imagefieldset.removeAttr('id')
  imagefieldset.children('div')[0].remove()
  fieldset = imagefieldset.wrap('<div>').parent().html()

  addImageFieldButton.addEventListener 'click', (evt) ->
    evt.preventDefault()
    html = $.parseHTML(fieldset)
    $('#form-buttons').before(html)


do ->
  console.log 'initialize'
  initialize()
