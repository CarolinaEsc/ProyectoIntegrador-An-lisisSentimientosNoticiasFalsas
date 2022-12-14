from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import HashingTF, Tokenizer, StopWordsRemover
import pyspark
from pyspark.sql import SparkSession


def createSession():
    appName = "Analisis de sentimientos Fakes News"
    spark = SparkSession \
        .builder \
        .appName(appName) \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate() 

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    return spark

def trainModel(spark):
    tweets_csv = spark.read.csv('resultAnalysis.csv', inferSchema=True, header=True)
    tweets_csv.show(truncate=False, n=3)

    data = tweets_csv.select("cleanTweet", col("sentiment").cast("Int").alias("label"))
    data.show(truncate = False,n=10)

    dividedData = data.randomSplit([0.7, 0.3]) 
    trainingData = dividedData[0] #index 0 = data training
    testingData = dividedData[1] #index 1 = data testing
    train_rows = trainingData.count()
    test_rows = testingData.count()
    print ("Training data rows:", train_rows, "; Testing data rows:", test_rows)

    tokenizer = Tokenizer(inputCol="cleanTweet", outputCol="SentimentWords")
    tokenizedTrain = tokenizer.transform(trainingData.dropna())
    tokenizedTrain.show(truncate=False, n=10)

    swr = StopWordsRemover(inputCol=tokenizer.getOutputCol(), 
                       outputCol="MeaningfulWords")
    SwRemovedTrain = swr.transform(tokenizedTrain)
    SwRemovedTrain.show(truncate=False, n=5)

    hashTF = HashingTF(inputCol=swr.getOutputCol(), outputCol="features")
    numericTrainData = hashTF.transform(SwRemovedTrain).select('label', 'MeaningfulWords', 'features')
    numericTrainData.show(truncate=False, n=20)

    lr = LogisticRegression(labelCol="label" , featuresCol="features",  
                        maxIter=10, regParam=0.01, family="multinomial")
    model = lr.fit(numericTrainData)
    print ("Termino el entrenamiento!")

    tokenizedTest = tokenizer.transform(testingData.dropna())
    SwRemovedTest = swr.transform(tokenizedTest)
    numericTest = hashTF.transform(SwRemovedTest).select(
        'Label', 'MeaningfulWords', 'features')
    numericTest.show(truncate=False, n=10)

    prediction = model.transform(numericTest)
    predictionFinal = prediction.select(
        "MeaningfulWords", "prediction", "Label")
    predictionFinal.show(n=23, truncate = False)
    correctPrediction = predictionFinal.filter(
        predictionFinal['prediction'] == predictionFinal['Label']).count()
    totalData = predictionFinal.count()
    print("correct prediction:", correctPrediction, ", total data:", totalData, 
        ", accuracy:", correctPrediction/totalData)
    
def main():
    sparkSession = createSession()
    trainModel(sparkSession)

if __name__ == "__main__":
    main()