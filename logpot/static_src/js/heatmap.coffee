setContainerWidth = ->
  graphWidth = $('.cal-heatmap-container').width()
  $('#heatmapContainer').css( width: graphWidth ).fadeIn()

do ->
  startDate = new Date()
  startDate.setMonth(0)

  cal = new CalHeatMap()
  cal.init(
    itemSelector: "#heatmap"
    data: "/api/v1/entry/heatmap"
    dataType: "json"
    cellSize: 8
    domain: "month"
    subDomain: "day"
    domainGutter: 6
    range: 12
    tooltip: true
    start: startDate
    domainLabelFormat: "%b"
    legend: [1, 3, 5, 7, 9]
    legendColors:
      min: "#dae289"
      max: "#44a340"
      empty: "#eee"

    onClick: (date, nb) ->
      console.log("onClick:", date, " : ", nb)
    afterLoad: ->
      console.log("afterLoad")
    onComplete: ->
      console.log("onComplete")
      setContainerWidth()
  )
