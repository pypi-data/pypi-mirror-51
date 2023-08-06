Class = modelPerformance:

Evaluate the performance of single models.

- Append key performance statistics: Error, AbsError
- Append key performance and confidence semgmentations: Performance Bands, Confidence Bands
- Produce key statistics: performance and confidence band frequencies, confidence by condidence bands (# & &)

EXAMPLES:
CL = avmstat.modelPerformance(sample, 'URN', 'CL',' Property value CL ', ' Conf CL ', ' Property value ')

perfTable = CL.modelStatistics()
confXperf, confperfDF = CL.performancebyConfidence()
CL.performancebySegment(segments = ['Type', 'Bedrooms'])
CL.featureMatrix(features = ['Type', 'Bedrooms', 'LivingArea'])

Class = modelCompare:

Compare the performance of models against each other.

- Supply a list of model 'pricePerformance' classes.
- Compare all combinations of models to show which perform stronger and weaker.

EXAMPLES:
compareTable = avmstat.modelCompare([CL,RM,HT])
compareTable.comparePerformance()
