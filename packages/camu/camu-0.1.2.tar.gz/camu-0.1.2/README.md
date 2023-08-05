<p align="center">
  <img height="200" src="images/Camufi_py.png" alt="Camufipy Logo"/>
</p>

# Filtering false-positive candidate mutations to accelerate DNM-counting for direct µ estimates

For direct estimation of the spontaneous mutation rate µ, it is necessary to calculate the rate of spontaneous de-novo mutations (DNM) occuring per site per generation.
Consequently, counting DNM is essential for estimating µ.

The raw approach is:
* Sequencing samples and control --> .fastq files
* Assembly of sequencing results --> .bam files
* perform some filtering steps
* Variant calling 
* extraction of variants occurring in samples but not in control --> candidate mutations

The resulting list of candidate mutations (CM) currently has to be manually curated using a genome browser like IGV.

Unfortunately, approx. 90 % of these CM are no true DNM, they turn out to be false-positives.

**Camufi.py** aims to accelerate the whole procedure of DNM counting by filtering out the vast majority of false-positive CM and by preparing the remaining CM for fast manual curation with IGV. 

**Camufi.py** consists of 3 main Python modules:
1. `filterDupAndLinked.py`  
2. `detectFIO.py`
3. `snapshotIGV.py`



