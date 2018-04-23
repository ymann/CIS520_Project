%% LOAD DATA
X = load('em_gun_data.csv'); %%CHANGE DATA HERE
Y = X(:,16); %%GET LABELS FROM ROW 16 (COMMENT OUT BELOW IF LABELS GIVEN SEPARATELY)
Y = Y(1:15222,:);
X(:,16)=[];
X_labeled = X(1:15222,:);
X_unlabeled = X(15223:23897,:);
cv = cvpartition(Y, 'k', 5);

%% NAIVE BAYES
err = zeros(cv.NumTestSets,1);
for i = 1:cv.NumTestSets
    trainIdx = cv.training(i);
    testIdx = cv.test(i);
    mdl = fitcnb(X_labeled(trainIdx,:),Y(trainIdx,:));
    ytest = predict(mdl,X_labeled(testIdx,:));
    err(i) = size(find(ytest ~= Y(testIdx,:)),1) / size(Y(testIdx,:),1);
end
cvErr = sum(err)/5;

% %% DRAW FIGURE
% figure
% gscatter(X(:,1),X(:,2),Y);
% h = gca;
% cxlim = h.XLim;
% cylim = h.YLim;
% hold on
% Params = cell2mat(mdl.DistributionParameters);
% Mu = Params(2*(1:3)-1,1:2); % Extract the means
% Sigma = zeros(24,24,3);
% for j = 1:3
%     Sigma(:,:,j) = diag(Params(2*j,:)).^2; % Create diagonal covariance matrix
%     xlim = Mu(j,1) + 4*[1 -1]*sqrt(Sigma(1,1,j));
%     ylim = Mu(j,2) + 4*[1 -1]*sqrt(Sigma(2,2,j));
%     ezcontour(@(x1,x2)mvnpdf([x1,x2],Mu(j,:),Sigma(:,:,j)),[xlim ylim])
%         % Draw contours for the multivariate normal distributions
% end
% h.XLim = cxlim;
% h.YLim = cylim;
% hold off

%% LOGISTIC REGRESSION WITH L1

Lambda = logspace(-6,-0.5,11);
CVMdl = fitclinear(X_labeled,Y,'ObservationsIn','rows','KFold',5,...
    'Learner','logistic','Solver','sparsa','Regularization','lasso',...
    'Lambda',Lambda,'GradientTolerance',1e-8);
numCLModels = numel(CVMdl.Trained);
Mdl1 = CVMdl.Trained{1};
ce = kfoldLoss(CVMdl);

% Mdl = fitclinear(X_labeled,Y,'ObservationsIn','rows',...
%     'Learner','logistic','Solver','sparsa','Regularization','lasso',...
%     'Lambda',Lambda,'GradientTolerance',1e-8);
% numNZCoeff = sum(Mdl.Beta~=0);
% 
% %plot
% figure;
% [h,hL1,hL2] = plotyy(log10(Lambda),log10(ce),...
%     log10(Lambda),log10(numNZCoeff)); 
% hL1.Marker = 'o';
% hL2.Marker = 'o';
% ylabel(h(1),'log_{10} classification error')
% ylabel(h(2),'log_{10} nonzero-coefficient frequency')
% xlabel('log_{10} Lambda')
% title('Test-Sample Statistics')
% hold off
