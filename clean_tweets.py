from os import listdir
import pandas as pd
import re

class Cleaner(object):

    def execute(self, files, path_file_destino):
        
        # uso apenas pra setar que o parametro header é verdadeiro ao exportar do CSV no final na primeira execucao
        first_execution = False

        for pathfile in files:

            # ler arquivo .CSV
            df = pd.read_csv(pathfile)

            # remove colunas sem utilidade
            df.drop(columns=['tweet_id', 'lang'], axis=1, inplace=True)
            df.drop(df.columns[[0]], axis=1, inplace=True)

            # troca nome da coluna 'date' por 'tweet_date' e 'country_code' por 'city'
            df.rename(columns={"date":"tweet_date"}, inplace=True)
            df.rename(columns={"country_code":"city"}, inplace=True)

            # remove linhas invalidas da coluna 'user_location' / basicamente onde não tem o termo ", Brasil" é removido
            df['user_location'] = df['user_location'].map(self.verify_location_from_brazil)
            df.drop(df[(df['user_location'] == 'undefined')].index, inplace=True)

            # remove marcações de outras pessoas, por exemplo: @nome_pessoa
            df['text'] = df['text'].map(self.on_text_remove_person_citation)

            # remove links contidos na coluna 'text' do dataframe
            df['text'] = df['text'].map(self.remove_https_from_str)

            # remove linhas onde a mensagem é menor que 12 caracteres
            df['text'] = df['text'].map(self.verify_length_msg)
            df.drop(df[(df['text'] == 'short_msg')].index, inplace=True)

            # adiciona cidade extraido da coluna 'user_location'
            df['city'] = df['user_location'].map(self.extract_city)

            # exporta para arquivo .CSV sem incluir INDEX e sem deletar dados anteriores (append)
            if first_execution == False: 
                df.to_csv(path_file_destino, index=False, header=True, encoding='utf-8', mode='a')
                # df.to_excel("./resultado.xlsx", index=False, header=True, encoding='utf-8')
            else:
                df.to_csv(path_file_destino, index=False, header=False, encoding='utf-8', mode='a')
                # df.to_excel("./resultado.xlsx", index=False, header=False, encoding='utf-8')

            first_execution = True

    def extract_city(self, string):
        try:
            string = re.search(".*,", string, re.IGNORECASE)
            string = str(string.group(0))
            string = re.sub('[,@!/->:;()<*&%#]+', '', string)
            string = string.strip()
            string = re.sub('\s{1}[-]\s{1}', '', string)
            string = string.strip()
            string = re.sub('\s{1}[-]', '', string)
            string = string.strip()
            string = re.sub('[-]\s{1}', '', string)
            string = string.strip()
            string = re.sub('[A-Z][A-Z]', '', string)
            string = string.strip()
            string = re.sub('[-]$', '', string)
            string = string.strip()
            string = re.sub('^[.]', '', string)
            city = string.strip()
        except:
            city = 'erro'
        finally:
            return city

    def verify_location_from_brazil(self, text_location):
        mark = 'undefined'
        try:
            if re.search(".*, Brasil$", text_location, re.IGNORECASE):
                mark = text_location
            elif re.search(".*, Brazil$", text_location, re.IGNORECASE):
                mark = text_location
            elif re.search(".*,Brazil$", text_location, re.IGNORECASE):
                mark = text_location
            elif re.search(".*,Brasil$", text_location, re.IGNORECASE):
                mark = text_location
        except:
            mark = 'undefined'
        finally:
            return mark

    def verify_length_msg(self, text):
        mark = 'short_msg'
        try:
            if len(text.strip()) > 12:
                mark = text
        except:
            mark = 'short_msg'
        finally:
            return mark

    def on_text_remove_person_citation(self, text):
        text_replaced = re.sub("@[a-zA-Z0-9.-_]*", "", text)
        text_replaced = re.sub(' +', ' ', text_replaced)
        return text_replaced.strip()

    def remove_https_from_str(self, text):
        try:
            str_replaced = re.sub("https://t.*", "", text) 
        except:
            str_replaced = text
        finally:
            return str_replaced.strip()
    
    def find_csv_filenames(self, path_to_dir, suffix):
        filenames = listdir(path_to_dir)
        return [ (path_to_dir + filename) for filename in filenames if filename.endswith( suffix ) ]

path_root_files = "./tw/"
path_file_destino = "./preprocessed_tweets.csv"
type_files = ".csv"

cleaner = Cleaner()
files = cleaner.find_csv_filenames(path_root_files, type_files)

# passar lista de arquivos ('files') para processar e o nome do arquivo final para salvar ('path_file_destino')
cleaner.execute(files, path_file_destino)




