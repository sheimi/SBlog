window.iframeAutoResize = (id) ->
  delayPost = () ->
    if document.getElementById
      doc = document.getElementById(id).contentWindow.document.getElementsByClassName('gist')[0]
      if not doc
        return
      newheight = doc.scrollHeight
    document.getElementById(id).height = "#{newheight}px"
  setTimeout delayPost, 100

gistTag = (scope, elm, attrs) ->
  gistId = attrs.gist
  iframe = document.createElement('iframe')
  iframe.id = "gist-" + gistId
  iframe.setAttribute('width', '100%')
  iframe.setAttribute('frameborder', '0')
  iframe.setAttribute('onload', "iframeAutoResize('#{iframe.id}')")
  elm[0].appendChild(iframe)
  iframeHtml = """
  <html>
  <head>
    <base target="_parent">
    <style>
    table {
      font-size:12px;
    }
    .gist-file {
      margin: 0 !important;
    }
    </style>
  </head>
  <body style="margin:0;">
    <script src="https://gist.github.com/#{gistId}.js"></script>
  </body>
  </html>"""
  doc = iframe.document
  if iframe.contentDocument
    doc = iframe.contentDocument
  else if iframe.contentWindow
    doc = iframe.contentWindow.document
  doc.open()
  doc.writeln(iframeHtml)
  doc.close()


compileTag = ($compile) ->
  return (scope, element, attrs) ->
    watchForChange = (scope) ->
      # watch the 'compile' expression for changes
      return scope.$eval attrs.compile
    ifChange = (value) ->
      # when the 'compile' expression changes
      # assign it into the current DOM
      element.html value
      # compile the new DOM and link it to the current
      # scope.
      # NOTE: we only compile .childNodes so that
      # we don't get into infinite loojp compiling ourselves
      $compile(element.contents())(scope)
    scope.$watch watchForChange, ifChange


angular.module 'sblogApp'
       .directive 'gist', () ->
         return gistTag
       .directive 'compile', ['$compile', compileTag]
