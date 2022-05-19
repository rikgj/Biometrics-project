% The code is based on project structure

N_plots = 4;
plot_color = ['m', 'k', 'g', 'b'];

DIMS = ["64", "128", "256"];
REF = ["GT", "GT", "GT", "GT"];
%REF = ["GT", "bicubic", "BSRGAN", "SwinIR"];
PROBE = ["GT", "bicubic", "BSRGAN", "SwinIR"];

for DIM = DIMS
    ref_type = " Self";
    if strcmp(REF(2),"GT")
        ref_type = " GT";
    end
    curve_name = strcat(DIM, ref_type, ' ref');

    % Plot DET
    figure('Name',curve_name);
    title(curve_name);
    hold on;

    for n=1:N_plots
      mat_path = strcat('mat_scores\',DIM,'_ref_',REF(n),'_probe_',PROBE(n),'.mat');
      disp(mat_path)
      True_scores = load(mat_path, 'gen_score').gen_score;
      False_scores =  load(mat_path, 'imp_score').imp_score;

      [P_miss,P_fa] = Compute_DET(True_scores,False_scores);
      Plot_DET (P_miss,P_fa,plot_color(n));
    end

    % add legend if it is self ref
    if strcmp(REF(2),"GT") == 0
        legend("GT", "Bicubic", "BSRGAN", "SwinIR", 'Location','northeastoutside');
    end

    % save figure in imgs folder
    cd imgs
    saveas(gcf,curve_name,'jpg');
    cd ..
end