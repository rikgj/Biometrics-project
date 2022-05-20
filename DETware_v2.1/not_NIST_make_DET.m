% The code is based on project structure

N_plots = 4;
plot_color = ['m', 'k', 'g', 'b'];

DIMS = ["64", "128", "256"];
%DIMS = ["64"];
%REF = ["GT", "GT", "GT", "GT"];
REF = ["GT", "bicubic", "BSRGAN", "SwinIR"];
PROBE = ["GT", "bicubic", "BSRGAN", "SwinIR"];

save_fig = false;
adjust_bounds = true;

for num = 1:size(DIMS,2)
    DIM = DIMS(num);
    
    ref_type = " Self";
    if strcmp(REF(2),"GT")
        ref_type = " GT";
    end
    curve_name = strcat(DIM, ref_type, ' ref');
    
    % adjust bounds
    if adjust_bounds 
        % set bounds
        if strcmp(DIM,"64")
            y_min = 0.001;
            y_max = 0.90;
            x_min = 0.001;
            x_max = 0.40;
        elseif strcmp(DIM,"128") 
            y_min = 0.001;
            y_max = 0.55;
            x_min = 0.001;
            x_max = 0.4;
        elseif strcmp(DIM,"256")
            y_min = 0.001;
            y_max = 0.09;
            x_min = 0.00002;
            x_max = 0.003;
        end
       Set_DET_limits(y_min,y_max,x_min,x_max);
    end
    
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
    if save_fig
        cd imgs
        saveas(gcf,curve_name,'jpg');
        cd ..
    end
end

clear global DET_limits;