#let's import our packages
import pandas as pd 
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

#read the dataset
df=pd.read_csv("/content/all_data.csv")

#Do you see what I see?
#yes it seems that TYPE and Committee columns are gathered like they are lists
#that's because of my mistakes in episode1 , no worry I corrected the that part in code file
df.head()


# let's clean the data
df2=df.drop(columns=['Unnamed: 0', 'Num','DATE'])
#because we don't need them and they are not useful moreover they are not clean 
df3=df2.drop_duplicates(subset="Title")
#there are duplicates not because of the data itself but because of the way I crawl the site
# ethics.research.ac.ir update in times which I don't have any idea about it but the point is that 
#instead of adding the new studies to the end of the previous data ; they add to the begining of them
#let's save the cleaned data
df3=df3.dropna()
df3.to_csv("/content/all_data_df3.csv")

df3.shape

df3.isnull().sum()

df3["TYPE"].value_counts()

#draw the wordcloud
mask = np.array(Image.open("/content/mostlast.jpg"))

corpus = " ".join(str(cat).lower() for cat in df3.Title)
stopwords = set(STOPWORDS)
wordcloud = WordCloud(width = 1000, height = 1000,background_color ='white', 
                      random_state=1,collocations=False,stopwords = stopwords,
                      min_font_size =1, mask=mask).generate(corpus_thesis)

# plot the WordCloud image                      
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
 
plt.show()

#and also let's take a look at data
df3.describe()

#End of episode2
