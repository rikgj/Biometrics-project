% The code will compute DET curves using the scores produced by
% get_similarity_scores.py.
% Note that the NIST code assumes high score --> match


% The code is based on project structure
%   GT
%   bicubic
%   BSRGAN
%   SwinIR

DIMS = ["64", "128", "256"];
REF = 'GT';
PROBE = 'bicubic';

for DIM = DIMS

%base_path = strcat('..\scores\',DIM,'\',DIM,'_similarity\');
base_path = strcat('..\true_sim_score\',DIM,'\');
base_name = strcat(DIM,'_ref_',REF,'_probe_',PROBE);

gen_name = strcat(base_name ,'_genuine_scores');
gen_score_path = strcat(base_path, gen_name, '.txt');

imp_name = strcat(base_name, '_imposter_scores');
imp_score_path = strcat(base_path, imp_name, '.txt');

% read genuine score
fileID = fopen(gen_score_path,'r');
formatSpec = '%f';
gen_score = fscanf(fileID,formatSpec);
% adapt score to NIST assumption
% gen_score = abs(gen_score-1);

save_at = strcat('mat_scores\',base_name);
save(save_at, 'gen_score');
fclose(fileID);

% read imposter score (repeat above)
fileID = fopen(imp_score_path,'r');
formatSpec = '%f';
imp_score = fscanf(fileID,formatSpec);
% adapt score to NIST assumption
%imp_score = abs(imp_score-1);

save_at = strcat('mat_scores\',base_name);
save(save_at, 'imp_score', '-append');
fclose(fileID);

end
