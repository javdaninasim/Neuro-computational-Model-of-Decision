
function [response, confidence] = getMouseResponse(leftBarBase, rightBarBase, barSegmentHeight, numLevels)
    response = '';
    confidence = 0;
    
    leftBarBounds = [leftBarBase(1), leftBarBase(2), leftBarBase(3), leftBarBase(4)];
    rightBarBounds = [rightBarBase(1), rightBarBase(2), rightBarBase(3), rightBarBase(4)];
    
    [x, y, buttons] = GetMouse;
    
    if x >= leftBarBounds(1) && x <= leftBarBounds(3) && y >= leftBarBounds(2) && y <= leftBarBounds(4)
        response = 'NonAnimall';
        relativeY = y - leftBarBounds(2);
        confidence = numLevels - floor(relativeY / barSegmentHeight);
        confidence = max(1, min(numLevels, confidence));
    end
    
    if x >= rightBarBounds(1) && x <= rightBarBounds(3) && y >= rightBarBounds(2) && y <= rightBarBounds(4)
        response = 'Animall';
        relativeY = y - rightBarBounds(2);
        confidence = numLevels - floor(relativeY / barSegmentHeight);
        confidence = max(1, min(numLevels, confidence));
    end
end
