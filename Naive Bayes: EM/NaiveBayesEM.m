X = allgundata_em; % data set
acc_super = 0;
for j = 1:5
    data = X(cv.training(j), 4:15);
    d = size(data, 2);
    
    
    y_train = allgundata(cv.training(j), 16);
    x_train = data;
    % x_train(:, 16) = [];
    x_unlabel = x_train(y_train(:,1) == -1,:);
    x_train = x_train(y_train(:,1) ~= -1,:);
    y_train = y_train(y_train(:,1) ~= -1,:);
    
    m_train = size(y_train, 1);
    m_unlabel = size(x_unlabel, 1);
    m_train_pos = size(y_train(y_train(:,1) == 1, :), 1);
    p_pos = m_train_pos/m_train;
    
    x_train_pos = x_train(y_train(:,1) == 1, :);
    m_train_pos_pos = sum(x_train_pos == 1);
    m_train_pos_mis = sum(x_train_pos == -1);
    theta_pos_mis = m_train_pos_mis/m_train_pos;
    theta_pos_pos = m_train_pos_pos/m_train_pos;
    
    x_train_neg = x_train(y_train(:,1) == 0, :);
    m_train_neg_pos = sum(x_train_neg == 1);
    m_train_neg_mis = sum(x_train_neg == -1);
    theta_neg_mis = m_train_neg_mis/(m_train - m_train_pos);
    theta_neg_pos = m_train_neg_pos/(m_train - m_train_pos);
    
    for i = 1:100
        % E step
        %log_ratio = x_unlabel * (log(theta_neg_pos./theta_pos_pos))' + (1-x_unlabel) * (log((1-theta_neg_pos)./(1-theta_pos_pos)))';
        %new code starts
        log_ratio = (0.5 * x_unlabel .* (x_unlabel + 1) ) * (log(theta_neg_pos./theta_pos_pos))' ...
            + (0.5 * x_unlabel .* (x_unlabel - 1) ) * (log((theta_neg_mis)./(1-theta_pos_mis)))' ...
            + (-1 * (x_unlabel + 1) .* (x_unlabel - 1) ) * (log((1 - theta_neg_pos - theta_neg_mis)./(1-theta_pos_pos - theta_pos_mis)))';
        %new code ends
        q = 1./(1 + ((1-p_pos)/p_pos).*exp(log_ratio));
        
        % M step
        p_pos = (m_train_pos + sum(q))/(m_train + m_unlabel);
        num_pos_pos = m_train_pos_pos + q' * (x_unlabel == 1);
        dem_pos_pos = m_train_pos + sum(q);
        theta_pos_pos = num_pos_pos/dem_pos_pos;
        % add new code
        num_pos_mis = m_train_pos_mis + q' * (x_unlabel == -1);
        theta_pos_mis = num_pos_mis/dem_pos_pos;
        % end
        
        num_neg_pos = (m_train_neg_pos + (1-q)' * (x_unlabel == 1));
        dem_neg_pos = (m_train - m_train_pos) + sum(1-q);
        theta_neg_pos = num_neg_pos/dem_neg_pos;
        % add new code
        num_neg_mis = m_train_neg_mis + (1-q)' * (x_unlabel == -1);
        theta_neg_mis = num_neg_mis/dem_neg_pos;
        % end
    end
    w = log(theta_pos_pos./theta_neg_pos) - log((1-theta_pos_pos)./(1-theta_neg_pos)); 
    b = sum(log((1-theta_pos_pos)./(1-theta_neg_pos)),2) - log((1-p_pos)/p_pos);
    
    x_test = X(cv.test(j), 4:15);
    y_test = allgundata(cv.test(j), 16);
    
    log_ratio = (0.5 * x_test .* (x_test + 1) ) * (log(theta_neg_pos./theta_pos_pos))' ...
            + (0.5 * x_test.* (x_test - 1) ) * (log((theta_neg_mis)./(1-theta_pos_mis)))' ...
            + (-1 * (x_test + 1) .* (x_test - 1) ) * (log((1 - theta_neg_pos - theta_neg_mis)./(1-theta_pos_pos - theta_pos_mis)))';
    %new code ends
    q_test = 1./(1 + ((1-p_pos)/p_pos).*exp(log_ratio));
    
    m_test = size(y_test, 1);
    y_test_pred = q_test > 0.5;
    d = y_test((y_test_pred - y_test) == 0, :);
    acc_super = acc_super + size(y_test((y_test_pred - y_test) == 0, :), 1)/size(y_test(y_test ~= -1, :), 1); 
    
    
end
em_cv_error = 1 - (acc_super / 5);