library(ggplot2)
library(plotly)
library(magick)
# Download the data we will use for plotting
# download.file("https://raw.githubusercontent.com/biocorecrg/CRG_RIntroduction/master/de_df_for_volcano.rds", "de_df_for_volcano.rds", method="curl")

# logFC_threshold = 0.45
# pv_threshold = 0.05
generateVocPlot <- function(input_df, logFC_threshold, pv_threshold) {
    # tmp <- read.csv("static/data/colorectal/colorectal_DMP_analysis_result_TN.csv")
    tmp <- input_df
    # remove rows that contain NA values
    # de <- tmp[complete.cases(tmp), ]
    de <- tmp
    is_hyper <- de$logFC > logFC_threshold & de$P.Value < pv_threshold
    is_hypo <- de$logFC < -logFC_threshold& de$P.Value < pv_threshold
    is_in_prom_reg <- grepl("TSS", de$feature, perl=TRUE) & !grepl("opensea", de$cgi, perl=TRUE)

    de$diffexpressed <- "No"
    de$diffexpressed[is_hyper] <- "Hyper"
    de$diffexpressed[is_hypo] <- "Hypo"
    de$diffexpressed[is_in_prom_reg] <- "Prom_reg"


    # Now write down the name of genes beside the points...
    # Create a new column "delabel" to de, that will contain the name of genes differentially expressed (NA in case they are not)
    # de$delabel <- NA
    # de$delabel[de$diffexpressed != "NO"] <- de$gene[de$diffexpressed != "NO"]

    # plot without labels
    my_plot <- ggplot(data=de, aes(x=logFC, y=-log10(P.Value), col=diffexpressed)) + geom_point() + theme_minimal() + ggtitle(label="TN")

    # plot with labels
    # my_plot <- ggplot(data=de, aes(x=logFC, y=-log10(P.Value), col=diffexpressed, label=delabel)) + geom_point() + theme_minimal() +  geom_text()
    p2 <- my_plot +
        theme_dark() +
        scale_color_manual(values=c("#65ebc033", "#db273c33", "#ffffff33", "#000000")) + # Hyper, Hypo, No, Prom
        geom_vline(xintercept=c(-logFC_threshold, logFC_threshold), col="red") +
        geom_hline(yintercept=-log10(0.05), col="blue")
    # png("volcano_plot_TN_male.png")
    # print(p2)
    # dev.off()
    fig <- image_graph(width = 500, height=500, res=96)
    print(p2)
    dev.off()
    figpng <- image_write(fig, path=NULL, format="png")

    return (figpng)
}
# The RDS format is used to save a single R object to a file, and to restore it.
# Extract that object in the current session:
