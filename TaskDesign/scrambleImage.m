function scrambledImg = scrambleImage(img, blockSize)
    [h, w, c] = size(img);
    h = h - mod(h, blockSize);
    w = w - mod(w, blockSize);
    img = img(1:h, 1:w, :);
    numBlocksH = h / blockSize;
    numBlocksW = w / blockSize;
    blocks = cell(numBlocksH, numBlocksW);

    for i = 1:numBlocksH
        for j = 1:numBlocksW
            blocks{i,j} = img((i-1)*blockSize+1:i*blockSize, (j-1)*blockSize+1:j*blockSize, :);
        end
    end

    idx = randperm(numBlocksH * numBlocksW);
    scrambledImg = zeros(size(img), 'uint8');

    for i = 1:numBlocksH
        for j = 1:numBlocksW
            k = idx((i-1)*numBlocksW + j);
            src_i = ceil(k / numBlocksW);
            src_j = mod(k-1, numBlocksW) + 1;
            scrambledImg((i-1)*blockSize+1:i*blockSize, (j-1)*blockSize+1:j*blockSize, :) = blocks{src_i, src_j};
        end
    end
end
