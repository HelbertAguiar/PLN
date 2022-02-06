from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

class NuvemPalavras(object):

    def execute(self, path_file_read, path_png_file):
        # lendo os dados
        data = pd.read_csv(path_file_read)
        df = pd.DataFrame(data, columns=['text'])

        # salvando cada tweet numa lista de str
        todas_palavras = []
        for index, row in df.iterrows():
            todas_palavras.append(str(row))

        # convertendo em string
        todas_palavras = ' '.join([texto for texto in todas_palavras])

        # gerando nuvem de palavras
        nuvem_palavras = WordCloud(width= 800, height= 500,
                                max_font_size = 110,
                                collocations = False).generate(todas_palavras)

        # plotando/salvando imagem da nuvem de palavras
        plt.figure(figsize=(10,7))
        plt.imshow(nuvem_palavras, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(path_png_file)

path_read_file = "./tw/collected_tweets_2021-04-01.csv"
path_save_pngfile = "work_cloud.png"

nuvem = NuvemPalavras()
nuvem.execute(path_read_file, path_save_pngfile)

