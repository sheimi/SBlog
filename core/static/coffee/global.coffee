$(document).ready () ->
  # for tooltip
  $('.bs-tooltip').tooltip()

  # set image wall wrapper
  $('img[alt="content image"]').each (index, value) ->
    $(this).addClass 'img-polaroid'

  $(window).on 'resize', (e) ->
    windowResize()

  windowResize()

window.windowResize = () ->
  if $('html').height() < $(window).height()
    $('.footer').addClass 'fix-bottom'
  else
    $('.footer').removeClass 'fix-bottom'
