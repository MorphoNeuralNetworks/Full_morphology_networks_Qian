library(ggpubr)
library(reticulate)

np <- import("numpy")

dens_hom <- np$load("../Code_figs/Figure1+Sup1/Code_single_neuron_av_dens__ancova/best_density_neuron.npy", allow_pickle = T)
dens_hom <- unlist(dens_hom)*0.061

bt_n <- read.csv("../Code_figs/Code20230209/Figure1/BoutonDataCellType.csv", header=F)

sum(bt_n$V1==names(dens_hom))

inc_stypes <- c('LGd','MG','VPL','VPM','RT','CP','DG','VISp','SSp-ul','MOs','MOp','SSp-n','SSp-bfd','SSp-m','SSs','CLA','AId','RSPv')
dens_hom <- dens_hom[bt_n$V2 %in% inc_stypes]
bt_n <- bt_n[bt_n$V2 %in% inc_stypes,]

ncells <- table(bt_n$V2)

df_plot <- data.frame(label=paste0(bt_n$V2," (N=",ncells[bt_n$V2],")"),
                      bt_dens=dens_hom)

df_plot$coarse_reg <- bt_n$V2
df_plot$coarse_reg[df_plot$coarse_reg %in% c("LGd","MG","VPL","VPM","RT")] <- "Thalamus"
df_plot$coarse_reg[df_plot$coarse_reg %in% c("CP")] <- "Striatum"
df_plot$coarse_reg[df_plot$coarse_reg %in% c("DG")] <- "Hippocampus"
df_plot$coarse_reg[!(df_plot$coarse_reg %in% c("LGd","MG","VPL","VPM","RT","CP","DG"))] <- "Cortex"

df_plot[]

ggboxplot(df_plot,x="label",y="bt_dens",fill="coarse_reg",
          position = position_dodge(), palette="Set1")+
  xlab("Soma region") +
  ylab("Bouton density [boutons/1um]") +
  scale_fill_brewer(name = "Soma region", palette="Set1") +
  theme(axis.text.x = element_text(angle = 45, vjust = 1, hjust=1)) +
  scale_y_continuous(expand = c(0,0)) 
