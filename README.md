# geodatafw

## environment

- install anaconda
- install pycharm

- install environment in a suitable folder:
    - git clone https://github.com/oknuutti/geodatafw.git geodatafw
    - cd geodatafw
    - conda env create -f conda_env.yml
    - geopyspark install-jar

- get sentinel data file
- install gdal http://download.gisinternals.com/sdk/downloads/release-1911-x64-gdal-2-2-3-mapserver-7-0-7/gdal-202-1911-x64-core.msi
- following https://hernandezpaul.wordpress.com/2016/01/24/apache-spark-installation-on-windows-10/:
	- install java jdk 1.8
	- download & extract apache spark: https://spark.apache.org/downloads.html (move ./python to ./bin folder)
	- install scala: https://downloads.lightbend.com/scala/2.12.6/scala-2.12.6.msi
	- dowload winutils: https://github.com/steveloughran/winutils
	- edit environment variables by adding two system-variables:
		- SCALA_HOME to point to scala/bin folder
		- SPARK_HOME to point to spark root folder
		- HADOOP_HOME point to folder that has bin/winutils.exe
		- JAVA_HOME D:\Program Files\Java\jdk1.8.0_171
		- JAVA_OPTIONS -Xmx512M -Xms512M
