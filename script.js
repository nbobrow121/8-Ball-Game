$(document).ready(function() {
    var $cueBall = $('circle[fill="WHITE"]');
    var isDragging = false;
    var $svg = $('svg');
    var $line = $('#line');

    function getCursorPoint(evt) {
        var point = $svg[0].createSVGPoint();
        point.x = evt.clientX;
        point.y = evt.clientY;
        return point.matrixTransform($svg[0].getScreenCTM().inverse());
    }

    function toggleTurn() {
        $('#turn-message-p1, #turn-message-p2').toggle();
    }

    function drawLine(coords) {
        $line.attr({
            'x1': $cueBall.attr('cx'),
            'y1': $cueBall.attr('cy'),
            'x2': coords.x,
            'y2': coords.y,
            'stroke': "red",
            'stroke-width': "5"
        });
    }

    function resetLine() {
        $line.attr({
            'x1': 0,
            'y1': 0,
            'x2': 0,
            'y2': 0
        });
    }

    $svg.on('mousemove', function(evt) {
        if (isDragging) {
            drawLine(getCursorPoint(evt));
        }
    });

    $cueBall.on('mousedown', function() {
        isDragging = true;
    });

    $(document).on('mouseup', function(evt) {
        if (isDragging) {
            isDragging = false;
            resetLine();
            var coords = getCursorPoint(evt);
            var postData = {
                x: Math.max(Math.min(-(coords.x - $cueBall.attr('cx')) * 4, 10000), -10000),
                y: Math.max(Math.min(-(coords.y - $cueBall.attr('cy')) * 4, 10000), -10000)
            };

            $.post("game.html", postData, function(data, status) {
                console.log("Response:", data, "Status:", status);
                animateSVGSequence(data);
            });
        }
    });

    function animateSVGSequence(data) {
        var svgArray = data.split(',');
        var $svgContainer = $('#svg-container');
        var delay = 15;
        $svgContainer.empty();
        svgArray.forEach(function(svgData, index) {
            setTimeout(function() {
                $svgContainer.html(svgData);
                refreshEventListeners();                 
            }, delay * index);
        });
    }

    function refreshEventListeners() {
        $cueBall = $('circle[fill="WHITE"]');
        $cueBall.off('mousedown').on('mousedown', function() {
            isDragging = true;
        });
    }
});